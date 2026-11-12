import math
from lib2 import *
from kit import bezier
cv = Cv()
cv.tx(540, 340, 'WHAT MOST PEOPLE GET WRONG', 'mono', 28, DIM, 1, sp=6)
cv.tx(540, 480, 'Quantum doesn\'t', 'serif', 132, CREAM, 1)
cv.tx(540, 625, 'break encryption', 'serif', 128, OR, 1)
cv.tx(540, 750, 'the way you think', 'serif', 80, DIM, 1)
cx, cy, R = 540, 1135, 290
cv.ci(cx, cy, R, line=LINE, lw=3)
pos = lambda v: (cx + R * math.cos(-math.pi / 2 + v * 2 * math.pi / 15), cy + R * math.sin(-math.pi / 2 + v * 2 * math.pi / 15))
seq = [1, 7, 4, 13, 1]
for i in range(4):
    a, b = pos(seq[i]), pos(seq[i + 1])
    mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    ctrl = (cx + (mid[0] - cx) * .25, cy + (mid[1] - cy) * .25)
    cv.ln(bezier(a, ctrl, b), OR, 9, 1)
for v in range(15):
    x, y = pos(v)
    if v in seq:
        cv.ci(x, y, 34, fill=OR); cv.tx(x, y + 1, str(v), 'mono', 30, DARK, 1)
    else:
        cv.ci(x, y, 15, fill=RAIL, line=LINE, lw=2)
cv.ci(cx, cy, 135, fill=BG, line=LINE, lw=3)
cv.tx(cx, cy - 18, 'r = 4', 'serif', 96, CREAM, 1)
cv.tx(cx, cy + 50, 'HIDDEN LOOP', 'mono', 22, DIM, 1, sp=6)
cv.rr(540, 1560, 700, 96, 48, line=CREAM, lw=3)
cv.tx(540, 1560, 'SHOR\'S ALGORITHM, EXPLAINED', 'sans', 34, CREAM, 1)
im = cv.out()
im.save('../out/thumbnail.png'); im.convert('RGB').save('../out/thumbnail.jpg', quality=93)
