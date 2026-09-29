#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zenith AI 研学社 · 官网社交分享封面生成器
产出 assets/og-cover.png（1200x630，微信/飞书/Twitter 分享卡片标准尺寸）

用法：  python tools/make_og_cover.py
改文案：直接改下方 TITLE / SUB / FOOT 常量后重跑即可（同输入同输出，可重复生成）
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BRAND_BG_TOP = (247, 245, 252)      # #F7F5FC
BRAND_BG_BOTTOM = (239, 235, 249)   # #EFEBF9
PURPLE = (139, 92, 246)             # #8B5CF6
PURPLE_DEEP = (124, 58, 237)        # #7C3AED
PURPLE_LIGHT = (167, 139, 250)      # #A78BFA
TEXT = (62, 58, 82)                 # #3E3A52
TEXT_SOFT = (107, 100, 128)         # #6B6480

TITLE = "向下扎根，向上破界。"
SUB = "探索 AI 业务落地，分享真实可落地的经验"
FOOT = "山顶见。"
URL = "zenith0097.github.io/zenithweb"
BRAND = "Zenith AI 研学社"

FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"


def font(path, size):
    return ImageFont.truetype(path, size)


def vgradient(size, top, bottom):
    """竖向渐变底"""
    w, h = size
    base = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        base.putpixel((0, y), tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return base.resize((w, h), Image.BILINEAR)


def soft_circle(img, cx, cy, r, color, alpha):
    """柔和光斑"""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (alpha,))
    return Image.alpha_composite(img, layer)


def mountains(draw, y_base, layers):
    """山顶剪影：与站点 Hero 同款意象"""
    for pts, color in layers:
        draw.polygon(pts + [(W, H), (0, H)], fill=color)


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(root, "assets")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "og-cover.png")

    img = vgradient((W, H), BRAND_BG_TOP, BRAND_BG_BOTTOM).convert("RGBA")

    # 光斑：右侧暖紫光晕，呼应站点趣味区
    img = soft_circle(img, 1010, 120, 260, PURPLE_LIGHT, 46)
    img = soft_circle(img, 1120, 520, 220, PURPLE, 30)

    draw = ImageDraw.Draw(img, "RGBA")

    # 山影（底部两层，浅→深）
    mountains(draw, H, [
        ([(300, 630), (520, 470), (700, 630)], PURPLE_LIGHT + (60,)),
        ([(0, 630), (170, 520), (340, 630)], PURPLE_LIGHT + (48,)),
        ([(820, 630), (1010, 500), (1200, 630)], PURPLE_LIGHT + (48,)),
    ])
    draw.rectangle([0, H - 8, W, H], fill=PURPLE)

    f_brand = font(FONT_BOLD, 34)
    f_title = font(FONT_BOLD, 78)
    f_sub = font(FONT_REG, 32)
    f_foot = font(FONT_BOLD, 30)
    f_url = font(FONT_REG, 26)

    # 品牌行
    draw.text((88, 78), "▲", font=font(FONT_BOLD, 40), fill=PURPLE)
    draw.text((140, 82), BRAND, font=f_brand, fill=TEXT)

    # 主标题（两行，按标点断）
    draw.text((88, 210), TITLE, font=f_title, fill=PURPLE_DEEP)

    # 副标题
    draw.text((90, 330), SUB, font=f_sub, fill=TEXT_SOFT)

    # 分隔线
    draw.rectangle([90, 400, 210, 405], fill=PURPLE_LIGHT)

    # 口号 + 网址
    draw.text((90, 452), FOOT, font=f_foot, fill=TEXT)
    draw.text((90, 512), URL, font=f_url, fill=TEXT_SOFT)

    img.convert("RGB").save(out, "PNG", optimize=True)
    print("已生成:", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
