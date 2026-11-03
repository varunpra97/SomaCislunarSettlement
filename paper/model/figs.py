import json, math
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, FancyArrowPatch, Wedge
D=json.load(open('ops.json'))
BG='#0a0b10'; PAN='#11131b'; FG='#ece6d8'; MUT='#b8ab8e'; GOLD='#f0b860'; CY='#66c2d4'; LINE='#2c2a24'; NAVY='#3a5f80'
plt.rcParams.update({'font.family':'DejaVu Sans Mono','font.size':11,'text.color':FG,'axes.labelcolor':FG,'xtick.color':MUT,'ytick.color':FG,
  'axes.edgecolor':LINE,'figure.facecolor':BG,'axes.facecolor':BG,'savefig.facecolor':BG})
OUT='../figures/'
def save(fig,name): fig.savefig(OUT+name,dpi=220,bbox_inches='tight'); plt.close(fig); print(name)

# ---------- cost per cell type: point + range, sorted
rows=sorted(D['rows'],key=lambda r:r['opt'])
fig,ax=plt.subplots(figsize=(10,5.2))
y=range(len(rows))
for i,r in enumerate(rows):
    ax.plot([r['opt'],r['cons']],[i,i],color=NAVY,lw=7,solid_capstyle='round')
    ax.plot(r['opt'],i,'o',color=GOLD,ms=8); ax.plot(r['cons'],i,'o',color=CY,ms=8)
    ax.text(r['cons']+18,i,f"${r['opt']:.0f}–{r['cons']:.0f}M   ×{r['count']}",va='center',color=FG,fontsize=10)
ax.set_yticks(list(y)); ax.set_yticklabels([r['type'] for r in rows])
ax.set_xlim(0,1020); ax.set_xlabel('Build cost per cell, $ million')
ax.grid(axis='x',color='#1d2029'); ax.set_axisbelow(True)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.plot([],[],'o',color=GOLD,label='optimistic'); ax.plot([],[],'o',color=CY,label='conservative')
ax.legend(loc='lower right',frameon=False,labelcolor=FG)
ax.set_title('Build cost of one cell, by type (180 m of tube, 45 levels)',loc='left',color=GOLD,fontsize=13)
save(fig,'cost_per_cell.png')

# ---------- interior mass per cell (lunar materials) + Earth kit
rows=D['rows']
fig,(a1,a2)=plt.subplots(1,2,figsize=(11,5.2),gridspec_kw=dict(width_ratios=[1.6,1]))
names=[r['type'] for r in rows]; yy=range(len(rows))
left=[0]*len(rows)
for key,lab,col in (('struct_kt','decks and frames',  '#c7b89a'),('soil_kt','soil','#6f8b52'),('water_kt','water',CY)):
    vals=[r[key] for r in rows]; a1.barh(list(yy),vals,left=left,color=col,label=lab,height=.62)
    left=[l+v for l,v in zip(left,vals)]
a1.set_yticks(list(yy)); a1.set_yticklabels(names); a1.invert_yaxis()
a1.set_xlabel('Lunar-sourced interior mass per cell, kt'); a1.legend(frameon=False,labelcolor=FG,loc='lower right')
a1.set_title('Interior, per cell (all lunar)',loc='left',color=GOLD)
a2.barh(list(yy),[r['kit_t'] for r in rows],color=GOLD,height=.62); a2.set_yticks(list(yy)); a2.set_yticklabels([]); a2.invert_yaxis()
a2.set_xlabel('Earth kit per cell, t'); a2.set_title('Earth-made kit, per cell',loc='left',color=GOLD)
for a in (a1,a2):
    a.grid(axis='x',color='#1d2029'); a.set_axisbelow(True)
    for s in ('top','right'): a.spines[s].set_visible(False)
fig.text(0.01,-0.03,'Every cell also carries an equal share of the shell: ~465 kt of regolith shield, basalt-fibre hoop bands, aluminium hull and glass.',color=MUT,fontsize=10)
save(fig,'mass_per_cell.png')

# ---------- Starship launches by stage (log), ranges as whiskers
L=D['launch']
items=[('Lunar seed factory\n(20,000 t landed)',L['seed']),('Lunar full build-out\n(250,000 t, shared by 100 rings)',L['buildout']),
       ('Spine, per 6-ring stack\n(280 Starships stay as the core)',[L['spine_per_stack']]*2),
       ('Bay factories, per ring\n(6 × 7 flights)',[L['factories']]*2),('Robot fleet, per ring\n(~5,000 t)',[L['robots']]*2),
       ('Earth high-tech kit, per ring\n(~50,000 t)',[L['kit']]*2),('Batteries, per ring\n(~37,500 t)',[L['batteries']]*2),
       ('Nitrogen, per ring\n(0.3–0.6 Mt from Earth)',L['n2'])]
fig,ax=plt.subplots(figsize=(10.5,6))
for i,(lab,(lo,hi)) in enumerate(items):
    mid=(lo*hi)**.5
    if hi>lo: ax.plot([lo,hi],[i,i],color=NAVY,lw=8,solid_capstyle='round')
    ax.plot(mid,i,'o',color=GOLD,ms=8)
    ax.text(hi*1.25,i,f"{lo:,.0f}" + (f"–{hi:,.0f}" if hi>lo else ''),va='center',fontsize=10,color=FG)
ax.set_xscale('log'); ax.set_xlim(150,2.5e5)
ax.set_yticks(range(len(items))); ax.set_yticklabels([i[0] for i in items],fontsize=9.5); ax.invert_yaxis()
ax.set_xlabel('Starship launches, including tanker flights (log scale)')
ax.grid(axis='x',color='#1d2029',which='both'); ax.set_axisbelow(True)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.set_title('Starship launches by stage',loc='left',color=GOLD,fontsize=13)
save(fig,'launches.png')

# ---------- material flow: sources -> plants -> products -> ring
fig,ax=plt.subplots(figsize=(12,6.6)); ax.set_xlim(0,12); ax.set_ylim(0,6.6); ax.axis('off')
def box(x,y,w,h,t,c,fs=10.5):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.02,rounding_size=0.08',fc=PAN,ec=c,lw=1.6))
    ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=fs,color=FG,linespacing=1.3)
def arrow(x0,y0,x1,y1,c=MUT,lw=1.4):
    ax.add_patch(FancyArrowPatch((x0,y0),(x1,y1),arrowstyle='-|>',mutation_scale=12,color=c,lw=lw,shrinkA=2,shrinkB=2))
cols=[0.2,3.1,6.1,9.2]; W=2.5
for x,t in zip(cols,('SOURCE','PROCESS ON THE MOON','PRODUCT','INTO THE RING')): ax.text(x,6.35,t,color=GOLD,fontsize=10.5,fontweight='bold')
src=[('Mare regolith\n(basalt plains)',4.9),('Highland regolith\n(anorthite)',3.5),('Polar ice\n(shadowed craters)',2.1),('Earth and asteroids',0.7)]
prc=[('Dig, sieve, magnets\n40 Mt/yr feed',5.4),('Basalt melt 1,500 °C\nand fibre drawing',4.3),('Molten-salt electrolysis\nAl + O₂',3.2),('Ice mining, purify',2.1)]
prd=[('Shield fines ~26 Mt/yr',5.5),('Basalt fibre 1.8 Mt/yr',4.55),('Aluminium 0.4 Mt/yr\nglass 0.1 Mt/yr',3.6),('Oxygen (by-product)',2.65),('Water 0.5 Mt/yr',1.75),('N₂, carbon, Earth kit',0.7)]
dst=[('Regolith shield\n260 Mt/ring',5.3),('Hoop bands + spokes\n18 Mt/ring',4.15),('Hull panels + windows\n5 Mt/ring',3.0),('Air, water, soil\n~21 Mt/ring',1.85),('Life support, labs,\nelectronics',0.7)]
H=0.78
for t,y in src: box(cols[0],y-H/2,W,H,t,'#c7b89a')
for t,y in prc: box(cols[1],y-H/2,W+0.2,H,t,CY,10)
for t,y in prd: box(cols[2],y-0.34,W+0.3,0.68,t,GOLD,10)
for t,y in dst: box(cols[3],y-H/2,W,H,t,'#e6b85c')
S=dict(src); P=dict(prc); R=dict(prd); T=dict(dst)
e=lambda a,b,ya,yb,c=MUT: arrow(cols[a]+(W if a==0 else W+0.2 if a==1 else W+0.3),ya,cols[b],yb,c)
e(0,1,S['Mare regolith\n(basalt plains)'],P['Dig, sieve, magnets\n40 Mt/yr feed'])
e(0,1,S['Highland regolith\n(anorthite)'],P['Dig, sieve, magnets\n40 Mt/yr feed'])
e(0,1,S['Mare regolith\n(basalt plains)'],P['Basalt melt 1,500 °C\nand fibre drawing'])
e(0,1,S['Highland regolith\n(anorthite)'],P['Molten-salt electrolysis\nAl + O₂'])
e(0,1,S['Polar ice\n(shadowed craters)'],P['Ice mining, purify'])
e(1,2,P['Dig, sieve, magnets\n40 Mt/yr feed'],R['Shield fines ~26 Mt/yr'])
e(1,2,P['Basalt melt 1,500 °C\nand fibre drawing'],R['Basalt fibre 1.8 Mt/yr'])
e(1,2,P['Molten-salt electrolysis\nAl + O₂'],R['Aluminium 0.4 Mt/yr\nglass 0.1 Mt/yr'])
e(1,2,P['Molten-salt electrolysis\nAl + O₂'],R['Oxygen (by-product)'])
e(1,2,P['Ice mining, purify'],R['Water 0.5 Mt/yr'])
arrow(cols[0]+W,S['Earth and asteroids'],cols[2],R['N₂, carbon, Earth kit'],GOLD)
pairs=[('Shield fines ~26 Mt/yr','Regolith shield\n260 Mt/ring'),('Basalt fibre 1.8 Mt/yr','Hoop bands + spokes\n18 Mt/ring'),('Aluminium 0.4 Mt/yr\nglass 0.1 Mt/yr','Hull panels + windows\n5 Mt/ring'),
       ('Oxygen (by-product)','Air, water, soil\n~21 Mt/ring'),('Water 0.5 Mt/yr','Air, water, soil\n~21 Mt/ring'),('N₂, carbon, Earth kit','Life support, labs,\nelectronics'),('N₂, carbon, Earth kit','Air, water, soil\n~21 Mt/ring')]
for a,b in pairs: arrow(cols[2]+W+0.3,R[a],cols[3],T[b],GOLD if 'Earth' in a else CY)
ax.text(cols[3]-0.25,6.05,'via mass driver, 30 Mt/yr',color=CY,fontsize=9.5)
ax.text(0.2,0.02,'Lunar products are packed and thrown by the mass driver to a catcher near Soma; Earth goods fly up by Starship.',color=MUT,fontsize=9.5)
save(fig,'material_flow.png')
