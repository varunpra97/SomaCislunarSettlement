from common import *
def head(ctx): hdr(ctx,'THE CENTRE POD AND THE SPINE','A SHARED AXLE FOR SEVERAL RINGS')
Y=330; TL=91  # tug length at s=.35
def tugs(ctx,xl,xr,t,on=True,a=1):
    ship(ctx,xl-TL,Y,.35,a=a); ship(ctx,xr+TL,Y,.35,flip=True,a=a)
    if on:
        puff(ctx,xl-40,Y-8,0,-1,t,0,a); puff(ctx,xr+40,Y+8,0,1,t,3,a)
        puff(ctx,xl-TL-2,Y,-1,0,t*.7,5,a*.6)
def gauge(ctx,t,label_='AXIS: ALONG ORBIT NORMAL',wob=1.0,a=1):
    x,y=1130,150
    col(ctx,'#11131b',.9*a); ctx.rectangle(x-90,y-60,180,140); ctx.fill()
    ctx.new_path(); ctx.arc(x,y,40,0,2*math.pi); col(ctx,'#2c2a24',a); ctx.set_line_width(1); ctx.stroke()
    ang=math.radians(-90+3*wob*math.sin(t*1.3))
    col(ctx,GOLD,a); ctx.set_line_width(2); ctx.move_to(x-40*math.cos(ang),y-40*math.sin(ang)); ctx.line_to(x+40*math.cos(ang),y+40*math.sin(ang)); ctx.stroke()
    col(ctx,MUT,.5*a); ctx.set_dash([2,3]); ctx.move_to(x,y-44); ctx.line_to(x,y+44); ctx.stroke(); ctx.set_dash([])
    text(ctx,label_,x,y+62,10,MUT,anchor='c',a=a,spacing=1)
    text(ctx,'held to ±0.1°',x,y+76,10,GOLD,anchor='c',a=a)

SL=91  # one Starship body, px, in the close-up
def core_chain(ctx,x0,n,y=Y,a=1,s=.35):
    """n Starships docked nose to tail, noses pointing left, starting at x0."""
    for i in range(n): ship(ctx,x0+i*SL,y,s,a=a*.92)
def core_band(ctx,x0,x1,y=Y,h=8,a=1):
    if x1<=x0: return
    col(ctx,SHIP,a*.9); ctx.rectangle(x0,y-h/2,x1-x0,h); ctx.fill()
    col(ctx,'#8f8a7e',a); ctx.set_line_width(1)
    x=x0
    while x<x1: ctx.move_to(x,y-h/2); ctx.line_to(x,y+h/2); x+=6
    ctx.stroke()

def c1(ctx,t,dur):
    background(ctx); head(ctx)
    x0=150; N=11; per=.85; t0=.8
    n=max(0,min(N,int((t-t0)/per)))
    core_chain(ctx,x0,n)
    if n<N and t>t0:
        u=ease(((t-t0)%per)/per); xa=lerp(1400,x0+n*SL,u)
        ship(ctx,xa,Y,.35); 
        if u>.9: ctx.arc(x0+n*SL,Y,5,0,2*math.pi); col(ctx,SPARK,.8); ctx.fill()
    if n>=1:
        puff(ctx,x0-6,Y,-1,0,t,1); puff(ctx,x0+30,Y-8,0,-1,t,0)
    if n>=2:
        xr=x0+n*SL; puff(ctx,xr-20,Y+8,0,1,t,3)
    readout(ctx,'STARSHIPS IN THE SPINE',f'{n}',60,110,w=230)
    readout(ctx,'LENGTH',f'{n*50} m',300,110,CY,w=150)
    label(ctx,'each Starship docks nose to tail and stays',560,210,x0+SL*3.5,Y-8,FG,a=seg(t,2,3))
    label(ctx,'the end ships keep their engines: they steer',140,470,x0+20,Y+8,GOLD,a=seg(t,4,5))
    label(ctx,'inside: one pressurised corridor, 9 m across',620,470,x0+SL*5.5,Y+8,CY,a=seg(t,6,7))
    caption(ctx,'1 · THE SPINE IS MADE OF STARSHIPS','Instead of building a truss, cargo Starships unload and then dock nose to tail along the spin axis. Their stripped hulls become the spine\'s core, and the ships at each end keep their engines to steer it.')
    fade(ctx,t,dur)

def c2(ctx,t,dur):
    background(ctx); head(ctx); tag(ctx,'TIME-LAPSE',880,110)
    f=ease(seg(t,.8,8.5)); xl=lerp(600,170,f); xr=lerp(680,1110,f)
    core_band(ctx,xl,xr)
    tugs(ctx,xl,xr,t)
    gauge(ctx,t)
    n=int(lerp(11,280,f))
    readout(ctx,'STARSHIPS IN THE SPINE',f'{n}',60,110,w=230)
    readout(ctx,'LENGTH',f'{n*0.05:4.1f} km',300,110,CY,w=150)
    label(ctx,'280 hulls · ~30 kt of steel · 14 km',420,470,(xl+xr)/2,Y+6,SHIP,a=seg(t,2,3))
    label(ctx,'end Starships, drawn larger',820,520,xr+40,Y+10,GOLD,a=seg(t,3,4))
    caption(ctx,'2 · 280 SHIPS LATER, A 14 km CORE','Each delivery flight ends by adding its ship to the spine. The bare hulls hold only about 0.02% of the bending load the spine will need once rings spin, so for now it only has to carry the gentle steering loads of the build.')
    fade(ctx,t,dur)

def c3(ctx,t,dur):
    background(ctx); head(ctx); tag(ctx,'ONE CENTRE POD · CLOSE UP',1040,110)
    yc=330; x0,x1=460,820; y0,y1=yc-160,yc+160
    core_band(ctx,0,1280,yc,h=10)
    col(ctx,CY,.35); ctx.set_line_width(1); ctx.set_dash([4,6]); ctx.rectangle(0,yc-80,1280,160); ctx.stroke(); ctx.set_dash([])
    text(ctx,'room left for drums later (r 100 m)',60,yc-88,11,CY,a=.8)
    for xs_ in (x0+12,x1-12):
        col(ctx,STEEL,.8); ctx.set_line_width(2)
        for yy in (yc-80,yc+80): ctx.move_to(xs_,yc); ctx.line_to(xs_,yy)
        ctx.stroke()
    # bearings
    b=seg(t,.5,3.2)
    for bx in (x0+12,x1-12):
        n=int(16*b)
        for i in range(n):
            yy=y0+i*(y1-y0)/16; col(ctx,GLASS); ctx.rectangle(bx-8,yy+1,16,(y1-y0)/16-2); ctx.fill()
    # motor ring
    m=seg(t,3.2,5.5); n=int(16*m)
    for i in range(n):
        yy=y0+i*(y1-y0)/16; col(ctx,GOLD); ctx.rectangle(636-10,yy+1,20,(y1-y0)/16-2); ctx.fill()
    # shell panels
    s=seg(t,5.5,9)
    cols=12; rows=8; tot=int(cols*rows*s)
    for k in range(tot):
        i,j=k//rows,k%rows; px=x0+22+i*(x1-x0-44)/cols; py=y0+j*(y1-y0)/rows
        if abs(px+((x1-x0-44)/cols)/2-636)<14: continue
        col(ctx,PANEL,.55); ctx.rectangle(px+1,py+1,(x1-x0-44)/cols-2,(y1-y0)/rows-2); ctx.fill()
    ctx.rectangle(x0,y0,x1-x0,y1-y0); col(ctx,FG,.6); ctx.set_line_width(1.5); ctx.set_dash([5,5]); ctx.stroke(); ctx.set_dash([])
    # spoke sockets
    sk=seg(t,9,11)
    for xs in (560,712):
        for sg in (-1,1):
            h=60*ease(sk)
            col(ctx,CY); ctx.set_line_width(10); ctx.move_to(xs,yc+sg*160); ctx.line_to(xs,yc+sg*(160+h)); ctx.stroke()
    # transfer lock
    tl=seg(t,11,12.5)
    if tl>0: col(ctx,GREEN,tl); ctx.rectangle(600,yc-30,72,60); ctx.fill(); text(ctx,'LOCK',636,yc+5,12,BG,anchor='c',bold=True,a=tl)
    # robot arms on spine carts
    tgt=(x0+12,y0+b*(y1-y0)) if t<3.2 else (636,y0+m*(y1-y0)) if t<5.5 else (x0+40+s*(x1-x0-80),y0+40) if t<9 else (560,yc-160-60*sk)
    arm(ctx,(380,yc-75),tgt,150,140,CY,6)
    tgt2=(x1-12,y1-b*(y1-y0)) if t<3.2 else (636,y1-m*(y1-y0)) if t<5.5 else (x1-40-s*(x1-x0-80),y1-40) if t<9 else (712,yc+160+60*sk)
    arm(ctx,(900,yc+75),tgt2,150,140,CY,6,up=False)
    label(ctx,'MAGNETIC BEARINGS · 500 m apart',140,150,x0+12,y0+10,GLASS,a=seg(t,.8,1.6))
    label(ctx,'MOTOR RING spins the ring against its twin',830,560,636,y1-5,GOLD,a=seg(t,3.5,4.3))
    label(ctx,'HUB DRUM Ø 400 m',880,140,x1-5,y0+5,FG,a=seg(t,6,7))
    label(ctx,'6 SPOKE SOCKETS',150,560,560,yc+215,CY,a=seg(t,9.5,10.5))
    label(ctx,'STARSHIP CORE · 9 m',90,yc+130,200,yc+5,SHIP,a=seg(t,.5,1.5))
    caption(ctx,'3 · BUILDING ONE CENTRE POD AROUND THE CORE','Arms riding the Starship core set two magnetic bearings on a frame, a motor ring and the drum shell, then six spoke sockets and a lock into the corridor. The pod spins with its ring; the spine stays still.')
    fade(ctx,t,dur)

HX=[260,400,540,740,880,1020]
def pod(ctx,x,a=1,s=1):
    col(ctx,PANEL,.85*a); ctx.rectangle(x-14*s,Y-34*s,28*s,68*s); ctx.fill()
def c4(ctx,t,dur):
    background(ctx); head(ctx)
    core_band(ctx,170,1110)
    tugs(ctx,170,1110,t); gauge(ctx,t)
    n=0
    for i,x in enumerate(HX):
        a=seg(t,1+i*1.4,2+i*1.4)
        if a>0: pod(ctx,x,a); n+=a>=1
    # shuttle ship moving between sites
    k=min(5,int(max(0,t-1)/1.4)); ph=((t-1)%1.4)/1.4 if t>1 else 0
    sx=lerp(HX[k]+500,HX[k]+20,ease(min(1,ph*1.6))) if t<9.5 else 2000
    ship(ctx,sx,Y-80,.45,door=1)
    for j,(x0,x1,nm) in enumerate(((HX[0],HX[1],'PAIR A'),(HX[2],HX[3],'PAIR B'),(HX[4],HX[5],'PAIR C'))):
        a=seg(t,2+j*2.8,3+j*2.8); xm=(x0+x1)/2
        col(ctx,GOLD,.6*a); ctx.set_line_width(1); ctx.move_to(x0,Y+52); ctx.line_to(x0,Y+60); ctx.line_to(x1,Y+60); ctx.line_to(x1,Y+52); ctx.stroke()
        text(ctx,nm,xm,Y+80,13,GOLD,anchor='c',bold=True,a=a)
    readout(ctx,'CENTRE PODS',f'{n} of 6',60,110)
    label(ctx,'2 km between pods',600,520,(HX[2]+HX[3])/2,Y+20,FG,a=seg(t,4,5))
    caption(ctx,'4 · SIX PODS FOR THREE RING PAIRS','Pods go on 2 km apart. Neighbouring rings will spin in opposite directions, so each pair cancels its spin and the spine as a whole can be turned easily. The tugs keep steering while the mass grows.')
    fade(ctx,t,dur)

DR=[20,40,60,80,100]
def c4b(ctx,t,dur):
    background(ctx); head(ctx); tag(ctx,'A SECTION OF SPINE · LATER',990,110)
    yc=330; k=1.5  # px per m
    x0,x1=120,1160
    cum=0.0; m=0.0; need=397.9
    for i,r in enumerate(DR):
        f=ease(seg(t,.8+i*1.6,2.2+i*1.6))
        if f<=0: continue
        xe=lerp(x0,x1,f)
        for sg in (-1,1):
            yy=yc+sg*r*k
            col(ctx,PANEL if i%2==0 else '#a99b7f',.85); ctx.rectangle(x0,yy-3 if sg<0 else yy,xe-x0,3); ctx.fill()
        col(ctx,CY,.12); ctx.rectangle(x0,yc-r*k,xe-x0,2*r*k); ctx.fill()
        if f<1:
            for sg in (-1,1):
                ctx.rectangle(xe-10,yc+sg*r*k-8,20,16); col(ctx,GOLD); ctx.fill()
        cum+=r*r*0.02*f; m+=2*math.pi*r*0.02*2700*f
    core_band(ctx,0,1280,yc,h=max(8,9*k))
    pct=cum/need*100
    readout(ctx,'BENDING STRENGTH vs NEEDED',f'{max(pct,0.02):5.1f} %',60,110,GOLD if pct<100 else GREEN,w=260)
    readout(ctx,'SPINE MASS',f'{m*14000/1e9:4.2f} Mt',330,110,CY,w=170)
    label(ctx,'STARSHIP CORE',140,yc+40,200,yc+6,SHIP,a=seg(t,.3,1))
    label(ctx,'5 CONCENTRIC DRUMS, r 20 to 100 m, ~2 cm walls',700,560,900,yc+100*k,PANEL,a=seg(t,3,4))
    caption(ctx,'5 · LATER: CONCENTRIC DRUMS OVER THE STARSHIP CORE','Crawlers wrap drum after drum around the original hulls. Strength grows with the square of the radius, so five thin drums out to 100 m carry the Sun-tracking loads once the rings spin, for ~1.4 Mt.')
    fade(ctx,t,dur)

def c5(ctx,t,dur):
    card(ctx,'THE CENTRE POD AND THE SPINE',[
        ('Spine core','280 Starships nose to tail: 14 km, one 9 m pressurised corridor'),
        ('Spine ships','A spine-only variant can drop the heat shield, flaps and legs'),
        ('Spine drums','Later, 5 concentric drums out to r 100 m: ~1.4 Mt'),
        ('Why drums','A 9 m core holds 0.02% of the load (≤0.5% with a composite hull)'),
        ('Steering','The end Starships keep their engines during the build'),
        ('Centre pod','Ø 400 m drum: 2 magnetic bearings, motor ring, 6 spoke sockets'),
        ('Spin-up','Each ring pushes against its twin through the spine: ~70 days'),
    ],t,dur,'order-of-magnitude design study')

SCENES=[('sc1',c1,12),('sc2',c2,10),('sc3',c3,13.5),('sc4',c4,11),('sc4b',c4b,10.5),('sc5',c5,7)]
if __name__=='__main__': main(SCENES,'centre-pod-and-spine')
