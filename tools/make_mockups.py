"""Визитка, фирменный бланк и сцены-мокапы."""
import os, sys, subprocess, math
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from brand import *

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)


def save(name, body, w, h, pw, bg=None):
    p = f"{OUT}/{name}.svg"
    open(p, "w").write(svg(w, h, body, bg))
    subprocess.run(["rsvg-convert", "-w", str(pw), p, "-o", p[:-4] + ".png"], check=True)
    return Image.open(p[:-4] + ".png").convert("RGBA")


def T(text, x, y, size, f="Inter-Medium.otf", c=INK, anchor="start", tr=0.0, op=1):
    d, w = text_path(text, x, y, size, f, tracking=tr, anchor=anchor)
    return f'<path d="{d}" fill="{c}" opacity="{op}"/>'


tile = open(os.path.join(os.path.dirname(OUT), "ill", "pattern_tile.svg")).read()
tile_inner = tile.split(">", 1)[1].rsplit("</svg>", 1)[0]
tile_inner = tile_inner.split("/>", 1)[1]  # убрать фон
pat_dark = (f'<defs><pattern id="pd" width="160" height="160" patternUnits="userSpaceOnUse" patternTransform="scale(0.55)">'
            f'{tile_inner.replace(DARK, "#2E6B49")}</pattern></defs>')

# Визитка 90x50 мм -> 900x500
front = (pat_dark + f'<rect width="900" height="500" fill="{DARK}"/><rect width="900" height="500" fill="url(#pd)" opacity="0.5"/>'
         f'<g transform="translate(150,150)">{symbol(cx=100, cy=104, R=78, ring=CREAM, jar=CREAM, lid=GREEN, label=DARK, label_leaf=GREEN)}</g>'
         + T("ЗЕЛЁНЫЙ", 390, 245, 68, "InterDisplay-Black.otf", CREAM) + T("КРУГ", 390, 312, 68, "InterDisplay-Black.otf", CREAM)
         + T("продукты в многоразовой таре", 392, 352, 22, "Inter-Medium.otf", CREAM, op=0.85))
back = (f'<rect width="900" height="500" fill="{CREAM}"/>'
        f'<circle cx="840" cy="440" r="190" fill="none" stroke="{GREEN}" stroke-width="40" opacity="0.18"/>'
        f'<g transform="translate(60,60) scale(0.42)">{symbol()}</g>'
        + T("Анна Смирнова", 70, 220, 46, "InterDisplay-Black.otf", DARK)
        + T("менеджер по работе с партнёрами", 72, 262, 22, "Inter-Medium.otf", INK, op=0.7)
        + f'<rect x="72" y="296" width="60" height="6" rx="3" fill="{PUMPKIN}"/>'
        + T("+7 (900) 000-00-00", 72, 352, 24, "Inter-SemiBold.otf", INK)
        + T("anna@zelkrug.ru", 72, 390, 24, "Inter-SemiBold.otf", INK)
        + T("zelkrug.ru  ·  Москва, ул. Садовая, 12", 72, 428, 22, "Inter-Medium.otf", INK, op=0.7)
        + f'<rect x="0" y="480" width="900" height="20" fill="{GREEN}"/>')
im_front = save("card_front", front, 900, 500, 1350)
im_back = save("card_back", back, 900, 500, 1350)

# Бланк A4 840x1188
lines = ["Уважаемые партнёры!",
         "",
         "Сервис «Зелёный Круг» приглашает фермерские хозяйства и небольших",
         "производителей к сотрудничеству. Мы доставляем продукты горожанам",
         "в многоразовой стеклянной таре и забираем пустые банки при следующем",
         "заказе — без одноразовой упаковки.",
         "",
         "Предлагаем долгосрочный договор поставок, собственную логистику",
         "и прозрачные условия оплаты. Будем рады обсудить детали на встрече.",
         "",
         "С уважением,",
         "Анна Смирнова, менеджер по работе с партнёрами"]
body = [f'<rect width="840" height="1188" fill="#FFFFFF"/>',
        f'<g transform="translate(52,44) scale(0.42)">{symbol()}</g>',
        T("ЗЕЛЁНЫЙ", 150, 92, 30, "InterDisplay-Black.otf", DARK), T("КРУГ", 150, 122, 30, "InterDisplay-Black.otf", DARK),
        T("zelkrug.ru", 788, 76, 15, "Inter-SemiBold.otf", DARK, "end"),
        T("8 800 000-00-00", 788, 98, 15, "Inter-Medium.otf", INK, "end", op=0.75),
        T("Москва, ул. Садовая, 12", 788, 120, 15, "Inter-Medium.otf", INK, "end", op=0.75),
        f'<rect x="56" y="156" width="732" height="4" rx="2" fill="{GREEN}"/>',
        f'<rect x="56" y="156" width="120" height="4" rx="2" fill="{PUMPKIN}"/>',
        T("Исх. № 24/11 от 11.11.2026", 56, 210, 15, "Inter-Medium.otf", INK, op=0.6)]
y = 280
for i, l in enumerate(lines):
    if l:
        f = "Inter-SemiBold.otf" if i in (0, 11) else "Inter-Regular.otf"
        body.append(T(l, 56, y, 17, f, INK))
    y += 30
body.append(f'<g opacity="0.07" transform="translate(470,760) scale(2.0)">{symbol(ring=DARK, leaf=DARK, jar=DARK, lid=DARK, label="#fff", label_leaf=DARK)}</g>')
body.append(pat_dark.replace('id="pd"', 'id="pf"') + f'<rect x="0" y="1110" width="840" height="78" fill="{DARK}"/><rect x="0" y="1110" width="840" height="78" fill="url(#pf)" opacity="0.6"/>')
body.append(T("Тара едет по кругу", 56, 1156, 18, "InterDisplay-Black.otf", CREAM))
im_letter = save("letterhead", "".join(body), 840, 1188, 1260)


# Сцена
def shadowed(im, angle, blur=18, off=(14, 22), op=0.35):
    im = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    a = im.split()[-1]
    sh = Image.new("RGBA", im.size, (20, 30, 20, 0))
    sh.putalpha(a.point(lambda v: int(v * op)))
    pad = blur * 3
    canvas = Image.new("RGBA", (im.width + pad * 2 + abs(off[0]), im.height + pad * 2 + abs(off[1])), (0, 0, 0, 0))
    canvas.alpha_composite(sh, (pad + off[0], pad + off[1]))
    canvas = canvas.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(im, (pad, pad))
    return canvas


def desk(W, H, base):
    lin = Image.open(os.path.join(os.path.dirname(OUT), "site", "assets", "tex_linen.png")).convert("RGB")
    bg = Image.new("RGB", (W, H))
    for x in range(0, W, lin.width):
        for y in range(0, H, lin.height):
            bg.paste(lin, (x, y))
    tint = Image.new("RGB", (W, H), base)
    bg = Image.blend(bg, tint, 0.55)
    yy, xx = np.mgrid[0:H, 0:W]
    v = 1 - 0.35 * (((xx - W * 0.45) / W) ** 2 + ((yy - H * 0.4) / H) ** 2)
    arr = (np.asarray(bg, "f4") * v[..., None]).clip(0, 255).astype("u1")
    return Image.fromarray(arr).convert("RGBA")


W, H = 2400, 1500
scene = desk(W, H, (226, 236, 220))
L = im_letter.resize((820, int(820 * 1188 / 840)), Image.LANCZOS)
s = shadowed(L, 7)
scene.alpha_composite(s, (180, -60))
cb = shadowed(im_back.resize((760, 422), Image.LANCZOS), -9)
scene.alpha_composite(cb, (1180, 640))
cf = shadowed(im_front.resize((760, 422), Image.LANCZOS), 4)
scene.alpha_composite(cf, (1320, 170))
# листочки на столе
leaf_svg = svg(200, 120, f'<path d="M10,60 Q70,0 190,40 Q110,120 10,60Z" fill="{GREEN}"/><path d="M20,60 L160,45" stroke="{DARK}" stroke-width="4" opacity="0.4"/>')
open("/tmp/leaf.svg", "w").write(leaf_svg)
subprocess.run(["rsvg-convert", "-w", "260", "/tmp/leaf.svg", "-o", "/tmp/leaf.png"], check=True)
lf = Image.open("/tmp/leaf.png").convert("RGBA")
scene.alpha_composite(shadowed(lf, 30, 8, (6, 10), 0.3), (2050, 1150))
scene.alpha_composite(shadowed(lf.resize((180, 83)), -50, 8, (6, 10), 0.3), (1080, 1270))
scene.convert("RGB").save(f"{OUT}/mockup_stationery.jpg", quality=92)

# отдельная сцена визиток
scene2 = desk(1800, 1200, (31, 81, 54))
scene2.alpha_composite(shadowed(im_back.resize((900, 500), Image.LANCZOS), -6, 22, (16, 26), 0.5), (120, 470))
scene2.alpha_composite(shadowed(im_front.resize((900, 500), Image.LANCZOS), 8, 22, (16, 26), 0.5), (720, 80))
scene2.convert("RGB").save(f"{OUT}/mockup_cards.jpg", quality=92)
print("ok")
