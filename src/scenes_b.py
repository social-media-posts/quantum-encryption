import math
from lib2 import *
from kit import *

CX = 540

# ---------- S8: the loop ring (7^x mod 15) ----------
SEQ = [1, 7, 4, 13, 1]
HOPCOL = [OR, BLUE, YEL, GRN]
def node_pos(v, R=320, cy=900):
    a = -math.pi / 2 + v * 2 * math.pi / 15
    return CX + R * math.cos(a), cy + R * math.sin(a)

def s8(cv, T):
    cy = 900
    dash_circle(cv, CX, cy, 320, T, LINE, .08, 90, 3)
    # nodes
    for v in range(15):
        k, a = pop(T, 36.9 + v * .06, .4)
        if a <= 0: continue
        x, y = node_pos(v)
        used = v in SEQ[:4]
        reached = 0
        for hi, tgt in enumerate(SEQ):
            if tgt == v and T >= 38.1 + [0, .0, .0, .0, .0][0] + [0, 1.0, 2.3, 3.2, 5.0][hi]: reached = 1
        col = HOPCOL[SEQ.index(v) % 4] if (used and reached) else DIM
        cv.ci(x, y, 30 * k, fill=DARK, line=col, lw=4 if reached else 2.5, a=a, g=.8 if reached else 0)
        cv.tx(x, y + 1, str(v), 'mono', 26 * k, CREAM if reached else DIM, a)
    # hops
    times = [39.1, 40.0, 40.9, 43.15]
    ctrl_scale = .22
    for hi in range(4):
        p = e_io(pr(T, times[hi], .6))
        if p <= 0: continue
        a_, b_ = node_pos(SEQ[hi]), node_pos(SEQ[hi + 1])
        mid = ((a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2)
        ctrl = (CX + (mid[0] - CX) * ctrl_scale, cy + (mid[1] - cy) * ctrl_scale)
        pts = bezier(a_, ctrl, b_)
        q = partial(pts, p)
        cv.ln(q, HOPCOL[hi], 7, 1, g=1.0)
        if p < 1: cv.ci(*q[-1], 13, fill=CREAM, g=1.2)
    # start marker
    sk, sa = pop(T, 38.0, .45)
    x0, y0 = node_pos(1)
    ring_burst(cv, x0, y0, T, 38.05, OR, 30, 100, .7, 5)
    # center readout
    kk, ka = pop(T, 37.4, .4)
    cv.ci(CX, cy, 150 * kk, fill=DARK, line=LINE, lw=3, a=ka)
    if T < 38.9: cv.tx(CX, cy - 6, '× 7', 'serif', 120 * kk, OR, ka, g=.5); cv.tx(CX, cy + 76, 'KEEP MULTIPLYING', 'mono', 18, DIM, ka, sp=3)
    elif T < 40.0: cv.tx(CX, cy - 20, '7 → 49', 'serif', 66, CREAM, 1); cv.tx(CX, cy + 36, 'WRAP AT 15', 'mono', 24, BLUE, 1, sp=4, g=.4)
    elif T < 40.9: cv.tx(CX, cy - 20, '49 → 4', 'serif', 66, CREAM, 1); cv.tx(CX, cy + 36, '49 mod 15', 'mono', 24, YEL, 1, sp=3, g=.4)
    elif T < 43.15: cv.tx(CX, cy - 10, '4 → 13', 'serif', 66, CREAM, 1); cv.tx(CX, cy + 40, 'LOOKS RANDOM…', 'mono', 24, DIM, 1, sp=3)
    elif T < 45.0:
        k2, a2 = pop(T, 43.3, .4)
        cv.tx(CX, cy - 10, '13 → 1', 'serif', 66 * k2, GRN, a2, g=.7); cv.tx(CX, cy + 40, 'BACK AT START', 'mono', 24, GRN, a2, sp=3, g=.4)
    else:
        k2, a2 = pop(T, 45.2, .5)
        cv.tx(CX, cy - 16, 'r = 4', 'serif', 120 * k2, GRN, a2, g=.9)
        cv.tx(CX, cy + 62, 'LOOP LENGTH', 'mono', 24, GRN, a2, sp=4, g=.4)
    # loop glow polygon after closing
    cl = pr(T, 43.6, .5)
    if cl > 0:
        pts = [node_pos(v) for v in SEQ[:4]]
        pulse = .6 + .4 * math.sin(T * 5)
        cv.poly(pts, line=GRN, lw=6, a=cl * pulse, g=.35)
        for i, v in enumerate(SEQ[:4]):
            pass
    # sequence chips
    seq_t = [38.3, 39.5, 40.5, 41.5, 43.4]
    shown = [v for v, t0 in zip(SEQ, seq_t) if T >= t0]
    n = len(shown)
    for i, v in enumerate(shown):
        k, a = pop(T, seq_t[i], .4)
        x = CX + (i - (n - 1) / 2) * 100
        col = HOPCOL[i % 4] if i < 4 else GRN
        cv.rr(x, 1330, 82 * k, 66 * k, 16, fill=DARK, line=col, lw=3, a=a, g=.6)
        cv.tx(x, 1330, str(v), 'mono', 32 * k, col, a)
    kicker(cv, 'N = 15 · A TOY EXAMPLE', T, 37.2, 460, OR)
    if T < 41.5: caption(cv, 'MULTIPLY, THEN WRAP AROUND', T, 38.5, BLUE)
    elif T < 45: caption(cv, 'IT ALWAYS COMES BACK', T, 43.0, GRN)
    else: caption(cv, 'THE LOOP LENGTH IS THE KEY', T, 45.3, GRN)

# ---------- S9: laptop finishes the job ----------
def s9(cv, T):
    cy = 800
    k, a = pop(T, 46.5, .5)
    # incoming r badge
    bk, ba = pop(T, 46.45, .4)
    cv.rr(CX, 440, 260 * bk, 96 * bk, 48, fill=DARK, line=GRN, lw=4, a=ba, g=.9)
    cv.tx(CX, 440, 'r = 4', 'serif', 64 * bk, GRN, ba, g=.6)
    # beam down
    bp = e_out(pr(T, 46.9, .5))
    for i in range(3):
        ph = (T * 1.5 + i / 3) % 1
        cv.ci(CX, lerp(495, 570, ph), 6, fill=GRN, a=bp * (1 - ph), g=1)
    laptop(cv, CX, cy + 40, 520 * k, BLUE, a)
    sc = 3.1 * k
    lines = [(47.2, '7² = 49', CREAM), (47.9, 'gcd(48, 15) = 3', YEL), (48.5, 'gcd(50, 15) = 5', BLUE)]
    for i, (t0, txt, col) in enumerate(lines):
        n = int(len(txt) * clamp((T - t0) / .5))
        cv.tx(CX - 190, 640 + i * 70, txt[:n], 'mono', 40, col, a, anchor='lm', g=.4)
    if (T * 2) % 1 < .5 and T < 49.0:
        cv.rr(CX + 80, 640 + 140, 4, 36, 2, fill=CREAM)
    rk, ra = pop(T, 48.95, .45)
    cv.rr(CX, 1240, 520 * rk, 110 * rk, 55, fill=DARK, line=GRN, lw=5, a=ra, g=1.0)
    cv.tx(CX, 1240, '15 = 3 × 5', 'serif', 70 * rk, GRN, ra, g=.7)
    ring_burst(cv, CX, 1240, T, 48.95, GRN, 40, 420, .9, 8)
    caption(cv, 'A LAPTOP CAN FINISH THE JOB', T, 47.2, BLUE)

# ---------- S10: spiral -> wave ----------
NSP = 220
def spiral_pos(i):
    ang = i * .5; rad = 16 + i * 1.5
    return CX + rad * math.cos(ang), 880 + rad * math.sin(ang)
NW = 96
def s10(cv, T):
    cy = 880
    # phase 1: walk
    morph_start = 54.75
    for i in range(NSP):
        sx, sy = spiral_pos(i)
        k, a = pop(T, 49.55 + i * .0025, .4)
        if a <= 0: continue
        walk = int(max(0, T - 49.95) * 9) if T < 53.3 else int(max(0, 53.3 - 49.95) * 9)
        d = math.hypot(sx - CX, sy - cy)
        rip = clamp(((T - 53.3) * 1000 - d) / 120) if T >= 53.3 else 0
        col = DIM; g = 0; rad = 5.5
        if i < walk: col = OR; g = .5
        if i == walk and T < 53.3: col = CREAM; g = 1.2; rad = 11
        if rip > 0:
            col = lerp_c(col, rgb_wheel(i / NSP + T * .1), rip); g = .9 * rip; rad = 7
        # morph to wave
        mp = e_io(pr(T, morph_start + (i / NSP) * .75, .8))
        wx = 80 + i * (920 / (NSP - 1))
        wy = cy + 150 * math.sin(2 * math.pi * 3 * i / NSP - T * 2.2)
        x = lerp(sx, wx, mp); y = lerp(sy, wy, mp)
        if T >= morph_start + .2 and mp > .98: rad = 6
        cv.ci(x, y, rad * k, fill=col, a=a, g=g)
        if mp > .5:
            cv.ln([(x, cy), (x, y)], col, 3, (mp - .5) * 1.2, g=.4, cap=False)
    # steps counter
    if T < 53.3:
        n = int(max(0, T - 49.95) * 9) + 1
        cv.tx(CX, 1360, f'STEP {n}', 'mono', 54, OR, 1, sp=8, g=.5)
        cv.rr(CX, 1440, 700, 18, 9, fill=DARK, line=LINE, lw=2)
        cv.rr(CX - 350 + 3 + 700 * min(1, n / 2000) / 2, 1440, max(8, 700 * min(1, n / 2000)), 12, 6, fill=OR, g=.6)
        caption(cv, 'ONE STEP AT A TIME', T, 50.1, OR, y=1530)
    # quantum chip
    ck, ca = pop(T, 53.35, .5)
    if ca > 0:
        cy2 = 420 + 0
        chip_icon(cv, CX, 430, 150 * ck, BLUE, T, ca)
        for j in range(2):
            ph = (T * .8 + j * .5) % 1
            if T < 56.0: cv.ci(CX, 430, 90 + ph * 150, line=BLUE, lw=3 * (1 - ph) + .5, a=(1 - ph) * .6, g=.6)
    if 53.4 < T < 54.7: caption(cv, 'A QUANTUM COMPUTER', T, 53.45, BLUE, y=1530)
    if 54.7 <= T < 56.6: caption(cv, 'EVERY STEP IN ONE WAVE', T, 54.8, PUR, y=1530)
    # interference
    if T > 56.35:
        ip = e_io(pr(T, 56.5, .9))
        # upper wave moves up as second wave enters
        for q in range(0, 1):
            pass
        yA = lerp(880, 690, ip); yB = lerp(1500, 960, ip); yS = lerp(1700, 1260, ip)
        ph = T * 1.6
        ptsB = [(80 + x * 10, yB + 120 * math.sin(2 * math.pi * 3 * x / 92 - T * 2.2 + 1.6 * math.sin(ph * .5) * 1.2 + 1.2)) for x in range(93)]
        ptsA = [(80 + x * 10, yA + 120 * math.sin(2 * math.pi * 3 * x / 92 - T * 2.2)) for x in range(93)]
        ptsS = [(80 + x * 10, yS + .85 * ((ptsA[x][1] - yA) + (ptsB[x][1] - yB))) for x in range(93)]
        cv.ln(ptsB, OR, 7, ip, g=1.0)
        cv.ln(ptsS, CREAM, 9, ip, g=1.2)
        
        cv.tx(70, (yA + yB) / 2, '', 'serif', 10, DIM, 1)
        cv.tx(60, yS + 90, 'SUM OF BOTH', 'mono', 24, CREAM, ip, anchor='lm', sp=4)
        cv.tx(60, yB + 150, 'SAME WAVE, SHIFTED', 'mono', 24, OR, ip, anchor='lm', sp=3)
        caption(cv, 'THE WAVE INTERFERES WITH ITSELF', T, 56.7, CREAM, y=1530)

# ---------- S12: cancel / add ----------
def peak_amp(i):
    best = 0
    for c in (12, 36, 60, 84):
        best = max(best, math.exp(-((i - c) ** 2) / 5.0))
    return best
def phasor(cv, cx, cy, T, t0, aligned, col, label):
    k, a = pop(T, t0, .5)
    if a <= 0: return
    cv.ci(cx, cy, 110 * k, fill=DARK, line=col, lw=3, a=a, g=.6)
    ang = T * 2.2
    a1 = ang; a2 = ang + (0 if aligned else math.pi)
    for aa, c2 in ((a1, BLUE), (a2, OR)):
        x = cx + 80 * math.cos(aa) * k; y = cy + 80 * math.sin(aa) * k
        cv.ln([(cx, cy), (x, y)], c2, 6, a, g=.8)
        cv.ci(x, y, 9, fill=c2, a=a)
    sx = cx + (160 * math.cos(ang) if aligned else 0) * k * .5; sy = cy + (160 * math.sin(ang) if aligned else 0) * k * .5
    cv.ci(sx, sy, 10 if aligned else 6, fill=CREAM if aligned else RED, a=a, g=1.0)
    cv.tx(cx, cy + 150, label, 'mono', 26, col, a, sp=3, g=.4)

def s12(cv, T):
    base = 1000
    for i in range(NW):
        x = 62 + i * 10.45
        k, a = pop(T, 58.7 + i * .004, .35)
        if a <= 0: continue
        wr = 60 + 200 * hsh(i * 3.3 + int(T * 8) * .17)
        dec = e_out(pr(T, 59.05 + hsh(i) * .5, .55))
        pk = peak_amp(i)
        amp = wr * (1 - dec * (1 - pk))
        grow = e_io(pr(T, 60.6, 1.5))
        amp = lerp(amp, 120 + 280 * pk if pk > .02 else amp, grow * (1 if pk > .02 else 0))
        if T > 60.6: amp = amp * (1 - 0.0)
        col = lerp_c(BLUE, RED, clamp(dec * 2) * (1 - pk) if T < 60.5 else 0)
        if pk > .4 and T > 60.6: col = lerp_c(BLUE, GRN, grow)
        if T > 60.6 and pk <= .4: amp = max(2, amp * (1 - grow))
        h = max(3, amp * k)
        cv.rr(x, base - h / 2, 8, h, 4, fill=col, a=a, g=.8 if (pk > .4 and T > 60.6) else .15)
        cv.rr(x, base + 10 + h * .12, 8, h * .24, 4, fill=col, a=a * .25)
    cv.ln([(50, base + 2), (1030, base + 2)], LINE, 3, 1)
    # phasor panels
    phasor(cv, 300, 1290, T, 59.1, False, RED, 'OFF BEAT: CANCEL')
    phasor(cv, 780, 1290, T, 60.65, True, GRN, 'ON BEAT: ADD UP')
    # measure
    if T > 62.95:
        mp = e_out(pr(T, 62.98, .5))
        x1 = 62 + 12 * 10.45; x2 = 62 + 36 * 10.45
        yb = 560
        cv.ln([(x1, yb), (x1 + (x2 - x1) * mp, yb)], YEL, 5, 1, .9)
        cv.ln([(x1, yb - 16), (x1, yb + 16)], YEL, 5, 1); cv.ln([(x1 + (x2 - x1) * mp, yb - 16), (x1 + (x2 - x1) * mp, yb + 16)], YEL, 5, 1)
        cv.tx((x1 + x2) / 2, yb - 40, 'DISTANCE: 24', 'mono', 28, YEL, mp, sp=4, g=.4)
    if T > 63.75:
        rk, ra = pop(T, 63.8, .5)
        cv.rr(CX, 420, 640 * rk, 120 * rk, 60, fill=DARK, line=GRN, lw=5, a=ra, g=1.0)
        cv.tx(CX, 420, '96 ÷ 24 = 4', 'serif', 74 * rk, GRN, ra, g=.7)
        ring_burst(cv, CX, 420, T, 63.8, GRN, 60, 520, .9, 8)
    if T < 60.5: caption(cv, 'WRONG ANSWERS CANCEL', T, 59.2, RED, line=RED, y=1530)
    elif T < 62.9: caption(cv, 'THE RIGHT RHYTHM GETS LOUDER', T, 60.7, GRN, y=1530)
    elif T < 63.7: caption(cv, 'MEASURE IT', T, 63.0, YEL, y=1530)
    else: caption(cv, 'THE LOOP LENGTH APPEARS: r = 4', T, 63.9, GRN, y=1530)

# ---------- S13: bank ----------
def s13(cv, T):
    cy = 860
    k, a = pop(T, 65.7, .55)
    sh = math.sin(T * 40) * 5 * pr(T, 66.2, .4) * (1 - pr(T, 67.2, .4))
    cv.rr(CX + sh, cy, 560 * k, 350 * k, 34, fill=PANEL, line=CREAM, lw=4, a=a, g=.4)
    cv.rr(CX - 190 + sh, cy - 70, 100 * k, 76 * k, 14, fill=YEL, a=a, g=.4)
    cv.ln([(CX - 270 + sh, cy - 160), (CX + 270 + sh, cy - 160)], DIM, 3, a * 0)
    cv.tx(CX - 240 + sh, cy + 60, '4417  ••••  ••••  1234', 'mono', 33 * k, CREAM, a, anchor='lm')
    cv.tx(CX - 240 + sh, cy + 120, 'YOUR BANK ACCOUNT', 'mono', 22 * k, DIM, a, anchor='lm', sp=3)
    # radar threat
    for j in range(3):
        ph = (T * .9 + j / 3) % 1
        if 66.1 < T < 68.2: cv.ci(CX, cy, 180 + ph * 380, line=RED, lw=3 * (1 - ph) + .5, a=(1 - ph) * .6, g=.6)
    if 66.15 < T < 68.3:
        q = e_back(pr(T, 66.15, .4))
        cv.tx(CX + 250, cy - 180 + math.sin(T * 5) * 8, '?', 'serif', 220 * q, RED, 1, g=.8)
    if T > 68.25:
        sp, sa = pop(T, 68.25, .5)
        shield(cv, CX, cy + 10, 560 * sp, GRN, sa * .9, .8, fill=DARK) if False else None
        cv.rr(CX, 1240, 640 * sp, 170 * sp, 30, fill=DARK, line=GRN, lw=6, a=sa, g=1.0)
        cv.tx_rot(CX, 1240, 'NOT TODAY', 'serif', 108 * sp, GRN, 5, sa)
        ring_burst(cv, CX, 1240, T, 68.25, GRN, 60, 560, .9, 8)
        check(cv, CX + 205, cy - 75, 70 * sp, GRN, sa, 12, pr(T, 68.35, .4), 1.0)
    if T < 68.2: caption(cv, 'IS YOUR MONEY IN DANGER?', T, 66.3, RED, line=RED, y=1500)

# ---------- S14: qubit gauge ----------
def lpos(v, top=470, bot=1400): return bot - (math.log10(v) / 6) * (bot - top)
def s14(cv, T):
    lx = 250
    top, bot = 470, 1400
    k, a = pop(T, 69.0, .5)
    cv.rr(lx, (top + bot) / 2, 30 * k, (bot - top + 40) * k, 15, fill=DARK, line=LINE, lw=2, a=a)
    labs = ['1', '10', '100', '1,000', '10,000', '100,000', '1,000,000']
    for i, lb in enumerate(labs):
        y = lpos(10 ** i)
        cv.ln([(lx - 30, y), (lx + 30, y)], LINE, 3, a)
        cv.tx(lx - 44, y, lb, 'mono', 22, DIM, a, anchor='rm')
    # needed marker
    p1 = e_io(pr(T, 69.6, 2.6))
    v1 = 10 ** (6 * p1)
    y1 = lpos(max(1, v1))
    if T > 69.5:
        cv.rr(lx, (y1 + bot) / 2, 16, bot - y1 + 4, 8, fill=OR, g=.9)
        chip_icon(cv, lx, y1, 70, OR, T, 1)
        cv.tx(400, 560, fmt(v1) if p1 < .995 else '1,000,000', 'serif', 100, OR, 1, anchor='lm', g=.6)
        cv.tx(400, 640, 'STABLE QUBITS NEEDED', 'mono', 26, OR, 1, anchor='lm', sp=3, g=.3)
        cv.tx(400, 685, 'GOOGLE ESTIMATE · 2025', 'mono', 20, DIM, 1, anchor='lm', sp=3)
    if p1 >= 1: ring_burst(cv, lx, lpos(1e6), T, 72.2, OR, 40, 300, .9, 7)
    # today marker
    if T > 75.0:
        p2 = e_out(pr(T, 75.05, .8))
        v2 = 10 ** (3 * p2)
        y2 = lpos(max(1, v2))
        cv.ci(lx, y2, 22, fill=BLUE, g=1.1)
        cv.ln([(lx + 28, y2), (lx + 130, y2)], BLUE, 4, 1, .6)
        bk, ba = pop(T, 75.7, .5)
        cv.rr(660, y2, 460 * bk, 120 * bk, 22, fill=DARK, line=BLUE, lw=3, a=ba, g=.7)
        cv.tx(660, y2 - 20, 'TODAY: ~1,000+', 'serif', 52 * bk, BLUE, ba, g=.5)
        cv.tx(660, y2 + 30, 'NOISY QUBITS', 'mono', 22 * bk, DIM, ba, sp=3)
        gp = e_out(pr(T, 76.2, .6))
        gx = lx + 150
        cv.ln([(gx, lpos(1e6) + 10), (gx, lpos(1e6) + 10 + (lpos(1e3) - lpos(1e6) - 20) * gp)], YEL, 4, 1, .6)
        cv.rr(700, 790, 380 * gp, 96 * gp, 48, fill=DARK, line=YEL, lw=3, a=gp, g=.7)
        cv.tx(700, 790, '~1,000× GAP', 'serif', 46 * gp, YEL, gp, g=.5)
    if T < 74.9: caption(cv, 'WHAT RSA-2048 WOULD NEED', T, 69.9, OR, y=1530)
    else: caption(cv, 'WE ARE NOT THERE YET', T, 75.2, BLUE, y=1530)

# ---------- S15: harvest now, decrypt later ----------
def s15(cv, T):
    # sender and vault
    k, a = pop(T, 77.55, .5)
    laptop(cv, 190, 640, 190 * k, BLUE, a)
    server(cv, 880, 640, 190 * k, RED, T, a, .5, 1)
    cv.tx(190, 760, 'YOU', 'mono', 24, BLUE, a, sp=5); cv.tx(880, 770, "ATTACKER'S STORAGE", 'mono', 22, RED, a, sp=2)
    cv.ln([(290, 640), (770, 640)], LINE, 3, a)
    # packets
    for i in range(6):
        t0 = 77.9 + i * .38
        p = pr(T, t0, 1.0)
        if 0 < p <= 1:
            x = lerp(290, 770, p)
            cv.rr(x, 640, 70, 48, 12, fill=DARK, line=GRN, lw=3, a=1, g=.8)
            padlock(cv, x, 634, 34, GRN, 0, 1, .3)
    cv.tx(CX, 540, 'ENCRYPTED DATA', 'mono', 26, GRN, a, sp=6, g=.4)
    # stored locks
    n_st = int(clamp((T - 78.9) / 2.0) * 6) if T > 78.9 else 0
    # clock
    if T > 79.35:
        ck, ca = pop(T, 79.4, .5)
        cv.ci(CX, 1020, 140 * ck, fill=DARK, line=YEL, lw=6, a=ca, g=.8)
        for i in range(12):
            t_ = i * math.pi / 6
            cv.ln([(CX + math.sin(t_) * 118 * ck, 1020 - math.cos(t_) * 118 * ck), (CX + math.sin(t_) * 132 * ck, 1020 - math.cos(t_) * 132 * ck)], YEL, 4, ca, cap=False)
        ang = (T - 79.4) * 7
        cv.ln([(CX, 1020), (CX + math.sin(ang) * 100 * ck, 1020 - math.cos(ang) * 100 * ck)], YEL, 7, ca, g=.8)
        cv.ln([(CX, 1020), (CX + math.sin(ang / 12) * 62 * ck, 1020 - math.cos(ang / 12) * 62 * ck)], CREAM, 9, ca)
        cv.ci(CX, 1020, 9, fill=YEL, a=ca)
        cv.tx(CX, 1220, 'YEARS LATER…', 'mono', 28, YEL, ca, sp=5, g=.4)
    if T > 80.2:
        qk, qa = pop(T, 80.2, .5)
        chip_icon(cv, 190, 1020, 140 * qk, BLUE, T, qa)
        bp = e_out(pr(T, 80.7, .5))
        cv.ln([(260, 980), (260 + (880 - 260 - 40) * bp, 980 + (700 - 980) * bp)], BLUE, 5, 1, 1.0) if bp > 0 else None
        if bp >= 1:
            pk, pa = pop(T, 80.85, .45)
            cv.rr(880, 700, 90 * pk, 60 * pk, 14, fill=DARK, line=RED, lw=4, a=pa, g=.9)
            padlock(cv, 880, 698, 40 * pk, RED, 1, pa, .8)
            ring_burst(cv, 880, 640, T, 80.85, RED, 40, 220, .8, 7)
    if T < 79.3: caption(cv, 'HARVEST NOW', T, 78.1, GRN, y=1500)
    else: caption(cv, 'DECRYPT LATER', T, 79.6, RED, line=RED, y=1500)

# ---------- S16: standards ----------
def s16(cv, T):
    cy = 900
    p = e_io(pr(T, 81.9, 1.3))
    for j in range(3):
        ph = (T * .5 + j / 3) % 1
        if T > 83: cv.ci(CX, cy, 220 + ph * 200, line=GRN, lw=3 * (1 - ph) + .5, a=(1 - ph) * .5, g=.5)
    shield(cv, CX, cy, 540, GRN, 1, 1.0, fill=DARK, p=p) if p < 1 else shield(cv, CX, cy, 540, GRN, 1, 1.0, fill=DARK)
    if p >= 1:
        check(cv, CX, cy - 10, 200, GRN, 1, 22, e_out(pr(T, 83.25, .5)), 1.0)
    yr = 2022 + int(2 * e_out(pr(T, 82.2, .8)))
    hk, ha = pop(T, 82.0, .45)
    cv.rr(CX, 470, 640 * hk, 100 * hk, 50, fill=DARK, line=YEL, lw=3, a=ha, g=.7)
    cv.tx(CX, 470, f'NIST · AUGUST {yr}', 'mono', 32 * hk, YEL, ha, sp=3, g=.4)
    for i, (nm, col, ang0) in enumerate([('ML-KEM', BLUE, -2.3), ('ML-DSA', PUR, -.9), ('SLH-DSA', OR, 0.0)]):
        t0 = 82.5 + i * .5
        pk, pa = pop(T, t0, .5)
        if pa <= 0: continue
        pos = [(260, 1240), (540, 1340), (820, 1240)][i]
        sx = [-200, 540, 1280][i]
        e = e_out(pr(T, t0, .6))
        x = lerp(sx, pos[0], e); y = lerp(1700, pos[1], e)
        w = 250
        cv.rr(x, y, w * pk, 84 * pk, 42, fill=DARK, line=col, lw=3.5, a=pa, g=.8)
        cv.tx(x, y, nm, 'mono', 30 * pk, col, pa, sp=2, g=.4)
    if T > 83.6: caption(cv, 'QUANTUM-SAFE STANDARDS', T, 83.7, GRN, y=1530)
    else: caption(cv, 'NEW STANDARDS ARE HERE', T, 82.2, GRN, y=1530)

# ---------- S17: longer key ----------
def s17(cv, T):
    cols_ = 16; sz = 44; gp = 52
    x0 = CX - (cols_ - 1) * gp / 2
    y0 = 520
    for n in range(256):
        r, c = divmod(n, cols_)
        x = x0 + c * gp; y = y0 + r * gp
        second = n >= 128
        t0 = (86.25 + n * .0035) if not second else (87.0 + (n - 128) * .0045)
        k, a = pop(T, t0, .35)
        if a <= 0: continue
        wv = .5 + .5 * math.sin(T * 4 - (r + c) * .5)
        col = lerp_c(GRN, CREAM, wv * .35) if not second else lerp_c(OR, CREAM, wv * .35)
        cv.rr(x, y, sz * k, sz * k, 9, fill=col, a=a * (.55 + .45 * wv), g=.4)
    kind = pop(T, 86.3, .4)
    k1, a1 = pop(T, 86.3, .4)
    if T < 87.2: cv.tx(CX, 405, '128-BIT KEY', 'mono', 40, GRN, a1, sp=8, g=.5)
    else:
        k2, a2 = pop(T, 87.2, .4)
        cv.tx(CX, 405, '256-BIT KEY', 'mono', 40 * k2, OR, a2, sp=8, g=.7)
    if T > 88.0:
        sk, sa = pop(T, 88.0, .5)
        cv.rr(CX, 1430, 520 * sk, 100 * sk, 50, fill=DARK, line=GRN, lw=5, a=sa, g=1.0)
        check(cv, CX - 190, 1430, 50, GRN, sa, 10, pr(T, 88.1, .4))
        cv.tx(CX + 20, 1430, 'STILL SAFE', 'serif', 56 * sk, GRN, sa, g=.6)
    if T < 87.2: caption(cv, 'STRONG SYMMETRIC ENCRYPTION', T, 86.4, GRN, y=1560)
    else: caption(cv, 'JUST USE A LONGER KEY', T, 87.4, OR, y=1560)

# ---------- S18: finale ----------
def s18(cv, T):
    cy = 880
    ck, ca = pop(T, 89.3, .5)
    chip_icon(cv, CX, cy, 200 * ck, BLUE, T, ca)
    # rings carrying a pattern
    sync = e_io(pr(T, 91.3, .8))
    for j in range(5):
        r0 = 190 + j * 70
        ph = (T * .6 + j * .2) % 1
        pts = []
        for q in range(0, 121):
            th = q / 120 * 2 * math.pi
            wob = (1 - sync) * 26 * math.sin(th * (5 + j * 2) + T * 3) + sync * 18 * math.sin(th * 4 + T * 1.5)
            pts.append((CX + (r0 + wob) * math.cos(th), cy + (r0 + wob) * math.sin(th)))
        pa = pr(T, 89.6 + j * .12, .5)
        cv.ln(pts, [BLUE, PUR, OR, YEL, GRN][j], 4, pa * .9, g=.9)
    ring_burst(cv, CX, cy, T, 91.3, CREAM, 100, 500, 1.0, 8)
    if 89.2 < T < 91.0: caption(cv, 'THEY DO NOT TRY EVERYTHING', T, 89.4, RED, line=RED, y=1500)
    elif T < 92.25: caption(cv, 'THEY HEAR THE PATTERN', T, 91.4, BLUE, y=1500)
    if T >= 92.25:
        fk, fa = pop(T, 92.3, .5)
        pulse = 1 + .04 * math.sin(T * 6)
        cv.rr(CX, 1490, 640 * fk * pulse, 130 * fk * pulse, 65, fill=OR, a=fa, g=.3)
        cv.tx(CX, 1490, 'FOLLOW FOR MORE', 'sans', 48 * fk, DARK, fa)
        ring_burst(cv, CX, 1490, T, 92.3, OR, 80, 420, .9, 6)
