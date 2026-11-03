from common import *
from spokes import P, ANG, CXc, CYc, RP, planned, hub, spoke
def head(ctx): hdr(ctx,'INSTALLING SOLAR WINGS','AND RADIATOR FINS')

def blanket(ctx,x0,x1,y0,y1,a=1):
    if x1<=x0: return
    col(ctx,SOLAR,a); ctx.rectangle(x0,y0,x1-x0,y1-y0); ctx.fill()
    col(ctx,SOLARL,.55*a); ctx.set_line_width(.8)
    x=x0
    while x<x1: ctx.move_to(x,y0); ctx.line_to(x,y1); x+=16
    ctx.stroke()
    for yy in (y0+(y1-y0)/3,y0+2*(y1-y0)/3): ctx.move_to(x0,yy); ctx.line_to(x1,yy)
    ctx.stroke()

def b1(ctx,t,dur):
    background(ctx); head(ctx); tag(ctx,'TIME-LAPSE · ONE SPOKE',1060,110)
    y=340; x0=130; x1=1180
    truss_h(ctx,x0,x1,y,30,CY,step=16)
    col(ctx,PANEL); ctx.rectangle(50,y-60,80,120); ctx.fill(); text(ctx,'HUB',90,y+82,13,MUT,anchor='c')
    f=ease(seg(t,1,11)); rx=lerp(x0+60,x1-40,f)
    W_=120
    blanket(ctx,x0+30,rx-26,y-15-W_,y-17); blanket(ctx,x0+30,rx-26,y+17,y+15+W_)
    # ribs
    col(ctx,STEEL); ctx.set_line_width(2)
    xr=x0+30
    while xr<rx-20:
        ctx.move_to(xr,y-15-W_); ctx.line_to(xr,y+15+W_); xr+=70
    ctx.stroke()
    # robot with rolls
    col(ctx,'#1b2a30'); ctx.rectangle(rx-26,y-24,44,48); ctx.fill(); col(ctx,CY); ctx.set_line_width(2); ctx.rectangle(rx-26,y-24,44,48); ctx.stroke()
    for sg in (-1,1):
        cy_=y+sg*(15+W_/2)
        col(ctx,STEEL); ctx.set_line_width(3); ctx.move_to(rx-4,y+sg*24); ctx.line_to(rx-4,cy_); ctx.stroke()
        rr=10+8*(1-f)
        ctx.new_path(); ctx.save(); ctx.translate(rx-22,cy_); ctx.scale(.5,1); ctx.arc(0,0,W_/2,0,2*math.pi); ctx.restore(); col(ctx,SOLARL,.9); ctx.set_line_width(rr*.35); ctx.stroke()
    readout(ctx,'WING LAID',f'{16*f:4.1f} of 16 km',60,110)
    label(ctx,'WING ROBOT unrolls lunar-made cells on film',min(rx-220,860),205,rx-10,y-26,CY,a=seg(t,1.5,2.5))
    label(ctx,'90 m each side of the spoke',260,560,300,y+15+W_,SOLARL,a=seg(t,3,4))
    label(ctx,'RIBS clip to the truss every 30 m',640,575,x0+240,y+15+W_,STEEL,a=seg(t,5,6))
    caption(ctx,'1 · A WING ROBOT WALKS EACH SPOKE','It clips ribs to the truss and unrolls two 90 m blankets of solar cells as it goes, then plugs each section into the conductor that runs down the spoke to the ring.')
    fade(ctx,t,dur)

def wing_top(ctx,d,f,a=1):
    if f<=0: return
    r0,r1=24,24+(RP-34-24)*f
    ang=math.radians(d); ux,uy=math.cos(ang),math.sin(ang); px,py=-uy,ux; w=7
    pts=[(CXc+ux*r0+px*w,CYc+uy*r0+py*w),(CXc+ux*r1+px*w,CYc+uy*r1+py*w),(CXc+ux*r1-px*w,CYc+uy*r1-py*w),(CXc+ux*r0-px*w,CYc+uy*r0-py*w)]
    ctx.move_to(*pts[0]); [ctx.line_to(*p) for p in pts[1:]]; ctx.close_path(); col(ctx,SOLAR,a); ctx.fill_preserve(); col(ctx,SOLARL,a); ctx.set_line_width(1); ctx.stroke()

def ring_top(ctx,a=1,w=9):
    ctx.new_path(); ctx.arc(CXc,CYc,RP,0,2*math.pi); col(ctx,CYD,a); ctx.set_line_width(w); ctx.stroke()
    ctx.new_path(); ctx.arc(CXc,CYc,RP/2,0,2*math.pi); col(ctx,GOLD,.6*a); ctx.set_line_width(3); ctx.stroke()

def b2(ctx,t,dur):
    background(ctx); head(ctx); ring_top(ctx)
    for d in ANG: spoke(ctx,d,1,CY,2.5)
    hub(ctx)
    tot=0
    for i,d in enumerate(ANG):
        f=ease(seg(t,.6+i*.9,2.2+i*.9)); wing_top(ctx,d,f); tot+=f
    readout(ctx,'WING AREA',f'{17*tot/6:4.1f} km²',990,150,SOLARL)
    readout(ctx,'POWER (START OF LIFE)',f'{6*tot/6:3.1f} GW',990,215,GOLD)
    label(ctx,'AXIS POINTS AT THE SUN: wings face it all day',820,560,P(160,30)[0],P(160,30)[1],FG,a=seg(t,5,6))
    caption(ctx,'2 · ALL SIX SPOKES','About 2.9 km² per spoke, 17 km² in all. With the spin axis pointed at the Sun, the wings face it constantly as they turn, with no tracking motors and no slip rings.')
    fade(ctx,t,dur)

def b3(ctx,t,dur):
    background(ctx); head(ctx); tag(ctx,'ONE CELL · LOOKING ALONG THE RING',990,110)
    cx,cy=430,420; Rt=110; Rs=140
    # shield ring + tube
    ctx.new_path(); ctx.arc(cx,cy,Rs,0,2*math.pi); col(ctx,SHIELD); ctx.set_line_width(36); ctx.stroke()
    ctx.new_path(); ctx.arc(cx,cy,Rt,0,2*math.pi); col(ctx,CY); ctx.set_line_width(3); ctx.stroke()
    for i in range(1,5):
        yy=cy-Rt+i*2*Rt/5; hw=math.sqrt(max(0,Rt**2-(yy-cy)**2))
        col(ctx,CYD,.6); ctx.set_line_width(1); ctx.move_to(cx-hw,yy); ctx.line_to(cx+hw,yy); ctx.stroke()
    text(ctx,'HABITAT TUBE Ø 150 m',cx,cy+6,13,CY,anchor='c')
    # slot at top (outward drawn up)
    sl=24; col(ctx,BG); ctx.rectangle(cx-sl/2,cy-Rs-20,sl,40); ctx.fill()
    # fin unfold
    fu=ease(seg(t,4,8)); Hf=110*fu; Wf=220
    if t>3:
        pk=seg(t,3,4)
        col(ctx,PANEL,.95); ctx.rectangle(cx-Wf/2,cy-Rs-18-max(Hf,14*pk),Wf,max(Hf,14*pk)); ctx.fill()
        n=max(1,int(Hf/23))
        col(ctx,'#8f846c'); ctx.set_line_width(1)
        for i in range(n+1):
            yy=cy-Rs-18-i*(max(Hf,14)/max(n,1)); ctx.move_to(cx-Wf/2,yy); ctx.line_to(cx+Wf/2,yy)
        ctx.stroke()
    # carrier
    u=ease(seg(t,.5,3))
    ang=lerp(-160,-118,u); cxr=cx+(Rs+30)*math.cos(math.radians(ang)); cyr=cy+(Rs+30)*math.sin(math.radians(ang))
    ctx.save(); ctx.translate(cxr,cyr); ctx.rotate(math.radians(ang+90)); col(ctx,'#1b2a30'); ctx.rectangle(-30,-12,60,24); ctx.fill(); col(ctx,GOLD); ctx.set_line_width(2); ctx.rectangle(-30,-12,60,24); ctx.stroke(); ctx.restore()
    # coolant
    cl=seg(t,8.3,9.5)
    if cl>0:
        col(ctx,CY,cl); ctx.set_line_width(3)
        for xx in (cx-60,cx+60):
            ctx.move_to(xx,cy-Rt); ctx.line_to(xx,cy-Rs-18-Hf*cl); ctx.stroke()
    if t>10:
        a=seg(t,10,10.6); ctx.arc(cx+Wf/2+30,cy-Rs-70,16,0,2*math.pi); col(ctx,GREEN,a); ctx.fill()
        col(ctx,BG,a); ctx.set_line_width(3); ctx.move_to(cx+Wf/2+22,cy-Rs-70); ctx.line_to(cx+Wf/2+28,cy-Rs-64); ctx.line_to(cx+Wf/2+38,cy-Rs-78); ctx.stroke()
        text(ctx,'LEAK TEST OK',cx+Wf/2+52,cy-Rs-65,13,GREEN,a=a)
    label(ctx,'REGOLITH SHIELD (thickness exaggerated)',820,560,cx+Rs*.7,cy+Rs*.7,SHIELDL,a=seg(t,.5,1.5))
    label(ctx,'FIN CARRIER on the shield rail',60,300,cxr-20,cyr,GOLD,a=seg(t,1,2))
    label(ctx,'FIN 150 × 75 m (to scale), folds out of its slot',700,135,cx+Wf/2-10,cy-Rs-18-Hf*.6 if Hf>0 else cy-Rs-20,PANEL,a=seg(t,5,6))
    label(ctx,'AMMONIA LOOPS connect',820,330,cx+60,cy-Rs,CY,a=seg(t,8.5,9.3))
    readout(ctx,'FIN TEMPERATURE','~27 °C',990,420,GOLD,a=seg(t,9,10))
    caption(ctx,'3 · ONE RADIATOR FIN PER CELL','A carrier rides the rail on the outer shield, docks a folded fin into the cell\'s slot and unfolds it to 75 m. Robots connect the coolant loops, test for leaks and move on to the next cell.')
    fade(ctx,t,dur)

def b4(ctx,t,dur):
    background(ctx); head(ctx); ring_top(ctx)
    for d in ANG: spoke(ctx,d,1,CY,2.5); wing_top(ctx,d,1)
    hub(ctx)
    N=650; f=ease(seg(t,.5,8.5)); n=int(N*f)
    col(ctx,PANEL); ctx.set_line_width(1.2)
    for i in range(n):
        a=math.radians(i*360/N - 90)
        ctx.move_to(CXc+(RP+6)*math.cos(a),CYc+(RP+6)*math.sin(a)); ctx.line_to(CXc+(RP+17)*math.cos(a),CYc+(RP+17)*math.sin(a))
    ctx.stroke()
    readout(ctx,'FINS INSTALLED',f'{n} of 650',990,150,PANEL)
    readout(ctx,'HEAT SHED',f'{6*f:3.1f} GW',990,215,GOLD)
    label(ctx,'faces point along the ring: Sun sees only their edges',780,560,P(RP+12,60)[0],P(RP+12,60)[1],FG,a=seg(t,3,4))
    caption(ctx,'4 · AROUND THE WHOLE RING','About 650 fins, 7.3 km² in all, go on district by district. Each district cools itself, so a fin failure only affects one cell.')
    fade(ctx,t,dur)

def b5(ctx,t,dur):
    card(ctx,'SOLAR WINGS AND RADIATORS',[
        ('Solar wings','2 × 90 m blankets along ~16 km of each spoke; 17 km², ~6 GW at start of life'),
        ('Installed by','One wing robot per spoke; lunar-made cells on film, ~1 kg/m²'),
        ('When','Before spin-up, in free fall, as each spoke is finished'),
        ('Radiators','~650 fins, 150 × 75 m, one per cell; 7.3 km² at ~27 °C'),
        ('Installed by','Fin carriers on the shield rail; ammonia loops, leak test per fin'),
        ('Upkeep','Spoke robots swap wing panels; hull robots swap fins (monthly checks)'),
    ],t,dur,'order-of-magnitude design study')

SCENES=[('sb1',b1,12),('sb2',b2,9),('sb3',b3,12),('sb4',b4,10),('sb5',b5,7)]
if __name__=='__main__': main(SCENES,'solar-and-radiators')
