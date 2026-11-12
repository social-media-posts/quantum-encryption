import math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H, S, GS = 1080, 1920, 2, 0.25
BG = (38, 38, 36); PANEL = (48, 48, 46); DARK = (27, 27, 26); CREAM = (244, 241, 232)
DIM = (150, 148, 140); LINE = (78, 78, 74); RAIL = (64, 64, 61)
OR = (217, 119, 87); BLUE = (118, 161, 240); YEL = (240, 184, 74); PUR = (183, 156, 240)
GRN = (126, 207, 126); RED = (232, 108, 100)
FONTS = {
    'serif': '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf',
    'sans': '/usr/share/fonts/opentype/inter/Inter-Bold.otf',
    'mono': '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
}
_fc = {}
def font(name, px):
    key = (name, int(round(px)))
    if key not in _fc:
        _fc[key] = ImageFont.truetype(FONTS[name], max(4, key[1]))
    return _fc[key]

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def pr(t, t0, d): return clamp((t - t0) / d) if d > 0 else (1.0 if t >= t0 else 0.0)
def e_out(x): return 1 - (1 - x) ** 3
def e_in(x): return x ** 3
def e_io(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def e_back(x):
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def lerp(a, b, x): return a + (b - a) * x
def lerp_c(a, b, x): return tuple(int(a[i] + (b[i] - a[i]) * x) for i in range(3))
def pop(t, t0, d=0.45):
    p = pr(t, t0, d)
    return (max(0.01, e_back(p)) if p > 0 else 0.0), clamp(p * 3)
def hsh(i):
    v = math.sin(i * 12.9898 + 78.233) * 43758.5453
    return v - math.floor(v)
def rgb_wheel(h):
    h %= 1.0
    cols = [OR, YEL, GRN, BLUE, PUR, RED]
    i = int(h * 6); f = h * 6 - i
    return lerp_c(cols[i % 6], cols[(i + 1) % 6], f)

def _make_bg():
    return Image.new('RGB', (W * S, H * S), BG)
BGIMG = _make_bg()

class Cv:
    def __init__(s):
        s.img = BGIMG.copy()
        s.d = ImageDraw.Draw(s.img)
        s.gl = Image.new('RGB', (int(W * GS), int(H * GS)))
        s.gd = ImageDraw.Draw(s.gl)
        s.ox = s.oy = 0.0; s.z = 1.0; s.zc = (540, 960); s.base = BG
    def P(s, x, y):
        return ((x - s.zc[0]) * s.z + s.zc[0] + s.ox, (y - s.zc[1]) * s.z + s.zc[1] + s.oy)
    def c(s, col, a=1.0):
        a = clamp(a); b = s.base
        return tuple(int(b[i] + (col[i] - b[i]) * a) for i in range(3))
    @staticmethod
    def gc(col, a): return tuple(int(v * clamp(a)) for v in col)
    def rr(s, cx, cy, w, h, r, fill=None, line=None, lw=3, a=1, g=0):
        if a <= 0: return
        x, y = s.P(cx, cy); z = s.z; w *= z; h *= z; r *= z
        if w < 1.5 or h < 1.5: return
        r = min(r, w / 2, h / 2)
        box = [x - w / 2, y - h / 2, x + w / 2, y + h / 2]
        s.d.rounded_rectangle([v * S for v in box], radius=r * S, fill=s.c(fill, a) if fill else None,
                              outline=s.c(line, a) if line else None, width=max(1, round(lw * z * S)) if line else 0)
        if g > 0:
            s.gd.rounded_rectangle([v * GS for v in box], radius=r * GS, fill=s.gc(fill, a * g * .6) if fill and not line else None,
                                   outline=s.gc(line or fill, a * g), width=max(1, round(lw * z * GS * 1.5)))
    def el(s, cx, cy, rx, ry, fill=None, line=None, lw=3, a=1, g=0):
        if a <= 0: return
        x, y = s.P(cx, cy); z = s.z; rx *= z; ry *= z
        if rx < .6 or ry < .6: return
        box = [x - rx, y - ry, x + rx, y + ry]
        s.d.ellipse([v * S for v in box], fill=s.c(fill, a) if fill else None,
                    outline=s.c(line, a) if line else None, width=max(1, round(lw * z * S)) if line else 0)
        if g > 0:
            s.gd.ellipse([v * GS for v in box], fill=s.gc(fill, a * g) if fill and not line else None,
                         outline=s.gc(line or fill, a * g), width=max(1, round(lw * z * GS * 1.5)))
    def ci(s, cx, cy, r, **kw): s.el(cx, cy, r, r, **kw)
    def ln(s, pts, col, w=4, a=1, g=0, cap=True):
        if a <= 0 or len(pts) < 2: return
        Pp = [s.P(x, y) for x, y in pts]; z = s.z
        ww = max(1, round(w * z * S))
        s.d.line([(x * S, y * S) for x, y in Pp], fill=s.c(col, a), width=ww, joint='curve')
        if cap and ww > 3:
            r = ww / 2
            for x, y in (Pp[0], Pp[-1]):
                s.d.ellipse([x * S - r, y * S - r, x * S + r, y * S + r], fill=s.c(col, a))
        if g > 0:
            gw = max(1, round(w * z * GS * 1.6))
            s.gd.line([(x * GS, y * GS) for x, y in Pp], fill=s.gc(col, a * g), width=gw, joint='curve')
    def poly(s, pts, fill=None, line=None, lw=3, a=1, g=0):
        if a <= 0: return
        Pp = [s.P(x, y) for x, y in pts]
        if fill: s.d.polygon([(x * S, y * S) for x, y in Pp], fill=s.c(fill, a))
        if line:
            s.d.line([(x * S, y * S) for x, y in Pp + [Pp[0]]], fill=s.c(line, a), width=max(1, round(lw * s.z * S)), joint='curve')
        if g > 0:
            s.gd.polygon([(x * GS, y * GS) for x, y in Pp], fill=s.gc(fill or line, a * g * .5))
    def arc(s, cx, cy, r, a0, a1, col, w=4, a=1, g=0, n=None):
        n = n or max(8, int(abs(a1 - a0) / 0.06))
        pts = [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
        s.ln(pts, col, w, a, g)
    def tx(s, x, y, text, f='sans', size=40, col=CREAM, a=1, anchor='mm', sp=0, g=0):
        if a <= 0 or not text: return
        px, py = s.P(x, y); sz = size * s.z
        if sz < 3: return
        fo = font(f, sz * S)
        if sp == 0:
            s.d.text((px * S, py * S), text, font=fo, fill=s.c(col, a), anchor=anchor)
            if g > 0:
                s.gd.text((px * GS, py * GS), text, font=font(f, sz * GS), fill=s.gc(col, a * g), anchor=anchor)
            return
        ws = [fo.getlength(ch) for ch in text]
        tot = sum(ws) + sp * S * s.z * (len(text) - 1)
        if anchor[0] == 'm': x0 = px * S - tot / 2
        elif anchor[0] == 'l': x0 = px * S
        else: x0 = px * S - tot
        for ch, w_ in zip(text, ws):
            s.d.text((x0, py * S), ch, font=fo, fill=s.c(col, a), anchor='l' + anchor[1])
            if g > 0:
                s.gd.text((x0 * GS / S, py * GS), ch, font=font(f, sz * GS), fill=s.gc(col, a * g), anchor='l' + anchor[1])
            x0 += w_ + sp * S * s.z
    def tw(s, text, f, size): return font(f, size * S).getlength(text) / S
    def tx_rot(s, x, y, text, f, size, col, ang, a=1):
        if a <= 0: return
        px, py = s.P(x, y); sz = size * s.z
        fo = font(f, sz * S)
        bb = fo.getbbox(text)
        tw_, th_ = bb[2] - bb[0] + 40, bb[3] - bb[1] + 40
        tmp = Image.new('L', (tw_, th_), 0)
        ImageDraw.Draw(tmp).text((tw_ // 2, th_ // 2), text, font=fo, fill=255, anchor='mm')
        tmp = tmp.rotate(ang, resample=Image.BICUBIC, expand=True)
        a_ = tmp.point(lambda v: int(v * clamp(a)))
        solid = Image.new('RGB', tmp.size, col)
        s.img.paste(solid, (int(px * S - tmp.width / 2), int(py * S - tmp.height / 2)), a_)
    def out(s):
        main = s.img.resize((W, H), Image.LANCZOS)
        g1 = s.gl.filter(ImageFilter.GaussianBlur(1.5))
        g2 = s.gl.filter(ImageFilter.GaussianBlur(6))
        gg = ImageChops.add(g1, g2).resize((W, H), Image.BICUBIC)
        return ImageChops.screen(main, gg)
