import json
D=json.load(open('ops.json')); Lu=D['lunar']; La=D['launch']
f=lambda x:f"{x:,.0f}"
out=[]
# per-cell cost and materials table
rows=sorted(D['rows'],key=lambda r:-r['count'])
t=[r"\begin{tabularx}{\textwidth}{@{}lrrrrrrX@{}}",r"\toprule",
   r"\textbf{Cell type} & \textbf{Cells} & \textbf{Decks} & \textbf{Soil} & \textbf{Water} & \textbf{Earth kit} & \textbf{Cost per cell} & \textbf{All cells of this type}\\",
   r" & & kt & kt & kt & t & \$M & \$B\\",r"\midrule"]
for r in rows:
    t.append(f"{r['type'].replace('&',r'\&')} & {r['count']} & {r['struct_kt']:.0f} & {r['soil_kt']:.0f} & {r['water_kt']:.0f} & {r['kit_t']:.0f} & {r['opt']:.0f}--{r['cons']:.0f} & {r['opt']*r['count']/1e3:.1f}--{r['cons']*r['count']/1e3:.1f}\\\\")
t+= [r"\midrule",f"\\textbf{{Ring}} & {D['N']} & {sum(r['struct_kt']*r['count'] for r in rows)/1e3:.1f} Mt & {sum(r['soil_kt']*r['count'] for r in rows)/1e3:.1f} Mt & {sum(r['water_kt']*r['count'] for r in rows)/1e3:.1f} Mt & {sum(r['kit_t']*r['count'] for r in rows):,.0f} & & \\textbf{{{D['tot']['opt']:.0f}--{D['tot']['cons']:.0f}}}\\\\",r"\bottomrule",r"\end{tabularx}"]
open('../t_cells.tex','w').write('\n'.join(t))
# lunar plant specs
s=[r"\begin{tabularx}{\textwidth}{@{}lXr@{}}",r"\toprule",r"\textbf{Unit} & \textbf{Spec} & \textbf{Power}\\",r"\midrule",
 f"Mining fleet & {Lu['excavators']} bucket-wheel excavators (100 t/h each, 7,000 h/yr) plus haulers; {Lu['feed_Mt']:.0f} Mt/yr of regolith dug from mare and highland fields & \\multirow{{2}}{{*}}{{{Lu['P_sort_MW']:.0f} MW}}\\\\",
 r"Sort plant & Sieves, magnetic and electrostatic separation; about 75\% of the feed is shipped, the rest is tailings & \\",
 f"Basalt fibre works & Electric furnaces at 1,500\\,\\textdegree C feeding {Lu['bushings']:,.0f} platinum--rhodium bushings (100 kg/h each); {Lu['fibre_Mt']:.1f} Mt/yr of continuous fibre & {Lu['P_fibre_MW']:.0f} MW\\\\",
 f"Aluminium smelter & Molten-salt electrolysis of anorthite at $\\sim$15 MWh/t; {Lu['al_Mt']:.1f} Mt/yr of aluminium and oxygen as a by-product & {Lu['P_al_MW']:.0f} MW\\\\",
 f"Glass line & Regolith melt to window glass; {Lu['glass_Mt']:.1f} Mt/yr & {Lu['P_glass_MW']:.0f} MW\\\\",
 f"Ice mine & Rovers and heated tents in a permanently shadowed crater (40 K floor); {Lu['water_Mt']:.1f} Mt/yr of water & {Lu['P_ice_MW']:.0f} MW\\\\",
 f"Packer and mass driver & 20 kg packets, {Lu['packets_per_s']:.0f} a second; {Lu['L_km']:.2f} km coilgun at {Lu['a_g']:.0f}\\,g to 2.4 km/s; {Lu['throughput_Mt']:.0f} Mt/yr & {Lu['Pmd_GW']*1e3:,.0f} MW\\\\",
 r"Crew base, pads, workshops & $\sim$200 crew, 2 landing pads of sintered regolith, robot repair shops & 150 MW\\",
 r"\midrule",
 f"\\textbf{{Solar field}} & $\\sim${Lu['array_km2']:.0f} km\\textsuperscript{{2}} of arrays at $\\sim$200 W/m\\textsuperscript{{2}} on a polar ridge with near-constant sun & \\textbf{{{Lu['P_tot_GW']:.1f} GW}}\\\\",
 r"\bottomrule",r"\end{tabularx}"]
open('../t_lunar.tex','w').write('\n'.join(s))
# launches
per_ring=La['factories']+La['robots']+La['kit']+La['batteries']+La['spine_per_stack']/6
L=[r"\begin{tabularx}{\textwidth}{@{}Xrr@{}}",r"\toprule",r"\textbf{Stage} & \textbf{Payload} & \textbf{Launches}\\",r"\midrule",
 r"\multicolumn{3}{@{}l}{\emph{Once, shared by all rings (to the lunar surface: 100 t a landing, 10--15 tankers each)}}\\",
 f"Lunar seed factory & 20,000 t & {f(La['seed'][0])}--{f(La['seed'][1])}\\\\",
 f"Lunar full build-out (Earth-made parts) & 250,000 t & {f(La['buildout'][0])}--{f(La['buildout'][1])}\\\\",
 r"\midrule",r"\multicolumn{3}{@{}l}{\emph{Each ring (to Soma's orbit: 100 t a delivery, $\sim$6 tankers each)}}\\",
 f"Spine share (280 Starships per 6-ring stack) & 47 ships & {f(La['spine_per_stack']/6)}\\\\",
 f"Bay factories (6 $\\times$ 7 flights) & 42 loads & {f(La['factories'])}\\\\",
 f"Robot fleet & 5,000 t & {f(La['robots'])}\\\\",
 f"Earth high-tech kit & 50,000 t & {f(La['kit'])}\\\\",
 f"Batteries & 37,500 t & {f(La['batteries'])}\\\\",
 f"\\textbf{{Subtotal, without nitrogen}} & & \\textbf{{{f(per_ring)}}}\\\\",
 f"Nitrogen from Earth & 0.3--0.6 Mt & {f(La['n2'][0])}--{f(La['n2'][1])}\\\\",
 f"\\textbf{{Per ring, all in}} & & \\textbf{{{f(per_ring+La['n2'][0])}--{f(per_ring+La['n2'][1])}}}\\\\",
 r"\bottomrule",r"\end{tabularx}"]
open('../t_launch.tex','w').write('\n'.join(L))
json.dump(dict(per_ring=per_ring),open('derived.json','w'))
print('per ring without N2',per_ring,'with',per_ring+La['n2'][0],per_ring+La['n2'][1])
