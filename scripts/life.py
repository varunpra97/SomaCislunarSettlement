import cairo, math, random, os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vid import (W, H, FPS, hx, col, text, wrap, background, tag, ease, seg, clamp, lerp, ell,
                 BG, FG, MUT, GOLD, CY, GLASS, KEEL, STEEL, SPARK, SHIP, NOSE, MONO, SANS)
OUT = os.path.dirname(os.path.abspath(__file__))
TR = 75.0; RING = 17350.0; L5 = 13.33

def mixc(a, b, u):
    a = hx(a); b = hx(b); return tuple(lerp(a[i], b[i], u) for i in range(3))
def setc(ctx, rgb, a=1.0): ctx.set_source_rgba(rgb[0], rgb[1], rgb[2], a)
def scale(rgb, k): return tuple(clamp(c * k) for c in rgb)

def header(ctx, clock):
    text(ctx, 'A DAY ON THE RING', 40, 44, 15, MUT, spacing=3)
    text(ctx, 'CISLUNAR SETTLEMENT · 550,000 PEOPLE', 40, 66, 12, '#6b6252', spacing=2)
    if clock: text(ctx, clock, 1240, 56, 30, FG, anchor='r', bold=True)

def caption(ctx, step, body):
    col(ctx, '#11131b', .9); ctx.rectangle(40, 600, 1200, 100); ctx.fill()
    col(ctx, GOLD); ctx.rectangle(40, 600, 4, 100); ctx.fill()
    text(ctx, step, 64, 630, 14, GOLD, bold=True, spacing=2)
    for i, l in enumerate(wrap(ctx, body, 19, SANS, 1150)[:2]): text(ctx, l, 64, 660 + i * 26, 19, FG, font=SANS)

def fade(ctx, t, dur, fi=.5, fo=.5):
    a = 0
    if t < fi: a = 1 - t / fi
    if t > dur - fo: a = max(a, (t - (dur - fo)) / fo)
    if a > 0: col(ctx, '#000000', clamp(a)); ctx.paint()

# ---------------- perspective renderer ----------------
F = 720.0; HY = 300.0; EYE_H = 22.0
EYE = {'h': 22.0, 'x': 0.0}
SLICES = [15 * (2600 / 15) ** (i / 70) for i in range(71)]
def proj(x, h, d):
    rise = d * d / (2 * RING)
    return (W / 2 + F * (x - EYE['x']) / d, HY - F * (h + rise - EYE['h']) / d)

def arc_pts(x_edge, h_edge, n=18):
    # upper wall from right edge (x>0) over the top to left edge
    a0 = math.asin(clamp((h_edge - TR) / TR, -1, 1)); a1 = math.pi - a0
    return [(TR * math.cos(a0 + (a1 - a0) * i / n), TR + TR * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]

def render_tunnel(ctx, profile_fn, haze, light, extras=None):
    # profile_fn(d) -> list of (x,h,colorhex) ; segment i from pt i to i+1 takes color of pt i
    setc(ctx, hx(haze)); ctx.paint()
    for k in range(len(SLICES) - 1, 0, -1):
        dfar, dnear = SLICES[k], SLICES[k - 1]
        pf, pn = profile_fn(dfar), profile_fn(dnear)
        fogk = clamp((dfar - 150) / 2300) ** .8
        for i in range(len(pn) - 1):
            c = pn[i][2]
            if c is None: continue
            rgb = scale(hx(c), light) if c not in ('#fff7df',) else hx(c)
            rgb = tuple(lerp(rgb[j], hx(haze)[j], fogk * .85) for j in range(3))
            a, b = proj(pf[i][0], pf[i][1], dfar), proj(pf[i + 1][0], pf[i + 1][1], dfar)
            c2, d2 = proj(pn[i + 1][0], pn[i + 1][1], dnear), proj(pn[i][0], pn[i][1], dnear)
            ctx.move_to(*a); ctx.line_to(*b); ctx.line_to(*c2); ctx.line_to(*d2); ctx.close_path()
            setc(ctx, rgb); ctx.fill_preserve(); ctx.set_line_width(.6); ctx.stroke()
        if extras: extras(ctx, dfar, dnear, fogk)

def topband(ctx):
    g = cairo.LinearGradient(0, 0, 0, 110); g.add_color_stop_rgba(0, .04, .04, .06, .85); g.add_color_stop_rgba(1, .04, .04, .06, 0)
    ctx.rectangle(0, 0, W, 110); ctx.set_source(g); ctx.fill()

def label_pill(ctx, s, x, y, a=1.0):
    ctx.select_font_face(MONO); ctx.set_font_size(13); w = ctx.text_extents(s).x_advance + 24
    col(ctx, '#11131b', .8 * a); ctx.rectangle(x - w / 2, y - 18, w, 26); ctx.fill()
    text(ctx, s, x, y, 13, FG, anchor='c', a=a)

def res_profile(d):
    wall = '#c9d6e3'
    pts = [(-70.7, 100, '#7fae5a'), (-20, 100, '#d9c7a6'), (-20, L5, '#6f9e4a'), (20, L5, '#d9c7a6'), (20, 100, '#7fae5a'), (70.7, 100, wall)]
    for (x, h) in arc_pts(70.7, 100)[1:]:
        pts.append((x, h, '#fff7df' if abs(x) < 22 and h > 140 else wall))
    return pts

# ---------------- scene L1: dawn in a home cell ----------------
def scene_dawn(ctx, t, dur):
    day = ease(seg(t, .5, dur - 1.5))
    haze = mixc('#1a1d2e', '#cfdde6', day); hazehex = '#%02x%02x%02x' % tuple(int(c * 255) for c in haze)
    light = lerp(.28, 1.0, day)
    cam = t * 6.0
    lit = 1 - day
    EYE['h'] = 106.0; EYE['x'] = -46.0
    def extras(ctx, dfar, dnear, fogk):
        if dnear > 1400: return
        # windows on both facades
        for side in (-1, 1):
            for fl in range(6, 30, 3):
                h = L5 + fl * 3.33
                p = proj(side * 20, h, dnear)
                sz = max(1.0, F * 1.4 / dnear)
                on = ((int(dnear * 7) + fl) % 3 != 0)
                rgb = mixc('#2a3a4a', '#ffd98a', lit if on else 0)
                setc(ctx, rgb, 1 - fogk); ctx.rectangle(p[0] - sz / 2 - side * sz, p[1] - sz, sz, sz * 1.2); ctx.fill()
        # trees in the canyon (fixed in the world, camera moves)
        for xt in (-12, 9, -62, -50, -32, -26, 30, 44, 58):
            wpos = dnear + cam + abs(xt) * 3
            if int(wpos / 22) % 2 == 0 and (wpos % 22) < (dfar - dnear + 1):
                rm = 4.0 if abs(xt) < 20 else 3.0
                p = proj(xt, (L5 + 5) if abs(xt) < 20 else 103, dnear); r = F * rm / dnear
                ctx.new_path(); setc(ctx, scale(hx('#4f7a3e'), light), 1 - fogk); ctx.arc(p[0], p[1], max(1, r), 0, 2 * math.pi); ctx.fill()
    render_tunnel(ctx, res_profile, hazehex, light, extras)
    EYE['h'] = 22.0; EYE['x'] = 0.0
    topband(ctx)
    header(ctx, '06:00')
    if t > 4: label_pill(ctx, 'the ground curves up into the sky ~2 km ahead', 640, 120, seg(t, 4, 5))
    caption(ctx, 'DAWN · LOOKING DOWN A HOME CELL', 'Louvres open over the window strip and daylight spills into the green canyon between the homes. Ahead, the land rises and disappears into the sky.')
    fade(ctx, t, dur)

# ---------------- cross-section helper ----------------
CXs, CYs, Rs = 640, 312, 270
PXs = Rs / TR
def cy_(h): return CYs + Rs - h * PXs
def cx_(x): return CXs + x * PXs
def xsec_base(ctx, sky='#16233a'):
    ctx.new_path(); ctx.save(); ctx.arc(CXs, CYs, Rs, 0, 2 * math.pi); ctx.clip()
    col(ctx, sky); ctx.paint()
    col(ctx, '#3a3530'); ctx.rectangle(0, cy_(L5), W, H); ctx.fill()
    col(ctx, '#6b6252', .7); ctx.set_line_width(1)
    for k in range(1, 4): y = cy_(k * 3.33); ctx.move_to(0, y); ctx.line_to(W, y); ctx.stroke()
def xsec_end(ctx):
    ctx.restore()
    ctx.new_path(); ctx.arc(CXs, CYs, Rs, math.radians(-107), math.radians(-73)); col(ctx, GLASS); ctx.set_line_width(9); ctx.stroke()
    ctx.new_path(); ctx.arc(CXs, CYs, Rs, 0, 2 * math.pi); col(ctx, GOLD); ctx.set_line_width(3); ctx.stroke()

def person(ctx, x, y, c='#ffffff', r=5):
    ctx.new_path(); col(ctx, c); ctx.arc(x, y - r * 2.2, r * .7, 0, 2 * math.pi); ctx.fill(); ctx.rectangle(x - r * .55, y - r * 1.5, r * 1.1, r * 1.5); ctx.fill()

def residence_xsec(ctx, lights=0.0):
    for side in (-1, 1):
        x0 = cx_(side * 20); x1 = cx_(side * 80)
        col(ctx, '#e6b85c'); ctx.rectangle(min(x0, x1), cy_(100), abs(x1 - x0), cy_(L5) - cy_(100)); ctx.fill()
        col(ctx, '#7fae5a'); ctx.rectangle(min(x0, x1), cy_(102), abs(x1 - x0), cy_(100) - cy_(102)); ctx.fill()
        col(ctx, '#0a0b10', .45); ctx.set_line_width(.8)
        for fl in range(1, 27):
            y = cy_(L5 + fl * 3.33); ctx.move_to(min(x0, x1), y); ctx.line_to(max(x0, x1), y); ctx.stroke()
        if lights > 0:
            for fl in range(26):
                for k in range(10):
                    x = cx_(side * (24 + k * 5)); y = cy_(L5 + fl * 3.33 + 1.6)
                    if (fl * 7 + k * 3 + side) % 4: col(ctx, SPARK, lights * .85); ctx.rectangle(x - 3, y - 3, 6, 5); ctx.fill()
    col(ctx, '#6f9e4a'); ctx.rectangle(cx_(-20), cy_(L5 + 1.5), 40 * PXs, 1.5 * PXs); ctx.fill()
    for xt in (-14, -5, 6, 15):
        col(ctx, '#4f7a3e'); ctx.arc(cx_(xt), cy_(L5 + 4.5), 10, 0, 2 * math.pi); ctx.fill()

def scene_home(ctx, t, dur):
    background(ctx)
    xsec_base(ctx, '#2c4a66')
    residence_xsec(ctx)
    # apartment highlight L18 on the left block
    ah = L5 + 13 * 3.33
    col(ctx, '#ffffff', .25 + .2 * math.sin(t * 3)); ctx.rectangle(cx_(-50), cy_(ah + 3.33), 28 * PXs, 3.33 * PXs); ctx.fill()
    # lift shaft near the canyon
    col(ctx, '#0a0b10', .5); ctx.rectangle(cx_(-24), cy_(100), 3 * PXs, cy_(2) - cy_(100)); ctx.fill()
    # train in the base
    tx = cx_(-90) + (seg(t, 5.2, 8) ** 2) * 900
    col(ctx, '#c9c5ba'); ctx.rectangle(tx, cy_(5.5), 160, 3.0 * PXs); ctx.fill()
    col(ctx, '#66c2d4'); ctx.rectangle(tx + 6, cy_(5.0), 148, 5); ctx.fill()
    # person path: apartment -> lift -> down -> platform
    if t < 1.8: px = lerp(cx_(-40), cx_(-22.5), ease(seg(t, .4, 1.8))); py = cy_(ah)
    elif t < 4.2: px = cx_(-22.5); py = lerp(cy_(ah), cy_(3.4), ease(seg(t, 1.8, 4.2)))
    else: px = lerp(cx_(-22.5), cx_(-10), ease(seg(t, 4.2, 5))); py = cy_(3.4)
    if t < 5.4: person(ctx, px, py, '#ffffff', 6)
    xsec_end(ctx)
    text(ctx, 'LEVEL 18 · HOME', cx_(-50) - 10, cy_(ah + 5), 13, FG, anchor='r')
    text(ctx, 'LIFT', cx_(-24) + 14, cy_(60), 12, MUT)
    text(ctx, 'DISTRICT TRAIN · BASE', cx_(70) + 34, cy_(4), 12, CY)
    header(ctx, '07:30')
    caption(ctx, 'MORNING · FROM HOME TO THE TRAIN', 'A level-18 apartment looks out over the canyon. The lift drops past the roof gardens and the homes below to the district train in the hardware base.')
    fade(ctx, t, dur)

# ---------------- scene L3: commute and the gravity gauge ----------------
def gauge(ctx, x, y, g, label='YOU WEIGH'):
    col(ctx, '#11131b', .9); ctx.rectangle(x, y, 300, 120); ctx.fill(); col(ctx, '#2c2a24'); ctx.set_line_width(1); ctx.rectangle(x + .5, y + .5, 299, 119); ctx.stroke()
    text(ctx, label, x + 16, y + 28, 12, MUT, spacing=1)
    text(ctx, f'{g:.2f} g', x + 16, y + 76, 40, GOLD, bold=True)
    col(ctx, '#2c2a24'); ctx.rectangle(x + 16, y + 94, 268, 8); ctx.fill()
    col(ctx, GOLD); ctx.rectangle(x + 16, y + 94, 268 * clamp(g / 1.5), 8); ctx.fill()
    col(ctx, FG); ctx.rectangle(x + 16 + 268 / 1.5 - 1, y + 90, 2, 16); ctx.fill()

def scene_commute(ctx, t, dur):
    background(ctx)
    v = 70 * ease(seg(t, .8, 4.5))
    off = sum(1 for _ in [0]) and (t * t * 40 if t < 4.5 else 4.5 * 4.5 * 40 + (t - 4.5) * 360)
    col(ctx, '#2a2620'); ctx.rectangle(0, 180, W, 300); ctx.fill()
    col(ctx, '#3a3530'); ctx.rectangle(0, 180, W, 30); ctx.fill(); ctx.rectangle(0, 450, W, 30); ctx.fill()
    for k in range(-1, 12):
        x = (k * 140 - off) % (W + 140) - 70
        col(ctx, '#4a4436'); ctx.rectangle(x, 210, 18, 240); ctx.fill()
        col(ctx, '#ffd98a', .8); ctx.rectangle(x - 30, 222, 40, 4); ctx.fill()
    col(ctx, '#66c2d4', .5); ctx.rectangle(0, 418, W, 4); ctx.fill()
    for c in range(3):
        x = 260 + c * 250
        col(ctx, '#d6d2c8'); ctx.rectangle(x, 300, 236, 112); ctx.fill()
        col(ctx, '#1d3b42'); ctx.rectangle(x + 14, 318, 208, 40); ctx.fill()
        for p in range(5): person(ctx, x + 40 + p * 38, 356, '#e6b85c', 5)
        col(ctx, CY); ctx.rectangle(x, 400, 236, 8); ctx.fill()
    g = ((412 + v / 3.6) / 412) ** 2
    gauge(ctx, 900, 90, g)
    text(ctx, f'{v:4.0f} km/h SPINWARD', 1200, 250, 16, FG, anchor='r', bold=True)
    if t > 5: text(ctx, 'at 300 km/h it would be 1.44 g', 1200, 276, 13, MUT, anchor='r', a=seg(t, 5, 5.6))
    header(ctx, '07:45')
    caption(ctx, 'COMMUTE · WHY THE TRAINS ARE SLOW', 'Riding with the spin adds to your speed around the ring, so you feel heavier; riding against it, lighter. At 70 km/h it is about 10% either way, so trains stay slow.')
    fade(ctx, t, dur)

# ---------------- scene L4: spoke elevator to low gravity ----------------
def scene_spoke(ctx, t, dur):
    background(ctx)
    u = ease(seg(t, 1, dur - 2))
    x = 520
    col(ctx, '#4a4232'); ctx.rectangle(x - 10, 100, 20, 470); ctx.fill()
    col(ctx, GOLD); ctx.set_line_width(3); ctx.move_to(x - 10, 100); ctx.line_to(x - 10, 570); ctx.move_to(x + 10, 100); ctx.line_to(x + 10, 570); ctx.stroke()
    col(ctx, '#e07a5f', .5)
    for k in range(10):
        y = 130 + k * 44; ctx.rectangle(x + 16, y, 90, 30); ctx.fill(); ctx.rectangle(x - 106, y, 90, 30); ctx.fill()
    text(ctx, 'RADIATOR FINS', x + 120, 300, 12, '#e07a5f')
    ctx.new_path(); col(ctx, '#11131b'); ctx.arc(x, 90, 46, 0, 2 * math.pi); ctx.fill_preserve(); col(ctx, CY); ctx.set_line_width(3); ctx.stroke()
    text(ctx, 'HUB', x, 95, 13, CY, anchor='c', bold=True)
    col(ctx, '#2a2416'); ctx.rectangle(x - 300, 560, 600, 40); ctx.fill(); col(ctx, GOLD); ctx.rectangle(x - 300, 560, 600, 3); ctx.fill()
    text(ctx, 'RESEARCH CELL', x - 290, 590, 12, '#9fb7e8')
    ey = lerp(548, 140, u)
    col(ctx, '#ffffff'); ctx.rectangle(x - 9, ey - 14, 18, 28); ctx.fill()
    for i in range(3):
        a = t * 1.5 + i * 2.1
        person(ctx, x + 80 + i * 40 + 6 * math.sin(a), 70 + 10 * math.cos(a * 1.3), '#9fb7e8', 5)
    if u > .97: text(ctx, 'MICROGRAVITY LABS', x + 80, 120, 12, '#9fb7e8', a=seg(t, dur - 2, dur - 1.4))
    km = 17.35 * u
    gauge(ctx, 880, 120, max(0.0, 1 - km / 17.35), 'GRAVITY HERE')
    text(ctx, f'{km:5.1f} km up the spoke', 1180, 290, 16, FG, anchor='r', bold=True)
    text(ctx, 'half a g at the halfway mark', 1180, 316, 13, MUT, anchor='r', a=seg(u, .45, .55))
    header(ctx, '09:00')
    caption(ctx, 'WORK · A LAB WITH ALMOST NO GRAVITY', 'Researchers ride an elevator 17 km up a spoke. Gravity fades with every kilometre: half a g halfway up, almost none at the hub, home of the microgravity labs.')
    fade(ctx, t, dur)

# ---------------- scene L5: farm cell ----------------
def scene_farm(ctx, t, dur):
    background(ctx)
    xsec_base(ctx, '#2c4a66')
    for i in range(9):
        h = L5 + 5 * i
        col(ctx, '#5b4630'); ctx.rectangle(0, cy_(h + 1.2), W, 1.2 * PXs); ctx.fill()
        grow = 1.4 + .9 * (.5 + .5 * math.sin(t * 1.2 + i * .9))
        col(ctx, '#7fbf5a'); ctx.rectangle(0, cy_(h + 1.2 + grow), W, grow * PXs); ctx.fill()
        col(ctx, '#e8d0ff' if i < 7 else '#ffe29a', .18); ctx.rectangle(0, cy_(h + 5), W, (5 - 1.2 - grow) * PXs); ctx.fill()
    top = L5 + 45
    col(ctx, '#5b4630'); ctx.rectangle(0, cy_(top + 2), W, 2 * PXs); ctx.fill()
    for xt in range(-55, 60, 14):
        col(ctx, '#8a6a3a'); ctx.rectangle(cx_(xt) - 2, cy_(top + 9), 4, 7 * PXs); ctx.fill()
        col(ctx, '#4f8a3a'); ctx.arc(cx_(xt), cy_(top + 10), 13, 0, 2 * math.pi); ctx.fill()
        col(ctx, '#e07a5f'); ctx.arc(cx_(xt) + 5, cy_(top + 9), 2.5, 0, 2 * math.pi); ctx.fill()
    for xl in (-40, 0, 40):
        col(ctx, '#ffe29a', .35 + .15 * math.sin(t * 4 + xl)); ctx.rectangle(cx_(xl) - 2, cy_(147), 4, cy_(top + 2) - cy_(147)); ctx.fill()
    for i in (1, 4, 6):
        rx = cx_(-60) + ((t * 60 + i * 300) % 900)
        col(ctx, CY); ctx.rectangle(rx, cy_(L5 + 5 * i + 3.3), 20, 10); ctx.fill()
    xsec_end(ctx)
    text(ctx, 'ORCHARD UNDER DAYLIGHT', cx_(62) + 40, cy_(top + 10), 12, '#7fbf5a')
    text(ctx, '9 GROWING TIERS', cx_(66) + 30, cy_(L5 + 22), 12, '#7fbf5a')
    text(ctx, 'LIGHT PIPES', cx_(40) + 20, cy_(100), 12, '#ffe29a')
    header(ctx, '12:00')
    caption(ctx, 'NOON · THE FARM CELLS', 'Nine tiers of crops under light pipes and LEDs, worked by harvest robots. On top, an orchard grows in deep soil under real daylight. One farm cell feeds about 4,500 people.')
    fade(ctx, t, dur)

# ---------------- scene L6: waterfront perspective ----------------
def water_profile(d):
    pts = []
    k = .9 + .5 * math.sin(d / 160)
    xs = [x for x in range(-74, 75, 4)]
    for x in xs:
        base = TR - math.sqrt(max(0, TR * TR - x * x))
        hill = L5 + (0 if abs(x) < 30 else (abs(x) - 30) * (0.5 if abs(x) < 36 else k * 1.6))
        h = max(hill, base)
        c = '#3f8fbf' if abs(x) < 30 else ('#e8d6a6' if abs(x) < 36 else ('#4f7a3e' if h < 60 else '#5f8a4a'))
        pts.append((x, h, c))
    ex, eh = pts[-1][0], pts[-1][1]
    for (x, h) in arc_pts(ex, eh)[1:]:
        pts.append((x, h, '#fff7df' if abs(x) < 22 and h > 140 else '#c9d6e3'))
    return pts

def scene_water(ctx, t, dur):
    light = 1.0
    cam = t * 5
    def extras(ctx, dfar, dnear, fogk):
        if dnear > 1200: return
        wpos = dnear + cam
        if (wpos % 35) < (dfar - dnear + 1):
            for side in (-1, 1):
                x = side * (44 + 10 * math.sin(wpos))
                base = TR - math.sqrt(max(0, TR * TR - x * x))
                h = max(L5 + 4 + (abs(x) - 36) * 1.3, base) + 9
                p = proj(x, h, dnear); r = max(1, F * 5 / dnear)
                ctx.new_path(); setc(ctx, hx('#2f5226'), 1 - fogk); ctx.arc(p[0], p[1], r, 0, 2 * math.pi); ctx.fill()
        if int(wpos / 60) % 3 == 0 and (wpos % 60) < (dfar - dnear + 1) and dnear < 500:
            p = proj(33 * (1 if int(wpos) % 2 else -1), L5 + 3, dnear)
            ctx.new_path(); setc(ctx, hx('#e07a5f')); ctx.arc(p[0], p[1] - F * 1.2 / dnear, max(1, F * .7 / dnear), 0, 2 * math.pi); ctx.fill()
        if dnear < 600:
            p = proj(math.sin(wpos * 3) * 25, L5 + .2, dnear)
            setc(ctx, (1, 1, 1), .5 * (1 - fogk)); ctx.rectangle(p[0], p[1], max(1, 8 * 30 / dnear), 1); ctx.fill()
    render_tunnel(ctx, water_profile, '#e9dcc4', light, extras)
    col(ctx, '#ffb070', .10); ctx.paint()
    topband(ctx)
    header(ctx, '17:00')
    caption(ctx, 'AFTERNOON · THE WATERFRONT', 'A swimming lake with sand beaches and wooded hills climbing the walls. The far shore rises into the sky: a landscape that wraps over your head.')
    fade(ctx, t, dur)

# ---------------- scene L7: food and night ----------------
def scene_night(ctx, t, dur):
    background(ctx)
    xsec_base(ctx, '#0f1626')
    for a, b, hh in ((-80, -50, 40), (-50, -25, 25), (25, 50, 25), (50, 80, 40)):
        col(ctx, '#7a3f30'); ctx.rectangle(cx_(a), cy_(L5 + hh), (b - a) * PXs, hh * PXs); ctx.fill()
        for fl in range(int(hh / 3.33)):
            for k in range(int((b - a) / 5)):
                if (fl + k + int(t * 2)) % 5:
                    col(ctx, SPARK, .55 + .35 * math.sin(t * 3 + fl * 1.7 + k)); ctx.rectangle(cx_(a + 2 + k * 5), cy_(L5 + fl * 3.33 + 2.5), 8, 6); ctx.fill()
    col(ctx, '#3a3530'); ctx.rectangle(cx_(-25), cy_(L5 + 1.5), 50 * PXs, 1.5 * PXs); ctx.fill()
    for i in range(26):
        xx = -24 + i * 1.9
        y = cy_(L5 + 18 + 3 * math.sin(i * .5))
        on = .5 + .5 * math.sin(t * 5 + i)
        col(ctx, ['#ffe29a', '#e07a5f', '#66c2d4'][i % 3], .5 + .5 * on); ctx.arc(cx_(xx), y, 3.5, 0, 2 * math.pi); ctx.fill()
    for i in range(40):
        xx = -22 + (i * 37 % 44); bob = abs(math.sin(t * 6 + i)) * 4
        person(ctx, cx_(xx), cy_(L5 + 1.5) - bob, ['#e6b85c', '#9fb7e8', '#d8a0b8', '#7fbf5a'][i % 4], 4.5)
    col(ctx, '#c9c5ba'); ctx.rectangle(cx_(-8), cy_(L5 + 5), 16 * PXs, 3.5 * PXs); ctx.fill()
    xsec_end(ctx)
    text(ctx, 'FOOD HALLS · BARS · CLUBS', cx_(-65), cy_(L5 + 46), 12, '#e07a5f', anchor='c')
    text(ctx, 'CONCERT PLAZA', cx_(0), cy_(L5 + 26), 12, SPARK, anchor='c')
    header(ctx, '21:00')
    caption(ctx, 'EVENING · FOOD AND NIGHT', 'Louvres close, the sky inside goes dark, and the food-and-night cells fill up: food halls, rooftop bars and a concert in the plaza under strings of lights.')
    fade(ctx, t, dur)

# ---------------- scene L8: life support while you sleep ----------------
random.seed(5)
PARTS = [(random.uniform(0, 1), random.uniform(-1, 1)) for _ in range(120)]
def scene_support(ctx, t, dur):
    background(ctx)
    xsec_base(ctx, '#0f1626')
    residence_xsec(ctx, lights=.25)
    col(ctx, '#0a0b10', .45); ctx.rectangle(0, 0, W, H); ctx.fill()
    col(ctx, GLASS, .35); ctx.rectangle(0, cy_(150), W, cy_(143) - cy_(150)); ctx.fill()
    # air up the canyon, back down beside the hull
    for i, (ph, lat) in enumerate(PARTS):
        u = (ph + t * .18) % 1.0
        if i % 2 == 0:
            x = cx_(lat * 16); h = lerp(L5, 140, u)
            c = '#66c2d4'
        else:
            side = 1 if lat > 0 else -1
            ang = lerp(math.pi / 2 * .62, -math.pi / 2 * .9, u)
            x = cx_(side * (TR - 4) * math.cos(ang)); h = TR + (TR - 4) * math.sin(ang)
            c = '#9fb7e8'
        col(ctx, c, .85); ctx.arc(x, cy_(h), 3, 0, 2 * math.pi); ctx.fill()
    for k in range(14):
        u = (k / 14 + t * .4) % 1.0
        col(ctx, '#5aa6d6'); ctx.arc(cx_(-70 + k * 10.5), cy_(lerp(L5 - .5, 2, u)), 2.5, 0, 2 * math.pi); ctx.fill()
    xsec_end(ctx)
    text(ctx, 'FRESH AIR RISES FROM THE BASE', cx_(0), cy_(60), 13, CY, anchor='c', bold=True)
    text(ctx, 'RETURNS UNDER THE WINDOW STRIP', cx_(0), cy_(132), 12, GLASS, anchor='c')
    text(ctx, 'DOWN THE WALLS TO THE PLANT', cx_(78) + 10, cy_(70), 12, '#9fb7e8')
    text(ctx, 'CONDENSATE + WASTEWATER → RECOVERY', cx_(0), cy_(0) + 26, 12, '#5aa6d6', anchor='c')
    header(ctx, '02:00')
    caption(ctx, 'NIGHT · WHILE YOU SLEEP', 'Air flows up through every cell and back to the base, where plants and the district plant restore its oxygen. Water from sweat, showers and crops is condensed, cleaned and reused.')
    fade(ctx, t, dur)

# ---------------- scene L9: the ring from outside ----------------
def scene_outside(ctx, t, dur):
    col(ctx, '#05060a'); ctx.paint()
    for x, y, r, a in [(random.uniform(0, W), random.uniform(0, H), random.uniform(.4, 1.3), random.uniform(.2, .9)) for _ in range(0)]: pass
    background(ctx)
    g = cairo.RadialGradient(60, 400, 10, -40, 470, 330); g.add_color_stop_rgba(0, .55, .75, .95, 1); g.add_color_stop_rgba(.6, .2, .45, .7, 1); g.add_color_stop_rgba(1, .05, .1, .2, 1)
    ctx.new_path(); ctx.arc(-40, 470, 330, 0, 2 * math.pi); ctx.set_source(g); ctx.fill()
    ctx.new_path(); col(ctx, '#c9c5ba'); ctx.arc(1150, 150, 34, 0, 2 * math.pi); ctx.fill()
    text(ctx, 'EARTH', 120, 230, 12, MUT); text(ctx, 'MOON', 1150, 210, 12, MUT, anchor='c')
    cx, cy, r = 700, 320, 220
    rot = t * 360 / 264 * 6
    ctx.new_path(); ctx.save(); ctx.translate(cx, cy); ctx.rotate(math.radians(rot))
    col(ctx, '#3a3530'); ctx.set_line_width(26); ctx.arc(0, 0, r, 0, 2 * math.pi); ctx.stroke()
    ctx.new_path(); col(ctx, '#ffd98a', .9); ctx.set_line_width(4); ctx.set_dash([10, 7]); ctx.arc(0, 0, r, 0, 2 * math.pi); ctx.stroke(); ctx.set_dash([])
    for i in range(6):
        a = math.radians(i * 60)
        col(ctx, GOLD); ctx.set_line_width(3); ctx.move_to(22 * math.cos(a), 22 * math.sin(a)); ctx.line_to((r - 14) * math.cos(a), (r - 14) * math.sin(a)); ctx.stroke()
        col(ctx, '#e07a5f', .45); ctx.set_line_width(10); ctx.move_to(60 * math.cos(a), 60 * math.sin(a)); ctx.line_to((r - 50) * math.cos(a), (r - 50) * math.sin(a)); ctx.stroke()
    ctx.restore()
    col(ctx, '#20335a'); ctx.rectangle(cx - 70, cy - 8, 140, 16); ctx.fill(); col(ctx, '#6d8fd6'); ctx.set_line_width(1); ctx.rectangle(cx - 70, cy - 8, 140, 16); ctx.stroke()
    ctx.new_path(); col(ctx, '#11131b'); ctx.arc(cx, cy, 20, 0, 2 * math.pi); ctx.fill_preserve(); col(ctx, CY); ctx.set_line_width(2); ctx.stroke()
    text(ctx, 'speeded up · one real turn takes 4.4 minutes', cx, cy + r + 46, 12, MUT, anchor='c')
    header(ctx, '')
    caption(ctx, 'THE RING · BETWEEN EARTH AND THE MOON', 'About 550,000 people, a third of the ring given to forests, lakes, food and play. From outside, only the lit window strips show.')
    fade(ctx, t, dur, fo=1.0)

SCENES = [('l1', scene_dawn, 10), ('l2', scene_home, 8), ('l3', scene_commute, 8), ('l4', scene_spoke, 9),
          ('l5', scene_farm, 8), ('l6', scene_water, 9), ('l7', scene_night, 8), ('l8', scene_support, 9), ('l9', scene_outside, 8)]

def render(name, fn, dur):
    tmp = os.path.join(OUT, f'{name}.tmp.mp4'); fin = os.path.join(OUT, f'{name}.mp4')
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for i in range(int(round(dur * FPS))):
        ctx = cairo.Context(surf); fn(ctx, i / FPS, dur); surf.flush(); p.stdin.write(bytes(surf.get_data()))
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, fin)
    else: sys.exit(name + ' failed')

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for name, fn, dur in SCENES:
            surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
            fn(ctx, float(sys.argv[2]) * dur, dur); surf.write_to_png(os.path.join(OUT, f'lst_{name}.png'))
    else:
        for name, fn, dur in SCENES:
            if sys.argv[1] in ('all', name): render(name, fn, dur)
