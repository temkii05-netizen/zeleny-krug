"""Фирменные иллюстрации, иконки и паттерн «Зелёный Круг»."""
import os, sys, math, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from brand import *
from mascot2d import MINT, PINK, carrot, recycle

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
S = 5  # контур


def save(name, body, w, h, png_w=None, bg=None):
    s = svg(w, h, body, bg)
    p = f"{OUT}/{name}.svg"
    open(p, "w").write(s)
    subprocess.run(["rsvg-convert", "-w", str(png_w or w * 2), p, "-o", p[:-4] + ".png"], check=True)


def blob(cx, cy, r, c):
    pts = []
    for i in range(8):
        a = i / 8 * 2 * math.pi
        rr = r * (1 + 0.08 * math.sin(i * 2.7))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    m0 = ((pts[-1][0] + pts[0][0]) / 2, (pts[-1][1] + pts[0][1]) / 2)
    d = f"M{m0[0]:.1f},{m0[1]:.1f} "
    for i in range(8):
        p0, p1 = pts[i], pts[(i + 1) % 8]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        d += f"Q{p0[0]:.1f},{p0[1]:.1f} {mx:.1f},{my:.1f} "
    return f'<path d="{d}Z" fill="{c}"/>'


def jar(x, y, w, h, fill_c, lid_c, content="dots", label=True):
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w*0.22}" fill="{MINT}" stroke="{DARK}" stroke-width="{S}"/>']
    # содержимое
    cy = y + h * 0.3
    o.append(f'<clipPath id="c{x}{y}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w*0.22}"/></clipPath>')
    g = [f'<rect x="{x}" y="{cy}" width="{w}" height="{h}" fill="{fill_c}"/>']
    if content == "dots":
        for i in range(40):
            px = x + 8 + (i * 37 % int(w - 16))
            py = cy + 10 + (i * 53 % int(h * 0.65))
            g.append(f'<ellipse cx="{px}" cy="{py}" rx="4" ry="2.6" fill="{DARK}" opacity="0.25" transform="rotate({i*40},{px},{py})"/>')
    elif content == "nuts":
        for i in range(14):
            px = x + 14 + (i * 41 % int(w - 28))
            py = cy + 14 + (i * 29 % int(h * 0.6))
            g.append(f'<ellipse cx="{px}" cy="{py}" rx="10" ry="7" fill="#C98B4B" stroke="{DARK}" stroke-width="2.5" transform="rotate({i*33},{px},{py})"/>')
    o.append(f'<g clip-path="url(#c{x}{y})">{"".join(g)}<path d="M{x},{cy} Q{x+w/2},{cy-8} {x+w},{cy}" fill="none" stroke="{DARK}" stroke-width="3"/></g>')
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w*0.22}" fill="none" stroke="{DARK}" stroke-width="{S}"/>')
    o.append(f'<rect x="{x + w*0.12}" y="{y-16}" width="{w*0.76}" height="22" rx="7" fill="{lid_c}" stroke="{DARK}" stroke-width="{S}"/>')
    if label:
        o.append(f'<rect x="{x}" y="{y + h*0.52}" width="{w}" height="{h*0.26}" fill="{CREAM}" stroke="{DARK}" stroke-width="3.5"/>')
        o.append(f'<circle cx="{x+w/2}" cy="{y + h*0.65}" r="{h*0.08}" fill="{GREEN}" stroke="{DARK}" stroke-width="3"/>')
    o.append(f'<rect x="{x+10}" y="{y+12}" width="8" height="{h*0.3}" rx="4" fill="#fff" opacity="0.7"/>')
    return "".join(o)


def bottle(x, y, w, h):
    nw = w * 0.42
    d = (f"M{x + (w-nw)/2},{y} L{x + (w+nw)/2},{y} L{x + (w+nw)/2},{y + h*0.18} "
         f"Q{x + w},{y + h*0.26} {x + w},{y + h*0.38} L{x + w},{y + h - 16} Q{x + w},{y + h} {x + w - 16},{y + h} "
         f"L{x + 16},{y + h} Q{x},{y + h} {x},{y + h - 16} L{x},{y + h*0.38} Q{x},{y + h*0.26} {x + (w-nw)/2},{y + h*0.18} Z")
    return (f'<path d="{d}" fill="#FFFFFF" stroke="{DARK}" stroke-width="{S}" stroke-linejoin="round"/>'
            f'<rect x="{x + (w-nw)/2 - 4}" y="{y - 18}" width="{nw + 8}" height="20" rx="5" fill="{GREEN}" stroke="{DARK}" stroke-width="{S}"/>'
            f'<rect x="{x}" y="{y + h*0.5}" width="{w}" height="{h*0.24}" fill="{CREAM}" stroke="{DARK}" stroke-width="3.5"/>'
            f'<circle cx="{x + w/2}" cy="{y + h*0.62}" r="{h*0.07}" fill="{GREEN}" stroke="{DARK}" stroke-width="3"/>'
            f'<rect x="{x+10}" y="{y + h*0.3}" width="7" height="{h*0.15}" rx="3.5" fill="{MINT}"/>')


def leaf(x, y, s, rot, c=GREEN, stroke=True):
    st = f'stroke="{DARK}" stroke-width="{3/s:.1f}"' if stroke else ""
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})"><path d="M0,0 Q14,-22 40,-12 Q22,14 0,0Z" fill="{c}" {st}/>'
            f'<path d="M4,-2 L30,-10" stroke="{DARK}" stroke-width="{2/s:.1f}" opacity="{0.6 if stroke else 0}"/></g>')


# 1. Банки с крупами и орехами
b = blob(200, 210, 170, "#E3F1DA")
b += jar(70, 150, 120, 170, "#E9D9B0", PUMPKIN, "dots")
b += jar(210, 110, 130, 210, "#D9B98A", GREEN, "nuts")
b += leaf(320, 120, 1.2, -30) + leaf(60, 300, 1.0, 160)
b += f'<rect x="40" y="318" width="320" height="8" rx="4" fill="{DARK}"/>'
save("ill_jars", b, 400, 380)

# 2. Молоко в стеклянной бутылке
b = blob(200, 200, 160, "#FCE7D2")
b += bottle(150, 90, 100, 230)
b += f'<circle cx="300" cy="120" r="26" fill="{PUMPKIN}" stroke="{DARK}" stroke-width="{S}"/>'
b += leaf(80, 280, 1.3, -20)
b += f'<rect x="60" y="318" width="280" height="8" rx="4" fill="{DARK}"/>'
save("ill_milk", b, 400, 380)

# 3. Эко-сумка с продуктами
b = blob(200, 210, 165, "#E3F1DA")
b += carrot(170, 120, -20) + carrot(200, 110, 10)
b += f'<path d="M240,60 Q250,20 270,40 Q268,70 245,110" fill="{GREEN}" stroke="{DARK}" stroke-width="{S}"/>'
b += f'<rect x="210" y="70" width="70" height="40" rx="18" fill="#E2B677" stroke="{DARK}" stroke-width="{S}" transform="rotate(-25,245,90)"/>'
b += f'<path d="M140,140 Q140,70 200,70 Q260,70 260,140" fill="none" stroke="{DARK}" stroke-width="10" stroke-linecap="round"/>'
b += f'<path d="M110,140 L290,140 L272,330 L128,330 Z" fill="{CREAM}" stroke="{DARK}" stroke-width="{S}" stroke-linejoin="round"/>'
b += f'<g transform="translate(152,175) scale(0.48)">{symbol(ring=DARK, jar=DARK)}</g>'
save("ill_bag", b, 400, 380)

# 4. Курьер на грузовом велосипеде
b = blob(220, 220, 170, "#DDEFD9")
for wx in (110, 330):
    b += f'<circle cx="{wx}" cy="290" r="42" fill="none" stroke="{DARK}" stroke-width="9"/><circle cx="{wx}" cy="290" r="6" fill="{DARK}"/>'
b += f'<path d="M110,290 L180,215 L270,215 L330,290 M180,215 L210,290 L270,215 M270,215 L282,170" stroke="{DARK}" stroke-width="8" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
b += f'<rect x="266" y="160" width="36" height="10" rx="5" fill="{DARK}"/>'
b += f'<rect x="60" y="150" width="120" height="76" rx="10" fill="{GREEN}" stroke="{DARK}" stroke-width="{S}"/>'
b += f'<g transform="translate(92,154) scale(0.34)">{symbol(ring=CREAM, jar=CREAM, lid=PUMPKIN, label=DARK, label_leaf=GREEN)}</g>'
b += f'<rect x="74" y="120" width="28" height="32" rx="7" fill="{MINT}" stroke="{DARK}" stroke-width="4"/><rect x="76" y="112" width="24" height="9" rx="3" fill="{PUMPKIN}" stroke="{DARK}" stroke-width="3"/>'
b += f'<rect x="132" y="128" width="26" height="24" rx="7" fill="{MINT}" stroke="{DARK}" stroke-width="4"/><rect x="134" y="120" width="22" height="9" rx="3" fill="{GREEN}" stroke="{DARK}" stroke-width="3"/>'
# курьер
b += f'<path d="M205,210 L230,140" stroke="{DARK}" stroke-width="22" stroke-linecap="round"/>'
b += f'<path d="M230,140 L232,138" stroke="{PUMPKIN}" stroke-width="40" stroke-linecap="round"/>'
b += f'<path d="M222,150 Q240,110 236,110 L250,150 Z" fill="{PUMPKIN}"/>'
b += f'<rect x="212" y="110" width="44" height="64" rx="18" fill="{PUMPKIN}" stroke="{DARK}" stroke-width="{S}"/>'
b += f'<path d="M240,128 L282,168" stroke="{DARK}" stroke-width="12" stroke-linecap="round"/>'
b += f'<path d="M226,172 L250,235 L215,288" stroke="{DARK}" stroke-width="13" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
b += f'<circle cx="236" cy="88" r="22" fill="#F2C9A5" stroke="{DARK}" stroke-width="{S}"/>'
b += f'<path d="M212,84 Q214,58 238,60 Q262,62 260,84 Z" fill="{DARK}"/><rect x="236" y="78" width="30" height="7" rx="3" fill="{DARK}"/>'
b += f'<circle cx="244" cy="92" r="2.6" fill="{DARK}"/>'
for i, sx in enumerate((30, 20, 34)):
    b += f'<line x1="{sx}" y1="{180 + i*22}" x2="{sx + 30}" y2="{180 + i*22}" stroke="{DARK}" stroke-width="5" stroke-linecap="round" opacity="0.5"/>'
save("ill_courier", b, 440, 360)

# 5. Иконки «как это работает» (линейные, 96x96)
ICON = {
 "order": f'<rect x="18" y="30" width="60" height="50" rx="10" fill="{CREAM}" stroke="{DARK}" stroke-width="{S}"/><path d="M34,30 Q34,14 48,14 Q62,14 62,30" fill="none" stroke="{DARK}" stroke-width="{S}"/><path d="M36,56 L45,64 L62,46" stroke="{GREEN}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
 "deliver": f'<rect x="10" y="30" width="48" height="36" rx="6" fill="{GREEN}" stroke="{DARK}" stroke-width="{S}"/><path d="M58,40 L74,40 L86,54 L86,66 L58,66 Z" fill="{CREAM}" stroke="{DARK}" stroke-width="{S}" stroke-linejoin="round"/><circle cx="26" cy="72" r="8" fill="{DARK}"/><circle cx="72" cy="72" r="8" fill="{DARK}"/>',
 "return": f'<rect x="32" y="34" width="32" height="40" rx="9" fill="{MINT}" stroke="{DARK}" stroke-width="{S}"/><rect x="34" y="24" width="28" height="11" rx="4" fill="{PUMPKIN}" stroke="{DARK}" stroke-width="4"/><path d="M14,52 A34,34 0 0 1 48,14" stroke="{GREEN}" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M82,44 A34,34 0 0 1 48,82" stroke="{GREEN}" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M44,8 L54,14 L44,21Z M52,88 L42,82 L52,75Z" fill="{GREEN}"/>',
 "wash": f'<rect x="30" y="30" width="36" height="48" rx="10" fill="{MINT}" stroke="{DARK}" stroke-width="{S}"/><circle cx="24" cy="26" r="9" fill="#fff" stroke="{DARK}" stroke-width="4"/><circle cx="72" cy="20" r="7" fill="#fff" stroke="{DARK}" stroke-width="4"/><circle cx="78" cy="44" r="5" fill="#fff" stroke="{DARK}" stroke-width="3.5"/><path d="M40,46 L46,52 M52,40 L58,46" stroke="#fff" stroke-width="5" stroke-linecap="round"/>',
}
for k, v in ICON.items():
    save("icon_" + k, v, 96, 96, 384)

# 6. Паттерн
tile = 160
els = [
    f'<g transform="translate(20,18) scale(0.22)">{symbol(ring=DARK, leaf=GREEN, jar=DARK, lid=GREEN, label=CREAM)}</g>',
    leaf(100, 40, 0.9, -20, GREEN, False),
    f'<circle cx="122" cy="110" r="14" fill="none" stroke="{GREEN}" stroke-width="6"/>',
    leaf(30, 130, 0.7, 140, DARK, False),
    f'<circle cx="75" cy="95" r="5" fill="{PUMPKIN}"/>',
    f'<circle cx="145" cy="20" r="4" fill="{DARK}" opacity="0.6"/>',
]
pat = f'<defs><pattern id="p" width="{tile}" height="{tile}" patternUnits="userSpaceOnUse">{"".join(els)}</pattern></defs>'
save("pattern_tile", "".join(els), tile, tile, 640, bg=CREAM)
save("pattern_preview", pat + f'<rect width="960" height="540" fill="{CREAM}"/><rect width="960" height="540" fill="url(#p)"/>', 960, 540, 1920)
# тёмный вариант
els_d = [e.replace(DARK, "#2E6B49") for e in els]
els_d[0] = f'<g transform="translate(20,18) scale(0.22)">{symbol(ring=GREEN, leaf=GREEN, jar=GREEN, lid=PUMPKIN, label=DARK, label_leaf=GREEN)}</g>'
patd = f'<defs><pattern id="p" width="{tile}" height="{tile}" patternUnits="userSpaceOnUse">{"".join(els_d)}</pattern></defs>'
save("pattern_dark_preview", patd + f'<rect width="960" height="540" fill="{DARK}"/><rect width="960" height="540" fill="url(#p)"/>', 960, 540, 1920)
print("ok")
