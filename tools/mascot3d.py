"""3D-талисман «Кругляш» — SDF-raymarching рендер на numpy.
Сцена: многоразовая банка с крышкой, росток, глаза, улыбка, ручки, ножки."""
import numpy as np
from PIL import Image
import sys, math

f32 = np.float32


def hexc(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], f32) ** 2.2


MAT = {
    0: hexc('#F3EEDF'),  # пол
    1: hexc('#BFE6C8'),  # стекло банки (мятное)
    2: hexc('#4CAF5A'),  # крышка
    3: hexc('#15241A'),  # глаза
    4: hexc('#FFFFFF'),  # блики глаз
    5: hexc('#1F5136'),  # руки/ноги
    6: hexc('#5DBB63'),  # листья
    7: hexc('#F6F1E4'),  # этикетка
    8: hexc('#2B4A35'),  # рот
    9: hexc('#F59C8B'),  # щёчки
    10: hexc('#F4A93B'),  # акцент этикетки
}


def length(x, y, z):
    return np.sqrt(x * x + y * y + z * z)


def sd_round_cyl(px, py, pz, r, h, rr):
    dx = np.sqrt(px * px + pz * pz) - r + rr
    dy = np.abs(py) - h + rr
    return np.minimum(np.maximum(dx, dy), 0) + np.sqrt(np.maximum(dx, 0) ** 2 + np.maximum(dy, 0) ** 2) - rr


def sd_capsule(px, py, pz, a, b, r):
    pax, pay, paz = px - a[0], py - a[1], pz - a[2]
    bax, bay, baz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    h = np.clip((pax * bax + pay * bay + paz * baz) / (bax * bax + bay * bay + baz * baz), 0, 1)
    return length(pax - bax * h, pay - bay * h, paz - baz * h) - r


def sd_ellipsoid(px, py, pz, c, r):
    x, y, z = (px - c[0]) / r[0], (py - c[1]) / r[1], (pz - c[2]) / r[2]
    k0 = length(x, y, z)
    k1 = length(x / r[0], y / r[1], z / r[2])
    return k0 * (k0 - 1) / np.maximum(k1, 1e-6)


def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


class Pose:
    def __init__(self, yaw=0.0, bounce=0.0, squash=1.0, blink=0.0, wave=0.0, smile=1.0, tilt=0.0):
        self.yaw, self.bounce, self.squash = yaw, bounce, squash
        self.blink, self.wave, self.smile, self.tilt = blink, wave, smile, tilt


FLOOR = -1.41


def scene(px, py, pz, P, want_mat=False):
    # пол
    d_floor = py - FLOOR
    # трансформация персонажа: прыжок, наклон, поворот
    y0 = py - P.bounce
    c, s = math.cos(P.yaw), math.sin(P.yaw)
    x = c * px + s * pz
    z = -s * px + c * pz
    ct, st = math.cos(P.tilt), math.sin(P.tilt)
    x, y = ct * x + st * y0, -st * x + ct * y0
    y = (y + 1.3) / P.squash - 1.3
    sq = P.squash

    parts = []
    body = sd_round_cyl(x, y, z, 0.92, 0.92, 0.38)
    neck = sd_round_cyl(x, y - 1.0, z, 0.66, 0.16, 0.08)
    glass = smin(body, neck, 0.12)
    parts.append((glass, 1))
    # крышка с рёбрами
    ang = np.arctan2(z, x)
    lid = sd_round_cyl(x, y - 1.27, z, 0.78, 0.17, 0.07) - 0.007 * np.cos(ang * 32)
    parts.append((lid, 2))
    # этикетка — тонкая лента вокруг низа банки
    lab = np.maximum(sd_round_cyl(x, y + 0.5, z, 0.945, 0.26, 0.02), -body - 0.03)
    parts.append((lab, 7))
    # значок-кружок на этикетке
    parts.append((sd_ellipsoid(x, y, z, (0.0, -0.5, 0.93), (0.17, 0.17, 0.05)), 6))
    # росток
    stem = sd_capsule(x, y, z, (0, 1.4, 0), (0.06, 1.78, 0.0), 0.045)
    parts.append((stem, 6))
    l1 = sd_ellipsoid(*_rot_z(x - 0.26, y - 1.86, z, -0.55), (0, 0, 0), (0.27, 0.085, 0.14))
    l2 = sd_ellipsoid(*_rot_z(x + 0.14, y - 1.8, z, 0.6), (0, 0, 0), (0.2, 0.07, 0.11))
    parts.append((np.minimum(l1, l2), 6))
    # глаза
    eh = 0.19 * max(0.08, 1 - P.blink)
    for sx in (-1, 1):
        e = sd_ellipsoid(x, y, z, (sx * 0.33, 0.28, 0.86), (0.12, eh, 0.1))
        parts.append((e, 3))
        if P.blink < 0.5:
            hl = length(x - (sx * 0.33 - 0.04), y - 0.35, z - 0.94) - 0.04
            parts.append((hl, 4))
        ck = sd_ellipsoid(x, y, z, (sx * 0.6, 0.02, 0.72), (0.15, 0.08, 0.06))
        parts.append((ck, 9))
    # улыбка — дуга тора
    mx, my, mz = x, y - 0.12, z - 0.9
    R = 0.17
    q = np.sqrt(mx * mx + (my / max(P.smile, 0.3)) ** 2) - R
    tor = np.sqrt(q * q + mz * mz) - 0.035
    mouth = np.maximum(tor, my + 0.02)
    parts.append((mouth, 8))
    # ручки
    w = P.wave
    for sx in (-1, 1):
        lift = w if sx == 1 else 0.0
        a = (sx * 0.88, 0.0, 0.05)
        b = (sx * (1.18 + 0.12 * lift), -0.32 + 0.9 * lift, 0.22)
        parts.append((sd_capsule(x, y, z, a, b, 0.12), 5))
        parts.append((sd_ellipsoid(x, y, z, b, (0.15, 0.15, 0.15)), 5))
    # ножки
    for sx in (-1, 1):
        parts.append((sd_ellipsoid(x, y, z, (sx * 0.4, -1.27, 0.22), (0.25, 0.14, 0.32)), 5))

    d = d_floor
    m = np.zeros_like(px, dtype=np.int8)
    for dd, mid in parts:
        dd = dd * min(sq, 1.0)
        if want_mat:
            sel = dd < d
            m = np.where(sel, mid, m)
        d = np.minimum(d, dd)
    return (d, m) if want_mat else d


def _rot_z(x, y, z, a):
    c, s = math.cos(a), math.sin(a)
    return c * x + s * y, -s * x + c * y, z


def render(W=600, H=600, P=None, bg_top='#F6F1E4', bg_bot='#E3EFD9', transparent=False, ss=1, cam_dist=7.2):
    P = P or Pose()
    Wr, Hr = W * ss, H * ss
    ro = np.array([0.0, 0.55, cam_dist], f32)
    ta = np.array([0.0, 0.2, 0.0], f32)
    fw = ta - ro; fw /= np.linalg.norm(fw)
    rt = np.cross(fw, [0, 1, 0]); rt /= np.linalg.norm(rt)
    up = np.cross(rt, fw)
    ys, xs = np.mgrid[0:Hr, 0:Wr].astype(f32)
    u = (xs - Wr / 2) / Hr
    v = -(ys - Hr / 2) / Hr
    fl = 1.55
    dx = rt[0] * u + up[0] * v + fw[0] * fl
    dy = rt[1] * u + up[1] * v + fw[1] * fl
    dz = rt[2] * u + up[2] * v + fw[2] * fl
    n = length(dx, dy, dz); dx /= n; dy /= n; dz /= n
    N = dx.size
    dx, dy, dz = dx.ravel(), dy.ravel(), dz.ravel()
    t = np.zeros(N, f32)
    hit = np.zeros(N, bool)
    alive = np.ones(N, bool)
    for i in range(140):
        idx = np.nonzero(alive)[0]
        if idx.size == 0:
            break
        px = ro[0] + dx[idx] * t[idx]; py = ro[1] + dy[idx] * t[idx]; pz = ro[2] + dz[idx] * t[idx]
        d = scene(px, py, pz, P)
        t[idx] += d * 0.9
        done = d < 0.0015 * t[idx]
        far = t[idx] > 20
        hit[idx[done]] = True
        alive[idx[done | far]] = False
    px = ro[0] + dx * t; py = ro[1] + dy * t; pz = ro[2] + dz * t
    col = np.zeros((N, 3), f32)
    alpha = np.zeros(N, f32)
    # фон
    gy = (v.ravel() + 0.5)
    c_top, c_bot = hexc(bg_top), hexc(bg_bot)
    bgc = c_bot[None] * (1 - gy[:, None]) + c_top[None] * gy[:, None]
    hi = np.nonzero(hit)[0]
    hx, hy, hz = px[hi], py[hi], pz[hi]
    _, mat = scene(hx, hy, hz, P, want_mat=True)
    e = 0.002
    nx = scene(hx + e, hy, hz, P) - scene(hx - e, hy, hz, P)
    ny = scene(hx, hy + e, hz, P) - scene(hx, hy - e, hz, P)
    nz = scene(hx, hy, hz + e, P) - scene(hx, hy, hz - e, P)
    nl = length(nx, ny, nz) + 1e-9; nx /= nl; ny /= nl; nz /= nl
    L = np.array([-0.55, 0.8, 0.55], f32); L /= np.linalg.norm(L)
    dif = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
    # мягкая тень
    sh = np.ones(hi.size, f32)
    tt = np.full(hi.size, 0.03, f32)
    ox, oy, oz = hx + nx * 0.01, hy + ny * 0.01, hz + nz * 0.01
    for i in range(48):
        h = scene(ox + L[0] * tt, oy + L[1] * tt, oz + L[2] * tt, P)
        sh = np.minimum(sh, np.clip(10 * h / tt, 0, 1))
        tt += np.clip(h, 0.02, 0.25)
        if tt.min() > 6:
            break
    sh = sh * sh * (3 - 2 * sh)
    # AO
    ao = np.zeros(hi.size, f32)
    sc = 1.0
    for i in range(1, 6):
        hr = 0.03 + 0.09 * i
        dd = scene(hx + nx * hr, hy + ny * hr, hz + nz * hr, P)
        ao += (hr - dd) * sc
        sc *= 0.75
    ao = np.clip(1 - 2.2 * ao, 0, 1)
    vx, vy, vz = -dx[hi], -dy[hi], -dz[hi]
    hx_, hy_, hz_ = L[0] + vx, L[1] + vy, L[2] + vz
    hl = length(hx_, hy_, hz_); hx_ /= hl; hy_ /= hl; hz_ /= hl
    ndh = np.clip(nx * hx_ + ny * hy_ + nz * hz_, 0, 1)
    ndv = np.clip(nx * vx + ny * vy + nz * vz, 0, 1)
    fre = (1 - ndv) ** 4
    base = np.zeros((hi.size, 3), f32)
    for k, cval in MAT.items():
        base[mat == k] = cval
    shin = np.where(np.isin(mat, [1, 3, 4]), 90, 24).astype(f32)
    ks = np.where(np.isin(mat, [1, 3]), 0.9, np.where(mat == 0, 0.0, 0.25)).astype(f32)
    spec = ks * ndh ** shin * sh
    sky = 0.5 + 0.5 * ny
    lin = (dif * sh)[:, None] * np.array([1.0, 0.96, 0.88], f32) * 1.25
    lin += (sky * ao)[:, None] * np.array([0.42, 0.5, 0.48], f32)
    bounce = np.clip(-ny, 0, 1) * ao
    lin += bounce[:, None] * np.array([0.25, 0.22, 0.16], f32)
    rimw = np.where(mat == 1, 0.55, 0.15)
    c = base * lin + spec[:, None] + (fre * rimw * ao)[:, None] * np.array([0.9, 1.0, 0.95], f32)
    # пол: смешиваем с фоном, оставляя тень
    flo = mat == 0
    fade = np.clip(1 - np.sqrt(hx ** 2 + hz ** 2) / 3.5, 0, 1)
    shadow_amt = (1 - sh * (0.55 + 0.45 * ao)) * fade
    col[hi] = c
    a = np.ones(hi.size, f32)
    if transparent:
        col[hi[flo]] = 0
        a[flo] = np.clip(shadow_amt[flo] * 0.55, 0, 1)
    else:
        col[hi[flo]] = bgc[hi[flo]] * (1 - 0.5 * shadow_amt[flo])[:, None]
    alpha[hi] = a
    if not transparent:
        miss = ~hit
        col[miss] = bgc[miss]
        alpha[:] = 1
    col = np.clip(col, 0, 1) ** (1 / 2.2)
    img = np.concatenate([col, alpha[:, None]], 1).reshape(Hr, Wr, 4)
    im = Image.fromarray((img * 255).astype(np.uint8), 'RGBA')
    if ss > 1:
        im = im.resize((W, H), Image.LANCZOS)
    return im


if __name__ == '__main__':
    out = sys.argv[1]
    W = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    yaw = float(sys.argv[3]) if len(sys.argv) > 3 else -0.35
    im = render(W, W, Pose(yaw=yaw, wave=float(sys.argv[4]) if len(sys.argv) > 4 else 0))
    im.save(out)
