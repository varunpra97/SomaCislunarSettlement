from common import *
import json
from hubspine import tugs, gauge, TL
COST=json.load(open(os.path.join(OUT,'cost.json')))
def head(ctx): hdr(ctx,'BUILDING A RING STACK','SIX RINGS ON ONE SPINE')
Y=330; XS=[270,410,550,730,870,1010]; RXe,RYe=26,205
def pods(ctx):
    for x in XS: col(ctx,PANEL,.85); ctx.rectangle(x-8,Y-20,16,40); ctx.fill()
def epos(x,th,k=1.0): return (x+RXe*k*math.cos(th),Y+RYe*k*math.sin(th))
def ring(ctx,x,sp=0,tube=0,mid=0,wing=0,phi=0,tilt=0,fronts=True):
    ctx.save(); ctx.translate(x,Y); ctx.rotate(math.radians(tilt)); ctx.translate(-x,-Y)
    angs=[math.radians(60*i)+phi for i in range(6)]
    for a in angs:
        if wing>0:
            p=epos(x,a,.12); q=epos(x,a,.12+.8*wing)
            col(ctx,SOLAR); ctx.set_line_width(7); ctx.move_to(*p); ctx.line_to(*q); ctx.stroke()
        if sp>0:
            q=epos(x,a,sp); col(ctx,CY); ctx.set_line_width(1.6); ctx.move_to(x,Y); ctx.line_to(*q); ctx.stroke()
    for k,f,c,w in ((1,tube,CY,5),(.5,mid,GOLD,2.5)):
        if f<=0: continue
        for a in angs:
            for sg in (1,-1):
                ctx.new_path(); ctx.save(); ctx.translate(x,Y); ctx.scale(RXe*k,RYe*k)
                a0,a1=sorted((a,a+sg*math.radians(30)*f)); ctx.arc(0,0,1,a0,a1); ctx.restore()
                col(ctx,c); ctx.set_line_width(w); ctx.stroke()
                if fronts and f<1 and k==1:
                    q=epos(x,a+sg*math.radians(30)*f); ctx.arc(q[0],q[1],3,0,2*math.pi); col(ctx,SPARK); ctx.fill()
    ctx.restore()
def spine(ctx): truss_h(ctx,190,1130,Y,18,CYD,step=12)
def sun(ctx,a):
    if a<=0: return
    ctx.new_path(); ctx.arc(48,Y,20,0,2*math.pi); col(ctx,'#ffd27a',a); ctx.fill()
    col(ctx,'#ffd27a',.5*a); ctx.set_line_width(1.5)
    for i in range(12):
        an=i*math.pi/6; ctx.move_to(48+25*math.cos(an),Y+25*math.sin(an)); ctx.line_to(48+33*math.cos(an),Y+33*math.sin(an))
    ctx.stroke()
SPIN={}
def phi_of(i,t0,t):  # spin angle given start time t0 within the scene timeline (ramped)
    if t<t0: return 0
    d=t-t0; ramp=3.0
    s=(d*d/(2*ramp)) if d<ramp else (ramp/2+(d-ramp))
    return (1 if i%2==0 else -1)*s*.9

def d1(ctx,t,dur):
    background(ctx); head(ctx); spine(ctx); pods(ctx)
    ring(ctx,XS[0],sp=ease(seg(t,.5,3)),tube=ease(seg(t,2.5,6.5)),mid=ease(seg(t,4,7)),wing=ease(seg(t,6,8.5)))
    tugs(ctx,190,1130,t); gauge(ctx,t)
    readout(ctx,'RING 1','spokes, tube, wings',60,110)
    label(ctx,'RING 1 · 34.7 km across (not to scale)',330,560,XS[0]+10,Y+RYe-10,CY,a=seg(t,3,4))
    label(ctx,'MIDDLE RING',70,235,XS[0]-8,Y-RYe/2,GOLD,a=seg(t,5,6))
    label(ctx,'TUGS',1000,470,1130+40,Y+10,GOLD,a=seg(t,1,2))
    caption(ctx,'1 · THE FIRST RING GOES UP ON THE SPINE','Spokes grow out from its pod, then twelve bay-factory fronts close the main tube while smaller factories close the middle ring, and wing robots lay the solar wings. The tugs keep the growing stack steady.')
    fade(ctx,t,dur)

def d2(ctx,t,dur):
    background(ctx); head(ctx); spine(ctx); pods(ctx)
    T0=5
    ring(ctx,XS[0],1,1,1,1,phi=phi_of(0,T0,t))
    f=ease(seg(t,.3,4.5))
    ring(ctx,XS[1],sp=min(1,f*2),tube=f,mid=f,wing=f,phi=phi_of(1,T0,t))
    tugs(ctx,190,1130,t); gauge(ctx,t)
    if t>T0:
        a=seg(t,T0,T0+1)
        for i,x in enumerate(XS[:2]):
            sg=1 if i==0 else -1
            ctx.new_path(); ctx.save(); ctx.translate(x,Y); ctx.scale(40,30); ctx.arc(0,0,1,-2.6,-.6) if sg>0 else ctx.arc_negative(0,0,1,-.6,-2.6); ctx.restore()
            col(ctx,GOLD,a); ctx.set_line_width(2); ctx.stroke()
        readout(ctx,'SPIN-UP, EACH RING','4.2 TWh · ~70 days',60,110,a=a,w=260)
        label(ctx,'opposite spins: the pair has no net spin',560,560,(XS[0]+XS[1])/2,Y+30,FG,a=seg(t,T0+1,T0+2))
    else:
        readout(ctx,'RING 2','its counter-rotating twin',60,110,w=260)
    caption(ctx,'2 · ITS TWIN, THEN SPIN-UP','Ring 2 is built 2 km along. Motors in the two pods then push the rings against each other through the spine, so they spin up in opposite directions with no propellant and the pair has no net spin.')
    fade(ctx,t,dur)

def d3(ctx,t,dur):
    background(ctx); head(ctx)
    u=ease(seg(t,1,6)); tilt=4*math.sin(math.pi*u) if 0<u<1 else 0
    sun(ctx,seg(t,5,6.5)); spine(ctx); pods(ctx)
    for i in range(2): ring(ctx,XS[i],1,1,1,1,phi=phi_of(i,-20,t+30),tilt=tilt*(1 if i==0 else -1))
    tugs(ctx,190,1130,t,on=False)
    x,y=1130,150
    col(ctx,'#11131b',.9); ctx.rectangle(x-90,y-60,180,140); ctx.fill()
    ctx.new_path(); ctx.arc(x,y,40,0,2*math.pi); col(ctx,'#2c2a24'); ctx.set_line_width(1); ctx.stroke()
    ang=math.radians(-90+90*u)
    col(ctx,GOLD); ctx.set_line_width(2); ctx.move_to(x-40*math.cos(ang),y-40*math.sin(ang)); ctx.line_to(x+40*math.cos(ang),y+40*math.sin(ang)); ctx.stroke()
    text(ctx,'AXIS: TURNING TO THE SUN' if u<1 else 'AXIS: POINTED AT THE SUN',x,y+62,10,MUT,anchor='c',spacing=1)
    text(ctx,f'{90*u:4.1f}° of 90°',x,y+76,10,GOLD,anchor='c')
    label(ctx,'each ring tilts 0.004° against its twin (drawn 1,000× larger)',380,560,XS[0]+20,Y+120,GOLD,a=seg(t,1.2,2))
    label(ctx,'tugs idle: no propellant',900,470,1130+40,Y+8,FG,a=seg(t,2,3))
    caption(ctx,'3 · THE PAIR STEERS THE WHOLE STACK','Tilting the two spinning rings very slightly in opposite directions acts like a giant gyroscope, turning the stack to face the Sun and then holding it there through each orbit.')
    fade(ctx,t,dur)

def d4(ctx,t,dur):
    background(ctx); head(ctx); sun(ctx,1); spine(ctx); pods(ctx)
    for i in range(2): ring(ctx,XS[i],1,1,1,1,phi=phi_of(i,-20,t+30))
    starts=[.5,3.3,6.1,8.9]; L=2.8
    done=2
    for j,i in enumerate(range(2,6)):
        f=ease(seg(t,starts[j],starts[j]+L))
        pair_done=starts[j - (j%2) +1]+L if j%2==0 else starts[j]+L
        ring(ctx,XS[i],sp=min(1,f*2),tube=f,mid=f,wing=f,phi=phi_of(i,pair_done,t))
        done+=f
    tugs(ctx,190,1130,t,on=False)
    readout(ctx,'RINGS',f'{done:3.1f} of 6',60,110)
    readout(ctx,'PEOPLE AT FULL OCCUPANCY',f'{done*0.55:3.1f} M',300,110,GOLD,w=280)
    label(ctx,'bay factories hop along the spine to the next pod',560,560,XS[3],Y+RYe-20,CY,a=seg(t,1,2))
    caption(ctx,'4 · TWO MORE PAIRS','The same bay factories, crawlers and wing robots move down the spine to the next pod, so every pair after the first reuses the whole construction fleet. Six rings hold about 3.3 million people.')
    fade(ctx,t,dur)

def d5(ctx,t,dur):
    background(ctx); head(ctx)
    o=COST['opt'][:18]; c=COST['cons'][:18]
    x0,y0,x1,y1=120,230,1180,540
    text(ctx,'BUILD COST PER RESIDENT FOR EACH NEW RING',x0,108,15,FG,spacing=2)
    vmax=700e3
    for v in (0,200e3,400e3,600e3):
        yy=y1-(y1-y0)*v/vmax; col(ctx,'#2c2a24'); ctx.set_line_width(1); ctx.move_to(x0,yy); ctx.line_to(x1,yy); ctx.stroke()
        text(ctx,f'${v/1e3:.0f}k',x0-10,yy+4,11,MUT,anchor='r')
    bw=(x1-x0)/18
    for i in range(18):
        g=ease(seg(t,.5+i*.25,1.3+i*.25)); xx=x0+i*bw
        hc=(y1-y0)*c[i]['pp_spine']/vmax*g; ho=(y1-y0)*o[i]['pp_spine']/vmax*g
        col(ctx,CY,.25); ctx.rectangle(xx+bw*.12,y1-hc,bw*.76,hc); ctx.fill()
        col(ctx,CY,.9); ctx.set_line_width(1); ctx.rectangle(xx+bw*.12,y1-hc,bw*.76,hc); ctx.stroke()
        col(ctx,GOLD); ctx.rectangle(xx+bw*.25,y1-ho,bw*.5,ho); ctx.fill()
        text(ctx,str(i+1),xx+bw/2,y1+18,11,MUT,anchor='c')
    text(ctx,'ring number',x0,y1+34,11,MUT)
    for i in (6,12):
        xx=x0+i*bw; col(ctx,FG,.5); ctx.set_dash([3,4]); ctx.move_to(xx,y0); ctx.line_to(xx,y1); ctx.stroke(); ctx.set_dash([])
        text(ctx,'↑ new spine',xx+bw/2,y1+34,11,FG,anchor='c',a=.8)
    a=seg(t,5.5,6.5)
    col(ctx,GOLD,a); ctx.rectangle(120,y0-60,14,14); ctx.fill(); text(ctx,'optimistic',140,y0-48,12,FG,a=a)
    col(ctx,CY,a); ctx.rectangle(250,y0-60,14,14); ctx.stroke(); text(ctx,'conservative',270,y0-48,12,FG,a=a)
    a=seg(t,6.5,7.5)
    readout(ctx,'RING 1 → RING 100 (OPTIMISTIC)',f"${o[0]['pp_spine']/1e3:.0f}k → ${COST['opt'][99]['pp_spine']/1e3:.0f}k",580,118,GOLD,a=a,w=290)
    readout(ctx,'RING 1 → RING 100 (CONSERVATIVE)',f"${c[0]['pp_spine']/1e3:.0f}k → ${COST['cons'][99]['pp_spine']/1e3:.0f}k",880,118,CY,a=a,w=290)
    caption(ctx,'5 · EACH NEW RING COSTS LESS PER PERSON','Factories are reused and Earth-made parts get cheaper with each ring built. Each new spine adds a small bump. Over 100 rings the build cost per resident falls by about half (optimistic) or a quarter (conservative).')
    fade(ctx,t,dur)

def d6(ctx,t,dur):
    o=COST['opt']; c=COST['cons']
    card(ctx,'A RING STACK, IN NUMBERS',[
        ('Stack','6 rings (3 counter-rotating pairs) on a 14 km spine, 2 km apart'),
        ('People','~3.3 million (550,000 per ring, stacked homes)'),
        ('Steering','Tug Starships during the build; spinning pairs as gyroscopes after'),
        ('Cost per resident',f"ring 1 ${o[0]['pp_spine']/1e3:.0f}k–{c[0]['pp_spine']/1e3:.0f}k → ring 100 ${o[99]['pp_spine']/1e3:.0f}k–{c[99]['pp_spine']/1e3:.0f}k"),
        ('Home price (2.5 people)',f"ring 1 ${o[0]['home']/1e6:.2f}–{c[0]['home']/1e6:.2f}M → ring 100 ${o[99]['home']/1e6:.2f}–{c[99]['home']/1e6:.2f}M"),
        ('Shading','Each upstream ring shades ~2% of the next ring\'s wings, on average'),
    ],t,dur,'order-of-magnitude estimates · 100 rings sharing the lunar industry')

SCENES=[('sd1',d1,10),('sd2',d2,10.5),('sd3',d3,9),('sd4',d4,13.5),('sd5',d5,13),('sd6',d6,8)]
if __name__=='__main__': main(SCENES,'ring-stack')
