"""3D-визуализация упаковки: банки с этикетками + крафтовая коробка (SDF raymarching)."""
import sys, os, math
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from mascot3d import sd_round_cyl, length, hexc, f32

PACK = sys.argv[1] if len(sys.argv) > 1 else "pack"


def tex(path):
    return (np.asarray(Image.open(path).convert("RGB"), f32) / 255) ** 2.2


LABELS = [tex(f"{PACK}/label_jar_grechka.png"), tex(f"{PACK}/label_jar_ovsyanka.png"), tex(f"{PACK}/label_jar_mindal.png")]
BOXT = tex(f"{PACK}/box_front.png")

# x, z, радиус, высота, крышка, содержимое, этикетка
JARS = [(1.05, 0.25, 0.62, 1.9, hexc('#5DBB63'), hexc('#7A4A2E'), 0),
        (2.35, 0.75, 0.5, 1.35, hexc('#F4A93B'), hexc('#E6D3A6'), 1),
        (0.15, 1.35, 0.45, 1.05, hexc('#1F5136'), hexc('#B97A45'), 2)]
BOX_C = np.array([-1.35, 0.9, -0.6], f32)
BOX_H = np.array([1.3, 0.9, 0.75], f32)


def sd_box(px, py, pz, c, h, r=0.04):
    qx = np.abs(px - c[0]) - h[0] + r
    qy = np.abs(py - c[1]) - h[1] + r
    qz = np.abs(pz - c[2]) - h[2] + r
    return length(np.maximum(qx, 0), np.maximum(qy, 0), np.maximum(qz, 0)) + np.minimum(np.maximum(qx, np.maximum(qy, qz)), 0) - r


def scene(px, py, pz, want=False):
    d = py.copy()
    m = np.zeros(px.shape, np.int16)

    def put(dd, mid):
        nonlocal d, m
        if want:
            m = np.where(dd < d, mid, m)
        d = np.minimum(d, dd)

    put(sd_box(px, py, pz, BOX_C, BOX_H), 40)
    # крышка коробки — щель
    for k, (x, z, r, h, *_rest) in enumerate(JARS):
        lx, lz = px - x, pz - z
        hb = h * 0.42
        cyb = hb
        put(sd_round_cyl(lx, py - cyb, lz, r, hb, r * 0.3), 10 + k)
        put(sd_round_cyl(lx, py - (2 * hb + 0.05), lz, r * 0.78, 0.08, 0.03), 10 + k)
        put(sd_round_cyl(lx, py - (2 * hb + 0.17), lz, r * 0.86, 0.1, 0.035) - 0.004 * np.cos(np.arctan2(lz, lx) * 40), 20 + k)
        lab = np.maximum(sd_round_cyl(lx, py - hb * 0.9, lz, r + 0.012, hb * 0.55, 0.01), -sd_round_cyl(lx, py - cyb, lz, r - 0.02, hb, r * 0.3))
        put(lab, 30 + k)
    return (d, m) if want else d


def render(W, H, ss=1, out="pack_3d.png"):
    Wr, Hr = W * ss, H * ss
    ro = np.array([1.3, 2.7, 7.4], f32)
    ta = np.array([0.35, 0.8, 0.0], f32)
    fw = ta - ro; fw /= np.linalg.norm(fw)
    rt = np.cross(fw, [0, 1, 0]); rt /= np.linalg.norm(rt)
    up = np.cross(rt, fw)
    ys, xs = np.mgrid[0:Hr, 0:Wr].astype(f32)
    u = (xs - Wr / 2) / Hr; v = -(ys - Hr / 2) / Hr
    dx = rt[0] * u + up[0] * v + fw[0] * 1.6
    dy = rt[1] * u + up[1] * v + fw[1] * 1.6
    dz = rt[2] * u + up[2] * v + fw[2] * 1.6
    n = length(dx, dy, dz); dx = (dx / n).ravel(); dy = (dy / n).ravel(); dz = (dz / n).ravel()
    N = dx.size
    t = np.zeros(N, f32); hit = np.zeros(N, bool); alive = np.ones(N, bool)
    for i in range(160):
        idx = np.nonzero(alive)[0]
        if idx.size == 0: break
        p = (ro[0] + dx[idx] * t[idx], ro[1] + dy[idx] * t[idx], ro[2] + dz[idx] * t[idx])
        d = scene(*p)
        t[idx] += d * 0.9
        done = d < 0.0012 * t[idx]; far = t[idx] > 30
        hit[idx[done]] = True; alive[idx[done | far]] = False
    gy = v.ravel() + 0.5
    bg = hexc('#E6F0DE')[None] * (1 - gy[:, None]) + hexc('#F6F1E4')[None] * gy[:, None]
    col = bg.copy()
    hi = np.nonzero(hit)[0]
    hx, hy, hz = ro[0] + dx[hi] * t[hi], ro[1] + dy[hi] * t[hi], ro[2] + dz[hi] * t[hi]
    _, mat = scene(hx, hy, hz, True)
    e = 0.0015
    nx = scene(hx + e, hy, hz) - scene(hx - e, hy, hz)
    ny = scene(hx, hy + e, hz) - scene(hx, hy - e, hz)
    nz = scene(hx, hy, hz + e) - scene(hx, hy, hz - e)
    nl = length(nx, ny, nz) + 1e-9; nx /= nl; ny /= nl; nz /= nl
    base = np.zeros((hi.size, 3), f32)
    base[mat == 0] = hexc('#F1ECDD')
    box = mat == 40
    base[box] = hexc('#C9A06B')
    front = box & (nz > 0.9)
    if front.any():
        fu = (hx[front] - (BOX_C[0] - BOX_H[0])) / (2 * BOX_H[0])
        fv = 1 - (hy[front] - (BOX_C[1] - BOX_H[1])) / (2 * BOX_H[1])
        ix = np.clip((fu * BOXT.shape[1]).astype(int), 0, BOXT.shape[1] - 1)
        iy = np.clip((fv * BOXT.shape[0]).astype(int), 0, BOXT.shape[0] - 1)
        base[front] = BOXT[iy, ix]
    top = box & (ny > 0.9)
    seam = top & (np.abs(hz - BOX_C[2]) < 0.012)
    base[seam] = hexc('#9C7646')
    tape = top & (np.abs(hx - BOX_C[0]) < 0.18)
    base[tape] = hexc('#5DBB63')
    glassy = np.zeros(hi.size, bool)
    for k, (x, z, r, h, lidc, cont, li) in enumerate(JARS):
        g = mat == 10 + k
        level = h * 0.62
        base[g] = np.where((hy[g] < level)[:, None], cont[None] * 0.85, hexc('#CFEBD9')[None])
        glassy |= g
        base[mat == 20 + k] = lidc
        lb = mat == 30 + k
        if lb.any():
            ang = np.arctan2(hx[lb] - x, hz[lb] - z) - math.atan2(1.3 - x, 7.4 - z)
            ang = (ang + math.pi) % (2 * math.pi) - math.pi
            uu = 0.5 + 0.035 + ang / (2 * math.pi)
            hb = h * 0.42
            y0, y1 = hb * 0.9 - hb * 0.55, hb * 0.9 + hb * 0.55
            vv = 1 - (hy[lb] - y0) / (y1 - y0)
            T = LABELS[li]
            ix = np.clip((uu * T.shape[1]).astype(int), 0, T.shape[1] - 1)
            iy = np.clip((vv * T.shape[0]).astype(int), 0, T.shape[0] - 1)
            base[lb] = T[iy, ix]
    L = np.array([-0.5, 0.85, 0.45], f32); L /= np.linalg.norm(L)
    dif = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
    sh = np.ones(hi.size, f32); tt = np.full(hi.size, 0.03, f32)
    ox, oy, oz = hx + nx * 0.01, hy + ny * 0.01, hz + nz * 0.01
    for i in range(56):
        h_ = scene(ox + L[0] * tt, oy + L[1] * tt, oz + L[2] * tt)
        sh = np.minimum(sh, np.clip(9 * h_ / tt, 0, 1)); tt += np.clip(h_, 0.02, 0.3)
    sh = sh * sh * (3 - 2 * sh)
    ao = np.zeros(hi.size, f32); sc = 1.0
    for i in range(1, 6):
        hr = 0.03 + 0.1 * i
        ao += (hr - scene(hx + nx * hr, hy + ny * hr, hz + nz * hr)) * sc; sc *= 0.7
    ao = np.clip(1 - 2.0 * ao, 0, 1)
    vx, vy, vz = -dx[hi], -dy[hi], -dz[hi]
    hhx, hhy, hhz = L[0] + vx, L[1] + vy, L[2] + vz
    hl = length(hhx, hhy, hhz)
    ndh = np.clip((nx * hhx + ny * hhy + nz * hhz) / hl, 0, 1)
    ndv = np.clip(nx * vx + ny * vy + nz * vz, 0, 1)
    fre = (1 - ndv) ** 4
    ks = np.where(glassy, 1.0, np.where(mat >= 20, 0.3, 0.05))
    shin = np.where(glassy, 120, 30)
    lin = (dif * sh)[:, None] * np.array([1.0, 0.96, 0.9], f32) * 1.2 + ((0.5 + 0.5 * ny) * ao)[:, None] * np.array([0.42, 0.48, 0.45], f32)
    c = base * lin + (ks * ndh ** shin * sh)[:, None] + (fre * np.where(glassy, 0.6, 0.1) * ao)[:, None]
    flo = mat == 0
    fade = np.clip(1 - np.sqrt((hx - 0.3) ** 2 + hz ** 2) / 6, 0, 1)
    c[flo] = bg[hi[flo]] * (1 - 0.55 * (1 - sh[flo] * (0.5 + 0.5 * ao[flo])) * fade[flo])[:, None]
    col[hi] = c
    col = np.clip(col, 0, 1) ** (1 / 2.2)
    im = Image.fromarray((col.reshape(Hr, Wr, 3) * 255).astype(np.uint8))
    if ss > 1: im = im.resize((W, H), Image.LANCZOS)
    im.save(out)


if __name__ == "__main__":
    render(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
