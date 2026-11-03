import math, random
W,H=3520,470; CY=228; SX,SR=-560,700
bodies=[('MERCURY',420,11,'gMe'),('VENUS',650,20,'gVe'),('EARTH',950,27,'gEa'),('MARS',1300,17,'gMa'),
 ('JUPITER',1980,112,'gJu'),('SATURN',2560,84,'gSa'),('URANUS',3000,32,'gUr'),('NEPTUNE',3250,30,'gNe'),('PLUTO',3455,7,'gPl')]
o=[]; A=o.append
A(f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Settlements named after the bodies they orbit, from Ravi around the Sun to Yama around Pluto" style="display:block">')
A('''<defs>
<radialGradient id="gSun" cx="0.92" cy="0.5" r="0.6"><stop offset="0" stop-color="#ffb35c"/><stop offset="0.85" stop-color="#e8762e"/><stop offset="1" stop-color="#c4561f"/></radialGradient>
<radialGradient id="gMe" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#e6c79a"/><stop offset="1" stop-color="#9a7a4e"/></radialGradient>
<radialGradient id="gVe" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#ffe29a"/><stop offset="1" stop-color="#d79a2e"/></radialGradient>
<radialGradient id="gEa" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#7cc4ef"/><stop offset=".6" stop-color="#2f7fbf"/><stop offset="1" stop-color="#174a7a"/></radialGradient>
<radialGradient id="gMo" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#f2f0ea"/><stop offset="1" stop-color="#9c998f"/></radialGradient>
<radialGradient id="gMa" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#f08a5a"/><stop offset="1" stop-color="#a8381c"/></radialGradient>
<radialGradient id="gJu" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#f3d9b5"/><stop offset="1" stop-color="#c99a6a"/></radialGradient>
<radialGradient id="gSa" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#fbe7cc"/><stop offset="1" stop-color="#d9b48a"/></radialGradient>
<radialGradient id="gUr" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#c9f0f2"/><stop offset="1" stop-color="#6fbfcb"/></radialGradient>
<radialGradient id="gNe" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#7d9be8"/><stop offset="1" stop-color="#2d4aa3"/></radialGradient>
<radialGradient id="gPl" cx=".35" cy=".35" r=".8"><stop offset="0" stop-color="#e9dccb"/><stop offset="1" stop-color="#9e8a74"/></radialGradient>
<radialGradient id="gSh" cx=".3" cy=".3" r=".9"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient>
<clipPath id="cJu"><circle cx="1980" cy="228" r="112"/></clipPath>
<clipPath id="cSaF"><rect x="2300" y="228" width="520" height="200"/></clipPath>
</defs>''')
for n,x,r,g in bodies: A(f'<circle cx="{SX}" cy="{CY}" r="{x-SX}" fill="none" stroke="#a99f88" stroke-opacity=".22" stroke-width="1.4"/>')
random.seed(2)
for _ in range(160):
    rr=random.uniform(1500,1600)-SX; a=random.uniform(-.18,.18); x=SX+rr*math.cos(a); y=CY+rr*math.sin(a)
    if 0<y<H: A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(1,2.6):.1f}" fill="#8a7e6a" fill-opacity=".75"/>')
A('<text x="1550" y="452" text-anchor="middle" font-size="16" fill="#8a7e6a" letter-spacing="3" font-family="IBM Plex Mono, monospace">ASTEROID BELT</text>')
A(f'<circle cx="{SX}" cy="{CY}" r="{SR}" fill="url(#gSun)"/>')
for n,x,r,g in bodies:
    if n=='SATURN': A(f'<ellipse cx="{x}" cy="{CY}" rx="{r*1.95:.0f}" ry="{r*.36:.0f}" fill="none" stroke="#e8d3a8" stroke-width="11" stroke-opacity=".8"/>')
    A(f'<circle cx="{x}" cy="{CY}" r="{r}" fill="url(#{g})"/>')
    if n=='JUPITER':
        for dy,h,c in ((-70,18,'#c98d5e'),(-30,16,'#b9784a'),(10,22,'#d9a77a'),(50,14,'#b9784a'),(80,12,'#c98d5e')):
            A(f'<rect x="{x-r}" y="{CY+dy}" width="{2*r}" height="{h}" fill="{c}" fill-opacity=".55" clip-path="url(#cJu)"/>')
        A(f'<ellipse cx="{x+38}" cy="{CY+38}" rx="20" ry="10" fill="#b0473a" fill-opacity=".7"/>')
    if n=='SATURN': A(f'<ellipse cx="{x}" cy="{CY}" rx="{r*1.95:.0f}" ry="{r*.36:.0f}" fill="none" stroke="#e8d3a8" stroke-width="11" stroke-opacity=".9" clip-path="url(#cSaF)"/>')
    A(f'<circle cx="{x}" cy="{CY}" r="{r}" fill="url(#gSh)" {"clip-path=\"none\"" if True else ""}/>')
    ly=CY+max(r,40)+46
    A(f'<text x="{x}" y="{ly}" text-anchor="middle" font-size="16" fill="#b8ab8e" letter-spacing="3" font-family="IBM Plex Mono, monospace">{n}</text>')
MX,MY=1045,150
A(f'<circle cx="{MX}" cy="{MY}" r="9" fill="url(#gMo)"/><text x="{MX+34}" y="{MY+6}" font-size="16" fill="#b8ab8e" letter-spacing="2" font-family="IBM Plex Mono, monospace">MOON</text>')
def torus(x,y,s=1): A(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{11*s}" ry="{4.6*s}" transform="rotate(-30 {x:.1f} {y:.1f})" fill="#0a0b10" stroke="#f0b860" stroke-width="{3*s}"/>')
def loop(cx,cy,r,ang,main=False):
    A(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#f0b860" stroke-width="{4 if main else 2.6}" stroke-opacity="{1 if main else .85}"/>')
    a=math.radians(ang); x,y=cx+r*math.cos(a),cy+r*math.sin(a); torus(x,y,1.4 if main else 1); return x,y
RAVI_X=[(535,'I'),(800,'II'),(1125,'III'),(1450,'IV')]
for xr,num in RAVI_X:
    rr=xr-SX; A(f'<circle cx="{SX}" cy="{CY}" r="{rr}" fill="none" stroke="#f0b860" stroke-width="2.4" stroke-dasharray="10 8" stroke-opacity=".85"/>')
    a=math.asin((340-CY)/rr); x,y=SX+rr*math.cos(a),CY+rr*math.sin(a); torus(x,y)
    A(f'<text x="{x+16:.0f}" y="{y+6:.0f}" font-family="IBM Plex Mono, monospace" font-size="16" font-weight="600" fill="#f0b860" letter-spacing="2" stroke="#0a0b10" stroke-width="5" paint-order="stroke">RAVI {num}</text>')
A('<text x="520" y="398" font-family="IBM Plex Mono, monospace" font-size="17" fill="#ece6d8" letter-spacing="1" stroke="#0a0b10" stroke-width="5" paint-order="stroke">RAVI I–IV · Helios rings orbiting the Sun, one in each gap out to the asteroid belt · Sunday</text>')
rx_,ry_=0,0
P={'BUDHA':loop(420,CY,30,-120),'SHUKRA':loop(650,CY,44,-115),'SOMA':loop(MX,MY,26,-140,True),'MANGALA':loop(1300,CY,38,-120),
   'GURU':loop(1980,CY,150,-125),'SHANI':loop(2560,CY,182,-122),'VARUNA':loop(3000,CY,52,-120),'ARUNA':loop(3250,CY,50,-120),'YAMA':loop(3455,CY,22,-120)}
L=[   ('BUDHA',330,52,'BUDHA','orbits Mercury · Wednesday'),
   ('SHUKRA',620,52,'SHUKRA','orbits Venus · Friday'),
   ('SOMA',930,40,'SOMA','orbits the Moon · Monday'),
   ('MANGALA',1250,52,'MANGALA','orbits Mars · Tuesday'),
   ('GURU',1660,52,'GURU','orbits Jupiter · Thursday'),
   ('SHANI',2180,52,'SHANI','orbits Saturn · Saturday'),
   ('VARUNA',2850,52,'VARUNA','orbits Uranus'),
   ('ARUNA',3110,52,'ARUNA','orbits Neptune'),
   ('YAMA',3350,52,'YAMA','orbits Pluto')]
for k,x,y,name,line in L:
    px,py=P[k]; main=k=='SOMA'
    ty=y+36 if y<200 else y-28
    A(f'<line x1="{px:.0f}" y1="{py:.0f}" x2="{x+8}" y2="{ty}" stroke="#f0b860" stroke-opacity=".5" stroke-width="1.2"/>')
    A(f'<text x="{x}" y="{y}" font-family="IBM Plex Mono, monospace" font-size="{27 if main else 21}" font-weight="600" fill="{"#ffd27a" if main else "#f0b860"}" letter-spacing="3" stroke="#0a0b10" stroke-width="6" paint-order="stroke">{name}</text>')
    for j,part in enumerate(line.split(' · ')):
        A(f'<text x="{x}" y="{y+26+22*j}" font-family="IBM Plex Mono, monospace" font-size="17" fill="{"#ece6d8" if j==0 else "#b8ab8e"}" letter-spacing="1" stroke="#0a0b10" stroke-width="5" paint-order="stroke">{part}</text>')
A('</svg>')
open('header.svg','w').write('\n'.join(o))
p=open('poster.html').read()
a=p.index('<svg viewBox="0 0 3520 470"'); b=p.index('</svg>',a)+len('</svg>')
p=p[:a]+'\n'.join(o)+p[b:]
p=p.replace("SEVEN SETTLEMENTS, ONE FOR EACH DAY OF THE WEEK · EACH ORBITS ITS NAMESAKE","SETTLEMENTS NAMED FOR THE BODIES THEY ORBIT · RAVI TO YAMA")
open('poster.html','w').write(p); print('ok')
