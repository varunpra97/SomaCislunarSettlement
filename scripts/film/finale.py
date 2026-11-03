import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'stack'))
from common import *
import stackvid as SV
import logo as LG
OUTF=os.path.dirname(os.path.abspath(__file__))
SCX,SCY=640,330
K0=11.8      # px per km in the stack side view
EARTH_SCR=(630,345); R_FINAL=170
K1=R_FINAL/384400
MA=LG.MOON_ANG; RD=30000; ML=384400
M=(ML*math.cos(MA),ML*math.sin(MA))
def phi_at(t): return math.radians(205)+ (16-t)*0.05   # ring creeps along its loop (clockwise on screen)
def finale(ctx,t,dur):
    background(ctx)
    u=ease(seg(t,2.5,12.5))                     # zoom progress
    k=math.exp(math.log(K0)+(math.log(K1)-math.log(K0))*u)
    w2=ease(seg(t,10.5,13.5))                    # morph to logo proportions
    rl=RD*(1+0.97*w2*(59/(RD*K1)-1))             # loop radius in km, true -> logo
    ph=phi_at(t)
    S=(M[0]+rl*math.cos(ph),M[1]+rl*math.sin(ph))
    Cfin=(-(EARTH_SCR[0]-SCX)/K1,-(EARTH_SCR[1]-SCY)/K1)
    wc=ease(seg(u,0.3,1.0))
    Sf=(SCX+(S[0]-Cfin[0])*K1,SCY+(S[1]-Cfin[1])*K1)
    St=(lerp(SCX,Sf[0],wc),lerp(SCY,Sf[1],wc))
    C=(S[0]-(St[0]-SCX)/k,S[1]-(St[1]-SCY)/k)
    P=lambda q:(SCX+(q[0]-C[0])*k,SCY+(q[1]-C[1])*k)
    # Moon orbit + loop + bodies
    E=P((0,0)); Mo=P(M); Rs=ML*k
    a_orb=clamp(1-(Rs-900)/900) if Rs>0 else 1
    if a_orb>0:
        ctx.new_path(); ctx.arc(*E,Rs,0,2*math.pi); col(ctx,MUT,.7*a_orb); ctx.set_line_width(2); ctx.stroke()
    a_loop=clamp(1-(rl*k-1500)/1500)
    if a_loop>0:
        ctx.new_path(); ctx.arc(*Mo,rl*k,0,2*math.pi); col(ctx,GOLD,a_loop); ctx.set_line_width(lerp(2,5*0.0+2.6,w2)+1.5*w2); ctx.stroke()
    rm=max(1737*k,12*w2, min(1737*k,12)); re=max(6371*k,26*w2)
    if Mo[0]>-200 and Mo[0]<1480:
        ctx.new_path(); ctx.arc(*Mo,rm,0,2*math.pi); col(ctx,'#ede6d8'); ctx.fill()
    ctx.new_path(); ctx.arc(*E,max(re,1),0,2*math.pi); col(ctx,'#66c2d4'); ctx.fill()
    # the stack
    Sp=P(S); sc=k/K0
    a_side=clamp((sc-0.02)/0.05)
    if a_side>0:
        ctx.save(); ctx.translate(*Sp); ctx.scale(sc,sc); ctx.translate(-640,-330)
        ctx.push_group()
        SV.sun(ctx,1); SV.spine(ctx); SV.pods(ctx)
        for i in range(6): SV.ring(ctx,SV.XS[i],1,1,1,1,phi=SV.phi_of(i,-20,t+40))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a_side); ctx.restore()
    if a_side<1:
        a=1-a_side
        ctx.save(); ctx.translate(*Sp); ctx.rotate(math.radians(-30)); ctx.scale(1,.42)
        ctx.new_path(); ctx.arc(0,0,lerp(6,13,w2),0,2*math.pi); ctx.restore()
        col(ctx,BG,a); ctx.fill_preserve(); col(ctx,GOLD,a); ctx.set_line_width(lerp(2,4.5,w2)); ctx.stroke()
    # labels
    if t<4: label(ctx,'THE FINISHED STACK · 6 RINGS · 3.3 MILLION PEOPLE',820,560,Sp[0]+200*sc,Sp[1]+120*sc,GOLD,a=seg(t,.3,1)*(1-seg(t,3,4)))
    la=seg(t,6,7)*(1-seg(t,10,11))
    if la>0:
        label(ctx,'THE MOON',Mo[0]+70,Mo[1]-70,Mo[0]+rm*.7,Mo[1]-rm*.7,FG,a=la)
        label(ctx,'30,000 km loop, circled backwards every 4.7 days',Mo[0]-200,Mo[1]+rl*k+50,Mo[0],Mo[1]+rl*k,GOLD,a=la)
    lb=seg(t,10,10.8)*(1-seg(t,12.2,13))
    if lb>0:
        label(ctx,'EARTH',E[0]-90,E[1]+60,E[0]-re,E[1]+re*.5,CY,a=lb)
        label(ctx,'the Moon carries it around Earth each month',120,560,E[0]-Rs*.707,E[1]+Rs*.707,MUT,a=lb)
    # wordmark
    wa=seg(t,13.2,14.4)
    if wa>0:
        th=dict(LG.DARK); LG.word(ctx,640,640,44,th=th,a=wa,anchor='c',sub='CISLUNAR RING SETTLEMENT')
    if t>12.5:
        # arrows of the logo
        aa=seg(t,12.5,13.5)
        b=MA-math.radians(70); LG.arrowhead(ctx,E[0]+Rs*math.cos(b),E[1]+Rs*math.sin(b),b-math.pi/2,7,tuple(c*1 for c in LG.DARK['orbit'])) if aa>.5 else None
        c=math.radians(60); LG.arrowhead(ctx,Mo[0]+rl*k*math.cos(c),Mo[1]+rl*k*math.sin(c),c+math.pi/2,8,LG.DARK['gold']) if aa>.5 else None
    hdr(ctx,'THE FINISHED STACK','WHERE IT LIVES') if t<11 else None
    a_out=seg(t,dur-.8,dur)
    if a_out>0: col(ctx,'#000000',a_out); ctx.paint()
    if t<.4: col(ctx,'#000000',1-t/.4); ctx.paint()

def titlecard(ctx,t,dur):
    background(ctx)
    a=seg(t,.2,1.2)
    ctx.push_group(); LG.mark(ctx,630,300,k=.9,th=LG.DARK); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    LG.word(ctx,640,560,44,a=seg(t,.8,1.8),anchor='c')
    fade(ctx,t,dur,fi=.4,fo=.6)
CH=[('1','THE SPINE AND CENTRE PODS','280 Starships docked nose to tail, then wrapped in drums'),
    ('2','THE BAY FACTORY','the machine that builds the tube, 18 m at a time'),
    ('3','BUILDING THE TUBE','panels from Starships, sealed bay by bay, then shielded with lunar regolith'),
    ('4','SPOKES AND THE MIDDLE RING','six spokes in balanced pairs, then a 0.5 g ring halfway out'),
    ('5','SOLAR WINGS AND RADIATORS','6 GW of wings on the spokes, 650 fins on the tube'),
    ('6','THE RING STACK','twin rings, spin-up, Sun-pointing and the cost of each new ring')]
def chapter(i):
    n,ti,sub=CH[i]
    def f(ctx,t,dur):
        background(ctx)
        ctx.push_group(); LG.mark(ctx,628,250,k=.32,th=LG.DARK,arrows=False); ctx.pop_group_to_source(); ctx.paint_with_alpha(.85*seg(t,.1,.6))
        text(ctx,f'CHAPTER {n}',640,360,14,GOLD,anchor='c',spacing=4,a=seg(t,.2,.7))
        text(ctx,ti,640,405,30,FG,anchor='c',spacing=4,a=seg(t,.3,.9))
        text(ctx,sub,640,445,16,MUT,anchor='c',font=SANS,a=seg(t,.5,1.1))
        fade(ctx,t,dur,fi=.3,fo=.4)
    return f
SCENES=[('title',titlecard,4)]+[(f'ch{i+1}',chapter(i),2.6) for i in range(6)]+[('finale',finale,17)]
if __name__=='__main__':
    args=sys.argv[1:]
    if args and args[0]=='stills':
        for nm,fn,d in SCENES:
            if nm in ('title','ch1','finale'):
                for fr in [float(x) for x in args[1:]]:
                    print(still(nm,fn,d,fr*d,outdir=OUTF))
    else:
        for nm,fn,d in SCENES:
            if not args or nm in args: render(nm,fn,d,outdir=OUTF)
