import math, json
g=9.81; R=17350; w=math.sqrt(g/R); M_rot=176e9
I=M_rot*R**2; L=I*w; KE=.5*I*w**2
Om=2*math.pi/(365.25*86400)
tau_prec=L*Om
print(f"omega {w:.5f} rad/s rpm {w*60/2/math.pi:.3f} L {L:.2e} KE {KE/3.6e15:.2f} TWh  precession torque {tau_prec:.2e} N m")
# middle ring
rm=R/2; gm=w**2*rm; vm=w*rm
print(f"middle ring r {rm:.0f} m g {gm/g:.2f} g, rim {vm:.0f} m/s, Al self stress {2700*vm**2/1e6:.0f} MPa, circumference {2*math.pi*rm/1e3:.1f} km")
D=40; circ=2*math.pi*rm; hull=math.pi*D*circ*0.015*2700
print(f"middle ring hull {hull/1e9:.2f} Mt; with decks/equipment ~{(hull+200e6)/1e9:.2f} Mt")
# Mars/Moon gravity radii
for name,gg in [('Mars',3.71),('Moon',1.62)]: print(name, f"{gg/w**2:.0f} m")
# spine
spacing=2000; Nst=6; Ls=Nst*spacing+2000
Rs=100; sig=200e6
t_eq=tau_prec/(math.pi*Rs**2*sig)
m_per_m=2*math.pi*Rs*t_eq*2700
print(f"spine length {Ls/1e3:.0f} km, equivalent wall {t_eq*100:.1f} cm, {m_per_m/1e3:.0f} t/m, mass {m_per_m*Ls/1e9:.2f} Mt")
# spin-up torque through spine
P=2.5e9; Tsp=P/w
print(f"spin-up at {P/1e9} GW: torque {Tsp:.1e} N m, time {KE/P/86400:.0f} days; torsion wall {Tsp/(2*math.pi*Rs**2*sig)*1000:.1f} mm")
# hub bearings
for Lh in (200,500):
    print(f"hub bearing radial couple force at {Lh} m spacing: {tau_prec/Lh:.1e} N")
# gravity gradient, orbit
P_orb=10.3*86400; n=2*math.pi/P_orb
Mring=300e9; dI=Mring*R**2/2
tg=1.5*n**2*dI
print(f"n {n:.2e}; gravity-gradient peak torque per ring {tg:.1e} N m")
h=tg/n  # per quarter cycle approx
d=h/(2*L)
print(f"momentum to absorb per half-cycle {h:.1e} N m s -> scissor tilt {math.degrees(d):.3f} deg")
# construction misalignment holding (Starships)
for mis in (1,0.1):
    t=tg*math.sin(math.radians(2*mis))
    J=t/n/14000
    print(f"misalign {mis} deg: torque {t:.1e}, impulse/quarter-orbit {J:.1e} N s, prop {J/3730/1e3:.0f} t per quarter orbit, {J/3730/1e3/(P_orb/4/86400):.0f} t/day")
# starship tug capability
imp=4*1200e3*3730
print(f"4 tugs impulse {imp:.1e} N s -> dv on 1 Mt spine {imp/1e9:.0f} m/s, on 300 Mt ring {imp/300e9*100:.1f} cm/s")
# slew 90 deg of stack using scissor CMG
It=6*dI+1e19; ws=(math.pi/2)/(30*86400)
print(f"slew 90deg in 30 days: needs h {It*ws:.1e}, tilt {math.degrees(It*ws/(2*L)):.4f} deg")
# shading
wing=17e6; disc=math.pi*R**2
print(f"wing coverage of disc {wing/disc*100:.1f}%")
