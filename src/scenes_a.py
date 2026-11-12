import math, random
from lib2 import *
from kit import *

CX, CY = 540, 880
PW = ['123456', 'password', 'qwerty', 'letmein', 'hunter2', 'admin', 'iloveyou', 'dragon', 'monkey', 'abc123', 'secret', 'welcome',
      'sunshine', 'master', 'p@ssw0rd', 'trustno1', 'football', 'shadow', 'login', 'princess']
CHR = 'abcdefghijkmnpqrstuvwxyz23456789!@#$%'
def scr(i, T, n=8):
    k = int(T * 10)
    return ''.join(CHR[int(hsh(i * 7 + j + k * 13) * len(CHR))] for j in range(n))

# ---------- S1: the myth ----------
def s1(cv, T):
    cols, rows = 6, 14
    cur = int(max(0, (T - .5)) * 30)
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c
            x = 540 + (c - 2.5) * 160; y0 = 392 + r * 79; y = y0
            k, a = pop(T, .1 + (r + c) * .035, .4)
            if a <= 0: continue
            fall = T - (4.5 + hsh(i) * .55)
            tint = 0
            if fall > 0:
                y = y0 + 1500 * fall * fall; tint = 1
            lit = 0
            if T < 3.42:
                lit = 1 if i == cur else (.35 if i < cur else 0)
            else:
                d = math.hypot(x - 540, y0 - 880)
                lit = clamp(((T - 3.42) * 1700 - d) / 160)
            col = lerp_c(OR, RED, tint) if lit > 0 else DIM
            if tint: col = lerp_c(col, RED, .8)
            fillc = lerp_c(PANEL, lerp_c(OR, RED, tint), .28 * lit) if lit > 0 else PANEL
            w = 148 * k
            cv.rr(x, y, w, 52 * k, 14, fill=fillc, line=col if lit > 0 else LINE, lw=2.5, a=a, g=.7 * lit)
            txt = PW[i % len(PW)] if (lit > .8 and T > 3.42) else scr(i, T)
            if lit == 1 and T < 3.42: txt = PW[i % len(PW)]
            cv.tx(x, y, txt, 'mono', 23 * k, CREAM if lit > .6 else DIM, a * (.9 if lit > 0 else .55))
    # central quantum chip
    pk, pa = pop(T, .75, .5)
    if pa > 0:
        cy = 880
        if T > 4.4:
            pass
        cv.ci(CX, cy, 168 * pk, fill=DARK, line=BLUE, lw=4, a=pa, g=.8)
        dash_circle(cv, CX, cy, 196 * pk, T, BLUE, .5, 40, 3, pa, .5)
        chip_icon(cv, CX, cy, 160 * pk, BLUE, T, pa)
        for j in range(3):
            ph = (T * .7 + j / 3) % 1
            if T > .9: cv.ci(CX, cy, 168 + ph * 140, line=BLUE, lw=3 * (1 - ph) + .5, a=(1 - ph) * .7, g=.6)
    ring_burst(cv, CX, 880, T, 3.42, CREAM, 120, 900, 1.0, 10)
    # stamp
    if T > 4.4:
        sp, sa = pop(T, 4.4, .35)
        shake = math.sin(T * 90) * 6 * (1 - pr(T, 4.4, .4))
        cv.ci(CX + shake, 880, 215 * sp, line=RED, lw=20, a=sa, g=.9)
        cv.ln([(CX + shake - 152 * sp, 880 - 152 * sp), (CX + shake + 152 * sp, 880 + 152 * sp)], RED, 20, sa, .9)
        mk, ma = pop(T, 4.9, .4)
        if ma > 0:
            cv.rr(CX, 1235, 420 * mk, 150 * mk, 22, fill=DARK, line=RED, lw=6, a=ma, g=.8)
            cv.tx_rot(CX, 1235, 'MYTH', 'serif', 126 * mk, RED, 6, ma)
    if T < 4.3: caption(cv, 'TRY EVERY PASSWORD AT ONCE', T, 1.0, OR)
    else: caption(cv, 'NOT HOW IT WORKS', T, 5.0, RED, line=RED)

# ---------- S2: collapse + wave ----------
def s2(cv, T):
    N = 140; cy = 860
    cp = e_in(pr(T, 7.0, .55))
    for i in range(N):
        r = math.sqrt((i + .5) / N) * 330
        ang = i * 2.39996 + T * .35 * (1 - cp) + cp * 2
        x = CX + r * math.cos(ang); y = cy + r * math.sin(ang)
        k, a = pop(T, 6.2 + i * .004, .4)
        if a <= 0: continue
        if i == 70: pass
        x = lerp(x, CX, cp); y = lerp(y, cy, cp)
        flash = clamp(1 - abs(math.hypot(x - CX, y - cy) - (T - 6.55) * 900) / 40) if 6.55 < T < 7.1 else 0
        col = lerp_c(rgb_wheel(i / N + T * .08), CREAM, flash)
        rad = (7 + 3 * math.sin(T * 3 + i)) * k * (1 - .8 * cp)
        if i == 70:
            if T > 7.55: continue
        cv.ci(x, y, rad, fill=col, a=a * (1 - .0), g=.9 + flash)
    # chosen dot
    if 7.5 < T < 9.35:
        k, a = pop(T, 7.5, .35)
        sh = 1 - e_in(pr(T, 9.0, .4))
        cv.ci(CX, cy, 20 * k * sh, fill=CREAM, a=a, g=1.2)
        ring_burst(cv, CX, cy, T, 7.55, CREAM, 20, 340, .8, 8)
        dash_circle(cv, CX, cy, 56 * sh, T, YEL, 1.2, 20, 3, a, .6)
    # result tile
    if 7.85 < T < 9.5:
        k, a = pop(T, 7.9, .4); k *= (1 - e_in(pr(T, 9.0, .4)))
        txt = scr(3, T, 7) if T < 8.6 else 'q7!Zx9R'
        cv.rr(CX, 1130, 480 * k, 124 * k, 24, fill=DARK, line=YEL, lw=4, a=a, g=.7)
        cv.tx(CX, 1130, txt, 'mono', 54 * k, YEL if T >= 8.6 else DIM, a, g=.5 if T >= 8.6 else 0)
        kicker(cv, 'MEASURE THE STATE', T, 7.0, 520, BLUE)
    if T < 7.0: kicker(cv, 'EVERY ANSWER AT ONCE', T, 6.3, 520, BLUE)
    if 7.9 < T < 9.5: caption(cv, 'ONE RANDOM ANSWER', T, 8.0, YEL)
    # waves
    if T > 9.0:
        hw = e_out(pr(T, 9.1, 1.0)) * 520
        fade_to_sum = e_io(pr(T, 10.3, .8))
        cols = [OR, BLUE, YEL, PUR]
        yy = 900
        for j in range(4):
            lam = 190 + j * 70
            amp = (60 + j * 22) * e_out(pr(T, 9.3 + j * .15, .7))
            pts = []
            for q in range(0, 81):
                x = CX - hw + (2 * hw) * q / 80
                pts.append((x, yy + amp * math.sin((x - CX) / lam * 2 * math.pi + j * 1.3 - T * (1.2 + j * .4))))
            cv.ln(pts, cols[j], 5, .95 * (1 - .5 * fade_to_sum), g=.8)
        if fade_to_sum > 0:
            pts = []
            for q in range(0, 81):
                x = CX - hw + (2 * hw) * q / 80
                v = sum((60 + j * 22) * math.sin((x - CX) / (190 + j * 70) * 2 * math.pi + j * 1.3 - T * (1.2 + j * .4)) for j in range(4)) * .45
                pts.append((x, yy + 420 * 0 + v * fade_to_sum))
            cv.ln(pts, CREAM, 8, fade_to_sum, g=1.1)
        kicker(cv, 'WAVES, NOT GUESSES', T, 9.5, 560, CREAM)
        caption(cv, 'THE REAL TRICK IS STRANGER', T, 9.7, CREAM)

# ---------- S3: hub ----------
def s3(cv, T):
    cy = 900
    dash_circle(cv, CX, cy, 330, T, LINE, .12, 60, 3)
    dash_circle(cv, CX, cy, 440, T, LINE, -.1, 80, 3)
    kinds = ['browser', 'card', 'chat', 'mail', 'bank', 'globe']
    cols = [BLUE, YEL, GRN, OR, PUR, BLUE]
    for k in range(6):
        ang = T * .35 + k * math.pi / 3 - 1.2
        R = 330 if k % 2 == 0 else 440
        x = CX + R * math.cos(ang); y = cy + R * math.sin(ang) * .98
        pk, pa = pop(T, 12.15 + k * .17, .45)
        if pa <= 0: continue
        # data pulses
        for j in range(2):
            ph = (T * .8 + k * .37 + j * .5) % 1
            cv.ci(lerp(x, CX, ph), lerp(y, cy, ph), 5, fill=cols[k], a=pa * (1 - .4 * ph), g=.9)
        cv.ln([(x, y), (CX, cy)], cols[k], 2, pa * .25)
        cv.rr(x, y, 112 * pk, 112 * pk, 28, fill=PANEL, line=cols[k], lw=3, a=pa, g=.6)
        sat_icon(cv, kinds[k], x, y, 1.0 * pk, cols[k], pa)
    pk, pa = pop(T, 11.9, .5)
    for j in range(3):
        ph = (T * .6 + j / 3) % 1
        cv.ci(CX, cy, 120 + ph * 140, line=GRN, lw=3 * (1 - ph) + .5, a=(1 - ph) * .5, g=.5)
    cv.ci(CX, cy, 138 * pk, fill=DARK, line=GRN, lw=4, a=pa, g=.9)
    op = e_out(pr(T, 13.9, .5)) * .0
    padlock(cv, CX, cy - 12, 160 * pk, GRN, 0, pa, .9)
    ck, ca = pop(T, 12.6, .4)
    cv.rr(CX, 610, 190 * ck, 70 * ck, 35, fill=DARK, line=YEL, lw=3, a=ca, g=.6)
    cv.tx(CX, 610, 'RSA', 'mono', 40 * ck, YEL, ca, sp=8, g=.5)
    caption(cv, 'THE LOCK BEHIND THE INTERNET', T, 12.4, GRN)

# ---------- S4: giant number ----------
random.seed(7)
DIG = ''.join(str(random.randint(0, 9)) for _ in range(617)); DIG = '9' + DIG[1:]
def s4(cv, T):
    cy = 960; cols_, rows_ = 36, 18
    pk, pa = pop(T, 14.45, .5)
    cv.rr(CX, cy, 900 * pk, 640 * pk, 32, fill=DARK, line=OR, lw=4, a=pa, g=.8)
    typed = int(617 * e_io(pr(T, 14.85, 3.1)))
    for n in range(typed):
        r, c = divmod(n, cols_)
        x = 540 + (c - (cols_ - 1) / 2) * 23.5; y = cy - 280 + r * 31
        sc = 0
        sweep = (T * 14) % (rows_ + 10)
        hl = clamp(1 - abs(r - sweep) / 3)
        col = lerp_c(lerp_c(OR, CREAM, .4), CREAM, hl)
        recent = n > typed - 12 and typed < 617
        cv.tx(x, y, DIG[n], 'mono', 25, CREAM if recent else col, .95 if recent else (.55 + .4 * hl), g=.6 if recent else hl * .6)
    cnt = typed
    k, a = pop(T, 14.7, .5)
    cv.tx(CX, 470, fmt(cnt), 'serif', 150 * k, CREAM, a, g=.3)
    cv.tx(CX, 568, 'DIGITS' if cnt != 1 else 'DIGIT', 'mono', 30, OR, a, sp=10, g=.4)
    pl = padlock
    pl(cv, 330, 1380, 90, OR, 0, pa, .6)
    cv.tx(CX + 110, 1380, 'RSA-2048', 'mono', 44, CREAM, pa, sp=6, g=.3)
    if T > 18.3:
        ring_burst(cv, CX, cy, T, 18.3, OR, 300, 700, 1.0, 5)
    caption(cv, 'ONE GIANT SECRET NUMBER', T, 15.0, OR)

# ---------- S5: split + instant ----------
def block(cv, cx, cy, w, h, col, label, T, seed, a=1, k=1, cols_=16, rows_=11):
    cv.rr(cx, cy, w * k, h * k, 24, fill=DARK, line=col, lw=4, a=a, g=.8)
    for r in range(rows_):
        for c in range(cols_):
            if hsh(r * 31 + c + seed + int(T * 6 + r) * .01) < .0: continue
            ch = str(int(hsh(r * 17 + c * 3 + seed + int(T * 5) * (1 if (c + r) % 5 == 0 else 0)) * 10))
            cv.tx(cx + (c - (cols_ - 1) / 2) * (w * k / (cols_ + 1)), cy - h * k * .26 + r * (h * k * .52 / rows_ * 1.5), ch, 'mono', 19 * k, col, a * .8)
    cv.tx(cx, cy - h * k / 2 - 36, label, 'mono', 32 * k, col, a, sp=6, g=.5)

def s5(cv, T):
    sep = e_out(pr(T, 20.15, .6))
    mrg = e_io(pr(T, 21.7, .55))
    gap = 250 * sep * (1 - mrg)
    cy = 800
    if T < 22.35:
        block(cv, CX - gap, cy, 470 - 90 * sep, 400, YEL, 'PRIME p', T, 3, 1, 1)
        block(cv, CX + gap, cy, 470 - 90 * sep, 400, BLUE, 'PRIME q', T, 91, 1, 1)
        if sep > .3 and mrg < .7:
            cv.tx(CX, cy, '×', 'serif', 130, CREAM, clamp(sep * 2) * (1 - mrg), g=.6)
    else:
        k, a = pop(T, 22.2, .4)
        cv.rr(CX, cy, 640 * k, 340 * k, 26, fill=DARK, line=OR, lw=4, a=a, g=.9)
        cv.tx(CX, cy, 'N = p × q', 'serif', 100 * k, CREAM, a, g=.5)
        cv.tx(CX, cy - 140, 'THE PUBLIC NUMBER', 'mono', 30, OR, a, sp=6, g=.4)
    if 21.6 < T < 22.7: ring_burst(cv, CX, cy, T, 22.05, CREAM, 60, 500, .8, 8)
    # stopwatch
    k, a = pop(T, 23.3, .45)
    if a > 0:
        ang = (T - 23.3) * 22 if T < 23.9 else 0
        stopwatch(cv, CX, 1230, 120 * k, ang, GRN, a)
        ck = pr(T, 23.9, .4)
        if ck > 0: check(cv, CX + 210, 1230, 70, GRN, 1, 10, ck)
        if ck > 0: cv.tx(CX + 330, 1230, 'INSTANT', 'mono', 30, GRN, 1, sp=3, g=.4, anchor='lm') if False else None
    if T < 22.8: caption(cv, 'MULTIPLY: EASY', T, 21.0, YEL)
    else: caption(cv, 'MULTIPLY: INSTANT', T, 23.4, GRN)

# ---------- S6: age of the universe ----------
def s6(cv, T):
    xs0, xs1, by = 100, 980, 1080
    for j in range(3):
        sx = CX + (j - 1) * 270
        pk, pa = pop(T, 24.75 + j * .15, .45)
        hot = pr(T, 26.0, 3.0)
        server(cv, sx, 600, 190 * pk, ORR if False else OR, T + j, pa, .4, hot)
    kicker(cv, 'TIME TO FACTOR RSA-2048', T, 24.9, 430, OR)
    pk, pa = pop(T, 25.0, .4)
    cv.rr(CX, by, 880 * pk, 44, 22, fill=DARK, line=LINE, lw=2, a=pa)
    ticks = [(0, '1 YEAR'), (.2, '1 THOUSAND'), (.4, '1 MILLION'), (.6, '1 BILLION')]
    for f, lb in ticks:
        x = xs0 + (xs1 - xs0) * f * (1 / 1.0) * 1.0 * .98 / .98 * (0.85 / .85)
    # log scale: positions
    mark_x = xs0 + (xs1 - xs0) * .62
    prog = e_io(pr(T, 25.4, 3.6))
    fx = xs0 + (xs1 - xs0) * prog
    col = lerp_c(OR, RED, clamp((prog - .55) * 3))
    if pa > 0:
        cv.rr((xs0 + fx) / 2, by, max(10, fx - xs0), 36, 18, fill=col, a=pa, g=.9)
        cv.ci(fx, by, 20, fill=CREAM, a=pa, g=1.1)
    # universe marker
    mk, ma = pop(T, 26.0, .45)
    cv.ln([(mark_x, by - 40), (mark_x, by - 170 * mk)], YEL, 4, ma, .6)
    cv.rr(mark_x, by - 215, 330 * mk, 84 * mk, 18, fill=DARK, line=YEL, lw=3, a=ma, g=.6)
    cv.tx(mark_x, by - 232, 'AGE OF THE UNIVERSE', 'mono', 22 * mk, YEL, ma)
    cv.tx(mark_x, by - 200, '13.8 billion years', 'sans', 28 * mk, CREAM, ma)
    # overflow
    ov = pr(T, 27.7, .5)
    if ov > 0:
        for i in range(4):
            ph = (T * 2 + i * .25) % 1
            cv.tx(xs1 - 60 + 0 * i, by + 90 + 0, '', 'mono', 10, RED, 1)
        for i in range(5):
            x = mark_x + 60 + i * 52 + (T * 40) % 52
            if x < xs1 + 10: cv.poly([(x, by - 46), (x + 22, by - 46 + 0), (x + 40, by), (x + 22, by + 46), (x, by + 46), (x + 18, by)], fill=RED, a=ov * (1 - i * .12), g=.6)
        ring_burst(cv, xs1, by, T, 27.75, RED, 20, 200, .8, 7)
        cv.tx(CX, by + 120, 'LONGER THAN THAT', 'serif', 66, RED, ov, g=.6)
    years = int(10 ** lerp(0, 13.14, prog)) if prog < 1 else int(1.4e13)
    cv.tx(CX, by + 230 if ov <= 0 else by + 230, (fmt(years) + (' year' if years == 1 else ' years')) if prog < .995 else '> 13,800,000,000 years', 'mono', 34, CREAM, pa)
    caption(cv, 'BRUTE FORCE: HOPELESS', T, 26.4, RED, line=RED)

ORR = OR

# ---------- S7: Shor ----------
def s7(cv, T):
    # year odometer
    yk, ya = pop(T, 30.45, .5)
    yr = 1990 + int(4 * e_out(pr(T, 30.6, 1.0)))
    wob = 1 + .03 * math.sin(T * 6) * (1 - pr(T, 32, .5))
    cv.tx(CX, 600, str(yr), 'serif', 270 * yk, CREAM, ya, g=.4)
    ring_burst(cv, CX, 600, T, 31.6, YEL, 200, 560, .9, 6)
    nk, na = pop(T, 31.5, .5)
    cv.rr(CX, 830, 700 * nk, 118 * nk, 59, fill=DARK, line=YEL, lw=3, a=na, g=.6)
    cv.ci(CX - 285, 830, 40 * nk, fill=YEL, a=na)
    cv.tx(CX - 285, 831, 'PS', 'sans', 34 * nk, DARK, na)
    cv.tx(CX + 20, 818, 'PETER SHOR', 'sans', 38 * nk, CREAM, na)
    cv.tx(CX + 20, 852, 'MATHEMATICIAN · BELL LABS', 'mono', 19 * nk, DIM, na)
    # B1 shortcut
    y1 = slide_y(T, 31.9, 33.45)
    if y1 < 690:
        by = 1200 + y1
        pts = [(110 + i * 12.6, by + 100 * math.sin(i * .22) * (1 if i % 2 == 0 else 1)) for i in range(0, 71)]
        pts = [(110 + i * 12.6, by + 110 * math.sin(i * .35)) for i in range(71)]
        cv.ln(pts, LINE, 6, 1, 0)
        dp = (T * .35) % 1
        q = partial(pts, e_out(pr(T, 32.0, 1.2)))
        cv.ci(*q[-1], 12, fill=CREAM, g=1)
        cv.ln([(110, by), (970, by)], GRN, 7, e_out(pr(T, 32.5, .5)) if T > 32.5 else 0, g=1, cap=True) if False else None
        p2 = e_out(pr(T, 32.35, .6))
        if p2 > 0:
            cv.ln([(110, by), (110 + 860 * p2, by)], GRN, 9, 1, g=1.2)
            cv.poly([(110 + 860 * p2, by - 22), (110 + 860 * p2 + 36, by), (110 + 860 * p2, by + 22)], fill=GRN, a=1, g=1)
        cv.tx(CX, by + 190, 'SHORTCUT', 'mono', 36, GRN, p2, sp=10, g=.5)
    # B2 not faster: gauge
    y2 = slide_y(T, 33.5, 34.95)
    if 33.45 < T < 35.5 and y2 < 690:
        gy = 1240 + y2
        cv.arc(CX, gy, 230, math.pi, 2 * math.pi, LINE, 22, 1)
        sw = e_out(pr(T, 33.6, .5)) * math.pi
        cv.arc(CX, gy, 230, math.pi, math.pi + sw, lerp_c(OR, RED, pr(T, 33.6, .6)), 22, 1, g=.9)
        na = math.pi + sw + math.sin(T * 40) * .05 * (pr(T, 33.9, .3))
        cv.ln([(CX, gy), (CX + 200 * math.cos(na), gy + 200 * math.sin(na))], CREAM, 8, 1, g=.8)
        cv.ci(CX, gy, 16, fill=CREAM)
        cv.tx(CX, gy + 80, 'FASTER GUESSING', 'mono', 32, DIM, 1, sp=5)
        if T > 34.2:
            sp, sa = pop(T, 34.2, .3)
            cv.ci(CX, gy - 60, 120 * sp, line=RED, lw=14, a=sa, g=.9)
            cross(cv, CX, gy - 60, 120 * sp, RED, sa, 14, 1)
    # B3 listen
    y3 = slide_y(T, 35.05)
    if T > 34.95 and y3 < 690:
        ly = 1250 + y3
        N = 28
        mix = e_io(pr(T, 35.8, .8))
        for i in range(N):
            x = 90 + i * 34
            ph = T * 5 + i * .6
            h = 40 + 56 * abs(math.sin(ph)) * (1 - mix) + 62 * mix * abs(math.sin(i * .45 - T * 3)) 
            col = lerp_c(BLUE, PUR, i / N)
            cv.rr(x, ly, 16, h * 2, 8, fill=col, a=1, g=.8)
        # headphones
        cv.arc(CX, ly - 215, 70, math.pi, 2 * math.pi, CREAM, 8, 1, g=.5)
        cv.rr(CX - 70, ly - 188, 24, 52, 10, fill=CREAM)
        cv.rr(CX + 70, ly - 188, 24, 52, 10, fill=CREAM)
        cv.tx(CX, ly + 150, 'LISTEN FOR THE RHYTHM', 'mono', 32, PUR, 1, sp=5, g=.5)
