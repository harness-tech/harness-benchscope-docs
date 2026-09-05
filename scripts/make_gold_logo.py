#!/usr/bin/env python3
"""把 logo 染成金色（保留透明背景）。

背景为透明、主体为任意单色（白/黑/蓝等）的 PNG，将非透明主体整体替换为
指定金色，保留原始 alpha（透明度/抗锯齿边缘），输出透明背景的金色 logo。

用法:
    python make_gold_logo.py <input.png> [output.png] [--gold RRGGBB]

示例:
    python make_gold_logo.py logo-white.png logo-gold.png --gold c8a24a

依赖: Pillow   (pip install pillow)
"""
import argparse
import sys
from PIL import Image


# 主题金（与 source/_static/css/bs.css 的 --bs-gold 一致）
DEFAULT_GOLD = (200, 162, 74)  # #c8a24a


def hex_to_rgb(s: str):
    s = s.lstrip("#")
    if len(s) != 6:
        raise ValueError(f"非法颜色值: {s!r}（应为 6 位十六进制，如 c8a24a）")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def make_gold_logo(src: str, dst: str, gold: tuple[int, int, int]):
    im = Image.open(src)
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    pixels = im.load()
    w, h = im.size

    changed = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a > 0:                      # 非透明 → 染金，保留 alpha
                pixels[x, y] = (gold[0], gold[1], gold[2], a)
                changed += 1
    im.save(dst)
    print(f"OK  {src} -> {dst}")
    print(f"    尺寸 {w}x{h}，金色 #{''.join(f'{c:02X}' for c in gold)}，"
          f"着色像素 {changed} ({(changed / (w * h)) * 100:.1f}%)")


def main(argv=None):
    ap = argparse.ArgumentParser(description="把透明背景的单色 logo 染成金色")
    ap.add_argument("input", help="输入 PNG")
    ap.add_argument("output", nargs="?", default=None, help="输出 PNG（默认 input-gold.png）")
    ap.add_argument("--gold", default=None, help="金色十六进制，如 c8a24a（默认主题金）")
    args = ap.parse_args(argv)

    if args.output is None:
        args.output = args.input.replace(".png", "-gold.png")
    gold = hex_to_rgb(args.gold) if args.gold else DEFAULT_GOLD
    make_gold_logo(args.input, args.output, gold)
    return 0


if __name__ == "__main__":
    sys.exit(main())
