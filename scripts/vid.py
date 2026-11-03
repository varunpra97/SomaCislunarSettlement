import cairo, math, random, subprocess, sys, os

W, H, FPS = 1280, 720, 30
OUT = os.path.dirname(os.path.abspath(__file__))

def hx(c, a=1.0):
    c = c.lstrip('#'); return (int(c[0:2],16)/255, int(c[2:4],16)/255, int(c[4:6],16)/255, a)

BG='#0a0b10'; FG='#ece6d8'; MUT='#a99f88'; GOLD='#f0b860'; CY='#66c2d4'; CYD='#3f8796'; GLASS='#7fd6ec'
KEEL='#c98a3a'; STEEL='#9a917f'; SHIP='#c9c5ba'; NOSE='#d6d2c8'; SOLAR='#20335a'; SOLARL='#6d8fd6'; SPARK='#ffe29a'; HULL='#2a2416'

clamp=lambda v,a=0.0,b=1.0:max(a,min(b,v))
lerp=lambda a,b,u:a+(b-a)*u
def ease(u):
    u=clamp(u); return 2*u*u if u<.5 else 1-(-2*u+2)**2/2
def seg(t,a,b): return clamp((t-a)/(b-a))

random.seed(3)
STARS=[(random.uniform(0,W),random.uniform(0,600),random.uniform(.5,1.4),random.uniform(.25,.8)) for _ in range(170)]

MONO='DejaVu Sans Mono'; SANS='Inter'

def col(ctx,c,a=1.0):
    r,g,b,aa=hx(c,a); ctx.set_source_rgba(r,g,b,aa)

def text(ctx,s,x,y,size,c=FG,font=MONO,bold=False,anchor='l',a=1.0,spacing=0):
    ctx.select_font_face(font,cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size); col(ctx,c,a)
    if spacing:
        w=sum(ctx.text_extents(ch).x_advance+spacing for ch in s)-spacing
    else:
        w=ctx.text_extents(s).x_advance
    if anchor=='c': x-=w/2
    elif anchor=='r': x-=w
    if spacing:
        for ch in s:
            ctx.move_to(x,y); ctx.show_text(ch); x+=ctx.text_extents(ch).x_advance+spacing
    else:
        ctx.move_to(x,y); ctx.show_text(s)

def wrap(ctx,s,size,font,maxw):
    ctx.select_font_face(font); ctx.set_font_size(size)
    words=s.split(); lines=[]; cur=''
    for w_ in words:
        t=(cur+' '+w_).strip()
        if ctx.text_extents(t).x_advance>maxw and cur: lines.append(cur); cur=w_
        else: cur=t
    if cur: lines.append(cur)
    return lines

def background(ctx):
    col(ctx,BG); ctx.paint()
    for x,y,r,a in STARS:
        ctx.arc(x,y,r,0,2*math.pi); col(ctx,'#ffffff',a); ctx.fill()

def header(ctx):
    text(ctx,'THE BAY FACTORY',40,44,15,MUT,spacing=3)
    text(ctx,'DEPLOYMENT AND OPERATION',40,66,12,'#6b6252',spacing=2)

def caption(ctx,step,body):
    col(ctx,'#11131b',.92); ctx.rectangle(40,600,1200,100); ctx.fill()
    col(ctx,'#2c2a24'); ctx.set_line_width(1); ctx.rectangle(40.5,600.5,1199,99); ctx.stroke()
    col(ctx,GOLD); ctx.rectangle(40,600,4,100); ctx.fill()
    text(ctx,step,64,630,14,GOLD,bold=True,spacing=2)
    lines=wrap(ctx,body,19,SANS,1150)
    for i,l in enumerate(lines[:2]): text(ctx,l,64,660+i*26,19,FG,font=SANS)

def tag(ctx,s,x,y,c=CY):
    ctx.select_font_face(MONO,cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(12)
    w=ctx.text_extents(s).x_advance+16
    col(ctx,c); ctx.rectangle(x,y-15,w,22); ctx.fill()
    text(ctx,s,x+8,y,12,BG,bold=True)

def label(ctx,s,x,y,tx,ty,c=FG,a=1.0,size=13,anchor='l'):
    col(ctx,c,.6*a); ctx.set_line_width(1); ctx.move_to(tx,ty); ctx.line_to(x,y+(-4)); ctx.stroke()
    text(ctx,s,x+(4 if anchor=='l' else -4),y,size,c,anchor=anchor,a=a)

def starship(ctx,x,y,s=1.0,door=0.0,a=1.0):
    # nose tip at (x, y+18s), body to the right
    L=260*s; Hh=36*s; n=34*s
    col(ctx,NOSE,a); ctx.move_to(x+n,y); ctx.curve_to(x+n*.4,y+2*s,x+4*s,y+Hh*.3,x,y+Hh/2); ctx.curve_to(x+4*s,y+Hh*.7,x+n*.4,y+Hh-2*s,x+n,y+Hh); ctx.close_path(); ctx.fill()
    col(ctx,SHIP,a); ctx.rectangle(x+n,y,L-n,Hh); ctx.fill()
    col(ctx,'#a8a49a',a); ctx.move_to(x+L-30*s,y); ctx.line_to(x+L+4*s,y-18*s); ctx.line_to(x+L,y); ctx.close_path(); ctx.fill()
    ctx.move_to(x+L-30*s,y+Hh); ctx.line_to(x+L+4*s,y+Hh+18*s); ctx.line_to(x+L,y+Hh); ctx.close_path(); ctx.fill()
    if door>0:
        col(ctx,'#1a1810',a); ctx.rectangle(x+90*s,y+2*s,90*s,Hh*.5); ctx.fill()

def ik(b,t,L1,L2,up=True):
    dx,dy=t[0]-b[0],t[1]-b[1]; d=math.hypot(dx,dy); m=L1+L2-.5
    tx,ty=t
    if d>m: tx=b[0]+dx/d*m; ty=b[1]+dy/d*m; d=m
    d=max(d,1); a=math.atan2(ty-b[1],tx-b[0]); B=math.acos(clamp((L1*L1+d*d-L2*L2)/(2*L1*d),-1,1))
    e1=(b[0]+L1*math.cos(a+B),b[1]+L1*math.sin(a+B)); e2=(b[0]+L1*math.cos(a-B),b[1]+L1*math.sin(a-B))
    e=(e1 if e1[1]<e2[1] else e2) if up else (e1 if e1[1]>e2[1] else e2)
    return e,(tx,ty)

def arm(ctx,b,t,L1,L2,c=CY,w=7,up=True,hand=10,elbow_out=None):
    if elbow_out is not None:
        dx,dy=t[0]-b[0],t[1]-b[1]; d=math.hypot(dx,dy); m=L1+L2-.5
        tx,ty=t
        if d>m: tx=b[0]+dx/d*m; ty=b[1]+dy/d*m; d=m
        d=max(d,1); a=math.atan2(ty-b[1],tx-b[0]); B=math.acos(clamp((L1*L1+d*d-L2*L2)/(2*L1*d),-1,1))
        e1=(b[0]+L1*math.cos(a+B),b[1]+L1*math.sin(a+B)); e2=(b[0]+L1*math.cos(a-B),b[1]+L1*math.sin(a-B))
        cx,cy=elbow_out
        e=e1 if math.hypot(e1[0]-cx,e1[1]-cy)>math.hypot(e2[0]-cx,e2[1]-cy) else e2; tt=(tx,ty)
    else:
        e,tt=ik(b,t,L1,L2,up)
    col(ctx,c); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(*b); ctx.line_to(*e); ctx.line_to(*tt); ctx.stroke()
    ctx.arc(e[0],e[1],w*.7,0,2*math.pi); col(ctx,BG); ctx.fill_preserve(); col(ctx,c); ctx.set_line_width(2); ctx.stroke()
    ctx.arc(b[0],b[1],w,0,2*math.pi); col(ctx,c); ctx.fill()
    col(ctx,c); ctx.rectangle(tt[0]-hand/2,tt[1]-hand/2,hand,hand); ctx.fill()
    return tt

def ell(ctx,cx,cy,rx,ry,a0=0,a1=2*math.pi):
    ctx.save(); ctx.translate(cx,cy); ctx.scale(rx,ry); ctx.arc(0,0,1,a0,a1); ctx.restore()

def fade(ctx,t,dur,fi=.4,fo=.4):
    a=0
    if t<fi: a=1-t/fi
    if t>dur-fo: a=max(a,(t-(dur-fo))/fo)
    if a>0: col(ctx,'#000000',clamp(a)); ctx.paint()

# ---------------- end-on ring view (scenes 1-2) ----------------
CX,CY_,R=480,320,240
SEGD=360/32
def pol(r,deg): return (CX+r*math.cos(math.radians(deg)),CY_+r*math.sin(math.radians(deg)))

def truss_arc(ctx,a0,a1,frac=1.0,alpha=1.0):
    if a1<a0: a0,a1=a1,a0
    a1=a0+(a1-a0)*frac
    w=16*frac+2
    ctx.new_path(); ctx.arc(CX,CY_,R,math.radians(a0),math.radians(a1)); col(ctx,'#1d3b42',alpha); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_BUTT); ctx.stroke()
    for rr in (R-w/2,R+w/2):
        ctx.new_path(); ctx.arc(CX,CY_,rr,math.radians(a0),math.radians(a1)); col(ctx,CY,alpha); ctx.set_line_width(1.6); ctx.stroke()
    n=max(1,int((a1-a0)/2.2))
    col(ctx,CY,.55*alpha); ctx.set_line_width(1)
    for i in range(n):
        p=pol(R-w/2,a0+(a1-a0)*i/n); q=pol(R+w/2,a0+(a1-a0)*(i+1)/n)
        ctx.move_to(*p); ctx.line_to(*q); ctx.stroke()

def planned_ring(ctx,a=.5):
    ctx.new_path(); ctx.arc(CX,CY_,R,0,2*math.pi); col(ctx,CY,a); ctx.set_line_width(1); ctx.set_dash([4,7]); ctx.stroke(); ctx.set_dash([])
    text(ctx,'PLANNED WORK RING · Ø 180 m',CX,CY_-6,13,MUT,anchor='c')
    text(ctx,'view down the tube axis',CX,CY_+14,11,'#6b6252',anchor='c')

HUBX,HUBY=740,340   # hub ship nose tip x, top y
ARMB=(900,340)
SUPX,SUPY=800,150
def cart(ctx,ang,a=1.0):
    p=pol(R+16,ang)
    ctx.save(); ctx.translate(*p); ctx.rotate(math.radians(ang+90)); col(ctx,GLASS,a); ctx.rectangle(-11,-7,22,14); ctx.fill(); ctx.restore()
    return pol(R+16,ang)

def scene1(ctx,t,dur):
    background(ctx); header(ctx); planned_ring(ctx)
    sx=600*(1-ease(seg(t,0,3)))
    starship(ctx,HUBX+sx,HUBY,door=1)
    if t>3:
        u=ease(seg(t,3,5.2))
        b=ARMB; tgt=(lerp(1020,860,u),lerp(336,230,u))
        arm(ctx,b,tgt,130,130,CY,7)
        label(ctx,'LOADING ARM',940,215,905,250,CY,a=seg(t,4,5))
    if t>5:
        f=ease(seg(t,5,7))
        truss_arc(ctx,-SEGD/2,SEGD/2,frac=f)
        if t>7:
            a=seg(t,7,7.8); cart(ctx,-2.5,a); cart(ctx,3.5,a)
        label(ctx,'STARTER RAIL + 2 CARTS',760,250,725,300,GLASS,a=seg(t,6,7))
    text(ctx,'HUB STARSHIP · STAYS DOCKED',HUBX+sx+40,HUBY+70,13,FG,a=seg(t,2,3))
    if t>3.2: col(ctx,CY); ctx.set_line_width(4); ctx.move_to(HUBX+sx,HUBY+18); ctx.line_to(HUBX+sx-14,HUBY+18); ctx.stroke()
    caption(ctx,'1 · FLIGHT 1: THE HUB ARRIVES','The hub Starship parks at the spoke site, unfolds its loading arm and sets out a short starter rail with two rail carts on it.')
    fade(ctx,t,dur)

S2_START=2.5; SLOW=2.4; FAST=0.15; NSEG=31
S2_D=[SLOW if i<3 else FAST for i in range(NSEG)]
HOME=-9.0
PICK=(960,165)
HAND=pol(R-30,HOME)

def scene2(ctx,t,dur):
    background(ctx); header(ctx); planned_ring(ctx,.35)
    sx=500*(1-ease(seg(t,0,2.5)))
    starship(ctx,HUBX,HUBY,door=1)
    starship(ctx,SUPX+sx,SUPY,door=1)
    if t>2.3: col(ctx,CY); ctx.set_line_width(4); ctx.move_to(SUPX+sx+60,SUPY+36); ctx.line_to(SUPX+sx+60,SUPY+60); ctx.stroke()
    col(ctx,CY); ctx.set_line_width(4); ctx.move_to(HUBX,HUBY+18); ctx.line_to(HUBX-14,HUBY+18); ctx.stroke()
    # locate cycle
    tau=t-S2_START; k=0; u=0; acc=0; done=False
    if tau<0: k=0;u=0
    else:
        for i,d in enumerate(S2_D):
            if tau<acc+d: k=i;u=(tau-acc)/d;break
            acc+=d
        else: k=NSEG;done=True
    built=k  # segments fully built beyond starter
    truss_arc(ctx,-SEGD/2,SEGD/2)
    for i in range(built):
        a1=-SEGD/2-i*SEGD; truss_arc(ctx,a1-SEGD,a1)
    endang=-SEGD/2-built*SEGD
    armT=(860,230); cartA=HOME; walkT=None; carried=None
    if not done and tau>=0:
        prevA=HOME if k==0 else (-SEGD/2-(k-1)*SEGD)+5
        tgtA=endang+5
        if u<.1: armT=(lerp(860,PICK[0],ease(seg(u,0,.1))),lerp(230,PICK[1],ease(seg(u,0,.1))))
        elif u<.25: armT=(lerp(PICK[0],HAND[0],ease(seg(u,.1,.25))),lerp(PICK[1],HAND[1],ease(seg(u,.1,.25)))); carried=(armT,0)
        elif u<.3: armT=HAND
        elif u<.42: armT=(lerp(HAND[0],860,ease(seg(u,.3,.42))),lerp(HAND[1],230,ease(seg(u,.3,.42))))
        if u<.25: cartA=lerp(prevA,HOME,ease(seg(u,0,.25)))
        elif u<.3: cartA=HOME
        elif u<.65: cartA=lerp(HOME,tgtA,ease(seg(u,.3,.65)))
        else: cartA=tgtA
        if u>=.25 and u<.65:
            walkT=pol(R-30,cartA); carried=(walkT,cartA+90)
        elif u>=.65:
            f=ease(seg(u,.65,.95))
            truss_arc(ctx,endang-SEGD,endang,frac=max(.08,f) if True else 1)
            walkT=pol(R-8,endang-SEGD*f*.9)
    else:
        cartA=endang+5 if done else HOME
    # second cart parked
    cart(ctx,5.0)
    cp=cart(ctx,cartA)
    if walkT is None: walkT=pol(R-30,cartA)
    arm(ctx,cp,walkT,26,26,GLASS,4,hand=7,elbow_out=(CX,CY_))
    arm(ctx,ARMB,armT,130,130,CY,7)
    if carried:
        (px,py),ang=carried
        ctx.save(); ctx.translate(px,py); ctx.rotate(math.radians(ang)); col(ctx,'#1d3b42'); ctx.rectangle(-22,-6,44,12); ctx.fill(); col(ctx,CY); ctx.set_line_width(1.5); ctx.rectangle(-22,-6,44,12); ctx.stroke(); ctx.restore()
    if not done and k>=3: tag(ctx,'TIME-LAPSE',1120,110)
    text(ctx,f'SEGMENTS {min(32,1+built)}/32',1240,90,14,CY,anchor='r',bold=True)
    label(ctx,'SUPPLY STARSHIP · FOLDED TRUSS',920,130,960,150,FG,a=seg(t,1.5,2.5))
    if done:
        text(ctx,'WORK RING CLOSED',CX,CY_+46,16,CY,anchor='c',bold=True,a=seg(t,S2_START+sum(S2_D),S2_START+sum(S2_D)+.5))
    caption(ctx,'2 · FLIGHTS 2–5: GROW THE RING','The loading arm hands each folded truss segment to a cart. The cart rides to the end of the rail, unfolds the segment and bolts it on, then repeats. 32 segments close the ring.')
    fade(ctx,t,dur)

# ---------------- oblique side view (scenes 3-4) ----------------
FR=(780,300); RR=(560,300); RX,RY=62,230
def ring_side(ctx,c,cx,cy,frac=1.0,w=12,alpha=1.0):
    a0=-math.pi/2; a1=a0+2*math.pi*frac
    ctx.new_path(); ell(ctx,cx,cy,RX,RY,a0,a1); col(ctx,c,alpha); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_BUTT); ctx.stroke()
    ctx.new_path(); ell(ctx,cx,cy,RX,RY,a0,a1); col(ctx,BG,alpha); ctx.set_line_width(1.2); ctx.set_dash([3,12]); ctx.stroke(); ctx.set_dash([])

BEAMS=[-60,0,60,120,180,240]
def beam(ctx,deg,rx_,fx_,f=1.0,back=False):
    a=math.radians(deg)
    p=(rx_+RX*math.cos(a),300+RY*math.sin(a)); q=(fx_+RX*math.cos(a),300+RY*math.sin(a))
    q=(lerp(p[0],q[0],f),q[1])
    al=.4 if back else 1
    col(ctx,CY,al); ctx.set_line_width(7); ctx.move_to(*p); ctx.line_to(*q); ctx.stroke()
    L=q[0]-p[0]
    if L>20:
        col(ctx,BG,al); ctx.set_line_width(2)
        for fr in (.36,.68):
            x=p[0]+L*fr; ctx.move_to(x,p[1]-6); ctx.line_to(x,p[1]+6); ctx.stroke()

def hub_side(ctx,fx):
    starship(ctx,fx+16,FR[1]+RY-4,s=.9)
    col(ctx,CY); ctx.set_line_width(4); ctx.move_to(fx+4,FR[1]+RY-6); ctx.line_to(fx+18,FR[1]+RY+10); ctx.stroke()

def scene3(ctx,t,dur):
    background(ctx); header(ctx)
    f=ease(seg(t,.5,4.2))
    for d in BEAMS:
        if 90<d<270 and t>4.4:
            i=BEAMS.index(d); beam(ctx,d,RR[0],FR[0],ease(seg(t,4.4+i*.5,5.2+i*.5)),back=True)
    if f>0: ring_side(ctx,CYD,RR[0],RR[1],f,10)
    for d in BEAMS:
        if not (90<d<270) and t>4.4:
            i=BEAMS.index(d); beam(ctx,d,RR[0],FR[0],ease(seg(t,4.4+i*.5,5.2+i*.5)))
    ring_side(ctx,CY,FR[0],FR[1])
    hub_side(ctx,FR[0])
    label(ctx,'FRONT WORK RING',860,92,800,96,CY)
    label(ctx,'REAR GRIPPER RING',330,92,540,82,CYD,a=seg(t,.8,1.6))
    label(ctx,'6 TELESCOPING BEAMS · 4–22 m',300,560,600,505,CY,a=seg(t,5,6),anchor='l')
    if 0.5<t<4.4: tag(ctx,'TIME-LAPSE',1120,110)
    caption(ctx,'3 · SECOND RING AND BEAMS','Seen from the side now. The same cart loop builds the gripper ring behind the work ring, then six telescoping beams join the two rings.')
    fade(ctx,t,dur)

def solar(ctx,fx,f,a=1.0):
    col(ctx,STEEL,a); ctx.set_line_width(3); ctx.move_to(fx+RX,300); ctx.line_to(fx+RX+lerp(0,330,min(1,f*1.3)),300); ctx.stroke()
    w=300*f
    for y in (250,316):
        col(ctx,SOLAR,a); ctx.rectangle(fx+RX+28,y,w,34); ctx.fill(); col(ctx,SOLARL,a); ctx.set_line_width(1); ctx.rectangle(fx+RX+28,y,w,34); ctx.stroke()
        n=int(w/30)
        for i in range(1,n+1):
            x=fx+RX+28+i*30; ctx.move_to(x,y); ctx.line_to(x,y+34); ctx.stroke()

def grip_pads(ctx,cx,on=1.0,n=12,a=1.0):
    for i in range(n):
        ang=2*math.pi*i/n
        x=cx+(RX-12)*math.cos(ang); y=300+(RY-14)*math.sin(ang)
        col(ctx,SPARK if on>.5 else STEEL,a); ctx.rectangle(x-5,y-5,10,10); ctx.fill()

def scene4(ctx,t,dur):
    background(ctx); header(ctx)
    for d in BEAMS:
        if 90<d<270: beam(ctx,d,RR[0],FR[0],back=True)
    ring_side(ctx,CYD,RR[0],RR[1],1,10)
    a=seg(t,.5,1.2)
    if t>.5:
        n=int(clamp((t-.5)/2)*12+.999)
        for i in range(n):
            ang=2*math.pi*i/12; x=RR[0]+(RX-12)*math.cos(ang); y=300+(RY-14)*math.sin(ang)
            col(ctx,SPARK); ctx.rectangle(x-5,y-5,10,10); ctx.fill()
    for d in BEAMS:
        if not (90<d<270): beam(ctx,d,RR[0],FR[0])
    # bulkhead
    if t>5.5:
        f=ease(seg(t,5.5,7.5)); ctx.new_path(); ell(ctx,FR[0]+10,300,RX*.85*f+2,RY*.92*f+4); col(ctx,CY,.14); ctx.fill_preserve(); col(ctx,CY,.8); ctx.set_line_width(1.5); ctx.set_dash([5,5]); ctx.stroke(); ctx.set_dash([])
    if t>7:
        ctx.new_path(); ell(ctx,FR[0],300,RX*.78,RY*.86); col(ctx,STEEL,seg(t,7,7.8)); ctx.set_line_width(6); ctx.stroke()
    ring_side(ctx,CY,FR[0],FR[1])
    if t>2.5: solar(ctx,FR[0],ease(seg(t,2.5,4.5)))
    if t>4.5:
        for i,(x,y) in enumerate([(RR[0]-30,120),(RR[0]+40,140),(RR[0]-50,300),(RR[0]+56,330),(RR[0]-20,480),(RR[0]+30,470)]):
            if t>4.5+i*.15:
                col(ctx,CY); ctx.rectangle(x-8,y-6,16,12); ctx.fill(); col(ctx,SPARK); ctx.arc(x+9,y,3,0,2*math.pi); ctx.fill()
    hub_side(ctx,FR[0])
    label(ctx,'12 GRIPPER PADS',330,92,520,110,SPARK,a=seg(t,1,1.8))
    label(ctx,'SOLAR WINGS · ~1 MW',980,226,960,250,SOLARL,a=seg(t,3,4))
    label(ctx,'6 WELD CRAWLERS',330,520,500,478,CY,a=seg(t,4.8,5.5))
    label(ctx,'INFLATABLE BULKHEAD',880,140,820,190,CY,a=seg(t,6,7))
    label(ctx,'FIRST FRAME',880,500,820,450,STEEL,a=seg(t,7.3,8))
    caption(ctx,'4 · FLIGHTS 6–7: FIT OUT','Gripper pads, solar wings, weld crawlers and the inflatable bulkhead go on. The first frame goes into the work ring, and the factory is ready to build bay 1.')
    fade(ctx,t,dur)

# ---------------- operation (scene 5) ----------------
PX=10  # px per m
TRY=170; RRY=210; TRX=40; RRX=52
def scene5_state(t):
    T0=1.0; CYC=7.0; NC=2
    tau=t-T0
    c=int(clamp(tau,0,NC*CYC-1e-6)//CYC) if tau>0 else 0
    if tau>=NC*CYC: c=NC; tt=0.0
    else: tt=max(0.0,tau-c*CYC)
    xf=500+180*c
    st=dict(xf=xf,p=0,rear=xf-40,front=xf+180,rg=1,fg=0,phase='BUILD',newframe=xf+180,bay=c+1)
    if tt<3: st['p']=ease(tt/3)
    else:
        st['p']=1
        if tt<3.4: st['fg']=1; st['rg']=0 if tt>3.3 else 1; st['phase']='SWAP GRIP'
        elif tt<5.0: st['fg']=1; st['rg']=0; st['rear']=lerp(xf-40,xf+140,ease(seg(tt,3.4,5.0))); st['phase']='PULL'
        elif tt<5.4: st['rear']=xf+140; st['rg']=1; st['fg']=1 if tt<5.3 else 0; st['phase']='SWAP GRIP'
        else:
            st['rear']=xf+140; st['rg']=1; st['fg']=0; st['front']=lerp(xf+180,xf+360,ease(seg(tt,5.4,7.0))); st['phase']='PUSH'
            st['newframe2']=seg(tt,6.4,7.0)
    return st

def scene5(ctx,t,dur):
    background(ctx); header(ctx)
    st=scene5_state(t)
    cam=st['front']-820
    X=lambda wx:wx-cam
    xf=st['xf']
    # finished tube
    left=-50; right=X(xf)
    col(ctx,HULL); ctx.rectangle(left,300-TRY,right-left,2*TRY); ctx.fill()
    col(ctx,GLASS); ctx.set_line_width(6); ctx.move_to(left,300-TRY+5); ctx.line_to(right,300-TRY+5); ctx.stroke()
    col(ctx,KEEL); ctx.set_line_width(8); ctx.move_to(left,300+TRY-5); ctx.line_to(right,300+TRY-5); ctx.stroke()
    col(ctx,GOLD); ctx.set_line_width(2); ctx.move_to(left,300-TRY); ctx.line_to(right,300-TRY); ctx.move_to(left,300+TRY); ctx.line_to(right,300+TRY); ctx.stroke()
    j=0
    while True:
        x=X(xf-180*j)
        if x<-60: break
        ctx.new_path(); ell(ctx,x,300,TRX,TRY,-math.pi/2,math.pi/2); col(ctx,GOLD,.8); ctx.set_line_width(1.5); ctx.stroke(); j+=1
    # bay under construction
    bx0,bx1=X(xf),X(xf+180)
    p=st['p']
    col(ctx,GOLD,.8); ctx.set_line_width(1.5); ctx.set_dash([6,6]); ctx.move_to(bx0,300-TRY); ctx.line_to(bx1,300-TRY); ctx.move_to(bx0,300+TRY); ctx.line_to(bx1,300+TRY); ctx.stroke(); ctx.set_dash([])
    if p>0:
        h=2*TRY*p
        col(ctx,HULL if p>=1 else GOLD,1 if p>=1 else .75); ctx.rectangle(bx0,300+TRY-h,bx1-bx0,h); ctx.fill()
        col(ctx,KEEL); ctx.rectangle(bx0,300+TRY-10,bx1-bx0,10); ctx.fill()
        if p>=1:
            col(ctx,GLASS); ctx.set_line_width(6); ctx.move_to(bx0,300-TRY+5); ctx.line_to(bx1,300-TRY+5); ctx.stroke()
            col(ctx,GOLD); ctx.set_line_width(2); ctx.move_to(bx0,300-TRY); ctx.line_to(bx1,300-TRY); ctx.move_to(bx0,300+TRY); ctx.line_to(bx1,300+TRY); ctx.stroke()
        col(ctx,BG,.8); ctx.set_line_width(1.5)
        for i in range(1,4):
            x=bx0+(bx1-bx0)*i/4; ctx.move_to(x,300+TRY-h); ctx.line_to(x,300+TRY); ctx.stroke()
        if p<1:
            cx_=bx0+(bx1-bx0)*((t*1.3)%1); cy_=300+TRY-h
            col(ctx,CY); ctx.rectangle(cx_-8,cy_-6,16,12); ctx.fill(); col(ctx,SPARK); ctx.arc(cx_+9,cy_,3+abs(math.sin(t*25))*2,0,2*math.pi); ctx.fill()
    # frames at xf (finished) and new frame
    ctx.new_path(); ell(ctx,X(xf+180),300,TRX,TRY); col(ctx,STEEL); ctx.set_line_width(6); ctx.stroke()
    if 'newframe2' in st and st['newframe2']>0:
        ctx.new_path(); ell(ctx,X(xf+360),300,TRX,TRY); col(ctx,STEEL,st['newframe2']); ctx.set_line_width(6); ctx.stroke()
    rear,front=X(st['rear']),X(st['front'])
    # back beams
    def bm(deg,back):
        a=math.radians(deg); p0=(rear+RRX*math.cos(a),300+RRY*math.sin(a)); q0=(front+RRX*math.cos(a),300+RRY*math.sin(a))
        al=.4 if back else 1
        col(ctx,CY,al); ctx.set_line_width(7); ctx.move_to(*p0); ctx.line_to(*q0); ctx.stroke()
    for d in (120,180,240): bm(d,True)
    def ring(cx,c,grip):
        ctx.new_path(); ell(ctx,cx,300,RRX,RRY); col(ctx,c); ctx.set_line_width(11); ctx.stroke()
        for ang in (-math.pi/2,math.pi/2,0,math.pi):
            x=cx+(RRX-14)*math.cos(ang); y=300+(RRY-16)*math.sin(ang)
            col(ctx,SPARK if grip else '#4a4740'); ctx.rectangle(x-6,y-6,12,12); ctx.fill()
    ring(rear,CYD,st['rg'])
    for d in (-60,0,60): bm(d,False)
    ring(front,CY,st['fg'])
    starship(ctx,front+16,300+RRY-6,s=.85)
    # readouts
    L=(st['front']-st['rear'])/PX
    text(ctx,f'BEAMS {L:4.1f} m',(rear+front)/2,300-RRY-18,14,CY,anchor='c',bold=True)
    text(ctx,'REAR · GRIPPER',rear,300+RRY+30,12,CYD,anchor='c')
    text(ctx,'FRONT · WORK',front,300-RRY-46,12,CY,anchor='c')
    ph=st['phase']
    phs={'BUILD':'BUILD · rear ring grips, bay is built','SWAP GRIP':'SWAP GRIP','PULL':'PULL · beams shrink, rear ring moves up 18 m','PUSH':'PUSH · beams extend, front ring moves 18 m'}
    tag(ctx,phs[ph],40,110,GOLD)
    text(ctx,f'BAY {st["bay"]}',1240,90,16,FG,anchor='r',bold=True)
    col(ctx,SPARK); ctx.rectangle(1060,124,10,10); ctx.fill(); text(ctx,'= gripping',1076,134,12,MUT)
    caption(ctx,'5 · HOW IT MOVES','The rear ring grips the finished tube while the bay is built. Then the front ring grips, the beams shrink to pull the rear ring up, and extend again to push the front ring 18 m to the next bay.')
    fade(ctx,t,dur)

# ---------------- summary (scene 6) ----------------
def scene6(ctx,t,dur):
    background(ctx); header(ctx)
    cx,cy,r=360,320,200
    ctx.new_path(); ctx.arc(cx,cy,r,0,2*math.pi); col(ctx,'#3a372f'); ctx.set_line_width(16); ctx.stroke()
    g=ease(seg(t,.5,4.5))*30
    col(ctx,GOLD); ctx.set_line_width(16)
    for i in range(6):
        c=math.radians(i*60-90); gg=math.radians(g)
        if g>0: ctx.new_path(); ctx.arc(cx,cy,r,c-gg,c+gg); ctx.stroke()
    col(ctx,GOLD); ctx.set_line_width(3)
    for i in range(6):
        c=math.radians(i*60-90); ctx.move_to(cx+20*math.cos(c),cy+20*math.sin(c)); ctx.line_to(cx+(r-8)*math.cos(c),cy+(r-8)*math.sin(c)); ctx.stroke()
        if t<4.6: col(ctx,CY); ctx.rectangle(cx+r*math.cos(c)-8,cy+r*math.sin(c)-8,16,16); ctx.fill(); col(ctx,GOLD)
    ctx.arc(cx,cy,20,0,2*math.pi); col(ctx,'#11131b'); ctx.fill_preserve(); col(ctx,GOLD); ctx.set_line_width(2); ctx.stroke()
    rows=[('7','Starship flights to deploy one factory'),('6','factories, one at each spoke'),('≈42','flights to set up all six'),('12','build fronts that meet and close the ring')]
    for i,(n,s) in enumerate(rows):
        a=seg(t,.6+i*.6,1.2+i*.6)
        text(ctx,n,700,170+i*95,48,GOLD,bold=True,a=a)
        text(ctx,s,820,160+i*95,18,FG,font=SANS,a=a)
    if t>4.6: text(ctx,'RING CLOSED',cx,cy+6,16,GOLD,anchor='c',bold=True,a=seg(t,4.6,5.2))
    caption(ctx,'6 · ALL SIX FACTORIES','One factory at each spoke, building in both directions. The 12 fronts meet, the ring closes, and the hull flights take over from there.')
    fade(ctx,t,dur,fo=.8)

SCENES=[('s1',scene1,9),('s2',scene2,15),('s3',scene3,9),('s4',scene4,9.5),('s5',scene5,16),('s6',scene6,7.5)]

def render(name,fn,dur):
    tmp=os.path.join(OUT,f'{name}.tmp.mp4'); fin=os.path.join(OUT,f'{name}.mp4')
    p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgra','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',tmp],stdin=subprocess.PIPE)
    surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H)
    n=int(round(dur*FPS))
    for i in range(n):
        ctx=cairo.Context(surf); ctx.set_antialias(cairo.ANTIALIAS_BEST)
        fn(ctx,i/FPS,dur); surf.flush()
        p.stdin.write(bytes(surf.get_data()))
    p.stdin.close()
    if p.wait()==0: os.replace(tmp,fin)
    else: sys.exit(f'{name} failed')

def still(name,fn,dur,t):
    surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); ctx=cairo.Context(surf); fn(ctx,t,dur); surf.write_to_png(os.path.join(OUT,f'still_{name}_{t}.png'))

if __name__=='__main__':
    if sys.argv[1]=='stills':
        for name,fn,dur in SCENES:
            for tt in sys.argv[2:]:
                still(name,fn,dur,float(tt)*dur)
    else:
        for name,fn,dur in SCENES:
            if sys.argv[1] in ('all',name): render(name,fn,dur)
