import minfont; minfont.install(16)
import sys, math, random, cairo
sys.path.insert(0,'../stack'); sys.path.insert(0,'../video')
from common import text, GOLD, CY, FG, MUT
import os
LT=os.environ.get('LT'); W,H=1500,330; S=float(os.environ.get('LS','6'))
surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,round(W*S),round(H*S)); ctx=cairo.Context(surf); ctx.scale(S,S)
def rgb(h,a=1): ctx.set_source_rgba(int(h[1:3],16)/255,int(h[3:5],16)/255,int(h[5:7],16)/255,a)
rgb('#07080d'); ctx.paint()
random.seed(9)
for _ in range(300):
    ctx.arc(random.uniform(0,W),random.uniform(0,150),random.choice([.4,.6,.8]),0,2*math.pi); ctx.set_source_rgba(1,1,1,random.uniform(.15,.6)); ctx.fill()
# Earth in the sky
ex,ey=1420,50; g=cairo.RadialGradient(ex-6,ey-6,2,ex,ey,18); g.add_color_stop_rgb(0,.55,.8,.95); g.add_color_stop_rgb(1,.1,.3,.55)
ctx.arc(ex,ey,18,0,2*math.pi); ctx.set_source(g); ctx.fill()
GY=262  # ground line
# terrain
g=cairo.LinearGradient(0,GY-10,0,H); g.add_color_stop_rgb(0,.42,.41,.39); g.add_color_stop_rgb(1,.2,.2,.19)
ctx.move_to(0,GY+6)
for x in range(0,W+20,20): ctx.line_to(x,GY+4*math.sin(x/90)+2*math.sin(x/23))
ctx.line_to(W,H); ctx.line_to(0,H); ctx.close_path(); ctx.set_source(g); ctx.fill()
for _ in range(60):
    x=random.uniform(0,W); y=random.uniform(GY+12,H-4); r=random.uniform(2,9)
    ctx.save(); ctx.translate(x,y); ctx.scale(1,.35); ctx.arc(0,0,r,0,2*math.pi); ctx.restore(); ctx.set_source_rgba(0,0,0,.25); ctx.fill()
# distant hills
ctx.move_to(0,GY-6)
for x in range(0,W+30,30): ctx.line_to(x,GY-14-12*math.sin(x/160)-6*math.sin(x/47))
ctx.line_to(W,GY); ctx.line_to(0,GY); ctx.close_path(); rgb('#2e2d2b'); ctx.fill()
# solar array field (background)
for i in range(16):
    x=470+i*26; rgb('#20335a'); ctx.save(); ctx.translate(x,GY-24); ctx.transform(cairo.Matrix(1,0,-.5,1,0,0)); ctx.rectangle(0,0,22,10); ctx.restore(); ctx.fill()
    rgb('#6d8fd6',.6); ctx.set_line_width(.6); ctx.move_to(x+4,GY-14); ctx.line_to(x+4,GY-4); ctx.stroke()
# 1 · collector robots + regolith piles
def rover(x,y,s=1,scoop=0):
    rgb('#c7b89a'); ctx.rectangle(x-18*s,y-14*s,36*s,10*s); ctx.fill()
    rgb('#8a7e6a'); ctx.rectangle(x-14*s,y-22*s,18*s,8*s); ctx.fill()
    for dx in (-12,0,12):
        ctx.new_path(); ctx.arc(x+dx*s,y-3*s,4.5*s,0,2*math.pi); rgb('#3a3936'); ctx.fill()
    rgb('#66c2d4'); ctx.set_line_width(2.4*s); ctx.move_to(x+16*s,y-12*s); ctx.line_to(x+28*s,y-22*s+scoop); ctx.line_to(x+36*s,y-6*s+scoop); ctx.stroke()
    ctx.move_to(x+33*s,y-8*s+scoop); ctx.line_to(x+42*s,y-8*s+scoop); ctx.line_to(x+40*s,y-1*s+scoop); ctx.close_path(); rgb('#f0b860'); ctx.fill()
for (x,sc) in ((55,0),(160,4),(255,0)):
    rover(x,GY+8,1.35,sc)
for x in (108,210):
    ctx.move_to(x-26,GY+10); ctx.curve_to(x-10,GY-8,x+10,GY-8,x+26,GY+10); ctx.close_path(); rgb('#6e6a62'); ctx.fill()
# conveyor to the plant
rgb('#9a917f'); ctx.set_line_width(3); ctx.move_to(270,GY-2); ctx.line_to(372,GY-34); ctx.stroke()
for i in range(7):
    x=278+i*14; y=GY-4-i*4.4; rgb('#6e6a62'); ctx.rectangle(x,y-5,8,4); ctx.fill()
# 2 · sorting / refining plant
px=380
rgb('#2a2f38'); ctx.rectangle(px,GY-90,120,90); ctx.fill(); rgb('#66c2d4',.8); ctx.set_line_width(1.5); ctx.rectangle(px,GY-90,120,90); ctx.stroke()
for i in range(3): rgb('#3f8796',.6); ctx.rectangle(px+12+i*36,GY-76,26,18); ctx.fill()
rgb('#c7b89a'); ctx.rectangle(px+20,GY-40,80,14); ctx.fill()
text(ctx,'SIEVE · REFINE',px+60,GY-8,9.5,'#ece6d8',anchor='c')
# outputs arrows
def arrow(x0,y0,x1,y1,c='#f0b860'):
    rgb(c,.8); ctx.set_line_width(1.6); ctx.move_to(x0,y0); ctx.line_to(x1,y1); ctx.stroke()
    a=math.atan2(y1-y0,x1-x0); ctx.move_to(x1,y1); ctx.line_to(x1-8*math.cos(a-.4),y1-8*math.sin(a-.4)); ctx.line_to(x1-8*math.cos(a+.4),y1-8*math.sin(a+.4)); ctx.close_path(); ctx.fill()
arrow(px+120,GY-60,640,GY-80)
# 3 · furnace + fibre-drawing tower
fx=660
rgb('#2a2f38'); ctx.rectangle(fx,GY-70,90,70); ctx.fill(); rgb('#66c2d4',.8); ctx.rectangle(fx,GY-70,90,70); ctx.stroke()
g=cairo.RadialGradient(fx+45,GY-38,2,fx+45,GY-38,26); g.add_color_stop_rgba(0,1,.85,.4,1); g.add_color_stop_rgba(.6,1,.45,.1,.8); g.add_color_stop_rgba(1,1,.3,.05,0)
ctx.arc(fx+45,GY-38,26,0,2*math.pi); ctx.set_source(g); ctx.fill()
text(ctx,'FURNACE',fx+45,GY-6,9.5,'#ece6d8',anchor='c')
# solar concentrator dish feeding the furnace
ctx.new_path(); ctx.save(); ctx.translate(fx-40,GY-120); ctx.rotate(-.5); ctx.scale(1,.45); ctx.arc(0,0,28,0,math.pi); ctx.restore(); rgb('#e8e2d4',.85); ctx.set_line_width(3); ctx.stroke()
ctx.new_path(); rgb('#ffd27a',.5); ctx.set_line_width(1); ctx.move_to(fx-30,GY-112); ctx.line_to(fx+40,GY-60); ctx.stroke()
# drawing tower
tx=790; rgb('#9a917f'); ctx.set_line_width(2.5)
for dx in (0,30): ctx.move_to(tx+dx,GY); ctx.line_to(tx+dx,GY-170); ctx.stroke()
for i in range(9): ctx.move_to(tx,GY-i*19); ctx.line_to(tx+30,GY-(i+1)*19); ctx.stroke()
g=cairo.RadialGradient(tx+15,GY-176,1,tx+15,GY-176,12); g.add_color_stop_rgba(0,1,.85,.4,1); g.add_color_stop_rgba(1,1,.4,.1,0)
ctx.arc(tx+15,GY-176,12,0,2*math.pi); ctx.set_source(g); ctx.fill()
rgb('#ffe29a',.9); ctx.set_line_width(.8)
for dx in (-3,0,3): ctx.move_to(tx+15+dx,GY-170); ctx.line_to(tx+15+dx*.3,GY-28); ctx.stroke()
for (sx,sy) in ((tx+50,GY-18),(tx+76,GY-18)):
    ctx.new_path(); ctx.arc(sx,sy,11,0,2*math.pi); rgb('#d8c9a8'); ctx.fill(); ctx.new_path(); ctx.arc(sx,sy,4,0,2*math.pi); rgb('#5a4a34'); ctx.fill()
rgb('#ffe29a',.8); ctx.move_to(tx+15,GY-28); ctx.line_to(tx+50,GY-29); ctx.stroke()
arrow(fx+90,GY-40,tx-4,GY-150,'#ffd27a')
# 4 · packing + mass driver
pk=900
rgb('#2a2f38'); ctx.rectangle(pk,GY-46,60,46); ctx.fill(); rgb('#66c2d4',.8); ctx.rectangle(pk,GY-46,60,46); ctx.stroke()
for i in range(4): rgb('#f0b860'); ctx.rectangle(pk+6+i*13,GY-20,9,9); ctx.fill()
text(ctx,'PACK',pk+30,GY-28,9.5,'#ece6d8',anchor='c')
arrow(tx+90,GY-18,pk-2,GY-18)
# mass driver track rising gently to the right
x0,y0,x1,y1=970,GY-6,1460,GY-70
rgb('#9a917f'); ctx.set_line_width(4); ctx.move_to(x0,y0); ctx.line_to(x1,y1); ctx.stroke()
n=30
for i in range(n+1):
    u=i/n; x=x0+(x1-x0)*u; y=y0+(y1-y0)*u
    ctx.save(); ctx.translate(x,y); ctx.rotate(math.atan2(y1-y0,x1-x0)); ctx.scale(.35,1); ctx.new_path(); ctx.arc(0,0,9,0,2*math.pi); ctx.restore(); rgb('#66c2d4',.9); ctx.set_line_width(1.6); ctx.stroke()
    if i%5==0:
        rgb('#5a5650'); ctx.set_line_width(1.5); ctx.move_to(x,y+6); ctx.line_to(x,GY+4*math.sin(x/90)); ctx.stroke()
# packets in flight along the track and leaving
rgb('#ffd27a',.45); ctx.set_line_width(1.4); ctx.set_dash([5,6]); ctx.move_to(x1,y1); ctx.curve_to(x1+20,y1-40,x1+15,y1-120,x1-40,y1-170); ctx.stroke(); ctx.set_dash([])
def bez(v):
    P=[(x1,y1),(x1+20,y1-40),(x1+15,y1-120),(x1-40,y1-170)]
    return tuple((1-v)**3*P[0][j]+3*(1-v)**2*v*P[1][j]+3*(1-v)*v*v*P[2][j]+v**3*P[3][j] for j in (0,1))
def packet(x,y,a=1,glow=0):
    if glow:
        g=cairo.RadialGradient(x,y,0,x,y,12); g.add_color_stop_rgba(0,1,.85,.5,.7*a); g.add_color_stop_rgba(1,1,.85,.5,0)
        ctx.new_path(); ctx.arc(x,y,12,0,2*math.pi); ctx.set_source(g); ctx.fill()
    ctx.new_path(); ctx.arc(x,y,3.4,0,2*math.pi); rgb('#ffd27a',a); ctx.fill()
if LT is None:
    for u in (.35,.7): packet(x0+(x1-x0)*u,y0+(y1-y0)*u)
    packet(*bez(.18))
else:
    t=float(LT); PER=.5; TR=.8; FL=1.2
    for k in range(-6,10):
        s0=t-k*PER
        if 0<=s0<TR:
            u=(s0/TR)**2; x=x0+(x1-x0)*u; y=y0+(y1-y0)*u
            # coil flash where the packet is
            ctx.save(); ctx.translate(x,y); ctx.rotate(math.atan2(y1-y0,x1-x0)); ctx.scale(.35,1); ctx.new_path(); ctx.arc(0,0,10,0,2*math.pi); ctx.restore()
            rgb('#e9fbff',.9); ctx.set_line_width(2.4); ctx.stroke()
            packet(x,y,1,glow=u)
            # trail
            for j in range(1,5):
                uu=max(0,((s0-.03*j)/TR)**2); packet(x0+(x1-x0)*uu,y0+(y1-y0)*uu,.5-.1*j)
        elif TR<=s0<TR+FL:
            v=(s0-TR)/FL; a=1-max(0,(v-.7)/.3); packet(*bez(v),a,glow=.6)
# step labels
def step(n,title,sub,x,y):
    ctx.new_path(); ctx.arc(x,y-5,10,0,2*math.pi); rgb('#f0b860'); ctx.fill(); text(ctx,str(n),x,y-.8,11.5,'#1a1206',anchor='c',bold=True)
    text(ctx,title,x+16,y,13,GOLD,bold=True); text(ctx,sub,x+16,y+17,11,'#ece6d8')
step(1,'COLLECT','robots scoop regolith',30,40)
step(2,'SORT AND REFINE','shield fines, metals, O₂',330,40)
step(3,'MELT AND DRAW','basalt drawn into fibre',620,40)
step(4,'PACK AND LAUNCH','packets thrown at 2.4 km/s',930,40)
text(ctx,'~30 Mt a year · ~2.7 GW of lunar solar power · packets caught near Soma',W-12,H-10,11,MUT,anchor='r')
text(ctx,'SOLAR ARRAYS',560,GY-36,9.5,'#6d8fd6',anchor='c')
text(ctx,'to Soma\'s catcher',x1-58,y1-150,10.5,'#ffd27a',anchor='r')
text(ctx,'not to scale',12,H-10,10,MUT)
surf.write_to_png(os.environ.get('LOUT','img/lunarind.png')); print('ok')
