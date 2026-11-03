import sys, math, random, cairo
sys.path.insert(0,'../stack'); sys.path.insert(0,'../video')
from common import text, GOLD, CY, FG, MUT
W,H,S=820,580,3
surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W*S,H*S); ctx=cairo.Context(surf); ctx.scale(S,S)
def rgb(h,a=1): ctx.set_source_rgba(int(h[1:3],16)/255,int(h[3:5],16)/255,int(h[5:7],16)/255,a)
rgb('#0a0b10'); ctx.paint(); random.seed(6)
for _ in range(250): ctx.arc(random.uniform(0,W),random.uniform(0,H),random.choice([.4,.6,.8]),0,2*math.pi); ctx.set_source_rgba(1,1,1,random.uniform(.1,.5)); ctx.fill()
cx,cy,R=200,290,178
P=lambda r,d:(cx+r*math.cos(math.radians(d)),cy+r*math.sin(math.radians(d)))
# planned ring
ctx.new_path(); ctx.arc(cx,cy,R,0,2*math.pi); rgb('#66c2d4',.45); ctx.set_line_width(2); ctx.set_dash([8,9]); ctx.stroke(); ctx.set_dash([])
SP=[-90,-30,30,90,150,210]; grow=17  # degrees grown each way (~half)
for d in SP:
    rgb('#66c2d4'); ctx.set_line_width(3); ctx.move_to(cx,cy); ctx.line_to(*P(R,d)); ctx.stroke()
    # tube segments grown both ways, with bay seams
    ctx.new_path(); ctx.arc(cx,cy,R,math.radians(d-grow),math.radians(d+grow)); rgb('#f0b860'); ctx.set_line_width(20); ctx.stroke()
    for k in range(-grow,grow+1,3):
        a=math.radians(d+k); rgb('#0a0b10',.6); ctx.set_line_width(1.2); ctx.move_to(*P(R-8,d+k)); ctx.line_to(*P(R+8,d+k)); ctx.stroke()
    # junction node at the spoke
    x,y=P(R,d); ctx.rectangle(x-9,y-9,18,18); rgb('#c7b89a'); ctx.fill()
    # factories at both fronts
    for sg in (-1,1):
        fx,fy=P(R,d+sg*(grow+1.2))
        ctx.save(); ctx.translate(fx,fy); ctx.rotate(math.radians(d+sg*(grow+1.2))); ctx.rectangle(-13,-6,26,12); ctx.restore(); rgb('#66c2d4'); ctx.fill()
        ax,ay=P(R,d+sg*(grow+4.5))
        ctx.save(); ctx.translate(ax,ay); ctx.rotate(math.radians(d+sg*(grow+4.5)+90*(1 if sg>0 else -1))); ctx.move_to(9,0); ctx.line_to(-5,-6); ctx.line_to(-5,6); ctx.close_path(); ctx.restore(); rgb('#ffe29a'); ctx.fill()
ctx.new_path(); ctx.arc(cx,cy,14,0,2*math.pi); rgb('#c7b89a'); ctx.fill()
def lab(s,x,y,tx,ty,c,size=24):
    rgb(c,.7); ctx.set_line_width(1.6); ctx.move_to(tx,ty); ctx.line_to(x-6,y-8); ctx.stroke(); text(ctx,s,x,y,size,c,bold=True)
X=410
fx,fy=P(R,-30+grow+1.2); lab('FACTORY',X,137,fx+12,fy,CY,48)
x,y=P(R,30); lab('SPOKE',X,245,x+12,y,'#c7b89a',48)
x,y=P(R,90-10); lab('18 m BAYS',X,353,x+12,y-6,GOLD,48)
x,y=P(R,0); lab('GAPS CLOSE',X,461,x+18,y,'#ffe29a',48)
surf.write_to_png('img/f_halftorus.png'); print('ok')
