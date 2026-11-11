import sys, os, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from brand import *

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)


def save(name, s, png_w=None):
    p = os.path.join(OUT, name + ".svg")
    open(p, "w").write(s)
    if png_w:
        subprocess.run(["rsvg-convert", "-w", str(png_w), p, "-o", os.path.join(OUT, name + ".png")], check=True)


def wordmark(x, y, size, color, sub_color, tag=True, anchor="start"):
    d1, w1 = text_path("ЗЕЛЁНЫЙ", x, y, size, "InterDisplay-Black.otf", tracking=0.02, anchor=anchor)
    d2, w2 = text_path("КРУГ", x, y + size * 0.98, size, "InterDisplay-Black.otf", tracking=0.02, anchor=anchor)
    parts = [f'<path d="{d1}" fill="{color}"/>', f'<path d="{d2}" fill="{color}"/>']
    if tag:
        d3, _ = text_path("продукты в многоразовой таре", x, y + size * 1.62, size * 0.27,
                          "Inter-Medium.otf", tracking=0.02, anchor=anchor)
        parts.append(f'<path d="{d3}" fill="{sub_color}"/>')
    return "\n".join(parts), max(w1, w2)


# 1. Основной горизонтальный
wm, _ = wordmark(232, 92, 58, DARK, DARK)
save("logo_horizontal", svg(640, 200, symbol() + wm), 1600)
wm, _ = wordmark(232, 92, 58, CREAM, CREAM)
save("logo_horizontal_dark", svg(640, 200, symbol(ring=CREAM, jar=CREAM, label=DARK, label_leaf=GREEN) + wm, bg=DARK), 1600)

# 2. Вертикальный
wm, _ = wordmark(160, 268, 50, DARK, DARK, anchor="middle")
save("logo_vertical", svg(320, 380, f'<g transform="translate(60,10)">{symbol()}</g>' + wm), 1000)

# 3. Значок / favicon / аватар соцсетей
save("icon_color", svg(200, 200, symbol()), 512)
fav = f'<circle cx="100" cy="100" r="100" fill="{DARK}"/>' + \
      f'<g transform="translate(14,18) scale(0.86)">{symbol(ring=CREAM, jar=CREAM, lid=GREEN, simple=True)}</g>'
save("favicon", svg(200, 200, fav), 512)
for s in (16, 32, 48):
    subprocess.run(["rsvg-convert", "-w", str(s), os.path.join(OUT, "favicon.svg"), "-o", os.path.join(OUT, f"favicon_{s}.png")], check=True)
avatar = f'<rect width="200" height="200" rx="44" fill="{GREEN}"/>' + \
         f'<g transform="translate(14,18) scale(0.86)">{symbol(ring=DARK, leaf=CREAM, jar=DARK, lid=CREAM, label=CREAM, label_leaf=GREEN)}</g>'
save("avatar_social", svg(200, 200, avatar), 512)

# 4. Монохром
wm, _ = wordmark(232, 92, 58, "#000", "#000")
save("logo_mono_black", svg(640, 200, symbol(ring="#000", leaf="#000", jar="#000", lid="#000", label="#fff", label_leaf="#000") + wm, bg="#fff"), 1600)
wm, _ = wordmark(232, 92, 58, "#fff", "#fff")
save("logo_mono_white", svg(640, 200, symbol(ring="#fff", leaf="#fff", jar="#fff", lid="#fff", label="#000", label_leaf="#fff") + wm, bg="#000"), 1600)
save("icon_mono", svg(200, 200, symbol(ring="#000", leaf="#000", jar="#000", lid="#000", label="#fff", label_leaf="#000"), bg="#fff"), 512)
print("ok")
