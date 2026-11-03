import cairo, math
DARK=dict(bg=(10/255,11/255,16/255), orbit=(0.66,0.62,0.53), earth=(0.40,0.76,0.83), moon=(0.93,0.90,0.85), gold=(0.94,0.72,0.38), word=(0.95,0.93,0.89), sub=(0.66,0.62,0.53))
LIGHT=dict(bg=(0.98,0.97,0.94), orbit=(0.55,0.50,0.42), earth=(0.17,0.47,0.55), moon=(0.30,0.28,0.25), gold=(0.78,0.52,0.13), word=(0.10,0.10,0.12), sub=(0.42,0.38,0.32))
MOON_ANG=math.radians(-40)
def arrowhead(ctx,x,y,ang,s,c):
    ctx.save(); ctx.translate(x,y); ctx.rotate(ang)
    ctx.move_to(s,0); ctx.line_to(-s*.8,-s*.75); ctx.line_to(-s*.8,s*.75); ctx.close_path(); ctx.set_source_rgb(*c); ctx.fill(); ctx.restore()
def mark(ctx,ex,ey,k=1.0,th=DARK,phi=math.radians(205),a=1.0,arrows=True,R=170,rl=59,re=26,rm=12):
    """Earth at (ex,ey); Moon orbit radius R; loop radius rl around the Moon. k scales everything."""
    R,rl,re,rm=R*k,rl*k,re*k,rm*k
    mx,my=ex+R*math.cos(MOON_ANG),ey+R*math.sin(MOON_ANG)
    def src(c,al=1): ctx.set_source_rgba(*c,al*a)
    ctx.new_path(); ctx.arc(ex,ey,R,0,2*math.pi); src(th['orbit'],.7); ctx.set_line_width(max(1,2.2*k)); ctx.stroke()
    ctx.new_path(); ctx.arc(mx,my,rl,0,2*math.pi); src(th['gold']); ctx.set_line_width(max(1.2,5*k)); ctx.stroke()
    ctx.new_path(); ctx.arc(ex,ey,re,0,2*math.pi); src(th['earth']); ctx.fill()
    ctx.new_path(); ctx.arc(mx,my,rm,0,2*math.pi); src(th['moon']); ctx.fill()
    if arrows and a>0:
        # Moon goes counter-clockwise on screen (prograde); the ring loops clockwise (retrograde)
        b=MOON_ANG-math.radians(70); arrowhead(ctx,ex+R*math.cos(b),ey+R*math.sin(b),b-math.pi/2,7*k,th['orbit'])
        c=math.radians(60); arrowhead(ctx,mx+rl*math.cos(c),my+rl*math.sin(c),c+math.pi/2,8*k,th['gold'])
    # the ring itself: a small torus seen at an angle, on the loop
    rx,ry=mx+rl*math.cos(phi),my+rl*math.sin(phi)
    ctx.save(); ctx.translate(rx,ry); ctx.rotate(math.radians(-30)); ctx.scale(1,.42)
    ctx.new_path(); ctx.arc(0,0,13*k,0,2*math.pi); ctx.restore()
    src(th['bg']); ctx.fill_preserve(); src(th['gold']); ctx.set_line_width(max(1.2,4.5*k)); ctx.stroke()
    return mx,my,rx,ry
def word(ctx,x,y,size,th=DARK,a=1.0,anchor='l',sub=None):
    ctx.select_font_face('Inter',cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_NORMAL); ctx.set_font_size(size)
    s='SOMA'; sp=size*.42
    w=sum(ctx.text_extents(ch).x_advance for ch in s)+sp*(len(s)-1)
    if anchor=='c': x-=w/2
    ctx.set_source_rgba(*th['word'],a); xx=x
    for ch in s: ctx.move_to(xx,y); ctx.show_text(ch); xx+=ctx.text_extents(ch).x_advance+sp
    if sub:
        ctx.set_font_size(size*.22); ctx.set_source_rgba(*th['sub'],a)
        w2=sum(ctx.text_extents(ch).x_advance+size*.06 for ch in sub)
        xx=x+(w-w2)/2 if anchor=='c' else x
        for ch in sub: ctx.move_to(xx,y+size*.55); ctx.show_text(ch); xx+=ctx.text_extents(ch).x_advance+size*.06
def export(name,th,W=1200,H=1200,with_word=True,transparent=False):
    for kind in ('png','svg'):
        if kind=='png': surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H)
        else: surf=cairo.SVGSurface(f'{name}.svg',W,H)
        ctx=cairo.Context(surf)
        if not transparent: ctx.set_source_rgb(*th['bg']); ctx.paint()
        k=W/600
        mark(ctx,W*.42,H*(.52 if not with_word else .46),k=k,th=th)
        if with_word: word(ctx,W/2,H*.86,W*.095,th=th,anchor='c',sub='CISLUNAR RING SETTLEMENT')
        if kind=='png': surf.write_to_png(f'{name}.png')
        surf.finish()
if __name__=='__main__':
    export('soma-logo-dark',DARK); export('soma-logo-light',LIGHT)
    export('soma-mark-dark',DARK,with_word=False); export('soma-mark-light',LIGHT,with_word=False)
