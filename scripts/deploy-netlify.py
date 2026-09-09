#!/usr/bin/env python3
"""Deploy dist/ to Netlify via the Deploy API (no CLI needed)."""
import hashlib, json, os, urllib.request, argparse
from pathlib import Path

TOKEN = os.environ.get("NETLIFY_AUTH_TOKEN", "").strip()
DIR = Path("dist")
API = "https://api.netlify.com/api/v1"

def shasum(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()

def req(method, url, data=None, headers=None):
    h = {"Authorization": f"Bearer {TOKEN}"}
    if headers: h.update(headers)
    r = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        resp = urllib.request.urlopen(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:400]}")
    return json.loads(resp.read())

def upload_file(url, data):
    r = urllib.request.Request(url, data=data, method="PUT",
                              headers={"Authorization": f"Bearer {TOKEN}",
                                       "Content-Type": "application/octet-stream"})
    try:
        urllib.request.urlopen(r).read()
    except urllib.error.HTTPError as e:
        raise SystemExit(f"upload HTTP {e.code}: {e.read().decode(errors='replace')[:400]}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-id", default="")
    ap.add_argument("--name", default="benchscope-docs", help="new site name")
    ap.add_argument("--prod", action="store_true")
    args = ap.parse_args()

    if not TOKEN:
        raise SystemExit("NETLIFY_AUTH_TOKEN not set")

    # hash dist files
    files = {}
    for p in sorted(DIR.rglob("*")):
        if p.is_file():
            rel = p.relative_to(DIR).as_posix()
            files[f"/{rel}"] = shasum(p.read_bytes())
    print(f"hashed {len(files)} files")

    # create site (new) or reuse
    if args.site_id:
        site_id = args.site_id
        print("using site:", site_id)
    else:
        print("creating new site:", args.name)
        site = req("POST", f"{API}/sites", json.dumps({"name": args.name}).encode(),
                   {"Content-Type": "application/json"})
        site_id = site["id"]
        print("site id:", site_id)

    # create deploy
    print("creating deploy ...")
    d = req("POST", f"{API}/sites/{site_id}/deploys",
            json.dumps({"files": files}).encode(), {"Content-Type": "application/json"})
    deploy_id = d["id"]
    required = d.get("required", [])
    print("deploy:", deploy_id, "| required files:", len(required))

    # upload required files
    sha_to_rel = {s: rel for rel, s in files.items()}
    for n, sha in enumerate(required, 1):
        rel = sha_to_rel.get(sha)
        if rel is None:
            continue
        data = Path(DIR, rel.lstrip('/')).read_bytes()
        upload_file(f"{API}/deploys/{deploy_id}/files/{sha}", data)
        if n % 30 == 0 or n == len(required):
            print(f"  uploaded {n}/{len(required)}")

    # confirm
    c = req("POST", f"{API}/deploys/{deploy_id}/confirm", b"", {"Content-Type": "application/json"})
    state = c.get("state")
    print("deploy state:", state)

    # publish to production
    if args.prod:
        print("publishing to production ...")
        p = req("POST", f"{API}/sites/{site_id}/publish/{deploy_id}", b"",
                {"Content-Type": "application/json"})
        print("published:", p.get("state"))
        print("site URL:", p.get("url") or c.get("url") or d.get("url"))
    else:
        print("preview URL:", d.get("url") or c.get("url"))

    print("DONE")

if __name__ == "__main__":
    main()
