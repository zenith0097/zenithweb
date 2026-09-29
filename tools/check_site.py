#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zenith AI 研学社 · 官网自检
用法：  python tools/check_site.py       （在本目录或任意位置运行均可）

检查什么：
  1. HTML 标签配平（结构没被改坏）
  2. 导航锚点是否都有对应区块
  3. JS 里取用的元素 id 是否都在 HTML 里（防止改名后静默失效）
  4. 门面占位字样（"待填/待补/TODO" 这类内部口径不该出现在公开页面）
  5. 关键改动是否在位（可访问性/对比度/触屏处理）
  6. CSS 花括号配平
  7. 小字对比度是否达到 WCAG AA（>=4.5:1）
  8. 必需文件是否齐全
  9. 【提示，不计入成败】疑似死样式 —— v6 删板块后残留的 CSS 类

退出码：0 = 全过；1 = 有项目未通过
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results = []


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def chk(cond, label, extra=""):
    results.append(bool(cond))
    print(("  [OK] " if cond else "  [!!] ") + label + (("  " + extra) if extra else ""))


def lum(h):
    h = h.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def main():
    html = read("index.html")
    css = read("css/style.css")
    js = read("js/main.js")

    print("Zenith 官网自检 | 根目录:", ROOT)

    print("\n[1] HTML 结构")
    for tag in ["section", "div", "article", "header", "footer", "main", "nav", "blockquote", "svg", "span", "p"]:
        o = len(re.findall(r"<%s[\s>]" % tag, html))
        c = html.count("</%s>" % tag)
        chk(o == c, "标签平衡 <%s>" % tag, "开%d 闭%d" % (o, c))

    print("\n[2] 导航锚点")
    secs = re.findall(r'<section[^>]*id="([^"]+)"', html)
    chk(len(secs) >= 5, "内容区块数 %d" % len(secs), str(secs))
    for n in re.findall(r'<a href="#([^"]+)"', html):
        if n == "top":
            chk('id="top"' in html, "锚点 #top 有落点")
        else:
            chk(n in secs, "锚点 #%s 有对应区块" % n)

    print("\n[3] JS 取用的元素 id")
    js_ids = sorted(set(re.findall(r'getElementById\("([^"]+)"\)', js)))
    html_ids = set(re.findall(r'id="([^"]+)"', html))
    missing = [i for i in js_ids if i not in html_ids]
    chk(not missing, "JS 的 %d 个 id 全部命中" % len(js_ids), ("缺失: %s" % missing) if missing else "")

    print("\n[4] 门面占位字样（不该出现在公开页面）")
    for kw in ["待填", "待补", "TODO", "占位", "文件待提供"]:
        chk(html.count(kw) == 0, "无 '%s'" % kw, "出现 %d 次" % html.count(kw))

    print("\n[5] 关键改动在位")
    chk('aria-live="polite"' not in html, "Hero 打字机不刷屏读屏器")
    chk("公众号搜索" in html or any(k in html for k in ["comm-tag"]), "关注我们文案可操作")
    chk(":focus-visible" in css, "键盘焦点环")
    chk("--text-dim: #6D6682" in css, "灰字已加深")
    chk(".cursor-glow.is-on" in css, "光斑首次移动才亮")
    chk("reduceMotion" in js, "JS 尊重「减少动态效果」")
    chk("hover: hover" in js, "触屏不建光斑层")

    print("\n[6] CSS 语法")
    chk(css.count("{") == css.count("}"), "花括号配平", "开%d 闭%d" % (css.count("{"), css.count("}")))
    chk(not re.search(r"\{\s*\}", css), "无空规则块")

    print("\n[7] 小字对比度（WCAG AA 需 >=4.5:1）")
    m = re.search(r"--text-dim:\s*(#[0-9A-Fa-f]{6})", css)
    if m:
        worst = min(ratio(m.group(1), b) for b in ["#F7F5FC", "#EFEBF9", "#FFFFFF"])
        chk(worst >= 4.5, "辅助小字最低 %.2f:1" % worst, "色值 %s" % m.group(1))
    m2 = re.search(r"--text-soft:\s*(#[0-9A-Fa-f]{6})", css)
    if m2:
        worst2 = min(ratio(m2.group(1), b) for b in ["#F7F5FC", "#EFEBF9", "#FFFFFF"])
        chk(worst2 >= 4.5, "次级正文最低 %.2f:1" % worst2, "色值 %s" % m2.group(1))

    print("\n[8] 文件齐全")
    for f in ["index.html", "404.html", "robots.txt", "sitemap.xml", "css/style.css",
              "js/main.js", "assets/og-cover.png", "tools/make_og_cover.py"]:
        p = os.path.join(ROOT, f.replace("/", os.sep))
        chk(os.path.exists(p), f, "%d 字节" % os.path.getsize(p) if os.path.exists(p) else "缺失")

    print("\n[9] 上线前必删项")
    temp_marks = {
        "diagBadge": "临时诊断角标（窗口宽度/栏数）",
        "vwBadge": "小样宽度角标",
        "sample-flag": "小样标识",
    }
    noted = False
    for key, label in temp_marks.items():
        if key in html:
            noted = True
            chk(False, "页面里还留着：%s" % label, "上线前必须删掉")
    if not noted:
        chk(True, "没有残留的调试/小样标记", "")

    print("\n[10] 疑似死样式（提示，不计入成败）")
    live = set()
    for s in re.findall(r'class="([^"]+)"', html):
        live.update(s.split())
    css_nc = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    defined = sorted(set(re.findall(r"\.([a-zA-Z][\w-]*)", css_nc)))
    dead = [c for c in defined if c not in live and not re.search(r"\b" + re.escape(c) + r"\b", js)]
    if dead:
        print("  以下类 CSS 有定义、HTML/JS 都没用到，可考虑清理：")
        print("   ", ", ".join("." + d for d in dead))
    else:
        print("  无")

    total = len(results)
    passed = sum(1 for r in results if r)
    print("\n结论：%d/%d 项通过%s" % (passed, total, "" if passed == total else "  ← 见 [!!]"))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
