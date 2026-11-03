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

def c1(ctx,t,dur):
    background(ctx); head(ctx)
    u=ease(seg(t,0,3)); sx=lerp(1400,700,u)
    ship(ctx,sx,Y-90,.6,door=1)
    core=seg(t,3,5)
    if core>0:
        cx0=lerp(sx+60,580,ease(core)); truss_h(ctx,cx0,cx0+120,Y,30,CY,step=12)
    tg=ease(seg(t,5,8))
    if t>5:
        xl=580; xr=700
        ship(ctx,lerp(xl-TL-500,xl-TL,tg),Y,.35); ship(ctx,lerp(xr+TL+500,xr+TL,tg),Y,.35,flip=True)
        if tg>=1: puff(ctx,xl-40,Y-8,0,-1,t,0); puff(ctx,xr+40,Y+8,0,1,t,3)
    label(ctx,'CARGO STARSHIP with the spine core',860,170,sx+150,Y-95,FG,a=seg(t,1,2))
    label(ctx,'SPINE CORE · 200 m truss + docks',520,480,640,Y+16,CY,a=seg(t,4.5,5.5))
    label(ctx,'TUG STARSHIPS dock at both ends',140,200,500,Y-8,GOLD,a=seg(t,7,8))
    caption(ctx,'1 · THE SPINE STARTS AS ONE CORE','A cargo Starship sets out the first spine section with docking ports. Two tug Starships latch onto its ends: from now on they steer the structure, holding its attitude and position with small thruster pulses.')
    fade(ctx,t,dur)

def c2(ctx,t,dur):
    background(ctx); head(ctx); tag(ctx,'TIME-LAPSE',880,110)
    f=ease(seg(t,.8,10)); xl=lerp(580,170,f); xr=lerp(700,1110,f)
    truss_h(ctx,xl,xr,Y,30,CY,step=14)
    for x in (xl,xr): ctx.rectangle(x-5,Y-18,10,36); col(ctx,GOLD); ctx.fill()
    tugs(ctx,xl,xr,t)
    gauge(ctx,t)
    km=lerp(.2,14,f)
    readout(ctx,'SPINE LENGTH',f'{km:4.1f} km',60,110)
    label(ctx,'EXTRUDER HEADS at both tips',260,470,xl+5,Y+18,GOLD,a=seg(t,1.5,2.5))
    label(ctx,'tugs move out with the tips',620,520,xr+40,Y+10,FG,a=seg(t,3,4))
    caption(ctx,'2 · THE SPINE GROWS BOTH WAYS','Extruders at both tips lay truss bays, fed by cargo ships, until the spine is 14 km long (~1 Mt). Pointed along the orbit\'s normal, a long body like this is naturally stable, so the tugs only trim it.')
    fade(ctx,t,dur)

def c3(ctx,t,dur):
    background(ctx); head(ctx); tag(ctx,'ONE CENTRE POD · CLOSE UP',1040,110)
    yc=330; x0,x1=460,820; y0,y1=yc-160,yc+160
    truss_h(ctx,0,1280,yc,150,CYD,step=40,lw=2)
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
    caption(ctx,'3 · BUILDING ONE CENTRE POD AROUND THE SPINE','Arms riding the spine set two magnetic bearings, a motor ring and the drum shell, then six spoke sockets and a lock into the spine. The pod spins with its ring; the spine stays still.')
    fade(ctx,t,dur)

HX=[260,400,540,740,880,1020]
def pod(ctx,x,a=1,s=1):
    col(ctx,PANEL,.85*a); ctx.rectangle(x-14*s,Y-34*s,28*s,68*s); ctx.fill()
def c4(ctx,t,dur):
    background(ctx); head(ctx)
    truss_h(ctx,170,1110,Y,30,CY,step=14)
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

def c5(ctx,t,dur):
    card(ctx,'THE CENTRE POD AND THE SPINE',[
        ('Spine','14 km non-rotating truss, ~200 m across, ~1 Mt of lunar aluminium and basalt fibre'),
        ('Steering','2–4 tug Starships at the tips: attitude, position and damping during the build'),
        ('Build attitude','Axis along the orbit normal: a stable attitude, so tugs only trim (~12 t propellant a day at ±0.1°)'),
        ('Centre pod','Ø 400 m drum, 500 m long: 2 magnetic bearings, motor ring, 6 spoke sockets, lock'),
        ('Loads','Tracking the Sun puts ~2.5 × 10¹¹ N·m on each pod: ~0.5 GN on its bearings'),
        ('Spin-up','Motor ring pushes each ring against its twin through the spine: ~70 days at 2.5 GW'),
    ],t,dur,'order-of-magnitude design study')

SCENES=[('sc1',c1,9),('sc2',c2,11),('sc3',c3,13.5),('sc4',c4,11),('sc5',c5,7)]
if __name__=='__main__': main(SCENES,'centre-pod-and-spine')
