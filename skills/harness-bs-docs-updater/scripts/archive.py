#!/usr/bin/env python3
"""
文档归档脚本 — 将当前版本文档归档到 archives/vX.Y.Z/，并打包为 tar.gz。

用法：
  python scripts/archive.py --version 1.1.0
  python scripts/archive.py --version 1.1.0 --skip-docs  # 仅归档元数据
  python scripts/archive.py --version 1.1.0 --pack-only  # 仅打包已有归档目录
"""
import argparse
import json
import shutil
import sys
import tarfile
from datetime import datetime
from pathlib import Path

# 脚本位于 skills/harness-bs-docs-updater/scripts/，项目根在上三级
SKILL_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = SKILL_DIR.parent.parent
ARCHIVES_DIR = PROJECT_ROOT / "archives"
DOCS_ZH = PROJECT_ROOT / "src" / "content" / "docs" / "zh"
DOCS_EN = PROJECT_ROOT / "src" / "content" / "docs" / "en"


def get_current_version() -> str:
    """从 package.json 读取当前版本。"""
    pkg = PROJECT_ROOT / "package.json"
    if pkg.exists():
        return json.loads(pkg.read_text()).get("version", "unknown")
    return "unknown"


def pack_archive(archive_dir: Path, version: str) -> Path:
    """将归档目录打包为 tar.gz，放在归档目录同级。"""
    tar_name = f"v{version}.tar.gz"
    tar_path = ARCHIVES_DIR / tar_name

    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(archive_dir, arcname=f"v{version}")

    size_kb = tar_path.stat().st_size / 1024
    print(f"📦 Packed: {tar_path} ({size_kb:.1f} KB)")
    return tar_path


def create_archive(version: str, skip_docs: bool = False, pack_only: bool = False):
    """创建版本归档并打包为 tar.gz。"""
    version = version.lstrip("v")
    archive_dir = ARCHIVES_DIR / f"v{version}"

    if pack_only:
        if not archive_dir.exists():
            print(f"❌ Archive directory not found: {archive_dir}")
            sys.exit(1)
        pack_archive(archive_dir, version)
        return

    if archive_dir.exists():
        print(f"⚠️ Archive already exists: {archive_dir}")
        resp = input("Overwrite? (y/N): ").strip().lower()
        if resp != "y":
            print("Aborted.")
            return
        shutil.rmtree(archive_dir)

    archive_dir.mkdir(parents=True, exist_ok=True)

    # 归档文档
    if not skip_docs:
        if DOCS_ZH.exists():
            dst_zh = archive_dir / "docs" / "zh"
            print(f"📁 Archiving zh docs -> {dst_zh}")
            shutil.copytree(DOCS_ZH, dst_zh)

        if DOCS_EN.exists():
            dst_en = archive_dir / "docs" / "en"
            print(f"📁 Archiving en docs -> {dst_en}")
            shutil.copytree(DOCS_EN, dst_en)

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
archives/
├── v{version}/            # 归档目录
│   ├── META.md            # 本文件
{"│   ├── docs/" if not skip_docs else "│   └── (docs skipped)"}
{"│   │   ├── zh/           # 中文文档快照" if not skip_docs else ""}
{"│   │   └── en/           # 英文文档快照" if not skip_docs else ""}
└── v{version}.tar.gz      # 归档压缩包
```
"""
    meta_path.write_text(meta_content)
    print(f"📝 Meta written: {meta_path}")

    # 统计
    file_count = sum(1 for _ in archive_dir.rglob("*") if _.is_file())
    print(f"\n✅ Archive complete: {archive_dir}")
    print(f"   Files: {file_count}")

    # 打包 tar.gz
    pack_archive(archive_dir, version)


def main():
    parser = argparse.ArgumentParser(description="Archive docs for a version")
    parser.add_argument("--version", required=True, help="Version to archive (e.g. 1.1.0)")
    parser.add_argument("--skip-docs", action="store_true", help="Skip copying docs, only create META.md")
    parser.add_argument("--pack-only", action="store_true", help="Only pack existing archive dir to tar.gz")
    args = parser.parse_args()

    create_archive(args.version, args.skip_docs, args.pack_only)


if __name__ == "__main__":
    main()
