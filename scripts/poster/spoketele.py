"""Telescoping spokes: six spokes slide out of the centre pod in balanced pairs, section by section."""
import sys, math, random, cairo, os
sys.path.insert(0,'../stack'); sys.path.insert(0,'../video')
from vid import text
LW,LH=728,515; CX,CY=364,306; RIM=186; NSEC=5
def rgb(ctx,h,a=1): ctx.set_source_rgba(int(h[1:3],16)/255,int(h[3:5],16)/255,int(h[5:7],16)/255,a)
def ease(u): u=max(0,min(1,u)); return u*u*(3-2*u)
def draw(ctx,t):
    rgb(ctx,'#0a0b10'); ctx.paint(); random.seed(4)
    for _ in range(160):
        ctx.arc(random.uniform(0,LW),random.uniform(0,LH),random.choice([.5,.7,.9]),0,2*math.pi); ctx.set_source_rgba(1,1,1,random.uniform(.1,.45)); ctx.fill()
    # planned ring
    ctx.new_path(); ctx.arc(CX,CY,RIM,0,2*math.pi); rgb(ctx,'#66c2d4',.3); ctx.set_line_width(2); ctx.set_dash([7,8]); ctx.stroke(); ctx.set_dash([])
    R0=38; CELL=16; mid=(R0+RIM-CELL)/2; HALF=mid-R0; NP=9; w=28
    def origami(x0,d,u):
        """origami half-link: NP pleats; u=0 folded flat against x0, u=1 deployed to mid-span"""
        L=max(6,HALF*u); p=L/NP; amp=(w/2)*(0.72+0.28*(1-u))   # pleats flatten as it opens
        for i in range(NP):
            xa=x0+d*i*p; xb=x0+d*(i+1)*p; xm=(xa+xb)/2
            for sg in (-1,1):                    # two facets per pleat, light and dark
                ctx.move_to(xa,0); ctx.line_to(xm,sg*amp); ctx.line_to(xb,0); ctx.close_path()
                rgb(ctx,'#7fd6ec' if (i+(sg>0))%2 else '#2b6f80'); ctx.fill()
            rgb(ctx,'#0a0b10',.55); ctx.set_line_width(.8); ctx.move_to(xa,-amp); ctx.line_to(xa,amp); ctx.stroke()
        # outer crease lines
        rgb(ctx,'#bfeaf3'); ctx.set_line_width(1.3)
        for sg in (-1,1):
            ctx.move_to(x0,sg*amp*.2)
            for i in range(NP): ctx.line_to(x0+d*(i+.5)*p,sg*amp); ctx.line_to(x0+d*(i+1)*p,sg*amp*.2)
            ctx.stroke()
        return x0+d*L
    for j,ang in enumerate((-90,90,-30,150,30,210)):
        pair=j//2; t0=pair*0.3; a=math.radians(ang)
        u=ease((t-0.6-t0)/5.0)
        ctx.save(); ctx.translate(CX,CY); ctx.rotate(a)
        # connector cell on the tube, with short tube stubs either side
        ctx.new_path(); ctx.arc(0,0,RIM,-0.17,0.17); rgb(ctx,"#e6b85c"); ctx.set_line_width(16); ctx.stroke()
        rgb(ctx,'#66c2d4'); ctx.rectangle(RIM-CELL,-17,CELL*2,34); ctx.fill()
        rgb(ctx,'#0a0b10',.55); ctx.rectangle(RIM-CELL+5,-11,CELL*2-10,22); ctx.fill()
        origami(R0,1,u)                          # out of the spine pod
        origami(RIM-CELL,-1,u)                   # out of the tube's connector cell
        if u>=1:
            k=ease((t-5.6-t0)/0.5); rgb(ctx,'#ffe29a',k); ctx.rectangle(mid-4,-w/2-5,8,w+10); ctx.fill()
        ctx.restore()
    text(ctx,'ORIGAMI LINK',16,60,42,'#f0b860',bold=True)
    text(ctx,'BASALT FIBRE',LW-16,60,42,'#66c2d4',bold=True,anchor='r')
    # centre pod on the spine (the spine runs into the page, seen end-on)
    ctx.new_path(); ctx.arc(CX,CY,36,0,2*math.pi); rgb(ctx,'#c7b89a'); ctx.fill()
    ctx.new_path(); ctx.arc(CX,CY,14,0,2*math.pi); rgb(ctx,'#8a8070'); ctx.fill()
    ctx.new_path(); ctx.arc(CX,CY,6,0,2*math.pi); rgb(ctx,'#e8e2d4'); ctx.fill()
def render(path,t,W):
    S=W/LW; surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,round(LW*S),round(LH*S)); ctx=cairo.Context(surf); ctx.scale(S,S); draw(ctx,t); surf.write_to_png(path)
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='still': render('img/f_spokes.png',4.2,2912)
    else:
        W=int(sys.argv[2]); os.makedirs('anim/sf',exist_ok=True)
        for i in range(120): render(f'anim/sf/f{i:03d}.png',i/15,W)
