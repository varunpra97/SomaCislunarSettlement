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

ROD='#f6f3ec'
def rod(ctx,x0,x1,y=Y,h=8,a=1,blur=0.0):
    """The Starship core drawn as one white rod; blur>0 spreads it into a soft glow (diffusion)."""
    if x1<=x0 or a<=0: return
    for i in range(6,0,-1):
        r=h/2+blur*i/6+2*i
        col(ctx,ROD,a*.05*(1-blur/40)); ctx.rectangle(x0-r*.5,y-r,x1-x0+r,2*r); ctx.fill()
    col(ctx,ROD,a*max(0,1-blur/30)); ctx.rectangle(x0,y-h/2,x1-x0,h); ctx.fill()

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
    # Opens on scene 1's docked chain; each ship fades out (centre first) as a white rod diffuses in over it.
    x0=150; N=11; xe=x0+N*SL
    d=seg(t,1.0,5.0)
    for i in range(N):
        k=abs(i-(N-1)/2)/((N-1)/2)
        fo=1-ease(seg(d,k*.45,k*.45+.55))
        if fo>0: ship(ctx,x0+i*SL,Y,.35,a=.92*fo)
        g=seg(d,k*.45,k*.45+.55)*(1-seg(d,.85,1))
        if g>0:
            cx=x0+i*SL+SL/2
            for j in range(5,0,-1):
                ctx.arc(cx,Y,6+j*7*g,0,2*math.pi); col(ctx,ROD,.07*g*(1-j/6)); ctx.fill()
    if d<1:
        puff(ctx,x0-6,Y,-1,0,t,1,a=1-d); puff(ctx,xe-20,Y+8,0,1,t,3,a=1-d)
    rod(ctx,x0,xe,a=ease(d),blur=30*(1-ease(seg(d,.2,1))))
    gauge(ctx,t)
    f=ease(seg(t,1.0,8.5))
    n=int(lerp(11,280,f))
    readout(ctx,'STARSHIPS IN THE SPINE',f'{n}',60,110,w=230)
    readout(ctx,'LENGTH',f'{n*0.05:4.1f} km',300,110,CY,w=150)
    label(ctx,'the docked hulls, drawn from here as one rod',420,470,(x0+xe)/2,Y+6,FG,a=seg(t,4.6,5.6))
    label(ctx,'280 hulls · ~30 kt of steel · 14 km',820,520,xe-60,Y+6,SHIP,a=seg(t,6,7))
    caption(ctx,'2 · 280 SHIPS LATER, A 14 km CORE','Each delivery flight ends by adding its ship to the spine. The bare hulls hold only about 0.02% of the bending load the spine will need once rings spin, so for now it only has to carry the gentle steering loads of the build.')
    fade(ctx,t,dur)

def c3(ctx,t,dur):
    background(ctx); head(ctx); tag(ctx,'ONE CENTRE POD · CLOSE UP',1040,110)
    yc=330; x0,x1=460,820; y0,y1=yc-160,yc+160
    for i,r in enumerate(DR):
        for sg in (-1,1):
            col(ctx,PANEL if i%2==0 else "#a99b7f",.55); ctx.rectangle(0,yc+sg*r*.8-(1.5 if sg<0 else 0),1280,1.5); ctx.fill()
    col(ctx,CY,.08); ctx.rectangle(0,yc-80,1280,160); ctx.fill()
    rod(ctx,0,1280,yc,h=10)
    text(ctx,"spine drums already in place (r 100 m)",60,yc-88,11,CY,a=.8)
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
    caption(ctx,'4 · BUILDING ONE CENTRE POD AROUND THE SPINE','Arms riding the thickened spine set two magnetic bearings on a frame, a motor ring and the drum shell, then six spoke sockets and a lock into the corridor. The pod spins with its ring; the spine stays still.')
    fade(ctx,t,dur)

HX=[260,400,540,740,880,1020]
def pod(ctx,x,a=1,s=1):
    col(ctx,PANEL,.85*a); ctx.rectangle(x-14*s,Y-34*s,28*s,68*s); ctx.fill()
def c4(ctx,t,dur):
    background(ctx); head(ctx)
    rod(ctx,170,1110,h=12)
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
    caption(ctx,'5 · SIX PODS FOR THREE RING PAIRS','Pods go on 2 km apart. Neighbouring rings will spin in opposite directions, so each pair cancels its spin and the spine as a whole can be turned easily. The tugs keep steering while the mass grows.')
    fade(ctx,t,dur)

DR=[20,40,60,80,100]
NSEG=24  # rail-ring segments
def ring_side(ctx,x,yc,R,n=NSEG,c=CY,a=1,w=4):
    """A rail ring around the spine seen from the side (a thin ellipse), drawn n segments of NSEG."""
    for j in range(int(n)):
        a0=-math.pi/2+j*2*math.pi/NSEG; a1=a0+2*math.pi/NSEG*.86
        ctx.save(); ctx.translate(x,yc); ctx.scale(.09,1); ctx.new_path(); ctx.arc(0,0,R,a0,a1); ctx.restore()
        col(ctx,c,a); ctx.set_line_width(w); ctx.stroke()
def drum_factory(ctx,xf,yc,R,dirn,nf=NSEG,nr=NSEG,beams=1.0,t=0,a=1):
    """Bay-factory layout around the spine: front work ring, rear gripper ring, telescoping beams, carts."""
    xr=xf-dirn*30
    if beams>0:
        col(ctx,GOLD,.8*a*beams); ctx.set_line_width(2)
        for yy in (yc-R,yc-R*.55,yc+R*.55,yc+R): ctx.move_to(xr,yy); ctx.line_to(xf,yy)
        ctx.stroke()
    ring_side(ctx,xr,yc,R,nr,'#3f8796',a)
    ring_side(ctx,xf,yc,R,nf,CY,a)
    if nf>=NSEG and beams>=1:
        for j in range(4):  # carts riding the front ring
            ph=t*.9+j*math.pi/2; yy=yc-R*math.cos(ph)
            col(ctx,GOLD,a); ctx.rectangle(xf-5,yy-4,10,8); ctx.fill()
        for sg in (-1,1):  # gripper pads on the rear ring
            col(ctx,SPARK,.8*a); ctx.rectangle(xr-4,yc+sg*R-sg*6-3,8,6); ctx.fill()

def c4b(ctx,t,dur):
    background(ctx); head(ctx); tag(ctx,'DRUM FACTORY · A SECTION OF SPINE',940,110)
    yc=330; k=1.5  # px per m
    x0,x1=170,1110
    T0,TP=6.2,3.5  # first pass starts at T0; each pass (re-ring + lay one drum) takes TP
    cum=0.0; m=0.0; need=397.9
    # which pass are we in, and where is the factory
    ip=max(0,min(4,int((t-T0)//TP))) if t>=T0 else -1
    def fx(i,tt):
        u=ease(seg(tt,T0+i*TP+.5,T0+(i+1)*TP-.1))
        return lerp(x0,x1,u) if i%2==0 else lerp(x1,x0,u)
    # drums laid so far (drawn first, under the factory)
    for i,r in enumerate(DR):
        if t<T0+i*TP+.5: continue
        u=ease(seg(t,T0+i*TP+.5,T0+(i+1)*TP-.1))
        xe=fx(i,t)-(30 if i%2==0 else -30)*(u<1)
        xa,xb=(x0,max(x0,xe)) if i%2==0 else (min(x1,xe),x1)
        for sg in (-1,1):
            yy=yc+sg*r*k
            col(ctx,PANEL if i%2==0 else '#a99b7f',.85); ctx.rectangle(xa,yy-3 if sg<0 else yy,xb-xa,3); ctx.fill()
        col(ctx,CY,.10); ctx.rectangle(xa,yc-r*k,xb-xa,2*r*k); ctx.fill()
        cum+=r*r*0.02*u; m+=2*math.pi*r*0.02*2700*u
    rod(ctx,0,1280,yc,h=max(8,9*k))
    # factory size: grows one size up at the start of each pass
    if ip<0: R=DR[0]*k+14
    else:
        prev=DR[max(0,ip-1)]*k+14; new=DR[ip]*k+14
        R=lerp(prev,new,ease(seg(t,T0+ip*TP,T0+ip*TP+.5)))
    dirn=1 if ip<=0 or ip%2==0 else -1
    xf=x0+30 if ip<0 else fx(ip,t)
    if ip>=0 and t>T0+ip*TP+.5 and t<T0+(ip+1)*TP-.1:
        xf+=dirn*3*math.sin(t*14)  # inchworm shuffle while it moves
    # assembly: hub arrives, then rings bolt together segment by segment, then beams
    nf=NSEG*seg(t,2.2,4.2); nr=NSEG*seg(t,3.8,5.2); bm=seg(t,5.0,5.8)
    if t>2.2: drum_factory(ctx,xf,yc,R,dirn,nf,nr,bm,t)
    hx=lerp(1400,xf+8,ease(seg(t,.4,2.2)))
    ship(ctx,hx,yc-R-24,.3,door=1 if 2.2<t<5.8 else 0)
    # folded segments flying from the hub's cargo door to the ring while it is assembled
    if 2.2<t<5.2:
        for j in range(3):
            ph=((t*1.6+j/3)%1.0); sx=lerp(xf+30,xf,ph); sy=lerp(yc-R-20,yc-R*math.cos(ph*math.pi),ph)
            col(ctx,GOLD,.9); ctx.rectangle(sx-4,sy-3,8,6); ctx.fill()
    # one supply Starship per pass: arrives, docks under the factory with drum panels, leaves
    if ip>=0:
        tp=T0+ip*TP; side=1 if dirn>0 else -1
        arr=ease(seg(t,tp,tp+1.0)); dep=ease(seg(t,tp+2.6,tp+3.4))
        sx=lerp(1400 if side>0 else -150,xf+8,arr)+dep*(1500 if side>0 else -1500)
        ship(ctx,sx,yc+R+24,.3,door=1 if arr>=1 and dep<=0 else 0)
        if arr>=1 and dep<=0:
            ph=(t*2.2)%1.0
            col(ctx,PANEL,.95); ctx.rectangle(lerp(xf+40,xf,ph)-5,lerp(yc+R+16,yc+R-4,ph)-3,10,6); ctx.fill()
    pct=cum/need*100
    readout(ctx,'BENDING STRENGTH vs NEEDED',f'{max(pct,0.02):5.1f} %',60,110,GOLD if pct<100 else GREEN,w=260)
    readout(ctx,'SPINE MASS',f'{m*14000/1e9:4.2f} Mt',330,110,CY,w=170)
    readout(ctx,'DRUMS',f'{max(0,ip+(1 if t>T0+(ip+1)*TP-.1 else 0)) if ip>=0 else 0} of 5',520,110,FG,w=120)
    label(ctx,'STARSHIP CORE',140,yc+60,230,yc+6,SHIP,a=seg(t,.3,1)*(1-seg(t,5.5,6.3)))
    label(ctx,'HUB STARSHIP brings the factory, folded',560,200,hx+40,yc-R-30,FG,a=seg(t,1.0,1.8)*(1-seg(t,5.6,6.4)))
    label(ctx,'carts bolt rail-ring segments around the core',560,540,x0+30,yc+R,CY,a=seg(t,2.6,3.4)*(1-seg(t,6.0,6.8)))
    label(ctx,'DRUM FACTORY: a bay factory sized for the spine',620,215,xf,yc-R,CY,a=seg(t,5.6,6.4)*(1-seg(t,11.0,11.8)))
    label(ctx,'SUPPLY STARSHIP · drum panels',760,560,(xf+60) if ip>=0 else 900,yc+R+24,PANEL,a=seg(t,7.0,7.8)*(1-seg(t,11.5,12.3)))
    label(ctx,'it re-rings one size up for each drum',820,205,xf,yc-R,GOLD,a=seg(t,12.0,12.8)*(1-seg(t,16.5,17.3)))
    label(ctx,'5 CONCENTRIC DRUMS, r 20 to 100 m, ~2 cm walls',700,560,900,yc+100*k,PANEL,a=seg(t,T0+4*TP+.6,T0+4*TP+1.4))
    caption(ctx,'3 · THICKEN: A DRUM FACTORY WRAPS THE STARSHIP CORE','Starships bring a bay factory sized for the spine; its rings bolt together around the hulls, then it inchworms the 14 km laying one drum per pass, one size up each time. Five drums to r 100 m: ~1.4 Mt.')
    fade(ctx,t,dur)

def c5(ctx,t,dur):
    card(ctx,'THE CENTRE POD AND THE SPINE',[
        ('Spine core','280 Starships nose to tail: 14 km, one 9 m pressurised corridor'),
        ('Spine ships','A spine-only variant can drop the heat shield, flaps and legs'),
        ('Spine drums','Next, 5 concentric drums out to r 100 m: ~1.4 Mt'),
        ('Why drums','A 9 m core holds 0.02% of the load (≤0.5% with a composite hull)'),
        ('Steering','The end Starships keep their engines during the build'),
        ('Centre pod','Ø 400 m drum: 2 magnetic bearings, motor ring, 6 spoke sockets'),
        ('Spin-up','Each ring pushes against its twin through the spine: ~70 days'),
    ],t,dur,'order-of-magnitude design study')

SCENES=[('sc1',c1,12),('sc2',c2,10),('sc4b',c4b,24.5),('sc3',c3,13.5),('sc4',c4,11),('sc5',c5,7)]
if __name__=='__main__': main(SCENES,'centre-pod-and-spine')
