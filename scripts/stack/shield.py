from common import *
# The radiation shield: regolith from the Moon, thrown by mass driver, caught and packed on by a second bay factory.
GROUND=470
def mhead(ctx): hdr(ctx,'ON THE MOON','REGOLITH FOR THE SHIELD')
def shead(ctx): hdr(ctx,'BUILDING THE TUBE','HULL FIRST, THEN THE SHIELD')

def rover(ctx,x,load,a=1):
    col(ctx,'#3a3f4a',a); ctx.rectangle(x-22,GROUND-20,44,14); ctx.fill()
    if load>0: col(ctx,SHIELDL,a); ctx.rectangle(x-18,GROUND-20-8*load,30,8*load); ctx.fill()
    for dx in (-14,14):
        ctx.arc(x+dx,GROUND-4,5,0,2*math.pi); col(ctx,STEEL,a); ctx.fill()
    col(ctx,CY,a); ctx.set_line_width(2); ctx.move_to(x+22,GROUND-14); ctx.line_to(x+34,GROUND-4); ctx.stroke()

RAMP0=(560,GROUND-14); RAMP1=(1150,250)
def ramp_pt(u): return (lerp(RAMP0[0],RAMP1[0],u),lerp(RAMP0[1],RAMP1[1],u))

def moon(ctx,t,dur):
    background(ctx); mhead(ctx)
    # sky: Earth and a faint mark where Soma's catcher waits
    ctx.arc(1130,120,22,0,2*math.pi); col(ctx,CY,.8); ctx.fill()
    ctx.arc(1205,85,4,0,2*math.pi); col(ctx,GOLD,.9); ctx.fill()
    text(ctx,"to Soma's catcher",1150,72,11,GOLD,anchor='c',a=seg(t,6,7))
    # ground
    col(ctx,'#2a2c33'); ctx.rectangle(0,GROUND,W,H-GROUND); ctx.fill()
    col(ctx,'#3a3d46'); ctx.set_line_width(1); ctx.move_to(0,GROUND); ctx.line_to(W,GROUND); ctx.stroke()
    for cx,r in ((140,20),(420,12),(980,26),(760,10)):
        ctx.save(); ctx.translate(cx,GROUND+40); ctx.scale(1,.3); ctx.arc(0,0,r,0,2*math.pi); ctx.restore(); col(ctx,'#22242a'); ctx.fill()
    # solar field powering the driver
    for i in range(9):
        x=600+i*42; col(ctx,SOLAR); ctx.rectangle(x,GROUND+18,36,14); ctx.fill(); col(ctx,SOLARL,.6); ctx.set_line_width(1); ctx.rectangle(x,GROUND+18,36,14); ctx.stroke()
    # rovers shuttle regolith to the plant
    for k in range(3):
        ph=((t*.22+k/3)%1.0); go=ph<.5; u=ph*2 if go else 2-ph*2
        rover(ctx,lerp(60,270,u),0 if go else 1)
    # plant: sieve, sort, pack
    col(ctx,'#1b2a30'); ctx.rectangle(300,GROUND-70,110,70); ctx.fill(); col(ctx,CY); ctx.set_line_width(1.5); ctx.rectangle(300,GROUND-70,110,70); ctx.stroke()
    text(ctx,'SIEVE · PACK',355,GROUND-30,11,CY,anchor='c',bold=True)
    col(ctx,STEEL); ctx.set_line_width(3); ctx.move_to(410,GROUND-12); ctx.line_to(RAMP0[0],RAMP0[1]); ctx.stroke()
    # mass driver: rail and coils
    col(ctx,STEEL); ctx.set_line_width(4); ctx.move_to(*RAMP0); ctx.line_to(*RAMP1); ctx.stroke()
    for i in range(26):
        u=i/25; x,y=ramp_pt(u)
        ctx.save(); ctx.translate(x,y); ctx.rotate(math.atan2(RAMP1[1]-RAMP0[1],RAMP1[0]-RAMP0[0])); ctx.scale(.35,1)
        ctx.arc(0,0,11,0,2*math.pi); ctx.restore(); col(ctx,GLASS,.75); ctx.set_line_width(1.5); ctx.stroke()
    for i in range(6):   # pylons
        u=.12+i*.16; x,y=ramp_pt(u); col(ctx,'#3a3f4a'); ctx.set_line_width(2); ctx.move_to(x,y); ctx.line_to(x,GROUND); ctx.stroke()
    # packets: along the conveyor, accelerated up the ramp, then away into the sky
    on=seg(t,1.0,2.0)
    for k in range(14):
        ph=((t*.42+k/14)%1.0)
        if ph<.35:
            u=ph/.35; x=lerp(410,RAMP0[0],u); y=lerp(GROUND-16,RAMP0[1]-2,u)
        elif ph<.75:
            u=((ph-.35)/.4)**2; x,y=ramp_pt(u); y-=2
        else:
            u=(ph-.75)/.25; x=lerp(RAMP1[0],1260,u); y=lerp(RAMP1[1],60,u)
            col(ctx,SPARK,.35*on); ctx.set_line_width(1.5); ctx.move_to(x,y); ctx.line_to(x-24,y+18); ctx.stroke()
        col(ctx,GOLD,on); ctx.rectangle(x-4,y-4,8,8); ctx.fill()
    readout(ctx,'THROUGHPUT','30 Mt / yr',60,110,a=seg(t,1.5,2.2))
    readout(ctx,'EXIT SPEED','2.4 km/s',300,110,CY,w=150,a=seg(t,4,4.7))
    readout(ctx,'PACKETS','~1 t each · ~1 a second',460,110,FG,w=290,a=seg(t,6.5,7.2))
    label(ctx,'ROVERS scoop raw regolith',90,560,160,GROUND-24,FG,a=seg(t,1.2,2))
    label(ctx,'PLANT sieves it and packs ~1 t bags',250,330,355,GROUND-70,CY,a=seg(t,2.6,3.4))
    label(ctx,'MASS DRIVER · coils throw packets at lunar escape speed',600,190,ramp_pt(.55)[0],ramp_pt(.55)[1]-12,GLASS,a=seg(t,4,4.8))
    label(ctx,'~2.7 GW of solar on the regolith',880,560,880,GROUND+32,SOLARL,a=seg(t,8,8.8))
    caption(ctx,'7 · ON THE MOON: REGOLITH TO THE MASS DRIVER','Robots scoop regolith, a plant sieves it and packs it into ~1 t bags, and an electric mass driver throws them at 2.4 km/s, lunar escape speed, about one a second, to a catcher near Soma.')
    fade(ctx,t,dur)

YC=360; HR=60      # tube centre line and hull half-height (px)
GAP=7; SH=26       # gap between hull and shield, shield thickness (px)
def ring_side(ctx,x,R,c,a=1,w=4):
    ctx.save(); ctx.translate(x,YC); ctx.scale(.12,1); ctx.new_path(); ctx.arc(0,0,R,0,2*math.pi); ctx.restore()
    col(ctx,c,a); ctx.set_line_width(w); ctx.stroke()

def shield(ctx,t,dur):
    background(ctx); shead(ctx); tag(ctx,'SIDE VIEW · TIME-LAPSE',1050,110)
    xh=lerp(720,1080,t/dur)            # hull factory front
    xs=xh-330                          # shield factory, trailing
    # hull panels laid so far
    col(ctx,HULL); ctx.rectangle(0,YC-HR,xh-30,2*HR); ctx.fill()
    col(ctx,KEEL,.6); ctx.set_line_width(1)
    x=xh-30
    while x>0: ctx.move_to(x,YC-HR); ctx.line_to(x,YC+HR); x-=36
    ctx.stroke()
    col(ctx,CY,.8); ctx.set_line_width(2); ctx.move_to(0,YC-HR); ctx.line_to(xh-30,YC-HR); ctx.move_to(0,YC+HR); ctx.line_to(xh-30,YC+HR); ctx.stroke()
    # shield laid so far: packed packets outside the hull, with a gap (it does not spin)
    se=xs-24
    for sg in (-1,1):
        y0=YC+sg*(HR+GAP); y1=YC+sg*(HR+GAP+SH)
        col(ctx,SHIELD); ctx.rectangle(0,min(y0,y1),se,SH); ctx.fill()
        col(ctx,SHIELDL,.55); ctx.set_line_width(1)
        for i in range(int(se//10)+1):
            for j in range(3):
                px=i*10+(5 if j%2 else 0); py=min(y0,y1)+3+j*8
                if px<se-4: ctx.rectangle(px,py,7,5)
        ctx.stroke()
    # hull factory (cyan) with its supply Starship
    ring_side(ctx,xh,HR+18,CY); ring_side(ctx,xh-30,HR+18,'#3f8796')
    col(ctx,GOLD,.8); ctx.set_line_width(2)
    for yy in (YC-HR-18,YC+HR+18): ctx.move_to(xh-30,yy); ctx.line_to(xh,yy)
    ctx.stroke()
    ship(ctx,xh+30,YC+HR+44,.32,door=1)
    # shield factory (gold), larger, riding outside the hull
    RS=HR+GAP+SH+22
    ring_side(ctx,xs,RS,GOLD); ring_side(ctx,xs-34,RS,'#a07a30')
    col(ctx,GOLD,.6); ctx.set_line_width(2)
    for yy in (YC-RS,YC+RS): ctx.move_to(xs-34,yy); ctx.line_to(xs,yy)
    ctx.stroke()
    # catcher: a funnel above the shield factory
    cx,cy=xs+40,205
    ctx.move_to(cx-46,cy-30); ctx.line_to(cx+46,cy-30); ctx.line_to(cx+10,cy+14); ctx.line_to(cx-10,cy+14); ctx.close_path()
    col(ctx,'#1b2a30',.9); ctx.fill_preserve(); col(ctx,GOLD); ctx.set_line_width(1.5); ctx.stroke()
    col(ctx,GOLD,.7); ctx.move_to(cx,cy+14); ctx.line_to(xs,YC-RS); ctx.stroke()
    # incoming packets from the Moon, caught, then carried down and packed on at the shield front
    for k in range(9):
        ph=((t*.55+k/9)%1.0)
        if ph<.55:
            u=ph/.55; x=lerp(-40,cx,u); y=lerp(20,cy-26,u)-60*math.sin(u*math.pi)*.3
            col(ctx,SPARK,.35); ctx.set_line_width(1.2); ctx.move_to(x,y); ctx.line_to(x-20,y-6); ctx.stroke()
        elif ph<.8:
            u=(ph-.55)/.25; x=lerp(cx,xs,u); y=lerp(cy+14,YC-RS,u)
        else:
            u=(ph-.8)/.2; sg=-1 if k%2 else 1
            x=lerp(xs,se+2,u); y=lerp(YC+sg*RS,YC+sg*(HR+GAP+SH/2),u)
        col(ctx,GOLD); ctx.rectangle(x-4,y-4,8,8); ctx.fill()
    for sg in (-1,1):   # packing spark at the shield front
        if math.sin(t*9+sg)>.3:
            ctx.arc(se+2,YC+sg*(HR+GAP+SH/2),4,0,2*math.pi); col(ctx,SPARK,.8); ctx.fill()
    n=int(seg(t,0,dur)*3400+1200)
    readout(ctx,'SHIELD','~3 m · 4.5 t/m²',60,110,SHIELDL,w=230)
    readout(ctx,'PER RING','~260 Mt',300,110,GOLD,w=150)
    readout(ctx,'PACKETS CAUGHT',f'{n:,}',460,110,FG,w=200)
    label(ctx,'packets from the Moon · 2.4 km/s',80,200,lerp(-40,cx,.4),lerp(20,cy-26,.4)-10,SPARK,a=seg(t,.6,1.4)*(1-seg(t,7,7.8)))
    label(ctx,'CATCHER',cx+90,190,cx+40,cy-14,GOLD,a=seg(t,1.4,2.2))
    label(ctx,'SHIELD FACTORY packs regolith around the new hull',260,560,xs,YC+RS,GOLD,a=seg(t,2.4,3.2))
    label(ctx,'HULL FACTORY keeps laying panels ahead',860,215,xh,YC-HR-18,CY,a=seg(t,3.6,4.4))
    label(ctx,'gap: the shield stays still while the tube spins',160,540,120,YC+HR+GAP/2,FG,a=seg(t,8,8.8))
    caption(ctx,'8 · A SECOND FACTORY ADDS THE SHIELD','Right behind the hull factory, a shield factory catches the regolith packets and packs them around the new panels: a ~3 m static shell, ~260 Mt per ring, that blocks radiation and does not spin with the ring.')
    fade(ctx,t,dur)

SCENES=[('sm1',moon,14),('sm2',shield,18)]
if __name__=='__main__': main(SCENES,'moon-and-shield')
