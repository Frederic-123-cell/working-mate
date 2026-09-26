# -*- coding: utf-8 -*-
"""
官网 favicon 全套生成 —— **以用户原版图标为唯一设计源**。

⚠ 设计红线（2026-09-27 用户明确要求）：黑底白字「Working Mate」原版图标不许改动。
   本脚本不做任何重绘/换色/换字，只做一件事：拿 images/favicon.png（原版 64×64）
   等比放大/缩小，产出 Google 要求的 48 倍数尺寸与多尺寸 ico。

用法：  python gen_favicon.py
产出：  images/favicon-48/96/192.png、favicon.ico、images/apple-touch-icon.png
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "images", "favicon.png")   # 原版 64×64，设计基准
OUT = os.path.join(HERE, "images")
BG = (26, 30, 42, 255)                              # 站点 --bg #1A1E2A（apple-touch 铺底用）


def main():
    src = Image.open(SRC).convert("RGBA")
    print("设计源:", SRC, src.size)

    # 大尺寸：原图等比放大（不重绘）
    for s in (48, 96, 192):
        src.resize((s, s), Image.LANCZOS).save(
            os.path.join(OUT, "favicon-%d.png" % s), optimize=True)

    # favicon.ico：16/24/32/48/64 多尺寸
    src.resize((256, 256), Image.LANCZOS).convert("RGBA").save(
        os.path.join(HERE, "favicon.ico"), format="ICO",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64)])

    # apple-touch-icon：iOS 自己切圆角 → 满幅底 + 原图
    bg = Image.new("RGBA", (512, 512), BG)
    bg.alpha_composite(src.resize((512, 512), Image.LANCZOS))
    bg.resize((180, 180), Image.LANCZOS).convert("RGB").save(
        os.path.join(OUT, "apple-touch-icon.png"), optimize=True)

    print("完成：favicon-48/96/192.png、favicon.ico、apple-touch-icon.png")


if __name__ == "__main__":
    main()
