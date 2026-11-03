"""Panel B zoom-out: from the finished stack to its loop around the Moon, with sunlight from the left."""
import sys, os, math, cairo, inspect
FILM='/tmp/claude-0/-home-claude/2aa3f404-8de0-56e4-b320-595de06df08e/scratchpad/film'
sys.path.insert(0,FILM); sys.path.insert(0,os.path.join(FILM,'..','stack')); os.chdir(FILM)
import finale as FN
src=inspect.getsource(FN.finale)
rep=[("lb=seg(t,10,10.8)*(1-seg(t,12.2,13))","lb=seg(t,10,10.8)"),("label(ctx,'the Moon carries it around Earth each month',120,560,","label(ctx,'the Moon carries it around Earth each month',E[0]+Rs+30,E[1]+90,"),("ctx.rotate(math.radians(-30)); ctx.scale(1,.42)","ctx.scale(.42,1)"),
     ("hdr(ctx,'THE FINISHED STACK','WHERE IT LIVES') if t<11 else None",""),
     ("    if t<4: label(ctx,'THE FINISHED STACK","    if False: label(ctx,'THE FINISHED STACK"),
     ("    if t<.4: col(ctx,'#000000',1-t/.4); ctx.paint()",""),
     ("    background(ctx)\n","    background(ctx); sunlight(ctx)\n"),
     ("        col(ctx,BG,a); ctx.fill_preserve(); col(ctx,GOLD,a); ctx.set_line_width(lerp(2,4.5,w2)); ctx.stroke()",
      "        col(ctx,BG,a); ctx.fill_preserve(); col(ctx,GOLD,a); ctx.set_line_width(lerp(2,4.5,w2)); ctx.stroke()\n"
      "        L=lerp(16,26,w2); col(ctx,'#c9c5ba',a); ctx.set_line_width(2); ctx.move_to(Sp[0]-L,Sp[1]); ctx.line_to(Sp[0]+L,Sp[1]); ctx.stroke()\n"
      "        if 4.5<t<12.6: label(ctx,'SOMA · spin axis points at the Sun',Sp[0]-40,Sp[1]-70,Sp[0]-L,Sp[1],GOLD,a=a*seg(t,4.5,5.3))")]
for a,b in rep:
    assert a in src, a[:40]; src=src.replace(a,b)
def sunlight(ctx):
    FN.text(ctx,'SUNLIGHT',24,170,13,FN.GOLD,spacing=2)
    for y in (200,290,380,470):
        FN.col(ctx,FN.GOLD,.75); ctx.set_line_width(2); ctx.move_to(24,y); ctx.line_to(104,y); ctx.stroke()
        ctx.move_to(108,y); ctx.line_to(96,y-6); ctx.line_to(96,y+6); ctx.close_path(); ctx.fill()
FN.sunlight=sunlight
exec(src,FN.__dict__)
W,H=int(sys.argv[1]),int(sys.argv[2]); out=sys.argv[3]; N=int(sys.argv[4]); T1=12.4; FPS=15
k=W/1280; band_cy=335; bh=H/k
os.makedirs(out,exist_ok=True)
for i in range(N):
    t=min(T1, i/(FPS*3.6/T1)/ (FPS/FPS) * (1/FPS) * FPS) if False else min(T1, (i/FPS)*(T1/3.6))
    surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); ctx=cairo.Context(surf)
    ctx.scale(k,k); ctx.translate(0,-(band_cy-bh/2))
    FN.finale(ctx,t,99)
    surf.write_to_png(f'{out}/z{i:03d}.png')
print('done',N)
