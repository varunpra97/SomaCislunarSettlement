"""Six centre pods built one by one over the fixed spine; each spins on magnetic bearings once done."""
import sys, math, random, cairo, os
sys.path.insert(0,'../stack'); sys.path.insert(0,'../video')
from vid import text
LW,LH=640,452; CY=268; X0,X1=70,570; NP=6; PH=150; PW=40; SPH=34
XS=[X0+(X1-X0)*(i+.5)/NP for i in range(NP)]
def rgb(ctx,h,a=1): ctx.set_source_rgba(int(h[1:3],16)/255,int(h[3:5],16)/255,int(h[5:7],16)/255,a)
def ease(u): u=max(0,min(1,u)); return u*u*(3-2*u)
def win(i): a=0.5+i*1.12; return a,a+0.85
def draw(ctx,t):
    rgb(ctx,'#0a0b10'); ctx.paint(); random.seed(5)
    for _ in range(120):
        ctx.arc(random.uniform(0,LW),random.uniform(0,LH),random.choice([.5,.7]),0,2*math.pi); ctx.set_source_rgba(1,1,1,random.uniform(.1,.4)); ctx.fill()
    # spine skeleton: Starship core wrapped in drums, Starship noses at both ends
    rgb(ctx,'#3c5f68'); ctx.rectangle(X0-30,CY-SPH/2,X1-X0+60,SPH); ctx.fill()
    rgb(ctx,'#c9c5ba'); ctx.rectangle(X0-30,CY-5,X1-X0+60,10); ctx.fill()
    for k in (-1,1):
        rgb(ctx,'#8fb6bf',.7); ctx.set_line_width(1.2); ctx.move_to(X0-30,CY+k*SPH/2*.6); ctx.line_to(X1+30,CY+k*SPH/2*.6); ctx.stroke()
    for x,d in ((X0-30,-1),(X1+30,1)):
        ctx.move_to(x,CY-SPH/2); ctx.line_to(x+d*30,CY); ctx.line_to(x,CY+SPH/2); ctx.close_path(); rgb(ctx,'#c9c5ba'); ctx.fill()
    # pods
    for i,x in enumerate(XS):
        a,b=win(i); u=ease((t-a)/(b-a))
        if u<=0:
            rgb(ctx,'#66c2d4',.35); ctx.set_dash([4,4]); ctx.set_line_width(1.4); ctx.rectangle(x-PW/2,CY-PH/2,PW,PH); ctx.stroke(); ctx.set_dash([]); continue
        NS=8; shown=u*NS
        # segments wrap on from the spine outward (stack up and down)
        for s in range(NS):
            f=max(0,min(1,shown-s))
            if f<=0: break
            k=s//2; up=(s%2==0); h=(PH-SPH)/2/4
            y0=CY-SPH/2-(k+1)*h if up else CY+SPH/2+k*h
            rgb(ctx,'#c7b89a',f); ctx.rectangle(x-PW/2,y0,PW,h); ctx.fill()
        if u>=1:
            # spinning: bands sweep over the drum face; spin ramps up after completion
            sp=min(1,(t-b)/0.4); w0=2*math.pi/2.4; ph=1.3*math.sin(w0*(t-b))*sp; dirn=math.cos(w0*(t-b))  # rocks: clockwise half the cycle, anticlockwise the other
            ctx.save(); ctx.rectangle(x-PW/2,CY-PH/2,PW,PH); ctx.clip()
            for k in range(10):
                th=ph+k*2*math.pi/10; yy=CY-math.sin(th)*PH/2
                if math.cos(th)>0:
                    rgb(ctx,'#7a6e58',.75*math.cos(th)); ctx.rectangle(x-PW/2,yy-3,PW,6); ctx.fill()
            ctx.restore()
            # magnetic bearings glow on each side of the pod where it meets the fixed spine
            g=.5+.5*math.sin(t*6+i)
            for d in (-1,1):
                rgb(ctx,'#7fe7ff',.6+.4*g); ctx.rectangle(x+d*PW/2-(2 if d>0 else 0),CY-SPH/2-6,2,SPH+12); ctx.fill()
            # curved spin arrow
            a0,a1=math.pi*1.1,math.pi*1.9; ay=CY-PH/2-14
            ctx.new_path(); ctx.arc(x,ay,11,a0,a1); rgb(ctx,'#f0b860',sp); ctx.set_line_width(2.4); ctx.stroke()
            ang=a1 if dirn>0 else a0; hx,hy=x+11*math.cos(ang),ay+11*math.sin(ang)
            tang=ang+(math.pi/2 if dirn>0 else -math.pi/2)
            ctx.move_to(hx+6*math.cos(tang),hy+6*math.sin(tang))
            ctx.line_to(hx+5*math.cos(tang+2.4),hy+5*math.sin(tang+2.4)); ctx.line_to(hx+5*math.cos(tang-2.4),hy+5*math.sin(tang-2.4)); ctx.close_path(); ctx.fill()
        # builder crawler on the spine while this pod is being built
        if a<=t<b:
            ctx.new_path(); ctx.arc(x+PW/2+12,CY-SPH/2-7,6,0,2*math.pi); rgb(ctx,'#ffe29a'); ctx.fill()
    # crawler travelling to the next pod
    for i in range(NP-1):
        a,b=win(i); a2,_=win(i+1)
        if b<=t<a2:
            v=(t-b)/(a2-b); x=XS[i]+(XS[i+1]-XS[i])*ease(v)+PW/2+12
            ctx.new_path(); ctx.arc(x,CY-SPH/2-7,6,0,2*math.pi); rgb(ctx,'#ffe29a'); ctx.fill()
    text(ctx,'PODS FREE',16,56,38,'#f0b860',bold=True)
    text(ctx,'SPINE FIXED',LW-16,56,38,'#66c2d4',bold=True,anchor='r')
def render(path,t,W):
    S=W/LW; surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,round(LW*S),round(LH*S)); ctx=cairo.Context(surf); ctx.scale(S,S); draw(ctx,t); surf.write_to_png(path)
if __name__=='__main__':
    if sys.argv[1]=='still': render('img/f_pods.png',8.0,2560)
    else:
        W=int(sys.argv[2]); os.makedirs('anim/pf',exist_ok=True)
        for i in range(120): render(f'anim/pf/f{i:03d}.png',i/15,W)
