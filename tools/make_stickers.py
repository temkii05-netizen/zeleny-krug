"""Стикеры (PNG с белой обводкой) и GIF-анимации на основе плоского талисмана."""
import os, sys, math
import numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from mascot2d import *

OUT = sys.argv[1]
os.makedirs(OUT + "/svg", exist_ok=True)
VB = '0 -40 300 400'


def wrap(body, vb=VB):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="300" height="400">{body}</svg>'


def outline(im, r=14):
    a = np.array(im.split()[-1])
    big = Image.fromarray(a).filter(ImageFilter.MaxFilter(r * 2 + 1)).filter(ImageFilter.GaussianBlur(1.2))
    white = Image.new("RGBA", im.size, (255, 255, 255, 0))
    white.putalpha(big)
    sh = Image.new("RGBA", im.size, (20, 39, 28, 0))
    sh.putalpha(big.point(lambda v: int(v * 0.25)).filter(ImageFilter.GaussianBlur(6)))
    base = Image.new("RGBA", im.size, (0, 0, 0, 0))
    base.alpha_composite(sh, (6, 8))
    base.alpha_composite(white)
    base.alpha_composite(im)
    return base


def sticker(name, body):
    s = wrap(body)
    svgp = f"{OUT}/svg/{name}.svg"
    open(svgp, "w").write(s)
    tmp = f"/tmp/{name}.png"
    subprocess.run(["rsvg-convert", "-w", "420", svgp, "-o", tmp], check=True)
    im = Image.open(tmp).convert("RGBA")
    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    im.thumbnail((440, 440), Image.LANCZOS)
    canvas.alpha_composite(im, ((512 - im.width) // 2, (512 - im.height) // 2))
    outline(canvas).save(f"{OUT}/sticker_{name}.png")


STICK = {
    "privet": mascot("happy", right=(262, 150)) + bubble("ПРИВЕТ!", 150, -10, 34),
    "nyam": mascot("wink", right=(240, 230), extra=carrot(246, 205, 25)) + bubble("НЯМ!", 70, 10, 34, rot=-8),
    "lyublyu": mascot("love", left=(36, 160), right=(264, 160)) + heart(250, 50, 1.4) + heart(50, 60, 1.0) + heart(200, -5, 0.8),
    "vozvrat": mascot("happy", left=(40, 210), extra=small_jar(36, 200, 0.95)) + bubble("ВЕРНИ ТАРУ", 150, -12, 28),
    "splyu": mascot("sleep", left=(70, 270), right=(230, 270)) + bubble("Zzz", 245, 20, 30, bg=CREAM, rot=8),
    "wow": mascot("wow", left=(48, 140), right=(252, 140)) + bubble("БЕЗ ПЛАСТИКА!", 150, -14, 24, bg=GREEN, fg=DARK),
}
for k, v in STICK.items():
    sticker(k, v)

# GIF-анимации
FR = OUT + "/frames"
os.makedirs(FR, exist_ok=True)


def gif(name, frames_svg, dur=60, bg=CREAM):
    imgs = []
    for i, body in enumerate(frames_svg):
        s = wrap(f'<rect x="0" y="-40" width="300" height="400" fill="{bg}"/>' + body)
        p = f"{FR}/{name}_{i:03d}.svg"
        open(p, "w").write(s)
        subprocess.run(["rsvg-convert", "-w", "360", p, "-o", p[:-4] + ".png"], check=True)
        imgs.append(Image.open(p[:-4] + ".png").convert("RGB"))
    pal = [im.quantize(colors=128, method=Image.MEDIANCUT, dither=Image.NONE) for im in imgs]
    pal[0].save(f"{OUT}/{name}.gif", save_all=True, append_images=pal[1:], duration=dur, loop=0, optimize=True)


N = 20
fr = []
for i in range(N):
    t = i / N
    ang = math.sin(t * 4 * math.pi)
    hx, hy = 258 + 10 * ang, 148 - 14 * abs(ang)
    dy = -10 * abs(math.sin(t * 2 * math.pi))
    fr.append(mascot("happy" if i not in (13, 14) else "sleep", right=(hx, hy), dy=dy, leaf_rot=6 * ang)
              + bubble("ПРИВЕТ!", 150, -8, 32, rot=-4 + 3 * ang))
gif("gif_privet", fr, 60)

fr = []
for i in range(N):
    t = i / N
    br = 1 + 0.03 * math.sin(t * 2 * math.pi)
    zs = "".join(
        f'<g opacity="{max(0, 1 - ((t + k / 3) % 1)):.2f}">{text_svg}</g>'.replace(
            "{text_svg}", "")
        for k in range(0))
    zz = ""
    for k in range(3):
        p = (t + k / 3) % 1
        d, _ = text_path("Z", 220 + 40 * p, 100 - 90 * p, 22 + 18 * p, "InterDisplay-Black.otf")
        zz += f'<path d="{d}" fill="{DARK}" opacity="{(1 - p) * min(1, p * 4):.2f}"/>'
    fr.append(mascot("sleep", left=(70, 270), right=(230, 270), squash=br) + zz)
gif("gif_splyu", fr, 90, bg="#DDEFD9")

fr = []
for i in range(N):
    t = i / N
    hs = ""
    for k, (x0, sp) in enumerate([(60, 1), (150, 1.3), (240, 0.9), (105, 1.1), (200, 1.2)]):
        p = (t * sp + k * 0.21) % 1
        hs += heart(x0 + 10 * math.sin(p * 6 + k), 120 - 150 * p, 0.6 + 0.6 * p, op=f"{(1 - p):.2f}")
    beat = 1.3 + 0.15 * abs(math.sin(t * 2 * math.pi * 2))
    fr.append(mascot("love", left=(36, 160), right=(264, 160), dy=-6 * abs(math.sin(t * 4 * math.pi))) + heart(250, 50, beat) + hs)
gif("gif_lyublyu", fr, 70, bg="#FCE7D2")

fr = []
for i in range(N):
    t = i / N
    rot = t * 360
    fr.append(mascot("wink", right=(250, 160), dy=-4 * abs(math.sin(t * 2 * math.pi)))
              + f'<g transform="rotate({rot},48,120)">{recycle(48, 120, 26)}</g>'
              + bubble("ТАРА ПО КРУГУ", 175, -12, 24, bg=GREEN, rot=-3))
gif("gif_krug", fr, 60)
print("ok")
