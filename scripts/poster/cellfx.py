"""Small moving details over the cell cross-sections (flying cars, drones, instruments). 8 s loop."""
import sys, math, json, cairo, os
R=json.load(open('cellrects.json')); GW,GH=R['grid'][2],R['grid'][3]
TAU=2*math.pi; LOOP=8.0
def rgb(ctx,h,a=1): ctx.set_source_rgba(int(h[1:3],16)/255,int(h[3:5],16)/255,int(h[5:7],16)/255,a)
def osc(t,per,ph=0): return math.sin(TAU*(t/per)+ph)        # per must divide 8 s
def car(ctx,x,y,c='#d0302b',t=0,ph=0,cross=False):
    rgb(ctx,'#ffd27a',.55+.45*abs(osc(t,.5,ph))); ctx.new_path(); ctx.arc(x-3,y+3.2,1.4,0,TAU); ctx.arc(x+3,y+3.2,1.4,0,TAU); ctx.fill()
    rgb(ctx,c); ctx.new_path(); ctx.rectangle(x-5.5,y-1.6,11,3.6); ctx.fill()
    rgb(ctx,'#bfe0f0'); ctx.rectangle(x-2.5,y-3.4,5,1.9); ctx.fill()
    if cross: rgb(ctx,'#d0302b'); ctx.rectangle(x-.6,y-1.2,1.2,2.8); ctx.rectangle(x-1.4,y-.4,2.8,1.2); ctx.fill()
def drone(ctx,x,y,t):
    rgb(ctx,'#e8e2d4'); ctx.rectangle(x-2.5,y-1,5,2); ctx.fill()
    s=abs(osc(t,.25))*2.4+1
    rgb(ctx,'#9fd8e4',.8); ctx.rectangle(x-4.5-s/2,y-2,s,.8); ctx.rectangle(x+4.5-s/2,y-2,s,.8); ctx.fill()
def FX(ctx,key,t):
    if key=='res':
        car(ctx,80,126+22*osc(t,4),t=t); car(ctx,100,118+26*osc(t,4,2.2),c='#e6b85c',t=t,ph=1)
        car(ctx,48,100+10*osc(t,2,1.0),c='#66c2d4',t=t,ph=2)
    elif key=='lab':
        cx,cy=158,72; a=TAU*t/4; rgb(ctx,'#e8e2d4'); ctx.set_line_width(1.2)
        ctx.move_to(cx,cy+5); ctx.line_to(cx,cy); ctx.stroke()
        ctx.save(); ctx.translate(cx,cy); ctx.scale(math.cos(a),1); ctx.new_path(); ctx.arc(0,-2,4.5,math.pi,TAU); ctx.restore(); ctx.stroke()
        rgb(ctx,'#ff6b5a',.3+.7*(osc(t,1)>0)); ctx.new_path(); ctx.arc(22,70,1.6,0,TAU); ctx.fill()
        drone(ctx,90+30*osc(t,8),104+4*osc(t,2),t)
    elif key=='farm':
        for k,y in enumerate((133,121)):
            x=22+136*(((t/4)+k*.5)%1); drone(ctx,x,y,t)
    elif key=='out':
        car(ctx,90+40*osc(t,8),70+8*osc(t,2),c='#e6b85c',t=t)
        x=40+100*((t/8)%1); y=58+3*osc(t,1); f=3*osc(t,.5)
        rgb(ctx,'#e8e2d4'); ctx.set_line_width(1); ctx.move_to(x-4,y-f); ctx.line_to(x,y); ctx.line_to(x+4,y-f); ctx.stroke()
    elif key=='wat':
        x=73+9*osc(t,8); rgb(ctx,'#e8e2d4'); ctx.move_to(x-5,151.4); ctx.line_to(x+5,151.4); ctx.line_to(x+3,153.2); ctx.line_to(x-3,153.2); ctx.close_path(); ctx.fill()
        ctx.move_to(x,151.4); ctx.line_to(x,144); ctx.line_to(x+4,150.4); ctx.close_path(); rgb(ctx,'#f0b860'); ctx.fill()
        # diver dropping from the tower each 4 s
        u=(t%4)/1.2
        if u<1: rgb(ctx,'#ffe29a'); ctx.new_path(); ctx.arc(91,135+17*u*u,1.4,0,TAU); ctx.fill()
        car(ctx,112,98+14*osc(t,4,1),c='#66c2d4',t=t)
    elif key=='food':
        car(ctx,78,112+16*osc(t,4),t=t); car(ctx,104,100+18*osc(t,4,2.6),c='#d8a0b8',t=t,ph=1)
    elif key=='park':
        u=(t%2)/2; x=70+40*u; y=150-26*4*u*(1-u); rgb(ctx,'#ffffff'); ctx.new_path(); ctx.arc(x,y,1.8,0,TAU); ctx.fill()
        cy=138-50*((math.sin(TAU*t/8-math.pi/2)+1)/2); rgb(ctx,'#e07a5f'); ctx.new_path(); ctx.arc(147,cy,2,0,TAU); ctx.fill()
        rgb(ctx,'#e8e2d4',.6); ctx.set_line_width(.6); ctx.move_to(147,cy); ctx.line_to(147,82); ctx.stroke()
    elif key=='civ':
        car(ctx,90,118+20*osc(t,4),c='#ffffff',t=t,cross=True)
        car(ctx,60,96+8*osc(t,2,1),c='#66c2d4',t=t,ph=2)
    elif key=='hw':
        for i,x in enumerate((48.4,69.2,90.0,110.8,131.6)):
            a=TAU*t*(1 if i%2 else -1)/2
            rgb(ctx,'#e8e2d4',.9); ctx.set_line_width(1.2)
            for k in range(3):
                b=a+k*TAU/3; ctx.move_to(x,116.6); ctx.line_to(x+5*math.cos(b),116.6+5*math.sin(b))
            ctx.stroke()
        rgb(ctx,'#7fe7ff',.3+.5*abs(osc(t,2))); ctx.rectangle(14,108,152,2); ctx.fill()
    elif key=='ind':
        bx,by=90,113; a1=-math.pi/2+.7*osc(t,4); a2=a1+.9+.6*osc(t,4,1.2)
        x1,y1=bx+14*math.cos(a1),by+14*math.sin(a1); x2,y2=x1+11*math.cos(a2),y1+11*math.sin(a2)
        rgb(ctx,'#66c2d4'); ctx.set_line_width(2.6); ctx.move_to(bx,by); ctx.line_to(x1,y1); ctx.line_to(x2,y2); ctx.stroke()
        rgb(ctx,'#e8e2d4'); ctx.rectangle(bx-4,by-2,8,3); ctx.fill()
        if osc(t,1)>.3:
            rgb(ctx,'#ffe29a')
            for k in range(4): ctx.new_path(); ctx.arc(x2+3*math.cos(k*1.6+t*9),y2+3*math.sin(k*1.6+t*9),.8,0,TAU); ctx.fill()
        drone(ctx,40+100*((t/4)%1),98,t)
    elif key=='hub':
        y=80+50*osc(t,4); rgb(ctx,'#ffe29a'); ctx.rectangle(86,y-5,8,10); ctx.fill()
        rgb(ctx,'#0a0b10',.5); ctx.rectangle(87.5,y-3,5,3); ctx.fill()
        rgb(ctx,'#ff6b5a',.3+.7*(osc(t,1)>0)); ctx.new_path(); ctx.arc(40,112,1.6,0,TAU); ctx.arc(140,112,1.6,0,TAU); ctx.fill()
def draw(ctx,t):
    for key,(x,y,w,h) in R['cells'].items():
        ctx.save(); ctx.translate(x,y); ctx.scale(w/180,h/184)
        ctx.new_path(); ctx.arc(90,92,76,0,TAU); ctx.clip()
        FX(ctx,key,t); ctx.restore()
def render(path,t,S):
    surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,round(GW*S),round(GH*S)); ctx=cairo.Context(surf); ctx.scale(S,S); draw(ctx,t); surf.write_to_png(path)
if __name__=='__main__':
    if sys.argv[1]=='still': render('img/cellfx.png',1.3,6)
    else:
        S=float(sys.argv[2]); os.makedirs('anim/cf',exist_ok=True)
        for i in range(120): render(f'anim/cf/f{i:03d}.png',i/15,S)
