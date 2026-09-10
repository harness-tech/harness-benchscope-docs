#!/usr/bin/env python3
"""
源码快照工具 — 生成/对比 benchscope 源码目录结构与文件指纹。

用法：
  # 从源码路径生成快照（首次或全量更新）
  python scripts/snapshot.py generate --source /path/to/benchscope --output source-snapshot.json

  # 对比当前快照与源码差异（增量更新）
  python scripts/snapshot.py diff --source /path/to/benchscope --snapshot source-snapshot.json

  # 从 GitHub 克隆并生成快照
  python scripts/snapshot.py generate --github https://github.com/LABELNET/benchscope --tag v1.2.0

  # 仅更新版本号和时间戳（不重新扫描文件）
  python scripts/snapshot.py bump --version 1.2.0
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
SNAPSHOT_PATH = SKILL_DIR / "source-snapshot.json"


def file_hash(filepath: Path) -> str:
    """计算文件 SHA256 前 8 位。"""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def read_version(source_dir: Path) -> str:
    """从 pyproject.toml / setup.py / __init__.py 读取版本号。"""
    # pyproject.toml: version = "1.1.1"
    pyproject = source_dir / "pyproject.toml"
    if pyproject.exists():
        for line in pyproject.read_text().splitlines():
            line = line.strip()
            if line.startswith("version") and "=" in line:
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val
    # setup.py: version="1.1.1"
    setup = source_dir / "setup.py"
    if setup.exists():
        for line in setup.read_text().splitlines():
            if "version" in line and "=" in line:
                val = line.split("=", 1)[1].strip().strip('"').strip("'").rstrip(",")
                if val and val[0].isdigit():
                    return val
    # __init__.py: __version__ = "1.1.1"
    init = source_dir / "benchscope" / "__init__.py"
    if init.exists():
        for line in init.read_text().splitlines():
            if "__version__" in line and "=" in line:
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val
    return "unknown"


def discover_source(source_dir: Path) -> dict:
    """**自动发现**：从真实源码树构建 modules 结构（含文件指纹）。

    不再依赖预定义的陈旧 manifest，而是实际扫描以下目录：
      - benchscope/**/*.py   按顶级子包分组
      - benchscope/configs/*.yaml
      - benchscope/skills/**/*
      - web/src/**/*.{vue,js}
      - tests/**/*.py
      - mocks/**/*.py
      - 根文件：pyproject.toml / README.md / CHANGELOG.md（若存在）
    返回全新的 modules 结构（file_hashes 已填充）。
    """
    modules: dict = {}

    def add_group(group: str, rel_paths: list):
        if not rel_paths:
            return
        entries = {}
        for rel in rel_paths:
            fpath = source_dir / rel
            entries[rel] = file_hash(fpath) if fpath.exists() else "missing"
        modules[group] = {
            "files": sorted(entries.keys()),
            "file_hashes": entries,
        }

    # benchscope 包：按顶级子包分组（core/perf/accuracy/... 或直接文件）
    pkg = source_dir / "benchscope"
    pkg_groups: dict = {}
    if pkg.exists():
        for py in sorted(pkg.rglob("*.py")):
            rel = py.relative_to(source_dir).as_posix()
            parts = py.relative_to(pkg).parts
            group = parts[0] if len(parts) > 1 else "(root)"
            pkg_groups.setdefault(group, []).append(rel)
    for group, rels in sorted(pkg_groups.items()):
        add_group(f"benchscope/{group}", rels)

    # configs
    add_group("configs", [
        (source_dir / "benchscope" / "configs" / f).relative_to(source_dir).as_posix()
        for f in sorted(os.listdir(source_dir / "benchscope" / "configs"))
        if f.endswith(".yaml") and (source_dir / "benchscope" / "configs" / f).is_file()
    ]) if (source_dir / "benchscope" / "configs").exists() else None

    # skills
    add_group("skills", [
        p.relative_to(source_dir).as_posix()
        for p in sorted((source_dir / "benchscope" / "skills").rglob("*"))
        if p.is_file()
    ]) if (source_dir / "benchscope" / "skills").exists() else None

    # web
    web_groups: dict = {}
    web_src = source_dir / "web" / "src"
    if web_src.exists():
        for ext in ("*.vue", "*.js"):
            for f in sorted(web_src.rglob(ext)):
                rel = f.relative_to(source_dir).as_posix()
                parts = f.relative_to(web_src).parts
                group = parts[0] if len(parts) > 1 else "(root)"
                web_groups.setdefault(group, []).append(rel)
    for group, rels in sorted(web_groups.items()):
        add_group(f"web/{group}", rels)

    # tests
    add_group("tests", [
        p.relative_to(source_dir).as_posix()
        for p in sorted((source_dir / "tests").rglob("*.py"))
        if p.is_file()
    ]) if (source_dir / "tests").exists() else None

    # mocks
    add_group("mocks", [
        p.relative_to(source_dir).as_posix()
        for p in sorted((source_dir / "mocks").rglob("*.py"))
        if p.is_file()
    ]) if (source_dir / "mocks").exists() else None

    # 根文件
    root_files = []
    for name in ("pyproject.toml", "setup.py", "README.md", "CHANGELOG.md"):
        if (source_dir / name).exists():
            root_files.append(name)
    add_group("root", root_files)

    return {"modules": modules, "version": read_version(source_dir)}


def scan_source(source_dir: Path, snapshot: dict) -> dict:
    """扫描源码目录，更新快照中的文件指纹（基于快照已记录的 modules）。"""
    modules = snapshot.get("modules", {})
    changed = []

    for mod_name, mod_info in modules.items():
        files = mod_info.get("files", [])
        mod_info["file_hashes"] = {}
        for f in files:
            fpath = source_dir / f
            if fpath.exists():
                mod_info["file_hashes"][f] = file_hash(fpath)
            else:
                mod_info["file_hashes"][f] = "missing"
                changed.append({"module": mod_name, "file": f, "status": "missing"})

    return snapshot, changed


def diff_snapshot(source_dir: Path, snapshot: dict) -> dict:
    """对比快照与源码差异，返回变更报告。"""
    report = {
        "version": snapshot.get("version", "unknown"),
        "diff_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "modules_changed": [],
        "modules_unchanged": [],
        "new_files": [],
        "missing_files": [],
        "changelog_changed": False,
        "configs_changed": False,
    }

    modules = snapshot.get("modules", {})
    for mod_name, mod_info in modules.items():
        old_hashes = mod_info.get("file_hashes", {})
        files = mod_info.get("files", [])
        mod_changed = False

        for f in files:
            fpath = source_dir / f
            old_hash = old_hashes.get(f, "missing")
            if fpath.exists():
                new_hash = file_hash(fpath)
                if old_hash != new_hash:
                    mod_changed = True
                    report["modules_changed"].append({
                        "module": mod_name,
                        "file": f,
                        "old_hash": old_hash,
                        "new_hash": new_hash,
                    })
            else:
                if old_hash != "missing":
                    report["missing_files"].append({"module": mod_name, "file": f})

        if not mod_changed:
            report["modules_unchanged"].append(mod_name)

    # 检查 changelog
    changelog = snapshot.get("changelog", {})
    old_hashes = changelog.get("file_hashes", {})
    for f in changelog.get("files", []):
        fpath = source_dir / f
        if fpath.exists():
            new_hash = file_hash(fpath)
            if old_hashes.get(f) != new_hash:
                report["changelog_changed"] = True

    # 检查 configs
    configs = snapshot.get("configs", {})
    old_hashes = configs.get("file_hashes", {})
    for f in configs.get("files", []):
        fpath = source_dir / f
        if fpath.exists():
            new_hash = file_hash(fpath)
            if old_hashes.get(f) != new_hash:
                report["configs_changed"] = True

    # 汇总
    report["total_changed"] = len(report["modules_changed"])
    report["total_unchanged"] = len(report["modules_unchanged"])
    report["needs_update"] = report["total_changed"] > 0 or report["changelog_changed"]

    return report


def get_docs_to_update(report: dict, snapshot: dict) -> dict:
    """根据变更报告，输出需要更新的文档路径。"""
    docs = {"zh": set(), "en": set()}
    modules = snapshot.get("modules", {})

    for change in report["modules_changed"]:
        mod_name = change["module"]
        mod_info = modules.get(mod_name, {})
        doc_paths = mod_info.get("doc_paths", {})
        for path in doc_paths.get("zh", []):
            docs["zh"].add(path)
        for path in doc_paths.get("en", []):
            docs["en"].add(path)

    if report.get("configs_changed"):
        docs["zh"].add("install/configuration.md")
        docs["en"].add("install/configuration.md")

    return {
        "zh": sorted(docs["zh"]),
        "en": sorted(docs["en"]),
        "total": len(docs["zh"]) + len(docs["en"]),
    }


def clone_repo(github_url: str, tag: str = None) -> Path:
    """克隆 GitHub 仓库到临时目录。"""
    tmpdir = Path(tempfile.mkdtemp(prefix="benchscope-src-"))
    cmd = ["git", "clone", "--depth", "1"]
    if tag:
        cmd += ["--branch", tag]
    cmd += [github_url, str(tmpdir)]
    print(f"Cloning {github_url} (tag={tag}) -> {tmpdir}")
    subprocess.run(cmd, check=True, capture_output=True)
    return tmpdir


def main():
    parser = argparse.ArgumentParser(description="BenchScope source snapshot tool")
    sub = parser.add_subparsers(dest="command")

    # generate
    gen = sub.add_parser("generate", help="Generate snapshot from source")
    gen.add_argument("--source", help="Local source path")
    gen.add_argument("--github", help="GitHub repo URL")
    gen.add_argument("--tag", help="Git tag to checkout")
    gen.add_argument("--output", default=str(SNAPSHOT_PATH), help="Output snapshot path")
    gen.add_argument("--auto-discover", action="store_true", default=True,
                     help="从真实源码树自动发现 modules（默认开启，修复陈旧 manifest）")
    gen.add_argument("--no-auto-discover", dest="auto_discover", action="store_false",
                     help="使用快照中已记录的 modules（不重新发现）")

    # diff
    diff = sub.add_parser("diff", help="Diff snapshot against source")
    diff.add_argument("--source", help="Local source path")
    diff.add_argument("--github", help="GitHub repo URL")
    diff.add_argument("--tag", help="Git tag to checkout")
    diff.add_argument("--snapshot", default=str(SNAPSHOT_PATH), help="Snapshot file path")
    diff.add_argument("--json", action="store_true", help="Output as JSON")

    # bump
    bump = sub.add_parser("bump", help="Bump version in snapshot")
    bump.add_argument("--version", required=True, help="New version")
    bump.add_argument("--snapshot", default=str(SNAPSHOT_PATH), help="Snapshot file path")

    args = parser.parse_args()

    if args.command == "generate":
        # 加载或创建快照
        if Path(args.output).exists():
            snapshot = json.loads(Path(args.output).read_text())
        else:
            snapshot = {
                "snapshot_version": "2.0",
                "project": "benchscope",
                "modules": {},
            }

        # 获取源码
        source_dir = Path(args.source) if args.source else None
        tmpdir = None
        if args.github:
            tmpdir = clone_repo(args.github, args.tag)
            source_dir = tmpdir

        if not source_dir or not source_dir.exists():
            print("Error: source path not found")
            sys.exit(1)

        # 扫描
        snapshot["last_synced"] = datetime.now().strftime("%Y-%m-%d")
        changed = []
        if getattr(args, "auto_discover", True):
            # **自动发现**：从真实源码树重建 modules（修复陈旧 manifest）
            discovered = discover_source(source_dir)
            snapshot["modules"] = discovered["modules"]
            snapshot["version"] = discovered["version"]
            if args.tag:
                snapshot["version"] = args.tag.lstrip("v")
        else:
            if args.tag:
                snapshot["version"] = args.tag.lstrip("v")
            snapshot, changed = scan_source(source_dir, snapshot)

        snapshot["snapshot_version"] = "2.0"

        # 保存
        Path(args.output).write_text(json.dumps(snapshot, indent=2, ensure_ascii=False))
        print(f"✅ Snapshot saved: {args.output}")
        print(f"   Modules: {len(snapshot.get('modules', {}))}")
        print(f"   Version: {snapshot.get('version', 'unknown')}")
        if changed:
            print(f"   Missing files: {len(changed)}")

        if tmpdir:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)

    elif args.command == "diff":
        snapshot = json.loads(Path(args.snapshot).read_text())

        source_dir = Path(args.source) if args.source else None
        tmpdir = None
        if args.github:
            tmpdir = clone_repo(args.github, args.tag)
            source_dir = tmpdir

        if not source_dir or not source_dir.exists():
            print("Error: source path not found")
            sys.exit(1)

        report = diff_snapshot(source_dir, snapshot)
        docs = get_docs_to_update(report, snapshot)
        report["docs_to_update"] = docs

        if getattr(args, "json", False):
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print(f"\n📊 Diff Report (snapshot v{report['version']})")
            print(f"   Changed modules: {report['total_changed']}")
            print(f"   Unchanged modules: {report['total_unchanged']}")
            print(f"   Changelog changed: {report['changelog_changed']}")
            print(f"   Configs changed: {report['configs_changed']}")
            print(f"   Needs update: {report['needs_update']}")

            if report["modules_changed"]:
                print(f"\n📝 Changed files:")
                for c in report["modules_changed"]:
                    print(f"   [{c['module']}] {c['file']}")

            if docs["total"] > 0:
                print(f"\n📄 Docs to update ({docs['total']} files):")
                print(f"   zh: {', '.join(docs['zh'])}")
                print(f"   en: {', '.join(docs['en'])}")

        if tmpdir:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)

    elif args.command == "bump":
        snapshot = json.loads(Path(args.snapshot).read_text())
        old_version = snapshot.get("version", "unknown")
        snapshot["version"] = args.version.lstrip("v")
        snapshot["last_synced"] = datetime.now().strftime("%Y-%m-%d")
        Path(args.snapshot).write_text(json.dumps(snapshot, indent=2, ensure_ascii=False))
        print(f"✅ Snapshot version bumped: {old_version} -> {args.version}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
