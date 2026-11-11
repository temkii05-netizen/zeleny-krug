"""Развёртки этикеток для банок (для 3D-упаковки и для печати)."""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from brand import *

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
W, H = 1800, 300  # развёртка по окружности (лицевая сторона в центре)

PRODUCTS = [("jar_grechka", "ГРЕЧКА", "ядрица · 600 г", CREAM, DARK),
            ("jar_ovsyanka", "ОВСЯНКА", "хлопья · 450 г", "#FCE7D2", DARK),
            ("jar_mindal", "МИНДАЛЬ", "сырой · 300 г", DARK, CREAM)]

for name, title, sub, bg, fg in PRODUCTS:
    leaf_c = GREEN
    b = [f'<rect width="{W}" height="{H}" fill="{bg}"/>',
         f'<rect y="0" width="{W}" height="16" fill="{GREEN}"/><rect y="{H-16}" width="{W}" height="16" fill="{GREEN}"/>']
    cx = W / 2
    ringc = fg
    b.append(f'<g transform="translate({cx-220},70) scale(0.8)">{symbol(ring=ringc, jar=ringc, lid=GREEN, label=bg, label_leaf=GREEN)}</g>')
    d, _ = text_path(title, cx - 40, 150, 62, "InterDisplay-Black.otf", tracking=0.01)
    b.append(f'<path d="{d}" fill="{fg}"/>')
    d, _ = text_path(sub, cx - 38, 196, 26, "Inter-SemiBold.otf")
    b.append(f'<path d="{d}" fill="{fg}" opacity="0.8"/>')
    d, _ = text_path("ЗЕЛЁНЫЙ КРУГ", cx - 38, 236, 20, "InterDisplay-Black.otf", tracking=0.12)
    b.append(f'<path d="{d}" fill="{GREEN}"/>')
    # тыльная сторона: «верни банку»
    for bx in (230, W - 230):
        d, _ = text_path("ВЕРНИ БАНКУ", bx, 140, 24, "InterDisplay-Black.otf", anchor="middle")
        b.append(f'<path d="{d}" fill="{fg}"/>')
        d, _ = text_path("— получи бонус", bx, 172, 20, "Inter-Medium.otf", anchor="middle")
        b.append(f'<path d="{d}" fill="{fg}" opacity="0.8"/>')
    s = svg(W, H, "".join(b))
    p = f"{OUT}/label_{name}.svg"
    open(p, "w").write(s)
    subprocess.run(["rsvg-convert", "-w", str(W), p, "-o", p[:-4] + ".png"], check=True)

# лицевая сторона коробки
BW, BH = 800, 560
b = [f'<rect width="{BW}" height="{BH}" fill="#C9A06B"/>',
     f'<g transform="translate(120,150)">{symbol(cx=100, cy=104, R=78, ring=DARK, jar=DARK, lid=GREEN, label="#C9A06B", label_leaf=DARK)}</g>']
d, _ = text_path("ЗЕЛЁНЫЙ", 350, 260, 74, "InterDisplay-Black.otf")
b.append(f'<path d="{d}" fill="{DARK}"/>')
d, _ = text_path("КРУГ", 350, 334, 74, "InterDisplay-Black.otf")
b.append(f'<path d="{d}" fill="{DARK}"/>')
d, _ = text_path("тара едет обратно — к нам", 352, 380, 24, "Inter-SemiBold.otf")
b.append(f'<path d="{d}" fill="{DARK}"/>')
b.append(f'<rect x="0" y="470" width="{BW}" height="40" fill="{GREEN}"/>')
s = svg(BW, BH, "".join(b))
open(f"{OUT}/box_front.svg", "w").write(s)
subprocess.run(["rsvg-convert", "-w", str(BW), f"{OUT}/box_front.svg", "-o", f"{OUT}/box_front.png"], check=True)
print("ok")
