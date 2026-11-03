import minfont; minfont.install(16)
import sys, math, random, cairo, json
sys.path.insert(0,'../stack'); sys.path.insert(0,'../video')
import stackvid as SV
from common import text, GOLD, CY, FG, MUT
W,H,S=1500,500,6
surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W*S,H*S); ctx=cairo.Context(surf); ctx.scale(S,S)
ctx.set_source_rgb(10/255,11/255,16/255); ctx.paint()
random.seed(21)
for _ in range(700):
    x,y=random.uniform(0,W),random.uniform(0,H); ctx.arc(x,y,random.choice([.4,.5,.7,.9]),0,2*math.pi); ctx.set_source_rgba(1,1,1,random.uniform(.15,.7)); ctx.fill()
def rgb(h,a=1): ctx.set_source_rgba(int(h[1:3],16)/255,int(h[3:5],16)/255,int(h[5:7],16)/255,a)
SUN=(-1,0)   # sunlight comes from the left
# --- geometry (top-down, Earth fixed) ---
ex,ey,er=330,262,52
R=205; MA=math.radians(-32)
mx,my=ex+R*math.cos(MA),ey+R*math.sin(MA); mr=18
LR=62   # loop radius (drawn ~2.7x true scale)
# Moon orbit
ctx.new_path(); ctx.arc(ex,ey,R,0,2*math.pi); rgb('#a99f88',.5); ctx.set_line_width(1.6); ctx.set_dash([7,9]); ctx.stroke(); ctx.set_dash([])
b=MA+math.radians(26); x,y=ex+R*math.cos(b),ey+R*math.sin(b)
# arrow: Moon moves counter-clockwise on screen
ang=b-math.pi/2
ctx.save(); ctx.translate(ex+R*math.cos(MA-math.radians(30)),ey+R*math.sin(MA-math.radians(30))); ctx.rotate(MA-math.radians(30)-math.pi/2); ctx.move_to(11,0); ctx.line_to(-7,-7); ctx.line_to(-7,7); ctx.close_path(); rgb('#a99f88'); ctx.fill(); ctx.restore()
# Earth: sphere, continents, clouds, atmosphere, night side
g=cairo.RadialGradient(ex,ey,er*.9,ex,ey,er*1.25); g.add_color_stop_rgba(0,.45,.75,1,.35); g.add_color_stop_rgba(1,.45,.75,1,0)
ctx.new_path(); ctx.arc(ex,ey,er*1.25,0,2*math.pi); ctx.set_source(g); ctx.fill()
g=cairo.RadialGradient(ex-30,ey-30,8,ex,ey,er); g.add_color_stop_rgb(0,.33,.62,.9); g.add_color_stop_rgb(.7,.13,.38,.66); g.add_color_stop_rgb(1,.05,.17,.33)
ctx.new_path(); ctx.arc(ex,ey,er,0,2*math.pi); ctx.set_source(g); ctx.fill()
ctx.save(); ctx.arc(ex,ey,er,0,2*math.pi); ctx.clip()
random.seed(5)
for (cx,cy,rx,ry,rot,c) in ((-30,-25,34,22,.4,'#5f8f4e'),(-48,8,20,30,-.3,'#7c8f52'),(18,-40,26,14,.1,'#6e9152'),(30,20,30,22,.6,'#8a7e58'),(5,48,22,12,-.2,'#5f8f4e'),(-10,-5,12,9,0,'#9a8a62')):
    k=er/84; ctx.save(); ctx.translate(ex+cx*k,ey+cy*k); ctx.rotate(rot); ctx.scale(rx*k,ry*k); ctx.arc(0,0,1,0,2*math.pi); ctx.restore(); rgb(c,.9); ctx.fill()
for _ in range(26):
    cx,cy=random.uniform(-er,er),random.uniform(-er,er); rx,ry=random.uniform(4,13),random.uniform(1.5,3.5)
    ctx.save(); ctx.translate(ex+cx,ey+cy); ctx.rotate(random.uniform(-.6,.6)); ctx.scale(rx,ry); ctx.arc(0,0,1,0,2*math.pi); ctx.restore(); ctx.set_source_rgba(1,1,1,.32); ctx.fill()
g=cairo.LinearGradient(ex-er,ey,ex+er,ey); g.add_color_stop_rgba(0,0,0,0,0); g.add_color_stop_rgba(.5,0,0,0,.05); g.add_color_stop_rgba(.75,0,0,0,.55); g.add_color_stop_rgba(1,0,0,0,.85)
ctx.set_source(g); ctx.paint(); ctx.restore()
# Moon
g=cairo.RadialGradient(mx-6,my-6,2,mx,my,mr); g.add_color_stop_rgb(0,.96,.95,.91); g.add_color_stop_rgb(.75,.64,.62,.58); g.add_color_stop_rgb(1,.35,.34,.32)
ctx.new_path(); ctx.arc(mx,my,mr,0,2*math.pi); ctx.set_source(g); ctx.fill()
ctx.save(); ctx.arc(mx,my,mr,0,2*math.pi); ctx.clip(); random.seed(8)
for _ in range(30):
    a=random.uniform(0,2*math.pi); d=random.uniform(0,mr); cr=random.uniform(1.5,7)
    ctx.new_path(); ctx.arc(mx+d*math.cos(a),my+d*math.sin(a),cr,0,2*math.pi); ctx.set_source_rgba(.25,.24,.22,.22); ctx.fill()
for (cx,cy,rx,ry) in ((-8,-6,12,8),(8,8,10,6)):
    ctx.save(); ctx.translate(mx+cx,my+cy); ctx.scale(rx,ry); ctx.arc(0,0,1,0,2*math.pi); ctx.restore(); ctx.set_source_rgba(.28,.27,.25,.3); ctx.fill()
g=cairo.LinearGradient(mx-mr,my,mx+mr,my); g.add_color_stop_rgba(0,0,0,0,0); g.add_color_stop_rgba(.6,0,0,0,.05); g.add_color_stop_rgba(1,0,0,0,.6)
ctx.set_source(g); ctx.paint(); ctx.restore()
# Soma's loop around the Moon (retrograde: clockwise on screen)
ctx.new_path(); ctx.arc(mx,my,LR,0,2*math.pi); rgb('#f0b860'); ctx.set_line_width(3.2); ctx.stroke()
c=math.radians(55); ctx.save(); ctx.translate(mx+LR*math.cos(c),my+LR*math.sin(c)); ctx.rotate(c+math.pi/2); ctx.move_to(11,0); ctx.line_to(-7,-7); ctx.line_to(-7,7); ctx.close_path(); rgb('#f0b860'); ctx.fill(); ctx.restore()
# the stack on its loop: spine pointing at the Sun (left), rings edge-on
pa=math.radians(10); sx,sy=mx+LR*math.cos(pa),my+LR*math.sin(pa)
def mini(x,y,s):
    rgb('#9ab6be'); ctx.set_line_width(1.4*s); ctx.move_to(x-12*s,y); ctx.line_to(x+12*s,y); ctx.stroke()
    for i in range(6):
        xx=x-10*s+i*4*s; rgb('#66c2d4'); ctx.set_line_width(1.6*s); ctx.move_to(xx,y-8*s); ctx.line_to(xx,y+8*s); ctx.stroke()
mini(sx,sy,1.2)
# callout: an accurate close-up of the stack
cx_,cy_,cr_=1130,250,215
ctx.new_path(); ctx.arc(cx_,cy_,cr_,0,2*math.pi); rgb('#11131b',.96); ctx.fill_preserve(); rgb('#f0b860',.8); ctx.set_line_width(2); ctx.stroke()
# leader lines tangent-ish from stack to callout
for t in (math.radians(200),math.radians(150)):
    ctx.move_to(sx,sy); ctx.line_to(cx_+cr_*math.cos(t),cy_+cr_*math.sin(t)); rgb('#f0b860',.45); ctx.set_line_width(1.2); ctx.stroke()
ctx.save(); ctx.new_path(); ctx.arc(cx_,cy_,cr_-3,0,2*math.pi); ctx.clip()
ctx.translate(cx_,cy_); sc=.38; ctx.scale(sc,sc); ctx.translate(-640,-330)
SV.sun(ctx,1) if False else None
SV.spine(ctx); SV.pods(ctx)
for i in range(6): SV.ring(ctx,SV.XS[i],1,1,1,1,phi=math.radians(14*i)*(1 if i%2==0 else -1),fronts=False)
ctx.restore()
# sunlight arrows on the left
for yy in (110,200,320,420):
    rgb('#ffd27a',.55); ctx.set_line_width(1.6); ctx.move_to(14,yy); ctx.line_to(70,yy); ctx.stroke()
    ctx.move_to(78,yy); ctx.line_to(68,yy-5); ctx.line_to(68,yy+5); ctx.close_path(); rgb('#ffd27a',.7); ctx.fill()
text(ctx,'SUNLIGHT',16,92,13,'#ffd27a')
# labels
def lab(s,x,y,tx,ty,c,anchor='l',size=15,sub=None):
    rgb(c,.6); ctx.set_line_width(1.2); ctx.move_to(tx,ty); ctx.line_to(x,y-5); ctx.stroke()
    text(ctx,s,x+(6 if anchor=='l' else -6),y,size,c,anchor=anchor)
    if sub: text(ctx,sub,x+(6 if anchor=='l' else -6),y+20,12.5,MUT,anchor=anchor)
lab('EARTH',150,410,ex-30,ey+40,CY,sub='stays put in this view')
lab('THE MOON',600,52,mx+12,my-12,FG,sub="384,400 km from Earth, once every 27.3 days")
lab("SOMA'S LOOP AROUND THE MOON",560,300,mx+LR*.6,my+LR*.8,GOLD,sub='~30,000 km out, once every 4.7 days, backwards')
lab('THE MOON\'S ORBIT',330,488,ex+R*.3,ey+R*.95,MUT)

text(ctx,'SIX-RING STACK · CLOSE-UP',cx_-cr_-20,cy_+150,14,GOLD,anchor='r'); text(ctx,'spine points at the Sun',cx_-cr_-20,cy_+170,12.5,MUT,anchor='r'); text(ctx,'rings 34.7 km across, 2 km apart',cx_-cr_-20,cy_+188,12.5,MUT,anchor='r')
text(ctx,'top-down view · loop and bodies not to scale',W-16,24,12,MUT,anchor='r')
surf.write_to_png('img/orbitview.png'); print('ok')
