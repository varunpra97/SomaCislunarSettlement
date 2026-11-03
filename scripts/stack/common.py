import sys, os, math, subprocess, cairo, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from vid import (W,H,FPS,hx,col,text,wrap,caption,tag,label,starship,arm,ell,fade,ease,seg,lerp,clamp,
                 BG,FG,MUT,GOLD,CY,CYD,GLASS,KEEL,STEEL,SHIP,SOLAR,SOLARL,SPARK,HULL,MONO,SANS,STARS)
OUT=os.path.dirname(os.path.abspath(__file__))
GREEN='#7fd18b'; RED='#e07a5f'; SHIELD='#5a4a34'; SHIELDL='#8a7350'; PANEL='#c7b89a'

def background(ctx):
    col(ctx,BG); ctx.paint()
    for x,y,r,a in STARS:
        ctx.arc(x,y,r,0,2*math.pi); col(ctx,'#ffffff',a*.8); ctx.fill()

def hdr(ctx,a,b):
    text(ctx,a,40,44,15,MUT,spacing=3); text(ctx,b,40,66,12,'#6b6252',spacing=2)

def ship(ctx,x,y,s=.35,flip=False,a=1.0,door=0):
    """Starship with nose at (x, y) centre-line; body extends right (or left if flip)."""
    ctx.save(); ctx.translate(x,y)
    if flip: ctx.scale(-1,1)
    starship(ctx,0,-18*s,s=s,door=door,a=a); ctx.restore()

def puff(ctx,x,y,dx,dy,t,k=0,a=1.0):
    f=.5+.5*math.sin(t*23+k*1.7)
    if f<.25: return
    L=10+8*f
    n=math.hypot(dx,dy); ux,uy=dx/n,dy/n; px,py=-uy,ux
    ctx.move_to(x,y); ctx.line_to(x+ux*L+px*4,y+uy*L+py*4); ctx.line_to(x+ux*L-px*4,y+uy*L-py*4); ctx.close_path()
    col(ctx,SPARK,.75*f*a); ctx.fill()

def readout(ctx,lab,val,x,y,c=GOLD,a=1.0,w=230):
    col(ctx,'#11131b',.9*a); ctx.rectangle(x,y,w,52); ctx.fill()
    col(ctx,'#2c2a24',a); ctx.set_line_width(1); ctx.rectangle(x+.5,y+.5,w-1,51); ctx.stroke()
    text(ctx,lab,x+12,y+19,11,MUT,a=a,spacing=1.5); text(ctx,val,x+12,y+43,20,c,bold=True,a=a)

def card(ctx,title,rows,t,dur,sub=''):
    background(ctx)
    text(ctx,title,640,150,30,FG,anchor='c',spacing=4,a=seg(t,.2,1))
    if sub: text(ctx,sub,640,182,15,MUT,anchor='c',a=seg(t,.4,1.2))
    y=240
    for i,(k,v) in enumerate(rows):
        a=seg(t,.6+i*.35,1.2+i*.35)
        text(ctx,k,600,y,16,MUT,anchor='r',a=a); text(ctx,v,630,y,17,FG,a=a,font=SANS)
        y+=40
    fade(ctx,t,dur,fo=.8)

def truss_h(ctx,x0,x1,y,h,c=CY,a=1.0,step=14,lw=1.4):
    if x1<=x0: return
    col(ctx,c,a); ctx.set_line_width(lw*1.4)
    ctx.move_to(x0,y-h/2); ctx.line_to(x1,y-h/2); ctx.move_to(x0,y+h/2); ctx.line_to(x1,y+h/2); ctx.stroke()
    ctx.set_line_width(lw*.8); col(ctx,c,.6*a)
    x=x0; up=True
    while x<x1-1:
        nx=min(x1,x+step); ctx.move_to(x,y-h/2 if up else y+h/2); ctx.line_to(nx,y+h/2 if up else y-h/2); x=nx; up=not up
    ctx.stroke()

def render(name,fn,dur,outdir=OUT):
    tmp=os.path.join(outdir,f'{name}.tmp.mp4'); fin=os.path.join(outdir,f'{name}.mp4')
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgra','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',tmp],stdin=subprocess.PIPE)
    surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H)
    for i in range(int(round(dur*FPS))):
        ctx=cairo.Context(surf); ctx.set_antialias(cairo.ANTIALIAS_BEST)
        fn(ctx,i/FPS,dur); surf.flush(); p.stdin.write(bytes(surf.get_data()))
    p.stdin.close()
    if p.wait()==0: os.replace(tmp,fin)
    else: sys.exit(f'{name} failed')

def still(name,fn,dur,t,outdir=OUT):
    surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); ctx=cairo.Context(surf); fn(ctx,t,dur)
    p=os.path.join(outdir,f'st_{name}_{t:.1f}.png'); surf.write_to_png(p); return p

def main(SCENES,prefix):
    args=sys.argv[1:]
    if args and args[0]=='stills':
        fr=[float(x) for x in args[1:]] or [.5]
        ps=[]
        for nm,fn,d in SCENES:
            for f in fr: ps.append(still(nm,fn,d,f*d))
        print('\n'.join(ps))
    else:
        names=[]
        for nm,fn,d in SCENES:
            if not args or args[0] in ('all',nm): render(nm,fn,d)
            names.append(nm)
        lst=os.path.join(OUT,f'{prefix}.txt')
        open(lst,'w').write(''.join(f"file '{n}.mp4'\n" for n in names))
        subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',lst,'-c','copy',os.path.join(OUT,f'{prefix}.mp4')],check=True)
