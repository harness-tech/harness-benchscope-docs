#!/usr/bin/env python3
"""
文档归档脚本 — 将当前版本文档归档到 archives/vX.Y.Z/

用法：
  python scripts/archive.py --version 1.1.0
  python scripts/archive.py --version 1.1.0 --skip-docs  # 仅归档元数据
"""
import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
ARCHIVES_DIR = PROJECT_ROOT / "archives"
DOCS_ZH = PROJECT_ROOT / "src" / "content" / "docs" / "zh"
DOCS_EN = PROJECT_ROOT / "src" / "content" / "docs" / "en"


def get_current_version() -> str:
    """从 package.json 读取当前版本。"""
    import json
    pkg = PROJECT_ROOT / "package.json"
    if pkg.exists():
        return json.loads(pkg.read_text()).get("version", "unknown")
    return "unknown"


def create_archive(version: str, skip_docs: bool = False):
    """创建版本归档。"""
    version = version.lstrip("v")
    archive_dir = ARCHIVES_DIR / f"v{version}"

    if archive_dir.exists():
        print(f"⚠️ Archive already exists: {archive_dir}")
        resp = input("Overwrite? (y/N): ").strip().lower()
        if resp != "y":
            print("Aborted.")
            return

    archive_dir.mkdir(parents=True, exist_ok=True)

    # 归档文档
    if not skip_docs:
        if DOCS_ZH.exists():
            dst_zh = archive_dir / "docs" / "zh"
            print(f"📁 Archiving zh docs -> {dst_zh}")
            shutil.copytree(DOCS_ZH, dst_zh, dirs_exist_ok=True)

        if DOCS_EN.exists():
            dst_en = archive_dir / "docs" / "en"
            print(f"📁 Archiving en docs -> {dst_en}")
            shutil.copytree(DOCS_EN, dst_en, dirs_exist_ok=True)

    # 生成 META.md
    meta_path = archive_dir / "META.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    meta_content = f"""# Archive Metadata

| 项目 | 内容 |
|---|---|
| 归档版本 | v{version} |
| 归档时间 | {now} |
| 触发原因 | 版本更新至 v{version} |

## 归档文件清单

```
archives/v{version}/
├── META.md              # 本文件
{"├── docs/" if not skip_docs else "└── (docs skipped)"}
{"│   ├── zh/              # 中文文档快照" if not skip_docs else ""}
{"│   └── en/              # 英文文档快照" if not skip_docs else ""}
```
"""
    meta_path.write_text(meta_content)
    print(f"📝 Meta written: {meta_path}")

    # 统计
    file_count = sum(1 for _ in archive_dir.rglob("*") if _.is_file())
    print(f"\n✅ Archive complete: {archive_dir}")
    print(f"   Files: {file_count}")


def main():
    parser = argparse.ArgumentParser(description="Archive docs for a version")
    parser.add_argument("--version", required=True, help="Version to archive (e.g. 1.1.0)")
    parser.add_argument("--skip-docs", action="store_true", help="Skip copying docs, only create META.md")
    args = parser.parse_args()

    create_archive(args.version, args.skip_docs)


if __name__ == "__main__":
    main()
