"""Genera el isotipo de Vitruvium: el Hombre de Vitruvio como malla de elementos finitos
coloreada como mapa de esfuerzos. Uso: python3 generate.py  (escribe los SVG en esta carpeta)."""
import math, random, re

random.seed(11)
# Figura = unión de cápsulas cónicas (x1, y1, r1, x2, y2, r2), en un lienzo de 512.
S = [
    (256, 114, 21, 256, 118, 21),                                   # cabeza (rostro)
    (256, 96, 22, 256, 100, 22),                                    # cabello: copa
    (238, 104, 13, 232, 156, 9), (274, 104, 13, 280, 156, 9),       # cabello: melena a los lados
    (244, 98, 14, 240, 140, 10), (268, 98, 14, 272, 140, 10),
    (256, 138, 10, 256, 160, 12),                                   # cuello
    (232, 164, 12, 280, 164, 12),                                   # hombros
    (256, 172, 40, 256, 212, 36), (256, 212, 36, 256, 258, 28),     # tórax y cintura
    (256, 258, 29, 256, 292, 36),                                   # cadera
    (226, 176, 14, 160, 178, 10), (160, 178, 10, 104, 180, 7),      # brazos horizontales
    (286, 176, 14, 352, 178, 10), (352, 178, 10, 408, 180, 7),
    (228, 172, 12, 176, 140, 9), (176, 140, 9, 124, 112, 6),        # brazos alzados
    (284, 172, 12, 336, 140, 9), (336, 140, 9, 388, 112, 6),
    (241, 296, 20, 236, 372, 13), (236, 372, 13, 232, 446, 8),      # piernas rectas
    (271, 296, 20, 276, 372, 13), (276, 372, 13, 280, 446, 8),
    (224, 450, 7, 236, 452, 7), (288, 450, 7, 276, 452, 7),         # pies
    (238, 300, 17, 200, 370, 11), (200, 370, 11, 168, 438, 7),      # piernas abiertas
    (274, 300, 17, 312, 370, 11), (312, 370, 11, 344, 438, 7),
]

def hand(ex, ey, dx, dy):
    """Palma y cinco dedos al final de un brazo que termina en (ex, ey) con dirección (dx, dy)."""
    L = math.hypot(dx, dy); dx, dy = dx / L, dy / L
    px, py = ex + dx * 7, ey + dy * 7
    caps = [(ex, ey, 6, px, py, 7)]
    side = 1 if dx >= 0 else -1
    for ang, ln in ((-34, 12), (-11, 15), (11, 15), (32, 12), (-78 * side, 10)):
        a = math.radians(ang)
        fx, fy = dx * math.cos(a) - dy * math.sin(a), dx * math.sin(a) + dy * math.cos(a)
        sx, sy = px + fx * 5, py + fy * 5
        caps.append((sx, sy, 2.6, sx + fx * ln, sy + fy * ln, 2.0))
    return caps

HANDS = [(104, 180, -1, 0), (408, 180, 1, 0), (124, 112, -0.88, -0.47), (388, 112, 0.88, -0.47)]
for h in HANDS:
    S += hand(*h)

FACE = (256, 118, 17, 21)   # óvalo del rostro (sin cabello)
HAIR = [(256, 96, 22, 256, 100, 22), (238, 104, 13, 232, 156, 9), (274, 104, 13, 280, 156, 9),
        (244, 98, 14, 240, 140, 10), (268, 98, 14, 272, 140, 10)]

def in_caps(px, py, caps):
    for x1, y1, r1, x2, y2, r2 in caps:
        dx, dy = x2 - x1, y2 - y1; L = dx * dx + dy * dy
        t = 0 if L == 0 else max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / L))
        if math.hypot(px - (x1 + t * dx), py - (y1 + t * dy)) <= r1 + t * (r2 - r1):
            return True
    return False

def is_hair(x, y):
    fx, fy, rx, ry = FACE
    in_face = ((x - fx) / rx) ** 2 + ((y - fy) / ry) ** 2 <= 1
    return in_caps(x, y, HAIR) and not in_face and y < 160

def spacing2(x, y):
    """Malla más fina en manos y cabello para que se lean los detalles."""
    if any(math.hypot(x - hx, y - hy) < 30 for hx, hy, _, _ in HANDS):
        return 6
    if y < 165 and abs(x - 256) < 40:
        return 22
    return 60

def dist(px, py):
    best = 1e9
    for x1, y1, r1, x2, y2, r2 in S:
        dx, dy = x2 - x1, y2 - y1
        L = dx * dx + dy * dy
        t = 0 if L == 0 else max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / L))
        best = min(best, math.hypot(px - (x1 + t * dx), py - (y1 + t * dy)) - (r1 + t * (r2 - r1)))
    return best

def points():
    pts = []
    for x1, y1, r1, x2, y2, r2 in S:
        n = max(3, int(math.hypot(x2 - x1, y2 - y1) / (3 if r1 < 4 else 10)))
        for i in range(n + 1):
            t = i / n
            cx, cy, r = x1 + t * (x2 - x1), y1 + t * (y2 - y1), r1 + t * (r2 - r1)
            for a in range(0, 360, 45 if r1 < 4 else 30):
                ang = math.radians(a + i * 13)
                px, py = cx + r * math.cos(ang), cy + r * math.sin(ang)
                if abs(dist(px, py)) < 1.2:
                    pts.append((px, py))
    for _ in range(4000):
        px, py = random.uniform(85, 425), random.uniform(70, 460)
        if dist(px, py) < -4:
            pts.append((px, py))
    for hx, hy, _, _ in HANDS:              # puntos extra en las palmas
        for _ in range(60):
            px, py = hx + random.uniform(-25, 25), hy + random.uniform(-25, 25)
            if dist(px, py) < -1.5:
                pts.append((px, py))
    keep = []
    for p in pts:
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > spacing2(*p) for q in keep):
            keep.append(p)
    return keep

def circum(a, b, c):
    (ax, ay), (bx, by), (cx, cy) = a, b, c
    D = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(D) < 1e-9:
        return 0, 0, 1e18
    ux = ((ax*ax + ay*ay) * (by - cy) + (bx*bx + by*by) * (cy - ay) + (cx*cx + cy*cy) * (ay - by)) / D
    uy = ((ax*ax + ay*ay) * (cx - bx) + (bx*bx + by*by) * (ax - cx) + (cx*cx + cy*cy) * (bx - ax)) / D
    return ux, uy, (ax - ux) ** 2 + (ay - uy) ** 2

def triangulate(P):
    V = P + [(-4000, -4000), (4000, -4000), (0, 4000)]
    n = len(P)
    T = {(n, n + 1, n + 2): circum(*V[n:])}
    for i in range(n):
        p = V[i]
        bad = [t for t, c in T.items() if (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2 < c[2]]
        edges = {}
        for t in bad:
            for e in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                k = tuple(sorted(e)); edges[k] = edges.get(k, 0) + 1
            del T[t]
        for (a, b), cnt in edges.items():
            if cnt == 1:
                T[(a, b, i)] = circum(V[a], V[b], V[i])
    out = []
    for t in T:
        if max(t) >= n:
            continue
        a, b, c = (V[k] for k in t)
        cx, cy = (a[0] + b[0] + c[0]) / 3, (a[1] + b[1] + c[1]) / 3
        if dist(cx, cy) > 0 or any(dist((u[0] + v[0]) / 2, (u[1] + v[1]) / 2) > 0.5 for u, v in ((a, b), (b, c), (c, a))):
            continue
        out.append((a, b, c, cx, cy))
    return out

HAIR_TONES = ["#5A3A1E", "#6E4826", "#83592F", "#94693A"]

HOT = [(232, 168), (280, 168), (256, 294), (236, 372), (276, 372), (256, 150), (160, 178), (352, 178)]
STOPS = [(0, (42, 92, 214)), (0.3, (24, 178, 214)), (0.5, (72, 190, 110)), (0.72, (242, 196, 40)), (1, (220, 60, 50))]

def stress_color(x, y):
    v = max(math.exp(-((x - hx) ** 2 + (y - hy) ** 2) / 1500) for hx, hy in HOT)
    for (a, ca), (b, cb) in zip(STOPS, STOPS[1:]):
        if v <= b:
            t = (v - a) / (b - a)
            return "#%02x%02x%02x" % tuple(int(ca[k] + t * (cb[k] - ca[k])) for k in range(3))
    return "#dc3c32"

TRI = triangulate(points())

def mesh(ink="#2B2418", fill=True, opacity=0.78, width=1.1):
    s = []
    for a, b, c, cx, cy in TRI:
        f = (HAIR_TONES[int(cx * 7 + cy * 3) % 4] if is_hair(cx, cy) else stress_color(cx, cy)) if fill else "none"
        area = abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])) / 2
        w = min(width, max(0.25, math.sqrt(area) * 0.16))   # líneas finas en triángulos pequeños (dedos)
        s.append(f'<polygon points="{a[0]:.1f},{a[1]:.1f} {b[0]:.1f},{b[1]:.1f} {c[0]:.1f},{c[1]:.1f}" '
                 f'fill="{f}" fill-opacity="{opacity}" stroke="{ink}" stroke-width="{w:.2f}" stroke-linejoin="round"/>')
    return "".join(s)

def grid(color, op, step=16):
    return "".join(f'<path d="M{i},0V512M0,{i}H512" stroke="{color}" stroke-opacity="{op}" stroke-width="{1.4 if i % 64 == 0 else 0.8}"/>'
                   for i in range(0, 513, step))

def frame(color, w=3, op=0.75):
    return (f'<g fill="none" stroke="{color}" stroke-width="{w}" stroke-opacity="{op}">'
            f'<circle cx="256" cy="268" r="196"/><rect x="92" y="132" width="328" height="328"/></g>')

# La figura se escala para llenar el icono (más grande que la versión inicial).
FIG = 'transform="translate(256,262) scale(1.2) translate(-256,-268)"'

def icon(bg="#F6EFDC", gridc="#8A7A55", ink="#2B2418", framec="#5A4A2A", fill=True, rounded=True):
    clip = '<clipPath id="r"><rect width="512" height="512" rx="104"/></clipPath>' if rounded else ""
    g = 'clip-path="url(#r)"' if rounded else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">'
            f'<title>Vitruvium</title><defs>{clip}</defs><g {g}><rect width="512" height="512" fill="{bg}"/>'
            f'{grid(gridc, 0.28)}<g {FIG}>{frame(framec)}{mesh(ink, fill)}</g></g></svg>')

def mark(ink="#2B2418", framec="#5A4A2A", fill=True):
    """Isotipo sin fondo, para usar junto al nombre."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="16 22 480 480" width="480" height="480">'
            f'<title>Vitruvium</title><g {FIG}>{frame(framec)}{mesh(ink, fill)}</g></svg>')

if __name__ == "__main__":
    files = {
        "icon.svg": icon(),
        "icon-dark.svg": icon(bg="#1E1A14", gridc="#C9B98F", ink="#F6EFDC", framec="#E8D9B0"),
        "icon-mono.svg": icon(fill=False),
        "mark.svg": mark(),
        "mark-light.svg": mark(ink="#F6EFDC", framec="#E8D9B0"),
        # Tamaños pequeños (16–48 px): sin líneas de malla, que se vuelven ruido.
        "icon-small.svg": re.sub(r'stroke="#2B2418" stroke-width="[0-9.]+"', 'stroke="none"', icon()),
    }
    for name, svg in files.items():
        open(name, "w").write(svg)
    print(len(TRI), "triangles")
