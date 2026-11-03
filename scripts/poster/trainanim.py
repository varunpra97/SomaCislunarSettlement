"""The ring unrolled: cells of several districts, with trains in the hardware base stopping at each district."""
import sys, math, random, cairo, os
sys.path.insert(0,'../stack'); sys.path.insert(0,'../video')
from vid import text
LW,LH=1344,386; TOP,FLOOR=70,292; BASE0,BASE1=292,352; CW=112
TYPES=['res','wat','res','farm','lab','res','food','civ','res','out','hub','res']
COL={'res':'#e6b85c','lab':'#9fb7e8','food':'#e07a5f','civ':'#d8a0b8','hub':'#66c2d4','farm':'#7fbf5a','out':'#4f8a3a','wat':'#2e7fb8'}
def rgb(ctx,h,a=1): ctx.set_source_rgba(int(h[1:3],16)/255,int(h[3:5],16)/255,int(h[5:7],16)/255,a)
def ease(u): u=max(0,min(1,u)); return u*u*(3-2*u)
def cell(ctx,x,k):
    rgb(ctx,'#16233a'); ctx.rectangle(x,TOP,CW,FLOOR-TOP); ctx.fill()
    c=COL[k]; H=FLOOR-TOP
    if k in ('res','lab','food','civ'):
        n={'res':7,'lab':6,'food':4,'civ':5}[k]; rise=H*({'res':.78,'lab':.72,'food':.4,'civ':.55}[k])/n; tr=(CW/2-10)/n
        for side in (0,1):
            for i in range(n):
                w=CW/2-10-tr*i; y=FLOOR-rise*(i+1)
                rgb(ctx,c); ctx.rectangle(x if side==0 else x+CW-w,y,w,rise+1); ctx.fill()
                rgb(ctx,'#6f8b52'); ctx.rectangle(x if side==0 else x+CW-w,y-2,w,2); ctx.fill()
        if k=='lab': rgb(ctx,'#6d7fa8'); ctx.rectangle(x,FLOOR-30,CW,30); ctx.fill()
    elif k=='farm':
        for i in range(9):
            y=FLOOR-12-i*12; rgb(ctx,'#5b4630'); ctx.rectangle(x,y+4,CW,3); ctx.fill(); rgb(ctx,c); ctx.rectangle(x,y,CW,4); ctx.fill()
    elif k=='out':
        ctx.move_to(x,FLOOR); ctx.line_to(x,FLOOR-130); ctx.curve_to(x+30,FLOOR-100,x+40,FLOOR-30,x+56,FLOOR-10)
        ctx.curve_to(x+72,FLOOR-30,x+82,FLOOR-100,x+CW,FLOOR-130); ctx.line_to(x+CW,FLOOR); ctx.close_path(); rgb(ctx,c); ctx.fill()
        rgb(ctx,'#2e7fb8'); ctx.rectangle(x+44,FLOOR-8,24,8); ctx.fill()
    elif k=='wat':
        rgb(ctx,'#c9b27a'); ctx.move_to(x,FLOOR); ctx.line_to(x,FLOOR-70); ctx.line_to(x+26,FLOOR-14); ctx.line_to(x+CW-26,FLOOR-14); ctx.line_to(x+CW,FLOOR-70); ctx.line_to(x+CW,FLOOR); ctx.close_path(); ctx.fill()
        rgb(ctx,c); ctx.rectangle(x+24,FLOOR-14,CW-48,14); ctx.fill()
    elif k=='hub':
        rgb(ctx,c,.8); ctx.rectangle(x,FLOOR-60,CW,60); ctx.fill(); rgb(ctx,c); ctx.rectangle(x+CW/2-8,TOP,16,H-60); ctx.fill()
    rgb(ctx,'#7fd6ec',.3); ctx.rectangle(x,TOP,CW,6); ctx.fill()
    rgb(ctx,'#0a0b10'); ctx.rectangle(x+CW-1,TOP,2,BASE1-TOP); ctx.fill()
def train(ctx,x,y,c,d):
    for i in range(4):
        cx=x-d*i*46
        rgb(ctx,c); ctx.rectangle(cx-20,y-8,40,16); ctx.fill()
        rgb(ctx,'#0a0b10',.55)
        for w in range(3): ctx.rectangle(cx-15+w*11,y-4,7,5); ctx.fill()
    nx=x+d*20; ctx.move_to(nx,y-8); ctx.line_to(nx+d*10,y); ctx.line_to(nx,y+8); ctx.close_path(); rgb(ctx,c); ctx.fill()
def pos(t,d):
    per=8/3; k=int(t//per); f=(t%per)/per
    mv=ease((f-.3)/.7)                         # stopped at the station for the first 30 %
    return (224+448*(k+mv)*d)%LW
def draw(ctx,t):
    rgb(ctx,'#0a0b10'); ctx.paint()
    for i,k in enumerate(TYPES): cell(ctx,i*CW,k)
    # hardware base and the two tracks
    rgb(ctx,'#3a3530'); ctx.rectangle(0,BASE0,LW,BASE1-BASE0); ctx.fill()
    for y in (309,335):
        rgb(ctx,'#8a806c'); ctx.rectangle(0,y+9,LW,2); ctx.fill()
    for i,x in enumerate((224,672,1120)):
        rgb(ctx,'#f0b860'); ctx.rectangle(x-36,BASE0+2,72,4); ctx.fill()
        rgb(ctx,'#f0b860',.5); ctx.rectangle(i*448,BASE0,2,BASE1-BASE0); ctx.fill()
    for (y,c,d) in ((309,'#f0b860',1),(335,'#66c2d4',-1)):
        x=pos(t,d)
        for off in (-LW,0,LW): train(ctx,x+off,y,c,d)
    text(ctx,'DISTRICT TRAINS',16,48,32,'#f0b860',bold=True)
    text(ctx,'RING UNROLLED · STOPS AT EACH DISTRICT',LW-16,48,30,'#b8ab8e',anchor='r')
    for i,x in enumerate((224,672,1120)): text(ctx,f'D{i+1}',x,LH-6,30,'#ece6d8',anchor='c',bold=True)
def render(path,t,W):
    S=W/LW; surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,round(LW*S),round(LH*S)); ctx=cairo.Context(surf); ctx.scale(S,S); draw(ctx,t); surf.write_to_png(path)
if __name__=='__main__':
    if sys.argv[1]=='still': render('img/f_train.png',1.6,4032)
    else:
        W=int(sys.argv[2]); os.makedirs('anim/tf',exist_ok=True)
        for i in range(120): render(f'anim/tf/f{i:03d}.png',i/15,W)
