"""Lunar base site plan (top-down, schematic) and mass driver side view."""
import json, math
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, FancyArrowPatch, Ellipse
D=json.load(open('ops.json')); Lu=D['lunar']
BG='#0a0b10'; PAN='#11131b'; FG='#ece6d8'; MUT='#b8ab8e'; GOLD='#f0b860'; CY='#66c2d4'; LINE='#2c2a24'
plt.rcParams.update({'font.family':'DejaVu Sans Mono','font.size':10.5,'text.color':FG,'figure.facecolor':BG,'axes.facecolor':'#2a2926','savefig.facecolor':BG})
OUT='../figures/'
# ---------- site plan
fig,ax=plt.subplots(figsize=(12,7.4)); ax.set_xlim(0,30); ax.set_ylim(0,18.5); ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_color(LINE)
import random; random.seed(3)
for _ in range(70):
    x,y,r=random.uniform(0,30),random.uniform(0,18.5),random.uniform(.1,.6); ax.add_patch(Circle((x,y),r,fc='#232220',ec='#3a3834',lw=.6))
def lab(x,y,t,c=FG,fs=10,ha='left'): ax.text(x,y,t,color=c,fontsize=fs,ha=ha,va='center',bbox=dict(fc=BG,ec='none',alpha=.75,pad=1.5))
def plant(x,y,w,h,c,t,sub,tx=None,ty=None):
    ax.add_patch(Rectangle((x,y),w,h,fc=PAN,ec=c,lw=1.8)); lab(tx if tx is not None else x, ty if ty is not None else y+h+.55,t,c,10.5); lab(tx if tx is not None else x,(ty if ty is not None else y+h+.55)-.55,sub,MUT,9)
# ice crater (permanently shadowed) bottom-left
ax.add_patch(Circle((3.6,3.4),2.7,fc='#151820',ec='#4b5a6a',lw=1.5)); lab(6.6,3.2,'SHADOWED CRATER: ICE MINE',CY,10.5); lab(6.6,2.65,'0.5 Mt water a year, 40 K floor',MUT,9)
for i in range(5): ax.add_patch(Rectangle((2.6+i*.45,3.0),.3,.3,fc=CY,ec='none'))
# mining field (mare) top-left
ax.add_patch(Rectangle((0.8,11.5),8.5,5.2,fc='none',ec='#c7b89a',lw=1.4,ls=(0,(5,4)))); lab(0.9,17.3,'MARE MINING FIELD',  '#c7b89a',10.5); lab(0.9,16.75,f"{Lu['excavators']} excavators + haulers, 40 Mt a year",MUT,9)
for i in range(12):
    x=1.5+(i%6)*1.3; y=12.4+(i//6)*2.2; ax.add_patch(Rectangle((x,y),.55,.3,fc='#c7b89a')); ax.add_patch(Circle((x+.75,y+.15),.12,fc=GOLD))
# highland field
ax.add_patch(Rectangle((10.5,14.2),6.5,3.2,fc='none',ec='#d9cfb6',lw=1.4,ls=(0,(5,4)))); lab(10.6,17.95,'HIGHLAND FIELD (ANORTHITE)','#d9cfb6',10.5)
# conveyors
for (x0,y0,x1,y1) in ((9.3,13.5,11.2,10.3),(13.6,14.2,13.0,10.9),(4.8,5.8,11.0,9.0)):
    ax.plot([x0,x1],[y0,y1],color=GOLD,lw=2.2,alpha=.85)
plant(11,8.3,3.4,2.4,GOLD,'SORT PLANT','sieves, magnets, 40 Mt/yr',tx=10.2,ty=7.6)
plant(15.4,8.6,2.6,2.0,'#e07a5f','BASALT FIBRE',f"{Lu['bushings']:,.0f} bushings",tx=14.9,ty=12.0)
plant(19,8.6,2.8,2.0,'#9fb7e8','Al SMELTER',f"{Lu['P_al_MW']:.0f} MW",tx=19.3,ty=7.6)
plant(16.3,4.6,2.4,1.6,'#d8a0b8','GLASS + PACK','packets of 20 kg',tx=15.2,ty=3.8)
for x,y in ((14.4,9.5),(18.0,9.6),(21.8,9.6)): ax.plot([x,x+1.0],[y,y],color=GOLD,lw=2)
ax.plot([17.5,17.5],[8.6,6.2],color=GOLD,lw=2); ax.plot([20.4,18.7],[8.6,6.0],color=GOLD,lw=2); ax.plot([12.7,16.3],[8.3,5.4],color=GOLD,lw=2)
# solar fields
for i in range(4):
    for j in range(3): ax.add_patch(Rectangle((23.2+i*1.6,13.0+j*1.6),1.3,1.2,fc='#20335c',ec='#6d8fd6',lw=.8))
lab(23.1,18.1,'SOLAR FIELD',('#9fb7e8'),10.5); lab(23.1,17.55,f"~{Lu['array_km2']:.0f} km², {Lu['P_tot_GW']:.1f} GW",MUT,9)
# mass driver
ax.plot([18.7,29.4],[5.4,1.2],color='#c9c5ba',lw=3)
for k in range(24):
    u=k/23; x=18.7+(29.4-18.7)*u; y=5.4+(1.2-5.4)*u; ax.add_patch(Ellipse((x,y),.18,.55,angle=-21,fc='none',ec=CY,lw=1.2))
lab(22.8,2.0,'MASS DRIVER',CY,10.5); lab(22.8,1.45,f"{Lu['L_km']:.1f} km, {Lu['a_g']:.0f} g, 2.4 km/s",MUT,9)
# landing pads + habitat
for x in (6.6,8.2):
    ax.add_patch(Circle((x,9.0),.62,fc='#3a3834',ec=FG,lw=1.2)); ax.plot([x-.25,x+.25],[9,9],color=FG,lw=1); ax.plot([x,x],[8.75,9.25],color=FG,lw=1)
lab(5.6,10.2,'LANDING PADS',FG,10.5)
ax.add_patch(Rectangle((8.0,5.6),1.8,1.2,fc=PAN,ec=GOLD,lw=1.6)); lab(7.9,5.05,'CREW BASE ~200',GOLD,10)
# scale bar + north
ax.plot([1,4],[0.7,0.7],color=FG,lw=2); lab(1,1.2,'≈ 3 km (schematic)',MUT,9)
ax.set_title('Lunar base: one mass-driver line, sized for 30 Mt a year (one ring every ~10 years)',loc='left',color=GOLD,fontsize=12.5)
fig.savefig(OUT+'lunar_site.png',dpi=200,bbox_inches='tight'); plt.close(fig); print('lunar_site')

# ---------- mass driver side view
fig,ax=plt.subplots(figsize=(12,3.8)); ax.set_xlim(-0.2,10.5); ax.set_ylim(-1,3); ax.axis('off'); fig.patch.set_facecolor(BG)
ax.add_patch(Rectangle((-0.2,-1),10.7,0.9,fc='#3a3834',ec='none'))
ax.plot([0.5,9.0],[0.0,0.95],color='#c9c5ba',lw=4)
for k in range(40):
    u=k/39; x=0.5+8.5*u; y=0.95*u; ax.add_patch(Ellipse((x,y),0.09,0.42,angle=-6,fc='none',ec=CY,lw=1.3))
    if k%6==0: ax.plot([x,x],[y-0.2,-0.1],color='#5a5650',lw=1.2)
for u,c in ((.08,GOLD),(.35,GOLD),(.75,GOLD)):
    ax.add_patch(Circle((0.5+8.5*u,0.95*u),0.07,fc=c))
ax.add_patch(FancyArrowPatch((9.1,1.0),(10.3,2.6),arrowstyle='-|>',mutation_scale=14,color=GOLD,lw=1.6,connectionstyle='arc3,rad=-0.2'))
ax.add_patch(Rectangle((0.0,-0.1),0.55,0.5,fc=PAN,ec='#d8a0b8',lw=1.5)); ax.text(0.27,0.55,'packer',ha='center',color='#d8a0b8',fontsize=9.5)
specs=[f"length {Lu['L_km']:.2f} km at {Lu['a_g']:.0f} g",f"exit speed 2.4 km/s (lunar escape 2.38 km/s)",f"{Lu['packets_per_s']:.0f} packets/s of 20 kg = {Lu['mdot_kg_s']:.0f} kg/s",
       f"beam power {Lu['Pk_GW']:.1f} GW kinetic, {Lu['Pmd_GW']:.1f} GW electric at 80%",'coils: aluminium windings, lunar-made; switching electronics from Earth']
for i,t in enumerate(specs): ax.text(0.5,2.75-i*0.38,t,color=FG if i else GOLD,fontsize=10.5)
ax.text(10.3,2.85,'to the catcher\nnear Soma',color=GOLD,ha='right',fontsize=10)
fig.savefig(OUT+'mass_driver.png',dpi=200,bbox_inches='tight'); plt.close(fig); print('mass_driver')
