# -*- coding: utf-8 -*-
"""
生成官网 favicon 全套（中英通用，无文字图形标，16px 可辨识）。

设计：暗炭灰圆角方 + 琥珀金「W」单字标（呼应 Working Mate 品牌色 #F5B642）。
旧图标把「Working Mate」整串文字塞进方块，缩到 16~48px 完全糊掉 —— 本脚本改为单字形。

用法：  python gen_favicon.py
产出：  images/favicon-192.png / favicon-96.png / favicon-48.png / favicon-32.png
        favicon.ico（16/32/48/64 多尺寸）
        apple-touch-icon.png（180，不透明底）
        images/favicon.png（兼容旧引用，192 版本）
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images")

# ── 品牌色（与 index.html :root 一致）──
INK = (26, 30, 42, 255)        # --bg #1A1E2A 暗炭灰
AMBER = (245, 182, 66, 255)    # --brand #F5B642 琥珀金
AMBER_DEEP = (198, 138, 30, 255)  # --brandDeep #C68A1E
WHITE = (238, 240, 255, 255)   # --text #EEF0FF

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\bahnschrift.ttf",
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
]


def load_font(px):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, px)
            except Exception:
                pass
    return ImageFont.load_default()


def rounded_mask(size, radius, ss=4):
    """超采样绘制圆角矩形遮罩，边缘更干净。"""
    m = Image.new("L", (size * ss, size * ss), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, size * ss - 1, size * ss - 1],
                        radius=radius * ss, fill=255)
    return m.resize((size, size), Image.LANCZOS)


# 风格表：(背景色, 前景色, 字号占比, 是否画品牌圆点, 字形)
STYLES = {
    "dark_amber":  (INK,   AMBER, 0.60, True,  "W"),
    "amber_dark":  (AMBER, INK,   0.60, False, "W"),
    "dark_white":  (INK,   WHITE, 0.60, True,  "W"),
    # v2：字更大更粗、去掉圆点（小尺寸下圆点会被读成「蘑菇头」）
    "dark_amber2": (INK,   AMBER, 0.74, False, "W"),
    "amber_dark2": (AMBER, INK,   0.74, False, "W"),
    "wm_dark":     (INK,   AMBER, 0.52, False, "WM"),
    "wm_amber":    (AMBER, INK,   0.52, False, "WM"),
}


def draw_mark(size, style="dark_amber"):
    """绘制单张图标（RGBA）。"""
    bg, fg, scale, dot, letter = STYLES.get(style, STYLES["dark_amber"])
    ss = 4
    S = size * ss
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    radius = int(S * 0.225)

    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=radius, fill=bg)

    f = load_font(int(S * scale))
    bbox = d.textbbox((0, 0), letter, font=f)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    # 光学居中：略上提，抵消大写字母下沿留白
    x = (S - w) / 2 - bbox[0]
    y = (S - h) / 2 - bbox[1] - S * 0.015
    d.text((x, y), letter, font=f, fill=fg)

    # 品牌「火花」点：呼应原 logo 中那个琥珀小圆点
    if dot:
        dot_r = S * 0.055
        cx, cy = S * 0.5, S * 0.185
        d.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=AMBER)

    img = img.resize((size, size), Image.LANCZOS)
    return img


def flatten(img, bg=(26, 30, 42, 255)):
    """贴到不透明底（apple-touch / favicon.ico 用）。"""
    out = Image.new("RGBA", img.size, bg)
    out.alpha_composite(img)
    return out


def make_preview(style, path):
    """生成 16→256 的尺寸条，用于人工确认小尺寸辨识度。"""
    sizes = [16, 24, 32, 48, 64, 128, 256]
    pad, gap = 24, 26
    W = pad * 2 + sum(sizes) + gap * (len(sizes) - 1)
    H = pad * 2 + 256 + 26
    canvas = Image.new("RGBA", (W, H), (244, 246, 250, 255))
    x = pad
    for s in sizes:
        ic = draw_mark(s, style)
        canvas.alpha_composite(ic, (x, pad + (256 - s) // 2))
        x += s + gap
    canvas.save(path)
    return path


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)

    # 预览模式：python gen_favicon.py preview
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        for st in ("dark_amber", "amber_dark", "dark_white"):
            p = os.path.join(HERE, "_favicon_preview_%s.png" % st)
            make_preview(st, p)
            print("preview:", p)
        sys.exit(0)

    style = sys.argv[1] if len(sys.argv) > 1 else "dark_amber"
    print("style =", style)

    # 主图（透明底，圆角）
    master = draw_mark(512, style)

    # PNG 多尺寸
    for s in (192, 96, 48, 32):
        master.resize((s, s), Image.LANCZOS).save(
            os.path.join(OUT, "favicon-%d.png" % s), optimize=True)
    # 兼容旧引用 images/favicon.png
    master.resize((192, 192), Image.LANCZOS).save(
        os.path.join(OUT, "favicon.png"), optimize=True)
    # apple-touch-icon：iOS 自己切圆角，所以这边必须是「满幅方图」——
    # 若沿用透明圆角，四角会露出底色，在 iOS 主屏上非常难看。
    at = Image.new("RGBA", (512, 512), STYLES.get(style, STYLES["dark_amber"])[0])
    at.alpha_composite(master)
    at.resize((180, 180), Image.LANCZOS).convert("RGB").save(
        os.path.join(OUT, "apple-touch-icon.png"), optimize=True)

    # favicon.ico（站点根目录，Google/浏览器兜底；保留透明圆角，与 PNG 一致）
    ico = os.path.join(HERE, "favicon.ico")
    master.resize((256, 256), Image.LANCZOS).convert("RGBA").save(
        ico, format="ICO",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64)])

    print("写出：")
    for f in sorted(os.listdir(OUT)):
        if f.startswith(("favicon", "apple-touch")):
            print("  images/%-24s %7d bytes" % (f, os.path.getsize(os.path.join(OUT, f))))
    print("  %-31s %7d bytes" % ("favicon.ico", os.path.getsize(ico)))
