"""A day on the ring, v2: terrace homes where every home is a top floor,
and Roadsters that climb the end walls of each block."""
import cairo, math, random, os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import life
from life import (W, H, FPS, hx, col, text, wrap, background, ease, seg, clamp, lerp,
                  FG, MUT, GOLD, CY, GLASS, SPARK, MONO, SANS, TR, L5, F,
                  mixc, setc, scale, caption, fade, proj, arc_pts, render_tunnel, topband, label_pill,
                  EYE, cx_, cy_, PXs, xsec_base, xsec_end, person, gauge)

def header(ctx, clock):
    text(ctx, 'A DAY ON THE RING', 40, 44, 15, MUT, spacing=3)
    text(ctx, 'CISLUNAR SETTLEMENT · TERRACE HOMES', 40, 66, 12, '#6b6252', spacing=2)
    if clock: text(ctx, clock, 1240, 56, 30, FG, anchor='r', bold=True)
life.header = header

# ---------- terrace geometry (cross-section, metres) ----------
CANYON = 10.0; TREAD = 6.0; RISE = 8.7; NSTEP = 10
def step_h(i): return L5 + RISE * (i + 1)          # terrace height of step i
def step_x(i): return CANYON + TREAD * i           # riser position of step i (inner edge)
TOPH = step_h(NSTEP - 1); TOPX = step_x(NSTEP)

ROADSTER = '#d0302b'

def terrace_profile(d):
    wall = '#c9d6e3'; pts = []
    pts.append((-TOPX, TOPH, '#7fae5a'))
    for i in range(NSTEP - 1, -1, -1):
        pts.append((-step_x(i), step_h(i), '#b9c9d6'))            # riser (glass front) going down
        lower = step_h(i - 1) if i > 0 else L5
        pts.append((-step_x(i), lower, '#7fae5a' if i > 0 else '#6f9e4a'))
    pts[-1] = (-CANYON, L5, '#6f9e4a')
    pts.append((CANYON, L5, '#b9c9d6'))
    for i in range(NSTEP):
        pts.append((step_x(i), step_h(i), '#7fae5a'))
        if i < NSTEP - 1: pts.append((step_x(i + 1), step_h(i), '#b9c9d6'))
    pts.append((TOPX, TOPH, wall))
    for (x, h) in arc_pts(TOPX, TOPH)[1:]:
        pts.append((x, h, '#fff7df' if abs(x) < 22 and h > 140 else wall))
    return pts

BLOCK = 180.0; GAP = 14.0

def block_face(ctx, d, side, light, fogk, lit):
    """Stepped end face of a block (the trapezoid), with its climb lane."""
    pts = [(side * CANYON, L5)]
    for i in range(NSTEP):
        pts.append((side * step_x(i), step_h(i)))
        pts.append((side * step_x(i + 1), step_h(i)))
    pts.append((side * TOPX, L5))
    sp = [proj(x, h, d) for x, h in pts]
    ctx.new_path(); ctx.move_to(*sp[0])
    for p in sp[1:]: ctx.line_to(*p)
    ctx.close_path()
    face = tuple(lerp(c, h_, fogk * .85) for c, h_ in zip(scale(hx('#cdb88f'), light), hx('#cfdde6')))
    setc(ctx, face); ctx.fill()
    # climb lane: a vertical strip on the face near the canyon edge, full height
    x0 = side * (CANYON + 2); x1 = side * (CANYON + 4.5)
    a, b = proj(x0, L5, d), proj(x1, L5, d); c, e = proj(x1, step_h(NSTEP - 1), d), proj(x0, step_h(NSTEP - 1), d)
    ctx.move_to(*a); ctx.line_to(*b); ctx.line_to(*c); ctx.line_to(*e); ctx.close_path()
    setc(ctx, scale(hx('#6a7280'), light), 1 - fogk); ctx.fill()
    # level marks on the lane
    for i in range(NSTEP):
        p = proj(side * (CANYON + 3.2), step_h(i), d); s = max(1, F * .5 / d)
        setc(ctx, hx('#ffd98a'), (1 - fogk) * (.4 + .6 * lit)); ctx.rectangle(p[0] - s, p[1] - s / 2, 2 * s, s); ctx.fill()

def roadster_persp(ctx, x, h, d, fogk, a=1.0):
    p = proj(x, h + .6, d); w = max(1.2, F * 2.0 / d); hh = max(.8, F * 1.0 / d)
    setc(ctx, hx(ROADSTER), (1 - fogk) * a); ctx.rectangle(p[0] - w / 2, p[1] - hh, w, hh); ctx.fill()

# ---------- scene 1: dawn over a terrace valley ----------
def scene_dawn(ctx, t, dur):
    day = ease(seg(t, .5, dur - 2))
    haze = mixc('#1a1d2e', '#cfdde6', day); hazehex = '#%02x%02x%02x' % tuple(int(c * 255) for c in haze)
    light = lerp(.3, 1.0, day); lit = 1 - day
    cam = t * 7.0
    EYE['h'] = 52.0; EYE['x'] = 0.0
    climber_d = 260 - t * 0  # a car climbing the lane of the block ahead
    def extras(ctx, dfar, dnear, fogk):
        if dnear > 1500: return
        span = dfar - dnear + 1
        # windows on risers
        for side in (-1, 1):
            for i in range(NSTEP):
                if (int(dnear * 3) + i) % 2: continue
                p = proj(side * step_x(i), step_h(i) - RISE * .45, dnear)
                sz = max(1.0, F * 1.6 / dnear)
                rgb = mixc('#5d7488', '#ffd98a', lit * (1 if (i + int(dnear)) % 3 else .2))
                setc(ctx, rgb, 1 - fogk); ctx.rectangle(p[0] - sz / 2, p[1] - sz * .6, sz, sz * 1.1); ctx.fill()
        # world-fixed props: trees and parked Roadsters on terraces, people in the canyon
        wpos = dnear + cam
        for side in (-1, 1):
            for i in range(0, NSTEP, 1):
                key = wpos + i * 17 + (side + 1) * 31
                if (key % 26) < span:
                    xt = side * (step_x(i) + TREAD * .7); p = proj(xt, step_h(i) + 3.2, dnear); r = F * 2.2 / dnear
                    ctx.new_path(); setc(ctx, scale(hx('#4f7a3e'), light), 1 - fogk); ctx.arc(p[0], p[1], max(1, r), 0, 2 * math.pi); ctx.fill()
                if ((key + 9) % 41) < span:
                    roadster_persp(ctx, side * (step_x(i) + TREAD * .35), step_h(i), dnear, fogk)
        if (wpos % 9) < span and dnear < 700:
            for k in range(2):
                xp = -6 + 12 * ((wpos * .37 + k * .5 + t * .05) % 1)
                p = proj(xp, L5, dnear); s = max(1, F * 1.7 / dnear)
                setc(ctx, hx('#2a2416'), 1 - fogk); ctx.rectangle(p[0] - s * .25, p[1] - s, s * .5, s); ctx.fill()
        # block end faces (the trapezoids) every block, fixed in the world
        bpos = (dnear + cam) % (BLOCK + GAP)
        if bpos < span:
            for side in (-1, 1): block_face(ctx, dnear, side, light, fogk, lit)
            # a Roadster partway up the climb lane on the right face
            if dnear < 900:
                hc = L5 + (step_h(8) - L5) * ((t * .12 + dnear * .001) % 1)
                p = proj(CANYON + 3.2, hc, dnear); w = max(1, F * 1.0 / dnear); hh = max(1.5, F * 2.2 / dnear)
                setc(ctx, hx(ROADSTER), 1 - fogk); ctx.rectangle(p[0] - w / 2, p[1] - hh, w, hh); ctx.fill()
    render_tunnel(ctx, terrace_profile, hazehex, light, extras)
    EYE['h'] = 22.0; EYE['x'] = 0.0
    topband(ctx)
    header(ctx, '06:00')
    if t > 3.5: label_pill(ctx, 'every home has its own terrace: a top floor for everyone', 640, 124, seg(t, 3.5, 4.5))
    if t > 6.5: label_pill(ctx, 'end walls of each block are climb lanes for cars', 640, 156, seg(t, 6.5, 7.5))
    caption(ctx, 'DAWN · THE TERRACE VALLEY', 'Homes step back from a green canyon like a valley of terraces, so every one has open sky and its own garden. Ahead, the valley curves up into the sky.')
    fade(ctx, t, dur)

# ---------- terrace cell cross-section ----------
def terrace_xsec(ctx, lights=0.0, t=0.0, mine=None, cars=True):
    for side in (-1, 1):
        # building mass between the steps and the hull
        pts = [(cx_(side * CANYON), cy_(L5))]
        for i in range(NSTEP):
            pts.append((cx_(side * step_x(i)), cy_(step_h(i))))
            pts.append((cx_(side * step_x(i + 1)), cy_(step_h(i))))
        pts.append((cx_(side * 80), cy_(step_h(NSTEP - 1))))
        pts.append((cx_(side * 80), cy_(0)))
        ctx.new_path(); ctx.move_to(*pts[0])
        for p in pts[1:]: ctx.line_to(*p)
        ctx.line_to(cx_(side * CANYON), cy_(0)); ctx.close_path()
        col(ctx, '#d9c7a6'); ctx.fill()
        for i in range(NSTEP):
            xr = side * step_x(i); hb = step_h(i - 1) if i else L5; ht = step_h(i)
            # glass front (riser)
            x0 = cx_(xr) - (0 if side > 0 else 3);
            col(ctx, '#7fa8c4'); ctx.rectangle(cx_(xr) - 2.5, cy_(ht), 5, cy_(hb) - cy_(ht)); ctx.fill()
            # home outline behind the front: a duplex reaching back under the next step
            col(ctx, '#0a0b10', .35); ctx.set_line_width(1)
            ctx.move_to(cx_(xr), cy_(hb)); ctx.line_to(cx_(side * (step_x(i) + TREAD * 2.2)), cy_(hb)); ctx.stroke()
            ctx.move_to(cx_(xr), cy_((hb + ht) / 2)); ctx.line_to(cx_(side * (step_x(i) + TREAD * 2.2)), cy_((hb + ht) / 2)); ctx.stroke()
            # terrace garden
            col(ctx, '#7fae5a'); ctx.rectangle(min(cx_(xr), cx_(side * step_x(i + 1))), cy_(ht + .9), TREAD * PXs, .9 * PXs); ctx.fill()
            if lights > 0:
                for k in range(3):
                    col(ctx, SPARK, lights * (.6 + .4 * math.sin(t * 2 + i + k + side)))
                    ctx.rectangle(cx_(xr) - 2, cy_(hb + 1.5 + k * 2.4), 4, 3); ctx.fill()
            if cars and (i + (side > 0)) % 2 == 0:
                cxp = cx_(side * (step_x(i) + TREAD * .6))
                col(ctx, ROADSTER); ctx.rectangle(cxp - 9, cy_(ht + .9) - 7, 18, 6); ctx.fill()
                col(ctx, '#1a1a1a'); ctx.rectangle(cxp - 5, cy_(ht + .9) - 10, 9, 3); ctx.fill()
            else:
                ctx.new_path(); col(ctx, '#4f7a3e'); ctx.arc(cx_(side * (step_x(i) + TREAD * .55)), cy_(ht + 3.5), 8, 0, 2 * math.pi); ctx.fill()
        # climb lane drawn as a dashed vertical line at the block end (seen edge-on)
        col(ctx, '#ffd98a', .7); ctx.set_line_width(2); ctx.set_dash([4, 4])
        ctx.move_to(cx_(side * (CANYON + 3.2)), cy_(L5)); ctx.line_to(cx_(side * (CANYON + 3.2)), cy_(TOPH)); ctx.stroke(); ctx.set_dash([])
    col(ctx, '#6f9e4a'); ctx.rectangle(cx_(-CANYON), cy_(L5 + 1), 2 * CANYON * PXs, PXs); ctx.fill()
    if mine is not None:
        side, i = mine
        hb = step_h(i - 1) if i else L5
        col(ctx, '#ffffff', .25 + .2 * math.sin(t * 3))
        ctx.rectangle(min(cx_(side * step_x(i)), cx_(side * (step_x(i) + TREAD * 2.2))), cy_(step_h(i) + .9), TREAD * 2.2 * PXs, cy_(hb) - cy_(step_h(i) + .9)); ctx.fill()

def scene_home(ctx, t, dur):
    background(ctx)
    xsec_base(ctx, '#3a5f80')
    terrace_xsec(ctx, t=t, mine=(-1, 6))
    xsec_end(ctx)
    hx_, hy = cx_(-(step_x(6) + TREAD * 1.1)), cy_(step_h(6))
    col(ctx, FG, .7); ctx.set_line_width(1); ctx.move_to(hx_, hy - 8); ctx.line_to(250, 210); ctx.stroke()
    text(ctx, 'YOUR HOME', 240, 200, 14, FG, anchor='r', bold=True)
    text(ctx, 'duplex + 6 m terrace + car pad', 240, 220, 12, MUT, anchor='r')
    text(ctx, 'STEPPED "TRAPEZOID" BLOCKS', 1040, 160, 13, GOLD, bold=True)
    text(ctx, '10 terraces per side, 8.7 m apart', 1040, 180, 12, MUT)
    text(ctx, 'nothing above you but sky', 1040, 198, 12, MUT)
    text(ctx, 'CLIMB LANE', cx_(CANYON + 3.2) + 14, cy_(60), 12, '#ffd98a')
    text(ctx, 'CANYON STREET', cx_(0), cy_(L5) + 22, 11, '#a7c88a', anchor='c')
    header(ctx, '07:00')
    caption(ctx, 'MORNING · EVERYONE LIVES ON A TOP FLOOR', 'The blocks step back like a trapezoid, so each home is a two-storey flat with its own terrace and car pad, and nothing above it but sky.')
    fade(ctx, t, dur)

# ---------- scene 3: a Roadster climbs home ----------
def roadster_side(ctx, x, y, ang, scale_=1.0, thrust=0.0, fans=False):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(scale_, scale_)
    if thrust > 0:
        for k in range(5):
            ctx.new_path(); col(ctx, '#e8eef2', thrust * (.5 - k * .08)); ctx.arc(-6 + k * 3, 10 + k * 7, 5 + k * 3, 0, 2 * math.pi); ctx.fill()
    col(ctx, ROADSTER); ctx.move_to(-22, 0); ctx.line_to(-20, -7); ctx.line_to(-6, -9); ctx.line_to(4, -14); ctx.line_to(14, -13); ctx.line_to(22, -6); ctx.line_to(23, 0); ctx.close_path(); ctx.fill()
    col(ctx, '#1d2a35'); ctx.move_to(-4, -9); ctx.line_to(5, -13); ctx.line_to(13, -12); ctx.line_to(16, -8); ctx.close_path(); ctx.fill()
    for wx in (-13, 14):
        ctx.new_path(); col(ctx, '#111111'); ctx.arc(wx, 0, 4.5, 0, 2 * math.pi); ctx.fill(); col(ctx, '#888888'); ctx.arc(wx, 0, 1.8, 0, 2 * math.pi); ctx.fill()
    if fans:
        col(ctx, '#66c2d4', .8); ctx.rectangle(-8, 1, 16, 2.5); ctx.fill()
    ctx.restore()

def scene_climb(ctx, t, dur):
    background(ctx)
    # elevation: looking across the canyon at one terrace block; ground y=560, 5 px per m along, 4.6 px per m up
    gy = 560; PXH = 4.4; X0, X1 = 110, 1010; LANE = 1052
    col(ctx, '#2c4a66'); ctx.rectangle(0, 80, W, gy - 80); ctx.fill()
    col(ctx, '#fff7df', .5); ctx.rectangle(0, 80, W, 6); ctx.fill()
    for i in range(NSTEP):
        hb = (step_h(i - 1) if i else L5) - L5; ht = step_h(i) - L5
        yb, yt = gy - hb * PXH, gy - ht * PXH
        col(ctx, '#d9c7a6'); ctx.rectangle(X0, yt, X1 - X0, yb - yt); ctx.fill()
        for k in range(18):
            xw = X0 + 10 + k * 50
            lit = .5 + .5 * math.sin(k * 1.7 + i)
            col(ctx, '#7fa8c4'); ctx.rectangle(xw, yt + 10, 34, yb - yt - 16); ctx.fill()
            col(ctx, '#ffd98a', .15 + .15 * lit); ctx.rectangle(xw, yt + 10, 34, yb - yt - 16); ctx.fill()
        col(ctx, '#7fae5a'); ctx.rectangle(X0, yt - 4, X1 - X0, 4); ctx.fill()
        for k in range(9):
            xt = X0 + 40 + k * 100 + (i * 23) % 40
            if (k + i) % 3 == 0:
                roadster_side(ctx, xt, yt - 5, 0, .55)
            else:
                ctx.new_path(); col(ctx, '#4f7a3e'); ctx.arc(xt, yt - 12, 8, 0, 2 * math.pi); ctx.fill()
    # cross street + climb lane on the block end
    col(ctx, '#3a4250'); ctx.rectangle(X1, gy - (TOPH - L5) * PXH, 70, (TOPH - L5) * PXH); ctx.fill()
    col(ctx, '#ffd98a', .6)
    for i in range(NSTEP):
        y = gy - (step_h(i) - L5) * PXH; ctx.rectangle(X1, y - 2, 70, 3); ctx.fill()
    col(ctx, '#6f9e4a'); ctx.rectangle(0, gy, W, 16); ctx.fill()
    col(ctx, '#3a3530'); ctx.rectangle(0, gy + 16, W, 30); ctx.fill()
    # the drive: canyon street -> lane -> up -> terrace street 7 -> home
    lvl = 6; y7 = gy - (step_h(lvl) - L5) * PXH
    home_x = 640
    fans = False; thrust = 0.0
    if t < 2.6:
        u = ease(seg(t, .3, 2.6)); x, y, ang = lerp(40, LANE, u), gy - 5, 0.0
    elif t < 3.1:
        u = seg(t, 2.6, 3.1); x, y, ang = LANE, gy - 5 - 10 * u, -math.pi / 2 * u; fans = True
    elif t < 6.2:
        u = ease(seg(t, 3.1, 6.2)); x, y, ang = LANE, lerp(gy - 15, y7 - 10, u), -math.pi / 2; fans = True
    elif t < 6.7:
        u = seg(t, 6.2, 6.7); x, y, ang = lerp(LANE, LANE - 12, u), y7 - 5, -math.pi / 2 * (1 - u) + math.pi * u * 0; fans = True
        ang = lerp(-math.pi / 2, -math.pi, u)
    elif t < 9.0:
        u = ease(seg(t, 6.7, 9.0)); x, y, ang = lerp(LANE - 12, home_x, u), y7 - 5, math.pi
    else:
        x, y, ang = home_x, y7 - 5, math.pi
    # roadster drawn facing direction of travel; when ang=pi it faces left (flip instead of upside down)
    if abs(ang - math.pi) < 1e-6:
        ctx.save(); ctx.translate(x, y); ctx.scale(-1, 1); roadster_side(ctx, 0, 0, 0, 1.0); ctx.restore()
    elif ang < -math.pi / 2:
        ctx.save(); ctx.translate(x, y); ctx.scale(-1, 1); roadster_side(ctx, 0, 0, -(ang + math.pi), 1.0, fans=fans); ctx.restore()
    else:
        roadster_side(ctx, x, y, ang, 1.0, fans=fans)
    # a neighbour hops between terraces on thrusters
    if 4.0 < t < 8.5:
        u = seg(t, 4.0, 8.5)
        ya, yb = gy - (step_h(2) - L5) * PXH - 5, gy - (step_h(3) - L5) * PXH - 5
        xh = lerp(300, 380, u); yh = lerp(ya, yb, u) - math.sin(u * math.pi) * 60
        roadster_side(ctx, xh, yh, 0, .8, thrust=math.sin(u * math.pi))
        if u < .9: text(ctx, 'THRUSTER HOP', xh, yh - 26, 11, '#e8eef2', anchor='c')
    if 9.0 < t: person(ctx, home_x + 30, y7 - 2, '#ffffff', 6)
    # readout
    col(ctx, '#11131b', .92); ctx.rectangle(560, 90, 340, 80); ctx.fill()
    text(ctx, 'ROADSTER', 576, 110, 11, MUT, spacing=1)
    state = 'DRIVING' if t < 2.6 else ('CLIMBING · SUCTION FANS ON' if t < 6.7 else ('TERRACE STREET' if t < 9 else 'PARKED AT HOME'))
    text(ctx, state, 576, 134, 14, GOLD, bold=True)
    climb = 0 if t < 3.1 else (step_h(lvl) - L5) * ease(seg(t, 3.1, 6.2))
    text(ctx, f'climb {climb:4.0f} m · level {lvl + 1} terrace', 576, 156, 12, FG)
    text(ctx, 'canyon street', 46, gy + 12, 11, '#a7c88a')
    text(ctx, 'CLIMB LANE', LANE, gy - (TOPH - L5) * PXH - 10, 12, '#ffd98a', anchor='c', bold=True)
    header(ctx, '18:30')
    caption(ctx, 'COMING HOME · STRAIGHT UP THE WALL', 'Roadsters hold themselves to the wall with suction fans and drive up the climb lane at the end of each block, then pull onto their terrace street and park at home.')
    fade(ctx, t, dur)

# ---------- scene: life support, now with terraces ----------
random.seed(5)
PARTS = [(random.uniform(0, 1), random.uniform(-1, 1)) for _ in range(140)]
def scene_support(ctx, t, dur):
    background(ctx)
    xsec_base(ctx, '#0f1626')
    terrace_xsec(ctx, lights=.6, t=t)
    col(ctx, '#0a0b10', .40); ctx.rectangle(0, 0, W, H); ctx.fill()
    col(ctx, GLASS, .35); ctx.rectangle(0, cy_(150), W, cy_(143) - cy_(150)); ctx.fill()
    for i, (ph, lat) in enumerate(PARTS):
        u = (ph + t * .18) % 1.0
        if i % 2 == 0:
            x = cx_(lat * (8 + 50 * u)); h = lerp(L5, 140, u); c = '#66c2d4'
        else:
            side = 1 if lat > 0 else -1
            ang = lerp(math.pi / 2 * .62, -math.pi / 2 * .9, u)
            x = cx_(side * (TR - 4) * math.cos(ang)); h = TR + (TR - 4) * math.sin(ang); c = '#9fb7e8'
        ctx.new_path(); col(ctx, c, .85); ctx.arc(x, cy_(h), 3, 0, 2 * math.pi); ctx.fill()
    for k in range(14):
        u = (k / 14 + t * .4) % 1.0
        ctx.new_path(); col(ctx, '#5aa6d6'); ctx.arc(cx_(-60 + k * 9), cy_(lerp(L5 - .5, 2, u)), 2.5, 0, 2 * math.pi); ctx.fill()
    xsec_end(ctx)
    text(ctx, 'FRESH AIR RISES OUT OF THE VALLEY', cx_(0), cy_(118), 13, CY, anchor='c', bold=True)
    text(ctx, 'RETURNS UNDER THE WINDOW STRIP', cx_(0), cy_(136), 12, GLASS, anchor='c')
    text(ctx, 'DOWN BEHIND THE HOMES TO THE PLANT', cx_(78) + 10, cy_(70), 12, '#9fb7e8')
    header(ctx, '02:00')
    caption(ctx, 'NIGHT · WHILE YOU SLEEP', 'Air rises out of the terrace valley and flows back down behind the homes to the base, where plants and the district plant restore its oxygen. Water is condensed, cleaned and reused.')
    fade(ctx, t, dur)

# ---------- re-headed scenes from v1 ----------
def wrap_scene(fn):
    def g(ctx, t, dur):
        fn(ctx, t, dur)
    return g

SCENES = [('m1', scene_dawn, 12), ('m2', scene_home, 9), ('m3', scene_climb, 11),
          ('m4', life.scene_commute, 8), ('m5', life.scene_spoke, 9), ('m6', life.scene_farm, 8),
          ('m7', life.scene_water, 9), ('m8', life.scene_night, 8), ('m9', scene_support, 9), ('m10', life.scene_outside, 8)]

def render(name, fn, dur):
    out = os.path.dirname(os.path.abspath(__file__))
    tmp = os.path.join(out, f'{name}.tmp.mp4'); fin = os.path.join(out, f'{name}.mp4')
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for i in range(int(round(dur * FPS))):
        ctx = cairo.Context(surf); fn(ctx, i / FPS, dur); surf.flush(); p.stdin.write(bytes(surf.get_data()))
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, fin)
    else: sys.exit(name + ' failed')

if __name__ == '__main__':
    out = os.path.dirname(os.path.abspath(__file__))
    if sys.argv[1] == 'stills':
        for name, fn, dur in SCENES:
            if len(sys.argv) > 3 and name not in sys.argv[3:]: continue
            surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
            fn(ctx, float(sys.argv[2]) * dur, dur); surf.write_to_png(os.path.join(out, f'v2_{name}.png'))
    else:
        for name, fn, dur in SCENES:
            if sys.argv[1] in ('all', name): render(name, fn, dur)
