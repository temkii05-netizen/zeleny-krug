"""Плоский векторный «Кругляш» для стикеров, гифок, иллюстраций."""
import math, os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from brand import *

MINT = "#C6EBCF"
PINK = "#F59C8B"
SW = 6  # толщина контура


def arm(sx, sy, ex, ey):
    return (f'<path d="M{sx},{sy} Q{(sx+ex)/2 + (8 if ex > sx else -8)},{(sy+ey)/2 + 6} {ex},{ey}" '
            f'stroke="{DARK}" stroke-width="15" stroke-linecap="round" fill="none"/>'
            f'<circle cx="{ex}" cy="{ey}" r="12" fill="{DARK}"/>')


def eyes(expr):
    o = []
    if expr in ("happy", "wow", "wave"):
        for x in (122, 178):
            ry = 15 if expr == "wow" else 13
            o.append(f'<ellipse cx="{x}" cy="170" rx="9.5" ry="{ry}" fill="{INK}"/>'
                     f'<circle cx="{x-3}" cy="{164}" r="3.6" fill="#fff"/>')
    elif expr == "sleep":
        for x in (122, 178):
            o.append(f'<path d="M{x-11},170 Q{x},180 {x+11},170" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    elif expr == "wink":
        o.append(f'<ellipse cx="122" cy="170" rx="9.5" ry="13" fill="{INK}"/><circle cx="119" cy="164" r="3.6" fill="#fff"/>')
        o.append(f'<path d="M167,172 Q178,162 189,172" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    elif expr == "love":
        for x in (122, 178):
            o.append(f'<path d="M{x},{182} C{x-22},{168} {x-10},{150} {x},{162} C{x+10},{150} {x+22},{168} {x},{182} Z" fill="#E8505B"/>')
    return "".join(o)


def mouth(expr):
    if expr == "wow":
        return f'<ellipse cx="150" cy="198" rx="9" ry="11" fill="{INK}"/><ellipse cx="150" cy="203" rx="5" ry="4" fill="{PINK}"/>'
    if expr == "sleep":
        return f'<ellipse cx="150" cy="198" rx="5" ry="4" fill="{INK}"/>'
    return (f'<path d="M134,190 Q150,212 166,190 Z" fill="{INK}"/>'
            f'<path d="M141,200 Q150,206 159,200 Q150,196 141,200Z" fill="{PINK}"/>')


def mascot(expr="happy", left=None, right=None, extra="", dy=0, squash=1.0, leaf_rot=0):
    """left/right — координаты кистей (x,y) или None (опущены)."""
    left = left or (52, 255)
    right = right or (248, 255)
    sq = f'translate(150,{330}) scale({2-squash:.3f},{squash:.3f}) translate(-150,-330)'
    body = f'''
<defs><clipPath id="bc"><rect x="70" y="118" width="160" height="186" rx="54"/></clipPath></defs>
<ellipse cx="150" cy="336" rx="80" ry="10" fill="{DARK}" opacity="0.15"/>
<g transform="translate(0,{dy}) {sq}">
 <ellipse cx="116" cy="318" rx="22" ry="13" fill="{DARK}"/>
 <ellipse cx="184" cy="318" rx="22" ry="13" fill="{DARK}"/>
 {arm(76, 215, *left)}
 {arm(224, 215, *right)}
 <rect x="100" y="98" width="100" height="30" rx="8" fill="{MINT}" stroke="{DARK}" stroke-width="{SW}"/>
 <rect x="70" y="118" width="160" height="186" rx="54" fill="{MINT}" stroke="{DARK}" stroke-width="{SW}"/>
 <g clip-path="url(#bc)"><rect x="60" y="238" width="180" height="46" fill="{CREAM}"/>
   <line x1="60" y1="238" x2="240" y2="238" stroke="{DARK}" stroke-width="4"/>
   <line x1="60" y1="284" x2="240" y2="284" stroke="{DARK}" stroke-width="4"/>
   <circle cx="150" cy="261" r="13" fill="{GREEN}" stroke="{DARK}" stroke-width="3"/></g>
 <rect x="70" y="118" width="160" height="186" rx="54" fill="none" stroke="{DARK}" stroke-width="{SW}"/>
 <rect x="86" y="140" width="11" height="48" rx="5.5" fill="#fff" opacity="0.65"/>
 <g transform="rotate({leaf_rot},150,72)">
  <path d="M150,72 Q148,52 152,36" stroke="{DARK}" stroke-width="5" fill="none" stroke-linecap="round"/>
  <path d="M152,38 Q170,14 196,24 Q180,48 152,38Z" fill="{GREEN}" stroke="{DARK}" stroke-width="4" stroke-linejoin="round"/>
  <path d="M150,42 Q132,24 112,32 Q126,52 150,42Z" fill="{GREEN}" stroke="{DARK}" stroke-width="4" stroke-linejoin="round"/>
 </g>
 <rect x="86" y="68" width="128" height="36" rx="11" fill="{GREEN}" stroke="{DARK}" stroke-width="{SW}"/>
 {''.join(f'<line x1="{x}" y1="76" x2="{x}" y2="96" stroke="{DARK}" stroke-width="2.5" opacity="0.35" stroke-linecap="round"/>' for x in range(100, 210, 12))}
 {eyes(expr)}
 <ellipse cx="104" cy="194" rx="11" ry="7" fill="{PINK}" opacity="0.9"/>
 <ellipse cx="196" cy="194" rx="11" ry="7" fill="{PINK}" opacity="0.9"/>
 {mouth(expr)}
 {extra}
</g>'''
    return body


def heart(x, y, s=1, c="#E8505B", op=1):
    return (f'<g transform="translate({x},{y}) scale({s})" opacity="{op}"><path d="M0,10 C-22,-4 -12,-24 0,-10 C12,-24 22,-4 0,10Z" '
            f'fill="{c}" stroke="{DARK}" stroke-width="3"/></g>')


def carrot(x, y, rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot})">'
            f'<path d="M-4,-30 Q-14,-48 -2,-52 M4,-30 Q10,-50 18,-44 M0,-30 Q2,-52 4,-56" stroke="{GREEN}" stroke-width="6" stroke-linecap="round" fill="none"/>'
            f'<path d="M-14,-30 Q0,-36 14,-30 L2,30 Q0,34 -2,30 Z" fill="{PUMPKIN}" stroke="{DARK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M-8,-14 L-2,-14 M-6,2 L0,2 M2,-22 L8,-22" stroke="{DARK}" stroke-width="3" stroke-linecap="round"/></g>')


def small_jar(x, y, s=1):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<rect x="-22" y="-20" width="44" height="50" rx="14" fill="{MINT}" stroke="{DARK}" stroke-width="4"/>'
            f'<rect x="-20" y="-34" width="40" height="14" rx="5" fill="{PUMPKIN}" stroke="{DARK}" stroke-width="4"/>'
            f'<circle cx="0" cy="8" r="8" fill="{GREEN}" stroke="{DARK}" stroke-width="3"/></g>')


def recycle(x, y, r=26, c=GREEN):
    o = []
    for k in range(3):
        a0 = k * 120 + 15
        a1 = a0 + 85
        p0 = (x + r * math.cos(math.radians(a0)), y + r * math.sin(math.radians(a0)))
        p1 = (x + r * math.cos(math.radians(a1)), y + r * math.sin(math.radians(a1)))
        o.append(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} A{r},{r} 0 0 1 {p1[0]:.1f},{p1[1]:.1f}" stroke="{c}" stroke-width="8" fill="none" stroke-linecap="round"/>')
        ang = math.radians(a1)
        tx, ty = -math.sin(ang), math.cos(ang)
        nx, ny = math.cos(ang), math.sin(ang)
        tip = (p1[0] + tx * 9, p1[1] + ty * 9)
        b1 = (p1[0] + nx * 9 - tx * 3, p1[1] + ny * 9 - ty * 3)
        b2 = (p1[0] - nx * 9 - tx * 3, p1[1] - ny * 9 - ty * 3)
        o.append(f'<path d="M{tip[0]:.1f},{tip[1]:.1f} L{b1[0]:.1f},{b1[1]:.1f} L{b2[0]:.1f},{b2[1]:.1f}Z" fill="{c}"/>')
    return "".join(o)


def bubble(text, cx, cy, size=30, bg=PUMPKIN, fg=DARK, rot=-4):
    d, w = text_path(text, cx, cy + size * 0.36, size, "InterDisplay-Black.otf", anchor="middle")
    pw, ph = w + size * 1.1, size * 1.7
    return (f'<g transform="rotate({rot},{cx},{cy})"><rect x="{cx-pw/2:.1f}" y="{cy-ph/2:.1f}" width="{pw:.1f}" height="{ph:.1f}" '
            f'rx="{ph/2:.1f}" fill="{bg}" stroke="{DARK}" stroke-width="5"/><path d="{d}" fill="{fg}"/></g>')


def render_svg(svg_text, path_png, w):
    tmp = path_png.replace(".png", ".svg")
    open(tmp, "w").write(svg_text)
    subprocess.run(["rsvg-convert", "-w", str(w), tmp, "-o", path_png], check=True)
    return tmp
