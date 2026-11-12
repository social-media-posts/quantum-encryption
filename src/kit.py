import math
from lib2 import *

# ---------------- generic helpers ----------------
def caption(cv, text, T, t0, col=CREAM, y=1500, line=None, a=1, size=34):
    k, al = pop(T, t0, 0.4)
    if al <= 0: return
    w = cv.tw(text, 'sans', size) + 70
    cv.rr(540, y, w * k, 78 * k, 39, fill=DARK, line=line or col, lw=2.5, a=al * a, g=.35)
    cv.tx(540, y, text, 'sans', size * k, col, al * a)

def kicker(cv, text, T, t0, y, col=OR, size=28, sp=6):
    al = e_out(pr(T, t0, .4))
    cv.tx(540, y + 14 * (1 - al), text, 'mono', size, col, al, sp=sp, g=.3)

def slide_y(T, t_in, t_out=None, dist=700, d=.55):
    y = dist * (1 - e_out(pr(T, t_in, d)))
    if t_out is not None: y += dist * e_in(pr(T, t_out, d))
    return y

def check(cv, cx, cy, sz, col, a=1, w=8, p=1.0, g=.5):
    pts = [(cx - sz * .5, cy + sz * .02), (cx - sz * .12, cy + sz * .38), (cx + sz * .5, cy - sz * .34)]
    d1 = math.hypot(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]); d2 = math.hypot(pts[2][0] - pts[1][0], pts[2][1] - pts[1][1])
    L = (d1 + d2) * p
    if L <= d1:
        f = L / d1; q = [pts[0], (lerp(pts[0][0], pts[1][0], f), lerp(pts[0][1], pts[1][1], f))]
    else:
        f = (L - d1) / d2; q = [pts[0], pts[1], (lerp(pts[1][0], pts[2][0], f), lerp(pts[1][1], pts[2][1], f))]
    cv.ln(q, col, w, a, g)

def cross(cv, cx, cy, sz, col, a=1, w=10, p=1.0, g=.5):
    h = sz / 2
    cv.ln([(cx - h, cy - h), (cx - h + sz * clamp(p * 2), cy - h + sz * clamp(p * 2))], col, w, a, g)
    if p > .5:
        q = (p - .5) * 2
        cv.ln([(cx + h, cy - h), (cx + h - sz * q, cy - h + sz * q)], col, w, a, g)

def ring_burst(cv, cx, cy, T, t0, col, r0=20, r1=260, d=.7, w=6):
    p = pr(T, t0, d)
    if 0 < p < 1:
        cv.ci(cx, cy, lerp(r0, r1, e_out(p)), line=col, lw=w * (1 - p) + 1, a=1 - p, g=.8)

def dash_circle(cv, cx, cy, r, T, col, speed=.3, n=48, w=3, a=1, g=0, frac=.55):
    for i in range(n):
        a0 = (i / n) * 2 * math.pi + T * speed
        cv.arc(cx, cy, r, a0, a0 + 2 * math.pi / n * frac, col, w, a, g)

def particles(cv, T):
    for i in range(70):
        sp = 8 + hsh(i * 3.1) * 26
        x = (hsh(i * 1.7) * 1180 - 50 + math.sin(T * .3 + i) * 14)
        y = (hsh(i * 5.3) * 2100 - sp * T) % 2100 - 90
        tw_ = .5 + .5 * math.sin(T * 1.7 + i * 2.1)
        col = (CREAM, OR, BLUE, PUR)[i % 4]
        r = 1.2 + hsh(i * 9.7) * 2.2
        cv.gd.ellipse([(x - r) * GS, (y - r) * GS, (x + r) * GS, (y + r) * GS], fill=cv.gc(col, .35 + .4 * tw_))
        cv.d.ellipse([(x - r * .6) * S, (y - r * .6) * S, (x + r * .6) * S, (y + r * .6) * S], fill=cv.c(col, .22 + .22 * tw_))

# ---------------- icons ----------------
def padlock(cv, cx, cy, sz, col, op=0.0, a=1, g=.6, fill=PANEL):
    u = sz / 100
    lift = op * 14 * u
    rr_ = 22 * u
    sy = cy - 6 * u - lift
    left = [(cx - rr_, cy - 4 * u)] + [(cx - rr_, sy)]
    cv.ln([(cx - rr_, cy - 4 * u), (cx - rr_, sy)], col, 7 * u, a, g)
    cv.arc(cx, sy, rr_, math.pi, 2 * math.pi, col, 7 * u, a, g)
    cv.ln([(cx + rr_, sy), (cx + rr_, cy - 4 * u - op * 12 * u)], col, 7 * u, a, g)
    cv.rr(cx, cy + 26 * u, 76 * u, 56 * u, 12 * u, fill=fill, line=col, lw=6 * u, a=a, g=g)
    cv.ci(cx, cy + 22 * u, 7 * u, fill=col, a=a)
    cv.ln([(cx, cy + 26 * u), (cx, cy + 40 * u)], col, 6 * u, a)

def chip_icon(cv, cx, cy, sz, col, T=0, a=1, g=.7, label='Q'):
    u = sz / 100
    for i in range(5):
        o = (i - 2) * 17 * u
        for sg in (-1, 1):
            cv.ln([(cx + o, cy + sg * 50 * u), (cx + o, cy + sg * 66 * u)], col, 4 * u, a, g * .5)
            cv.ln([(cx + sg * 50 * u, cy + o), (cx + sg * 66 * u, cy + o)], col, 4 * u, a, g * .5)
    pulse = .5 + .5 * math.sin(T * 4)
    cv.rr(cx, cy, 100 * u, 100 * u, 18 * u, fill=PANEL, line=col, lw=5 * u, a=a, g=g * (.7 + .3 * pulse))
    cv.rr(cx, cy, 58 * u, 58 * u, 10 * u, line=col, lw=3 * u, a=a * .6)
    cv.tx(cx, cy + 2 * u, label, 'mono', 36 * u, col, a, g=g * .6)

def laptop(cv, cx, cy, sz, col=BLUE, a=1, g=.4):
    u = sz / 100
    cv.rr(cx, cy - 20 * u, 100 * u, 64 * u, 8 * u, fill=DARK, line=col, lw=4 * u, a=a, g=g)
    cv.poly([(cx - 56 * u, cy + 20 * u), (cx + 56 * u, cy + 20 * u), (cx + 66 * u, cy + 34 * u), (cx - 66 * u, cy + 34 * u)], fill=PANEL, line=col, lw=3 * u, a=a, g=g * .6)
    cv.ln([(cx - 14 * u, cy + 27 * u), (cx + 14 * u, cy + 27 * u)], col, 3 * u, a)

def server(cv, cx, cy, sz, col, T=0, a=1, g=.4, hot=0.0):
    u = sz / 100
    for i in range(3):
        y = cy + (i - 1) * 30 * u
        cv.rr(cx, y, 100 * u, 24 * u, 6 * u, fill=DARK, line=col, lw=3.5 * u, a=a, g=g)
        for j in range(3):
            on = (math.sin(T * (5 + i * 1.7 + j * 2.3) + i * 3 + j) > 0)
            lc = lerp_c(GRN, RED, hot) if on else RAIL
            cv.ci(cx - 36 * u + j * 11 * u, y, 3.2 * u, fill=lc, a=a)
        cv.ln([(cx + 6 * u, y), (cx + 40 * u, y)], col, 3 * u, a * .6)

def shield_pts(cx, cy, sz, p=1.0):
    u = sz / 100
    base = [(0, -50), (44, -34), (44, 4)]
    for i in range(1, 9):
        th = i / 8
        base.append((44 * (1 - th) ** 1.15, 4 + 46 * th ** .9))
    R = [(cx + x * u, cy + y * u) for x, y in base]
    Lf = [(cx - x * u, cy + y * u) for x, y in reversed(base[:-1])]
    return R + Lf

def shield(cv, cx, cy, sz, col, a=1, g=.7, fill=PANEL, p=1.0):
    pts = shield_pts(cx, cy, sz)
    if p >= 1:
        cv.poly(pts, fill=fill, line=col, lw=max(5, sz * .05), a=a, g=g)
    else:
        n = max(2, int(len(pts) * p)); cv.ln(pts[:n + 1], col, max(5, sz * .05), a, g)

def stopwatch(cv, cx, cy, r, ang, col=GRN, a=1, g=.6):
    cv.ci(cx, cy, r, fill=DARK, line=col, lw=6, a=a, g=g)
    cv.rr(cx, cy - r - 12, 26, 14, 4, fill=col, a=a)
    cv.ln([(cx, cy), (cx + math.sin(ang) * r * .75, cy - math.cos(ang) * r * .75)], col, 6, a, g)
    cv.ci(cx, cy, 7, fill=col, a=a)
    for i in range(12):
        t_ = i * math.pi / 6
        cv.ln([(cx + math.sin(t_) * r * .84, cy - math.cos(t_) * r * .84), (cx + math.sin(t_) * r * .94, cy - math.cos(t_) * r * .94)], col, 3, a * .7, cap=False)

def sat_icon(cv, kind, cx, cy, u, col, a=1):
    if kind == 'card':
        cv.rr(cx, cy, 64 * u, 44 * u, 7 * u, line=col, lw=3.5 * u, a=a); cv.ln([(cx - 32 * u, cy - 8 * u), (cx + 32 * u, cy - 8 * u)], col, 5 * u, a, cap=False)
        cv.ln([(cx - 22 * u, cy + 10 * u), (cx - 4 * u, cy + 10 * u)], col, 3.5 * u, a)
    elif kind == 'mail':
        cv.rr(cx, cy, 64 * u, 46 * u, 7 * u, line=col, lw=3.5 * u, a=a); cv.ln([(cx - 28 * u, cy - 14 * u), (cx, cy + 6 * u), (cx + 28 * u, cy - 14 * u)], col, 3.5 * u, a)
    elif kind == 'chat':
        cv.rr(cx, cy - 2 * u, 66 * u, 46 * u, 14 * u, line=col, lw=3.5 * u, a=a); cv.poly([(cx - 16 * u, cy + 20 * u), (cx - 24 * u, cy + 34 * u), (cx - 2 * u, cy + 21 * u)], fill=col, a=a)
        for k in (-1, 0, 1): cv.ci(cx + k * 14 * u, cy - 2 * u, 3.6 * u, fill=col, a=a)
    elif kind == 'bank':
        cv.poly([(cx - 34 * u, cy - 8 * u), (cx, cy - 32 * u), (cx + 34 * u, cy - 8 * u)], line=col, lw=3.5 * u, a=a)
        for k in (-20, 0, 20): cv.ln([(cx + k * u, cy - 4 * u), (cx + k * u, cy + 22 * u)], col, 5 * u, a)
        cv.ln([(cx - 36 * u, cy + 30 * u), (cx + 36 * u, cy + 30 * u)], col, 5 * u, a)
    elif kind == 'globe':
        cv.ci(cx, cy, 32 * u, line=col, lw=3.5 * u, a=a); cv.el(cx, cy, 14 * u, 32 * u, line=col, lw=3 * u, a=a)
        cv.ln([(cx - 32 * u, cy), (cx + 32 * u, cy)], col, 3 * u, a, cap=False)
    elif kind == 'browser':
        cv.rr(cx, cy, 68 * u, 52 * u, 8 * u, line=col, lw=3.5 * u, a=a); cv.ln([(cx - 34 * u, cy - 12 * u), (cx + 34 * u, cy - 12 * u)], col, 3 * u, a, cap=False)
        for k in (-1, 0, 1): cv.ci(cx - 24 * u + (k + 1) * 8 * u, cy - 19 * u, 2.2 * u, fill=col, a=a)

def bezier(p0, p1, p2, n=26):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]

def partial(pts, p):
    n = len(pts) - 1
    f = clamp(p) * n
    i = int(f)
    if i >= n: return pts[:]
    fr = f - i
    q = pts[:i + 1] + [(lerp(pts[i][0], pts[i + 1][0], fr), lerp(pts[i][1], pts[i + 1][1], fr))]
    return q

def fmt(n): return f"{int(n):,}"

# ---------------- HUD ----------------
CHAPS = [(0, 'THE MYTH'), (11.5, 'THE LOCK'), (29.8, 'THE SHORTCUT'), (36.5, 'THE LOOP'), (49.4, 'THE QUANTUM TRICK'), (65.5, 'REALITY CHECK'), (77.3, 'WHAT TO DO'), (88.9, 'THE TAKEAWAY')]
def hud(cv, T, total):
    n = len(CHAPS); gap = 8; wseg = (880 - gap * (n - 1)) / n
    cur = max(i for i in range(n) if T >= CHAPS[i][0] - 0.0)
    for i in range(n):
        x0 = 100 + i * (wseg + gap)
        end = CHAPS[i + 1][0] if i + 1 < n else total
        p = clamp((T - CHAPS[i][0]) / (end - CHAPS[i][0]))
        cv.rr(x0 + wseg / 2, 250, wseg, 8, 4, fill=RAIL)
        if p > 0:
            col = OR if i == cur else GRN
            cv.rr(x0 + wseg * p / 2, 250, max(wseg * p, 8), 8, 4, fill=col, g=.5 if i == cur else 0)
    t0 = CHAPS[cur][0]
    al = e_out(pr(T, t0 + .15, .4)) if cur > 0 else e_out(pr(T, .3, .4))
    cv.tx(540, 292 + 12 * (1 - al), f"{cur + 1:02d} · {CHAPS[cur][1]}", 'mono', 26, OR, al, sp=5, g=.3)
