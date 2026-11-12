import math, sys
from lib2 import *
from kit import hud, particles
import scenes_a as A, scenes_b as B

TOTAL = 94.0
FPS = 30
TD = 0.65
SC = [  # (tb, fn, transition)
    (0.0, A.s1, None), (5.6, A.s2, 'up'), (11.35, A.s3, 'left'), (14.3, A.s4, 'up'), (19.45, A.s5, 'zoom'),
    (24.35, A.s6, 'left'), (29.7, A.s7, 'up'), (36.4, B.s8, 'zoom'), (46.3, B.s9, 'left'), (49.2, B.s10, 'up'),
    (58.45, B.s12, 'zoom'), (65.45, B.s13, 'up'), (68.9, B.s14, 'left'), (77.2, B.s15, 'up'), (81.3, B.s16, 'zoom'),
    (85.6, B.s17, 'left'), (88.6, B.s18, 'up'),
]

def tf(cv, kind, p, incoming):
    e = e_io(p)
    if kind == 'up':
        cv.oy = (1 - e) * 2100 if incoming else -e * 2100
    elif kind == 'left':
        cv.ox = (1 - e) * 1300 if incoming else -e * 1300
    elif kind == 'zoom':
        if incoming:
            cv.z = lerp(.3, 1, e_out(p)); cv.zc = (540, 900)
        else:
            cv.z = lerp(1, 3.2, e_in(p)); cv.zc = (540, 900)

def reset(cv): cv.ox = cv.oy = 0; cv.z = 1; cv.zc = (540, 960)

def streaks(cv, T, kind, p):
    amp = math.sin(p * math.pi)
    if amp <= 0: return
    for i in range(14):
        h = hsh(i * 3.7)
        if kind == 'up':
            x = 40 + h * 1000; L = 380 + 520 * hsh(i * 1.3) * amp
            y = (hsh(i * 9.1) * 2300 + p * 3000 * (1 + h)) % 2300 - 150
            cv.ln([(x, y), (x, y + L)], CREAM, 3, .35 * amp, g=1.0)
        elif kind == 'left':
            y = 260 + h * 1400; L = 380 + 520 * hsh(i * 1.3) * amp
            x = (hsh(i * 9.1) * 1500 - p * 3000 * (1 + h)) % 1500 - 150
            cv.ln([(x, y), (x + L, y)], CREAM, 3, .35 * amp, g=1.0)
        else:
            a = h * 2 * math.pi; r0 = 200 + 700 * p; r1 = r0 + 160 * amp
            cv.ln([(540 + r0 * math.cos(a), 900 + r0 * math.sin(a)), (540 + r1 * math.cos(a), 900 + r1 * math.sin(a))], CREAM, 3, .4 * amp, g=1.0)

def frame(T):
    cv = Cv()
    n = len(SC)
    idx = max(i for i in range(n) if T >= SC[i][0])
    tb, fn, kind = SC[idx]
    prog = pr(T, tb, TD) if kind else 1.0
    if kind and prog < 1:
        prev = SC[idx - 1][1]
        reset(cv); tf(cv, kind, prog, False); prev(cv, T)
        reset(cv); tf(cv, kind, prog, True)
        if kind == 'zoom' and prog < .3: pass
        else: fn(cv, T)
        reset(cv); streaks(cv, T, kind, prog)
    else:
        reset(cv); fn(cv, T)
    reset(cv)
    hud(cv, T, TOTAL)
    return cv.out()

if __name__ == '__main__':
    import subprocess, os
    from multiprocessing import Pool
    CH = 150
    nfr = int(TOTAL * FPS)
    os.makedirs('chunks', exist_ok=True)
    def work(ci):
        out = f'chunks/c{ci:03d}.mp4'
        if os.path.exists(out): return ci
        f0 = ci * CH; f1 = min(nfr, f0 + CH)
        p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-crf', '15', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-g', '30', out + '.tmp.mp4'], stdin=subprocess.PIPE)
        for f in range(f0, f1):
            p.stdin.write(frame(f / FPS).tobytes())
        p.stdin.close(); p.wait()
        os.rename(out + '.tmp.mp4', out)
        return ci
    nch = (nfr + CH - 1) // CH
    with Pool(2) as pool:
        for ci in pool.imap_unordered(work, range(nch)):
            print('chunk', ci, 'done', flush=True)
