from common import *
CXc,CYc,RP=640,330,235   # top view centre and ring radius in px (17.35 km)
ANG=[-90,-30,30,90,150,210]
PAIRC={-90:GOLD,90:GOLD,-30:CY,150:CY,30:GLASS,210:GLASS}
def P(r,d): return (CXc+r*math.cos(math.radians(d)),CYc+r*math.sin(math.radians(d)))
def head(ctx): hdr(ctx,'BUILDING THE SPOKES','AND THE MIDDLE RING')
def planned(ctx,a=.5,mid=False):
    ctx.new_path(); ctx.arc(CXc,CYc,RP,0,2*math.pi); col(ctx,CY,a); ctx.set_line_width(1); ctx.set_dash([4,7]); ctx.stroke()
    if mid: ctx.new_path(); ctx.arc(CXc,CYc,RP/2,0,2*math.pi); col(ctx,GOLD,a); ctx.stroke()
    ctx.set_dash([])
def hub(ctx,a=1):
    ctx.arc(CXc,CYc,11,0,2*math.pi); col(ctx,PANEL,a); ctx.fill(); ctx.arc(CXc,CYc,4,0,2*math.pi); col(ctx,BG,a); ctx.fill()
def spoke(ctx,d,f,c=CY,w=3.5,a=1):
    if f<=0: return
    p=P(12,d); q=P(12+(RP-12)*f,d)
    col(ctx,c,a); ctx.set_line_width(w); ctx.move_to(*p); ctx.line_to(*q); ctx.stroke()
    return q

def a1(ctx,t,dur):
    background(ctx); head(ctx)
    planned(ctx,.5*seg(t,.3,1.5)); hub(ctx,seg(t,0,.6))
    for i,d in enumerate(ANG):
        f=ease(seg(t,1.2+i*.25,2.2+i*.25))
        ctx.new_path(); p=P(12,d); q=P(12+(RP-12)*f,d); col(ctx,PAIRC[d],.7); ctx.set_line_width(1.2); ctx.set_dash([5,6]); ctx.move_to(*p); ctx.line_to(*q); ctx.stroke(); ctx.set_dash([])
    a=seg(t,4,5)
    label(ctx,'HUB (CENTRE POD)',700,250,CXc+8,CYc-8,FG,a=seg(t,.5,1.2))
    label(ctx,'PLANNED RING · r 17.35 km',890,140,P(RP,-50)[0],P(RP,-50)[1],CY,a=seg(t,1.2,2))
    for d,s in ((-90,'PAIR A'),(-30,'PAIR B'),(30,'PAIR C')):
        q=P(RP+30,d); text(ctx,s,q[0],q[1]+4,13,PAIRC[d],anchor='c',bold=True,a=a)
    readout(ctx,'SPOKES','6 × 17.35 km',990,250,a=seg(t,2.5,3.2))
    readout(ctx,'BUILT IN','3 OPPOSITE PAIRS',990,315,GOLD,a=a)
    caption(ctx,'1 · THE PLAN, SEEN FROM ABOVE','The hub sits at the centre. Six spokes run 17.35 km out to where the ring will be, built as three opposite pairs so the hub never goes off-centre.')
    fade(ctx,t,dur)

def a2(ctx,t,dur):
    background(ctx); head(ctx)
    tag(ctx,'TIME-LAPSE · ONE SPOKE',1060,110)
    y=330; x0=150; x1=1180
    f=ease(seg(t,1,10.5)); tip=lerp(x0+40,x1,f)
    # hub
    col(ctx,PANEL); ctx.rectangle(60,y-70,90,140); ctx.fill(); text(ctx,'HUB',105,y+92,13,MUT,anchor='c')
    truss_h(ctx,x0,tip,y,46,CY,step=18)
    col(ctx,GLASS,.35); ctx.rectangle(x0,y-6,tip-x0,12); ctx.fill()
    # cargo pods shuttle
    for k in range(3):
        ph=((t*0.33+k/3)%1)
        px=lerp(x0+10,tip-60,ph if ph<.5 else 1-ph)*1
        px=lerp(x0+10,tip-70,(ph*2) if ph<.5 else (2-ph*2))
        col(ctx,GOLD,.9); ctx.rectangle(px-12,y-38,24,12); ctx.fill()
    # crawler
    col(ctx,'#1b2a30'); ctx.rectangle(tip-48,y-34,48,68); ctx.fill(); col(ctx,CY); ctx.set_line_width(2); ctx.rectangle(tip-48,y-34,48,68); ctx.stroke()
    b=math.sin(t*6)
    arm(ctx,(tip-10,y-34),(tip+18,y-23+6*b),26,24,CY,4,hand=6)
    arm(ctx,(tip-10,y+34),(tip+18,y+23-6*b),26,24,CY,4,up=False,hand=6)
    if 1<t<10.6:
        ctx.arc(tip+16,y-23+6*b,4,0,2*math.pi); col(ctx,SPARK,.8); ctx.fill()
    km=17.35*f
    readout(ctx,'SPOKE LENGTH',f'{km:5.1f} km',60,110)
    label(ctx,'SPOKE CRAWLER · lays 30 m truss bays',min(tip-200,880),220,tip-24,y-36,CY,a=seg(t,1.5,2.5))
    label(ctx,'CARGO PODS bring fibre and strip from the hub',300,470,360,y+30,GOLD,a=seg(t,3,4))
    label(ctx,'ELEVATOR SHAFT inside the truss',600,520,640 if tip>660 else tip-20,y+6,GLASS,a=seg(t,5,6))
    caption(ctx,'2 · A CRAWLER BUILDS EACH SPOKE OUTWARD','It walks out on the truss it has just laid, adding a 30 m bay at a time from basalt fibre and lunar aluminium strip. Pods running along the finished truss keep it supplied.')
    fade(ctx,t,dur)

def a3(ctx,t,dur):
    background(ctx); head(ctx); planned(ctx,.45); hub(ctx)
    for i,d in enumerate(ANG):
        pair=[-90,-30,30].index(d) if d in (-90,-30,30) else [90,150,210].index(d)
        f=ease(seg(t,.6,8))
        q=spoke(ctx,d,f,PAIRC[d])
        if q and f<1: ctx.rectangle(q[0]-4,q[1]-4,8,8); col(ctx,SPARK); ctx.fill()
        if f>=1:
            a=seg(t,8,8.6); q=P(RP,d); ctx.rectangle(q[0]-7,q[1]-7,14,14); col(ctx,GOLD,a); ctx.fill()
    f=ease(seg(t,.6,8))
    readout(ctx,'ALL SIX SPOKES',f'{17.35*f:5.1f} km',990,150)
    readout(ctx,'MASS PER SPOKE','~35 kt',990,215,CY,a=seg(t,2,3))
    label(ctx,'JUNCTION NODES: where the bay factories start',870,470,P(RP,30)[0]+6,P(RP,30)[1]+6,GOLD,a=seg(t,8.2,9))
    label(ctx,'opposite spokes grow at the same pace',120,140,P(140,210)[0],P(140,210)[1],FG,a=seg(t,2,3))
    caption(ctx,'3 · SIX CRAWLERS, THREE BALANCED PAIRS','All six spokes grow together, so the structure stays balanced on the hub. At the rim each crawler leaves a junction node: the first cell of the ring and the starting point for its bay factories.')
    fade(ctx,t,dur)

def a4(ctx,t,dur):
    background(ctx); head(ctx); planned(ctx,.35,mid=True); hub(ctx)
    for d in ANG: spoke(ctx,d,1,CYD,3)
    for d in ANG: q=P(RP,d); ctx.rectangle(q[0]-5,q[1]-5,10,10); col(ctx,GOLD,.7); ctx.fill()
    f=ease(seg(t,1,9.5)); rm=RP/2
    for d in ANG:
        for sgn in (1,-1):
            a0=math.radians(d); a1=math.radians(d+sgn*30*f)
            ctx.new_path(); ctx.arc(CXc,CYc,rm,min(a0,a1),max(a0,a1)); col(ctx,GOLD); ctx.set_line_width(5); ctx.stroke()
            if f<1:
                q=P(rm,d+sgn*30*f); ctx.arc(q[0],q[1],5,0,2*math.pi); col(ctx,CY); ctx.fill()
    readout(ctx,'MIDDLE RING CLOSED',f'{f*100:3.0f} %',990,150)
    readout(ctx,'GRAVITY THERE','0.5 g',990,215,CY,a=seg(t,2,3))
    # inset cross sections
    a=seg(t,3,4); x,y=150,430
    col(ctx,'#11131b',.9*a); ctx.rectangle(40,350,330,230); ctx.fill()
    text(ctx,'TUBE CROSS-SECTIONS, TO SCALE',55,372,11,MUT,a=a,spacing=1.5)
    ctx.new_path(); ctx.arc(150,470,75,0,2*math.pi); col(ctx,CY,a); ctx.set_line_width(2); ctx.stroke()
    ctx.new_path(); ctx.arc(300,525,20,0,2*math.pi); col(ctx,GOLD,a); ctx.stroke()
    text(ctx,'main ring Ø 150 m',150,565,12,CY,anchor='c',a=a); text(ctx,'middle Ø 40 m',300,565,12,GOLD,anchor='c',a=a)
    label(ctx,'MIDDLE RING · r 8.7 km · 54.5 km around',780,560,P(rm,40)[0],P(rm,40)[1],GOLD,a=seg(t,1.5,2.5))
    caption(ctx,'4 · THE MIDDLE RING, HALFWAY OUT','Twelve small bay factories start at the spokes and build 40 m tube both ways until the arcs meet. At 0.5 g it holds industry, labs and the elevator transfer stop, and ties the spokes together.')
    fade(ctx,t,dur)

def a4b(ctx,t,dur):
    """Main ring closes: each factory's first stretch of tube locks onto its spoke, then grows both ways."""
    background(ctx); head(ctx); hub(ctx)
    T_LOCK=(2.6,3.6); T_GROW=(4.2,10.0); T_SPIN=(11.0,13.6)
    spin=ease(seg(t,*T_SPIN))*.35   # radians of visible turn during spin-up
    ctx.save(); ctx.translate(CXc,CYc); ctx.rotate(spin); ctx.translate(-CXc,-CYc)
    planned(ctx,.3*(1-seg(t,*T_GROW)))
    # middle ring: already closed in the scene before
    ctx.new_path(); ctx.arc(CXc,CYc,RP/2,0,2*math.pi); col(ctx,GOLD,.9); ctx.set_line_width(4); ctx.stroke()
    lock=seg(t,*T_LOCK)
    for d in ANG:
        # spokes stop just short of the tube until it locks on
        q=P(RP-16+16*ease(lock),d); col(ctx,CYD); ctx.set_line_width(3); ctx.move_to(*P(12,d)); ctx.line_to(*q); ctx.stroke()
    seed=ease(seg(t,.6,2.6))*6        # first stretch of tube at each spoke: up to ±6°
    grow=ease(seg(t,*T_GROW))*24      # then out to ±30° where neighbours meet
    half=seed+grow
    for d in ANG:
        if half<=0: continue
        ctx.new_path(); ctx.arc(CXc,CYc,RP,math.radians(d-half),math.radians(d+half))
        col(ctx,GOLD); ctx.set_line_width(11); ctx.stroke()
        if half<30:   # a bay factory at each of the two growing fronts
            for sg in (-1,1):
                q=P(RP,d+sg*half); ctx.rectangle(q[0]-7,q[1]-7,14,14); col(ctx,CY); ctx.fill()
        if 0<lock<1 or (lock>=1 and t<T_LOCK[1]+.5):   # flash where tube meets spoke
            q=P(RP,d); r=6+14*seg(t,T_LOCK[0],T_LOCK[1]+.5)
            ctx.new_path(); ctx.arc(q[0],q[1],r,0,2*math.pi); col(ctx,SPARK,.9*(1-seg(t,T_LOCK[1],T_LOCK[1]+.5))); ctx.set_line_width(2); ctx.stroke()
    if half>=30 and t<T_GROW[1]+1.2:   # the six joins
        for d in ANG:
            q=P(RP,d+30); r=6+16*seg(t,T_GROW[1],T_GROW[1]+1.2)
            ctx.new_path(); ctx.arc(q[0],q[1],r,0,2*math.pi); col(ctx,SPARK,1-seg(t,T_GROW[1],T_GROW[1]+1.2)); ctx.set_line_width(2); ctx.stroke()
    ctx.restore()
    if t>T_SPIN[0]-.4:   # spin arrow
        a=seg(t,T_SPIN[0]-.4,T_SPIN[0]+.4)
        ctx.new_path(); ctx.arc(CXc,CYc,RP+34,math.radians(-60),math.radians(-20)); col(ctx,GOLD,a); ctx.set_line_width(2); ctx.stroke()
        q=P(RP+34,-20); ctx.move_to(q[0]+2,q[1]-8); ctx.line_to(q[0]-4,q[1]+6); ctx.line_to(q[0]+9,q[1]+3); ctx.close_path(); col(ctx,GOLD,a); ctx.fill()
    pct=100*min(1,half/30)
    readout(ctx,'MAIN RING CLOSED',f'{pct:3.0f} %',990,150)
    readout(ctx,'BUILD FRONTS','12' if t>T_GROW[0] else '6 seeds',990,215,CY,a=seg(t,.8,1.5))
    rpm=0.23*ease(seg(t,*T_SPIN))
    readout(ctx,'SPIN',f'{rpm:4.2f} rpm',990,280,GREEN if rpm>=.229 else GOLD,a=seg(t,T_SPIN[0]-.6,T_SPIN[0]))
    text(ctx,'RING CLOSED',CXc,CYc-RP-34,16,GOLD,anchor='c',bold=True,a=seg(t,T_GROW[1]+.3,T_GROW[1]+.9))
    label(ctx,'first stretch of tube locks onto its spoke',120,150,P(RP,-30)[0]-6,P(RP,-30)[1]-6,SPARK,a=seg(t,2.4,3.0)*(1-seg(t,6.0,6.6)))
    label(ctx,'then each factory pair builds both ways',120,520,P(RP,150+12)[0],P(RP,150+12)[1],CY,a=seg(t,4.6,5.2)*(1-seg(t,9.6,10.2)))
    label(ctx,'MIDDLE RING · already closed',780,560,P(RP/2,40)[0],P(RP/2,40)[1],GOLD,a=seg(t,.6,1.3)*(1-seg(t,4.4,5.0)))
    caption(ctx,'5 · THE MAIN RING CLOSES','Each bay factory\'s first stretch of tube locks onto its spoke; then all six build both ways until the 12 fronts meet. With the middle ring tying the spokes together, the ring closes and spins up to 0.23 rpm.')
    fade(ctx,t,dur)

def a5(ctx,t,dur):
    card(ctx,'SPOKES AND MIDDLE RING',[
        ('Spokes','6 × 17.35 km basalt-fibre truss with an elevator shaft, ~35 kt each'),
        ('Built by','6 crawlers in 3 opposite pairs, fed by cargo pods from the hub'),
        ('Middle ring','r 8.7 km, 0.5 g, Ø 40 m tube, 54.5 km around, ~0.5 Mt'),
        ('Why it holds','Rim speed 206 m/s, so aluminium carries its own spin (~115 MPa); no fibre bands'),
        ('Used for','Industry and labs at half gravity, elevator transfer, spoke stiffening'),
        ('Order','Hub → spokes → junction nodes → main ring and middle ring in parallel'),
    ],t,dur,'order-of-magnitude design study')

SCENES=[('sa1',a1,8),('sa2',a2,12),('sa3',a3,10),('sa4',a4,11),('sa4b',a4b,14),('sa5',a5,7)]
if __name__=='__main__': main(SCENES,'spokes-and-middle-ring')
