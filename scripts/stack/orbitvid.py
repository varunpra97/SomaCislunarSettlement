from common import *
import json, numpy as np
D=json.load(open(os.path.join(OUT,'orbit.json')))
mu,LU,TU,ws,yr=D['mu'],D['LU'],D['TU'],D['ws'],D['yr']
P2=np.array(D['p2']); T2=np.array(D['t2']); B=np.array(D['B']); K=np.array(D['K']); TT=np.array(D['tt'])
MX,MY=700,330; SC=230/36000   # px per km
def rot2px(p): return (MX+(p[0]-(1-mu))*LU*SC, MY-(p[1])*LU*SC)
def head(ctx): hdr(ctx,'A STABLE ORBIT FOR THE STACK','LUNAR DISTANT RETROGRADE ORBIT · 30,000 km')
def moon(ctx,x,y,r=11):
    ctx.new_path(); ctx.arc(x,y,r,0,2*math.pi); col(ctx,'#b9b2a3'); ctx.fill()
def ringicon(ctx,x,y,n=1,s=1.0):
    for i in range(n):
        ctx.new_path(); ctx.arc(x+(i-(n-1)/2)*4*s,y,6*s,0,2*math.pi); col(ctx,GOLD); ctx.set_line_width(1.6); ctx.stroke()
def sun_dir(t_units): return -ws*t_units  # angle of Sun in rotating frame
def shadow(ctx,ang):
    ux,uy=-math.cos(ang),math.sin(ang)  # screen: y flipped
    px,py=-uy,ux; r=11; L=330
    ctx.move_to(MX+px*r,MY+py*r); ctx.line_to(MX+px*r*.9+ux*L,MY+py*r*.9+uy*L); ctx.line_to(MX-px*r*.9+ux*L,MY-py*r*.9+uy*L); ctx.line_to(MX-px*r,MY-py*r); ctx.close_path()
    col(ctx,'#000000',.55); ctx.fill()
def sunarrow(ctx,ang):
    x,y=MX+300*math.cos(ang),MY-300*math.sin(ang)
    x=clamp(x,70,1210); y=clamp(y,95,575)
    ctx.new_path(); ctx.arc(x,y,9,0,2*math.pi); col(ctx,'#ffd27a'); ctx.fill(); text(ctx,'SUN',x,y-14,10,'#ffd27a',anchor='c')
def scalebar(ctx):
    x,y=980,555; L=10000*SC; col(ctx,MUT); ctx.set_line_width(1.5); ctx.move_to(x,y); ctx.line_to(x+L,y); ctx.stroke()
    text(ctx,'10,000 km',x+L/2,y-8,11,MUT,anchor='c')
def earthmark(ctx):
    col(ctx,CY); ctx.set_line_width(1.5); ctx.move_to(130,MY); ctx.line_to(60,MY); ctx.stroke()
    ctx.move_to(60,MY); ctx.line_to(70,MY-5); ctx.line_to(70,MY+5); ctx.close_path(); ctx.fill()
    text(ctx,'EARTH',100,MY-12,11,CY,anchor='c'); text(ctx,'384,000 km',100,MY+20,11,MUT,anchor='c')

def o1(ctx,t,dur):
    background(ctx); head(ctx)
    days=28*seg(t,.5,dur-1)
    tu=days*86400/TU; i=int(np.searchsorted(T2,tu)); i=max(1,min(i,len(T2)-1))
    ang=sun_dir(T2[i]); shadow(ctx,ang); sunarrow(ctx,ang); earthmark(ctx); moon(ctx,MX,MY)
    pts=[rot2px(p) for p in P2[:i]]
    col(ctx,CY,.8); ctx.set_line_width(1.6); ctx.move_to(*pts[0]); [ctx.line_to(*p) for p in pts[1:]]; ctx.stroke()
    x,y=pts[-1]; ringicon(ctx,x,y)
    p=P2[i-1]; dm=math.hypot(p[0]-(1-mu),p[1])*LU; de=math.hypot(p[0]+mu,p[1])*LU
    # eclipse test
    sx,sy=math.cos(ang),math.sin(ang); rx,ry=(p[0]-(1-mu))*LU,p[1]*LU
    along=-(rx*sx+ry*sy); perp=abs(rx*sy-ry*sx); ecl=along>0 and perp<1600
    readout(ctx,'DAY',f'{days:4.1f}',60,110,w=150)
    readout(ctx,'FROM THE MOON',f'{dm/1e3:4.1f} thousand km',60,172,CY,w=250)
    readout(ctx,'FROM EARTH',f'{de/1e3:4.0f} thousand km',60,234,FG,w=250)
    if ecl: tag(ctx,'IN THE MOON\'S SHADOW',60,320,'#e07a5f')
    text(ctx,'view turns with the Moon around Earth',MX,585,11,MUT,anchor='c')
    scalebar(ctx)
    label(ctx,'ONE RING',x+40,y-30,x+6,y-6,GOLD,a=seg(t,1,2))
    caption(ctx,'1 · ONE RING, CIRCLING THE MOON BACKWARDS','It loops the Moon every 4.7 days, about 30,000 km out, while the Moon carries it around Earth. Now and then it crosses the Moon\'s shadow, for at most ~1.8 hours.')
    fade(ctx,t,dur)

EX,EY,ES=640,330,230/384400
def inert(p,tu):
    x,y=p[0]+mu,p[1]; c,s=math.cos(tu),math.sin(tu)
    return (EX+(x*c-y*s)*LU*ES, EY-(x*s+y*c)*LU*ES)
def o2(ctx,t,dur):
    background(ctx); head(ctx)
    days=60*seg(t,.5,dur-1); tu=days*86400/TU; i=int(np.searchsorted(T2,tu)); i=max(1,min(i,len(T2)-1))
    ctx.new_path(); ctx.arc(EX,EY,230,0,2*math.pi); col(ctx,MUT,.35); ctx.set_line_width(1); ctx.set_dash([3,6]); ctx.stroke(); ctx.set_dash([])
    ctx.new_path(); ctx.arc(EX,EY,9,0,2*math.pi); col(ctx,'#4f8fd6'); ctx.fill(); text(ctx,'EARTH',EX,EY+26,11,CY,anchor='c')
    pts=[inert(P2[k],T2[k]) for k in range(i)]
    col(ctx,GOLD,.85); ctx.set_line_width(1.3); ctx.move_to(*pts[0]); [ctx.line_to(*p) for p in pts[1:]]; ctx.stroke()
    m=(EX+(1)*math.cos(T2[i-1])*230, EY-(1)*math.sin(T2[i-1])*230); moon(ctx,*m,r=5)
    ringicon(ctx,*pts[-1],s=.7)
    readout(ctx,'DAY',f'{days:4.1f}',60,110,w=150)
    label(ctx,'MOON\'S PATH AROUND EARTH',820,140,EX+230*math.cos(.9),EY-230*math.sin(.9),MUT,a=seg(t,1,2))
    label(ctx,'THE STACK: small loops around the Moon',860,560,*pts[-1],GOLD,a=seg(t,2,3))
    caption(ctx,'2 · THE SAME ORBIT, SEEN FROM ABOVE EARTH','In a fixed view the stack simply rides along with the Moon, tracing small loops around it. Its distance from Earth only swings between about 355,000 and 415,000 km.')
    fade(ctx,t,dur)

def o3(ctx,t,dur):
    background(ctx); head(ctx); moon(ctx,MX,MY); earthmark(ctx)
    years=20*seg(t,.5,dur-1.5); tu=years*yr; i=int(np.searchsorted(TT,tu)); i=max(2,min(i,len(TT)))
    n=sum(1 for a in [0]+D['adds'] if years>=a)
    for arr,c,a in ((B,CY,.18),(K,GOLD,.18)):
        pts=[rot2px(p) for p in arr[:i]]
        col(ctx,c,a); ctx.set_line_width(.8); ctx.move_to(*pts[0]); [ctx.line_to(*p) for p in pts[1:]]; ctx.stroke()
    pB=rot2px(B[i-1]); pK=rot2px(K[i-1])
    ctx.new_path(); ctx.arc(*pB,3,0,2*math.pi); col(ctx,CY); ctx.fill()
    ringicon(ctx,*pK,n=min(n,6),s=.8)
    dmB=np.hypot(B[:i,0]-(1-mu),B[:i,1])*LU; dmK=np.hypot(K[:i,0]-(1-mu),K[:i,1])*LU
    readout(ctx,'YEAR',f'{years:4.1f}',60,110,w=150)
    readout(ctx,'RINGS IN THE STACK',f'{min(n,6)}  ·  {min(n,6)*0.3:.1f} Gt',60,172,GOLD,w=250)
    readout(ctx,'RANGE FROM THE MOON',f'{min(dmB.min(),dmK.min())/1e3:.0f}–{max(dmB.max(),dmK.max())/1e3:.0f} thousand km',60,234,CY,w=250)
    col(ctx,CY); ctx.rectangle(980,120,14,3); ctx.fill(); text(ctx,'no kicks',1000,125,11,FG)
    col(ctx,GOLD); ctx.rectangle(980,140,14,3); ctx.fill(); text(ctx,'2 m/s kick as each ring is added',1000,145,11,FG)
    scalebar(ctx)
    caption(ctx,'3 · TWENTY YEARS, SIX RINGS','Adding mass doesn\'t change the orbit: gravity pulls a 2-gigatonne stack exactly like a 1-tonne probe. Even a 2 m/s kick each time a ring is added leaves it bound, 28,000–36,000 km from the Moon.')
    fade(ctx,t,dur)

def o4(ctx,t,dur):
    background(ctx); head(ctx)
    x0,y0,x1,y1=140,190,1150,520
    text(ctx,'WHAT DOES GROW WITH EACH RING: THE COST OF CORRECTIONS',x0,130,15,FG,spacing=1.5)
    text(ctx,'reaction mass a year for each 1 m/s of correction, thrown by a mass driver at 2.4 km/s',x0,155,12,MUT)
    vmax=0.9
    for v in (0,.25,.5,.75):
        yy=y1-(y1-y0)*v/vmax; col(ctx,'#2c2a24'); ctx.set_line_width(1); ctx.move_to(x0,yy); ctx.line_to(x1,yy); ctx.stroke()
        text(ctx,f'{v:.2f} Mt',x0-10,yy+4,11,MUT,anchor='r')
    bw=(x1-x0)/6
    for k in range(1,7):
        g=ease(seg(t,.5+k*.4,1.3+k*.4)); v=k*0.3e12/2400/1e9*g
        h=(y1-y0)*v/vmax; xx=x0+(k-1)*bw
        col(ctx,GOLD); ctx.rectangle(xx+bw*.25,y1-h,bw*.5,h); ctx.fill()
        if g>.95: text(ctx,f'{k*0.125:.3f}',xx+bw/2,y1-h-8,12,FG,anchor='c')
        text(ctx,f'{k} ring'+('s' if k>1 else ''),xx+bw/2,y1+20,12,MUT,anchor='c')
    a=seg(t,4,5)
    readout(ctx,'LUNAR DRO','no correction needed to stay bound',x0+10,200,CY,a=a,w=450)
    readout(ctx,'L4/L5 AT ~10 m/s A YEAR, 6 RINGS','~7.5 Mt of reaction mass a year',x0+10,262,RED,a=a,w=450)
    caption(ctx,'4 · WHY THE ORBIT CHOICE MATTERS MORE AS IT GROWS','Every metre per second of correction costs more reaction mass as rings are added. The DRO needs only small navigation trims; an orbit that needs tens of m/s a year would cost millions of tonnes a year at six rings.')
    fade(ctx,t,dur)

def o5(ctx,t,dur):
    card(ctx,'THE ORBIT, IN NUMBERS',[
        ('Orbit','Lunar distant retrograde orbit, ~30,000 km from the Moon, 4.7-day loop'),
        ('Stability','Bound for 20 years in a model with Earth, Moon and Sun; 28,000–36,000 km from the Moon'),
        ('Larger DROs','40,000–70,000 km versions drifted off within 2–4 years unless set on a resonance'),
        ('Eclipses','Moon\'s shadow at most ~1.8 h, a few times a month in eclipse seasons'),
        ('From Earth','355,000–415,000 km; ~4–5 day trips'),
        ('As rings are added','Same path; only the cost of corrections grows with mass'),
    ],t,dur,'simplified model: planar Earth–Moon–Sun (bicircular) · confirm with a full ephemeris')

SCENES=[('so1',o1,13),('so2',o2,11),('so3',o3,15),('so4',o4,11),('so5',o5,8)]
if __name__=='__main__': main(SCENES,'stable-orbit')
