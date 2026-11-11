"""Фирменный стиль «Зелёный Круг»: цвета, символ, текст в кривых."""
import math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

# Палитра
DARK = "#1F5136"    # Хвойный
GREEN = "#5DBB63"   # Свежая зелень
CREAM = "#F6F1E4"   # Льняной
PUMPKIN = "#F4A93B" # Тыквенный (акцент)
INK = "#14271C"     # для мелкого текста

FONT_DIR = "/usr/share/fonts/opentype/inter/"
_fonts = {}


def font(name):
    if name not in _fonts:
        _fonts[name] = TTFont(FONT_DIR + name)
    return _fonts[name]


def text_path(text, x, y, size, fname="InterDisplay-ExtraBold.otf", tracking=0.0, anchor="start"):
    """Возвращает (d, width): SVG-путь текста (базовая линия y) и ширину."""
    f = font(fname)
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    upm = f["head"].unitsPerEm
    s = size / upm
    hmtx = f["hmtx"]
    names = [cmap.get(ord(ch), ".notdef") for ch in text]
    widths = [hmtx[n][0] * s for n in names]
    total = sum(widths) + tracking * size * (len(text) - 1)
    if anchor == "middle":
        x -= total / 2
    elif anchor == "end":
        x -= total
    ds = []
    cx = x
    for n, w in zip(names, widths):
        pen = SVGPathPen(gs)
        tp = TransformPen(pen, (s, 0, 0, -s, cx, y))
        gs[n].draw(tp)
        d = pen.getCommands()
        if d:
            ds.append(d)
        cx += w + tracking * size
    return " ".join(ds), total


def _pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def symbol(cx=100, cy=104, R=78, sw=17, ring=DARK, leaf=GREEN, jar=DARK,
           lid=GREEN, label=CREAM, label_leaf=GREEN, simple=False):
    """Знак: круг-цикл, вырастающий в лист, внутри многоразовая банка.
    Координаты рассчитаны на холст 200x200 (масштаб через R/100*...)."""
    k = R / 78.0
    a_start, a_end = -32, 285 - 360  # разрыв сверху справа
    x1, y1 = _pt(cx, cy, R, a_start)
    x2, y2 = _pt(cx, cy, R, a_end)
    ring_d = f"M{x1:.2f},{y1:.2f} A{R},{R} 0 1 1 {x2:.2f},{y2:.2f}"
    # лист растёт из конца кольца (угол -75°) по касательной, уходя наружу
    th = math.radians(a_end)
    tx, ty = -math.sin(th), math.cos(th)  # касательная по часовой
    rot = math.radians(-38)
    dx = tx * math.cos(rot) - ty * math.sin(rot)
    dy = tx * math.sin(rot) + ty * math.cos(rot)
    L = 50 * k
    bx, by = x2, y2
    ex, ey = bx + dx * L, by + dy * L
    nx, ny = -dy, dx
    w = 17 * k
    mx, my = bx + dx * L * 0.5, by + dy * L * 0.5
    c1 = (mx + nx * w, my + ny * w)
    c2 = (mx - nx * w, my - ny * w)
    leaf_d = (f"M{bx:.2f},{by:.2f} Q{c1[0]:.2f},{c1[1]:.2f} {ex:.2f},{ey:.2f} "
              f"Q{c2[0]:.2f},{c2[1]:.2f} {bx:.2f},{by:.2f} Z")
    vein = (f"M{bx + dx*L*0.12:.2f},{by + dy*L*0.12:.2f} "
            f"L{bx + dx*L*0.78:.2f},{by + dy*L*0.78:.2f}")
    out = [f'<path d="{ring_d}" fill="none" stroke="{ring}" stroke-width="{sw*k:.2f}" stroke-linecap="round"/>',
           f'<path d="{leaf_d}" fill="{leaf}"/>']
    if not simple:
        out.append(f'<path d="{vein}" stroke="{label}" stroke-width="{2.4*k:.2f}" stroke-linecap="round" fill="none" opacity="0.9"/>')
    # банка
    bw, bh = 62 * k, 60 * k
    jx, jy = cx - bw / 2, cy - 14 * k
    out.append(f'<rect x="{jx:.2f}" y="{jy:.2f}" width="{bw:.2f}" height="{bh:.2f}" rx="{17*k:.2f}" fill="{jar}"/>')
    # горлышко + крышка
    nw = 44 * k
    out.append(f'<rect x="{cx-nw/2:.2f}" y="{jy-8*k:.2f}" width="{nw:.2f}" height="{12*k:.2f}" rx="{3*k:.2f}" fill="{jar}"/>')
    lw = 52 * k
    out.append(f'<rect x="{cx-lw/2:.2f}" y="{jy-22*k:.2f}" width="{lw:.2f}" height="{14*k:.2f}" rx="{5*k:.2f}" fill="{lid}"/>')
    if not simple:
        # круглая этикетка с листочком
        lr = 15 * k
        lcx, lcy = cx, jy + bh * 0.52
        out.append(f'<circle cx="{lcx:.2f}" cy="{lcy:.2f}" r="{lr:.2f}" fill="{label}"/>')
        s = 9 * k
        ld = (f"M{lcx - s*0.7:.2f},{lcy + s*0.7:.2f} Q{lcx - s*0.9:.2f},{lcy - s*0.9:.2f} {lcx + s*0.75:.2f},{lcy - s*0.75:.2f} "
              f"Q{lcx + s*0.9:.2f},{lcy + s*0.9:.2f} {lcx - s*0.7:.2f},{lcy + s*0.7:.2f} Z")
        out.append(f'<path d="{ld}" fill="{label_leaf}"/>')
        # блик на стекле
        out.append(f'<rect x="{jx + 8*k:.2f}" y="{jy + 8*k:.2f}" width="{5*k:.2f}" height="{20*k:.2f}" rx="{2.5*k:.2f}" fill="{label}" opacity="0.35"/>')
    return "\n".join(out)


def svg(w, h, body, bg=None):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'{b}{body}</svg>')
