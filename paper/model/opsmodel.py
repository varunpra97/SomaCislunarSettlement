"""Soma operations model: materials and cost per cell type, lunar base sizing, Starship launch counts.
Anchored to the report's per-ring totals ($89B optimistic / $356B conservative standalone)."""
import json, math
CELLS={  # type: (count, earth kit weight t/cell, soil kt, water kt, interior structure kt)
 'Home':        (150,  60, 15,  5, 35),
 'Farm':        (120,  90, 45, 15, 20),
 'Lab':         ( 60, 220,  5,  4, 30),
 'Wild':        ( 60,  20, 60, 15, 10),
 'Play':        ( 60,  40, 30,  6, 15),
 'Civic':       ( 30, 200, 10,  5, 28),
 'Plant':       ( 30, 260,  2, 12, 25),
 'Make':        ( 30, 150,  2,  4, 30),
 'Water':       ( 30,  40, 20, 60,  8),
 'Food & night':( 30,  70, 10,  5, 25),
 'Hub':         (  6, 300,  3,  3, 40),
}
N=sum(v[0] for v in CELLS.values()); assert N==606, N
SHELL={'Regolith shield':260e3,'Basalt-fibre hoop bands':18e3,'Aluminium hull':4e3,'Glass (windows)':1e3}  # kt per ring
SOIL_T,WATER_T,KIT_T=15e3,5e3,50_000   # kt, kt, tonnes per ring
sum_w=sum(c*w for c,w,*_ in CELLS.values())
sum_soil=sum(c*s for c,_,s,_,_ in CELLS.values()); sum_wat=sum(c*x for c,_,_,x,_ in CELLS.values())
ks,kw,kk=SOIL_T/sum_soil, WATER_T/sum_wat, KIT_T/sum_w
CASE={'opt':dict(lunar=5,kit=30,n2=30,power=9,robots=5,design=10),'cons':dict(lunar=19,kit=60,n2=200,power=42,robots=15,design=20)}
rows=[]
shell_cell=sum(SHELL.values())/N
for name,(c,w,s,x,st) in CELLS.items():
    kit_t=w*kk; r=dict(type=name,count=c,shell_kt=shell_cell,struct_kt=st,soil_kt=s*ks,water_kt=x*kw,kit_t=kit_t)
    for cs,v in CASE.items():
        shared=(v['lunar']+v['n2']+v['power']+v['robots']+v['design'])*1e3/N   # $M per cell, equal share
        kit=v['kit']*1e3*kit_t/KIT_T                                              # $M per cell by its kit mass
        r[cs]=shared+kit; r[cs+'_kit']=kit; r[cs+'_shared']=shared
    rows.append(r)
tot={cs:sum(r[cs]*r['count'] for r in rows)/1e3 for cs in CASE}
print('ring totals $B',tot)
# ---- lunar base sizing (one mass driver line)
yr=365.25*86400; THRU=30e9  # kg/yr delivered
mdot=THRU/yr; v=2400; a=1000; L=v*v/(2*a); Pk=.5*mdot*v*v; eta=.8
pkt=20; rate=mdot/pkt
feed=THRU/0.75   # excavated, 75 % yield after sorting
exc_rate=100e3*7000  # kg per excavator-year (100 t/h, 7000 h)
n_exc=math.ceil(feed/exc_rate)
fibre=18e9/10; al=4e9/10; glass=1e9/10; water=5e9/10      # kg/yr for one ring per 10 years
P_fibre=fibre*1.0e9/1e3/yr     # 1 GJ/t melt+draw
P_al=al*15*3.6e9/1e3/yr        # 15 MWh/t molten-salt electrolysis
P_sort=feed*20*3.6e6/1e3/yr    # 20 kWh/t dig, haul, sieve, magnets
P_glass=glass*2e9/1e3/yr; P_ice=water*1.0*3.6e9/1e3/yr  # 1 MWh/t ice mine + purify
P_md=Pk/eta; P_misc=150e6
P_tot=P_md+P_fibre+P_al+P_sort+P_glass+P_ice+P_misc
array_wm2=1361*0.20*0.75; A=P_tot/array_wm2
bushings=fibre/1000/(0.1*7500)  # 100 kg/h per bushing, 7500 h
lunar=dict(throughput_Mt=THRU/1e9, mdot_kg_s=mdot, v=v, a_g=a/9.81, L_km=L/1e3, Pk_GW=Pk/1e9, Pmd_GW=P_md/1e9, packets_per_s=rate, packet_kg=pkt,
  feed_Mt=feed/1e9, excavators=n_exc, fibre_Mt=fibre/1e9, al_Mt=al/1e9, glass_Mt=glass/1e9, water_Mt=water/1e9,
  P_fibre_MW=P_fibre/1e6, P_al_MW=P_al/1e6, P_sort_MW=P_sort/1e6, P_glass_MW=P_glass/1e6, P_ice_MW=P_ice/1e6, P_tot_GW=P_tot/1e9, array_km2=A/1e6, bushings=bushings,
  years_per_ring=303e9/THRU)
print(json.dumps(lunar,indent=1))
# ---- Starship launches
TL=(10,15); TR=6
def lunar_launches(t): d=t/100; return (d*(1+TL[0]), d*(1+TL[1]))
def orbit_launches(t): d=t/100; return d*(1+TR)
L=dict(
 seed=lunar_launches(20_000), buildout=lunar_launches(250_000),
 kit=orbit_launches(50_000), batteries=orbit_launches(37_500),
 n2=(orbit_launches(300_000),orbit_launches(600_000)),
 spine_per_stack=280*(1+TR), factories=6*7*(1+TR), robots=orbit_launches(5_000))
print(json.dumps(L,indent=1))
json.dump(dict(rows=rows,tot=tot,lunar=lunar,launch=L,N=N),open('ops.json','w'),indent=1)
