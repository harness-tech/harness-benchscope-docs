#!/usr/bin/env python3
"""
自动截图脚本 — 使用 Playwright 对 benchscope-docs 页面截图。

依赖：pip install playwright && playwright install chromium

用法：
  python scripts/screenshot.py --url http://localhost:4321/zh/ --output public/images/screenshot.png
  python scripts/screenshot.py --url http://localhost:4321/zh/ --output public/images/screenshot.png --full-page
  python scripts/screenshot.py --all --output-dir public/images/
"""
import argparse
import sys
from pathlib import Path


def take_screenshot(url: str, output: str, full_page: bool = False, width: int = 1440, height: int = 900):
    """对指定 URL 截图。"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Error: playwright not installed. Run:")
        print("  pip install playwright && playwright install chromium")
        sys.exit(1)

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(2000)  # 等待动画完成
        page.screenshot(path=str(output_path), full_page=full_page)
        browser.close()

    print(f"✅ Screenshot saved: {output_path}")


def take_all_screenshots(base_url: str, output_dir: str):
    """对所有关键页面截图。"""
    pages = [
        ("landing-zh", "/zh/"),
        ("landing-en", "/en/"),
        ("docs-home-zh", "/zh/docs/"),
        ("docs-home-en", "/en/docs/"),
        ("quickstart-zh", "/zh/docs/quickstart/"),
        ("performance-zh", "/zh/docs/performance/"),
        ("accuracy-zh", "/zh/docs/accuracy/"),
    ]

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for name, path in pages:
        url = f"{base_url.rstrip('/')}{path}"
        output_file = output_path / f"benchscope-{name}.png"
        print(f"📸 Capturing {url} -> {output_file}")
        try:
            take_screenshot(url, str(output_file), full_page=True)
        except Exception as e:
            print(f"  ⚠️ Failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Screenshot benchscope-docs pages")
    parser.add_argument("--url", help="Page URL to screenshot")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--full-page", action="store_true", help="Capture full page")
    parser.add_argument("--width", type=int, default=1440, help="Viewport width")
    parser.add_argument("--height", type=int, default=900, help="Viewport height")
    parser.add_argument("--all", action="store_true", help="Capture all key pages")
    parser.add_argument("--output-dir", default="public/images/", help="Output directory for --all mode")
    args = parser.parse_args()

    if args.all:
        base_url = args.url or "http://localhost:4321"
        take_all_screenshots(base_url, args.output_dir)
    elif args.url and args.output:
        take_screenshot(args.url, args.output, args.full_page, args.width, args.height)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
