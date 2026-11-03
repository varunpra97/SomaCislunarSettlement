import minfont; minfont.install(16)
import sys, math, random, cairo
sys.path.insert(0,'../stack'); sys.path.insert(0,'../video')
from common import text, GOLD, CY, FG, MUT
W,H,S=960,890,6
surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,W*S,H*S); ctx=cairo.Context(surf); ctx.scale(S,S)
def rgb(h,a=1): ctx.set_source_rgba(int(h[1:3],16)/255,int(h[3:5],16)/255,int(h[5:7],16)/255,a)
rgb('#0a0b10'); ctx.paint()
random.seed(3)
for _ in range(400):
    ctx.arc(random.uniform(0,W),random.uniform(0,H),random.choice([.4,.6,.8]),0,2*math.pi); ctx.set_source_rgba(1,1,1,random.uniform(.1,.5)); ctx.fill()
# ---- left: one ring in perspective ----
cx,cy,rx,ry=470,250,390,150
def E(a,k=1.0): return (cx+rx*k*math.cos(a),cy+ry*k*math.sin(a))
def ell(k,col_,w,a=1,dash=None):
    ctx.save(); ctx.translate(cx,cy); ctx.scale(rx*k,ry*k); ctx.new_path(); ctx.arc(0,0,1,0,2*math.pi); ctx.restore()
    rgb(col_,a); ctx.set_line_width(w); 
    if dash: ctx.set_dash(dash)
    ctx.stroke(); ctx.set_dash([])
# back half of tube & shield
for i in range(6):
    a=math.radians(30+60*i)
    # wings along spokes
    p=E(a,.12); q=E(a,.9); ux,uy=q[0]-p[0],q[1]-p[1]; L=math.hypot(ux,uy); nx,ny=-uy/L*7,ux/L*7*.42
    ctx.move_to(p[0]+nx,p[1]+ny); ctx.line_to(q[0]+nx,q[1]+ny); ctx.line_to(q[0]-nx,q[1]-ny); ctx.line_to(p[0]-nx,p[1]-ny); ctx.close_path(); rgb('#20335a'); ctx.fill_preserve(); rgb('#6d8fd6',.8); ctx.set_line_width(.8); ctx.stroke()
    rgb('#66c2d4'); ctx.set_line_width(1.6); ctx.move_to(cx,cy); ctx.line_to(*E(a)); ctx.stroke()
ell(.5,'#f0b860',3,.9)
ell(1.0,'#5a4a34',30,1)        # static shield
ell(1.0,'#66c2d4',12,1)        # tube
ell(1.0,'#f0b860',2,.9,[6,6])  # hoop bands
# radiator fins: short ticks outward
for i in range(48):
    a=2*math.pi*i/48; p=E(a,1.06); q=E(a,1.14)
    rgb('#c7b89a',.8); ctx.set_line_width(1.6); ctx.move_to(*p); ctx.line_to(*q); ctx.stroke()
# centre pod on the Starship spine
rgb('#c9c5ba'); ctx.set_line_width(5); ctx.move_to(cx+18,cy-120); ctx.line_to(cx-18,cy+120); ctx.stroke()
ctx.save(); ctx.translate(cx,cy); ctx.scale(22,13); ctx.new_path(); ctx.arc(0,0,1,0,2*math.pi); ctx.restore(); rgb('#c7b89a'); ctx.fill()
# highlight the section that is cut open
ha=math.radians(125); hx,hy=E(ha)
ctx.new_path(); ctx.arc(hx,hy,24,0,2*math.pi); rgb('#f0b860'); ctx.set_line_width(2); ctx.stroke()
def lab(s,x,y,tx,ty,c,anchor='l',size=13):
    rgb(c,.6); ctx.set_line_width(1); ctx.move_to(tx,ty); ctx.line_to(x,y-4); ctx.stroke(); text(ctx,s,x+(5 if anchor=='l' else -5),y,size,c,anchor=anchor)
lab('STATIC REGOLITH SHIELD',30,40,*E(math.radians(235),1.0),'#8a7350',size=15)
lab('SPINNING TUBE · 109 km AROUND',560,40,*E(math.radians(-60),1.0),CY,size=15)
lab('SOLAR WINGS ON 6 SPOKES',20,455,*E(math.radians(150),.6),'#6d8fd6',size=15)
lab('MIDDLE RING · 0.5 g',300,455,*E(math.radians(105),.5),GOLD,size=15)
lab('CENTRE POD ON THE SPINE',250,72,cx-10,cy-10,FG,size=15)
lab('RADIATOR FIN PER CELL',540,455,*E(math.radians(70),1.12),'#c7b89a',size=15)
# leader to the cross-section
rgb('#f0b860',.5); ctx.set_line_width(1.2); ctx.move_to(hx-14,hy+18); ctx.line_to(120,500); ctx.move_to(hx+14,hy+18); ctx.line_to(360,500); ctx.stroke()
# ---- right: the tube cut open, layer by layer ----
tx,ty,R=240,665,140
layers=[  # (radius outer, radius inner, colour, name)
 (R+40,R+18,'#5a4a34'), # shield
]
# shield (static, separate)
ctx.new_path(); ctx.arc(tx,ty,R+30,0,2*math.pi); rgb('#5a4a34'); ctx.set_line_width(24); ctx.stroke()
# gap
# hoop bands
ctx.new_path(); ctx.arc(tx,ty,R+7,0,2*math.pi); rgb('#f0b860'); ctx.set_line_width(4); ctx.set_dash([9,5]); ctx.stroke(); ctx.set_dash([])
# hull
ctx.new_path(); ctx.arc(tx,ty,R,0,2*math.pi); rgb('#66c2d4'); ctx.set_line_width(4); ctx.stroke()
# interior: sky, floors
ctx.save(); ctx.new_path(); ctx.arc(tx,ty,R-2,0,2*math.pi); ctx.clip()
rgb('#162440'); ctx.paint()
for i in range(9):
    yy=ty+R-18-i*14; rgb('#3f8796',.5); ctx.set_line_width(1); ctx.move_to(tx-R,yy); ctx.line_to(tx+R,yy); ctx.stroke()
# soil + water layer at the bottom ("down" is outward)
rgb('#5c4a32'); ctx.rectangle(tx-R,ty+R-20,2*R,20); ctx.fill()
rgb('#5f8f4e'); ctx.rectangle(tx-R,ty+R-24,2*R,5); ctx.fill()
rgb('#3a7fa8'); ctx.rectangle(tx-40,ty+R-28,80,8); ctx.fill()
# step terraces either side of a green canyon
base=ty+R-24; n=7; rise=15; tread=14; c=32
for side in (-1,1):
    ctx.new_path(); ctx.move_to(tx+side*c,base)
    for i in range(n):
        x=tx+side*(c+tread*i); ctx.line_to(x,base-rise*(i+1)); ctx.line_to(tx+side*(c+tread*(i+1)) if i<n-1 else tx+side*R,base-rise*(i+1))
    ctx.line_to(tx+side*R,base); ctx.close_path(); rgb('#e6b85c'); ctx.fill()
    for i in range(n):
        x=tx+side*(c+tread*i); y=base-rise*(i+1)
        rgb('#bfe0f0'); ctx.rectangle(x-(2 if side>0 else 0),y,2,rise); ctx.fill()
        x1=tx+side*(c+tread*(i+1)) if i<n-1 else tx+side*R
        rgb('#5f8f4e'); ctx.rectangle(min(x,x1),y-3,abs(x1-x),3); ctx.fill()
for bx in (-16,0,16):
    ctx.new_path(); ctx.arc(tx+bx,ty+R-31,7,0,2*math.pi); rgb('#5f8f4e'); ctx.fill()
ctx.restore()
# window strip at the top (toward the hub)
ctx.new_path(); ctx.arc(tx,ty,R,math.radians(-120),math.radians(-60)); rgb('#7fd6ec'); ctx.set_line_width(5); ctx.stroke()

text(ctx,'↑ to the hub',tx,ty-60,12,MUT,anchor='c'); text(ctx,'down = outward',tx,ty+R-150,11,'#e8e2d4',anchor='c')
# numbered callouts
calls=[((tx+(R+30)*math.cos(math.radians(-35)),ty+(R+30)*math.sin(math.radians(-35))),'1'),
       ((tx+(R+7)*math.cos(math.radians(-8)),ty+(R+7)*math.sin(math.radians(-8))),'2'),
       ((tx+R*math.cos(math.radians(20)),ty+R*math.sin(math.radians(20))),'3'),
       ((tx+R*.55,ty+R*.86),'4'),
       ((tx+R*math.cos(math.radians(-90)),ty-R),'5')]
for (p,n) in calls:
    ctx.new_path(); ctx.arc(p[0],p[1],11,0,2*math.pi); rgb('#f0b860'); ctx.fill(); text(ctx,n,p[0],p[1]+4.5,12,'#1a1206',anchor='c',bold=True)
# legend
rows=[('1','REGOLITH SHIELD','~260 Mt · raw lunar regolith, 4.5 t/m²','static, so it adds no spin load'),
      ('2','HOOP BANDS','~18 Mt · basalt fibre from mare basalt','carry the spin; steel would need 1.3 GPa'),
      ('3','PRESSURE HULL','~4 Mt · aluminium, 84 panels per bay','Starship-sized units, welded by robots'),
      ('4','SOIL AND INTERIORS','~15 Mt · sieved regolith and carbon','0.5 m soil, step-terrace homes'),
      ('5','WINDOWS, AIR, WATER','glass ~1 Mt · water 5 Mt · O₂ 0.5 · N₂ 0.6 Mt','polar ice and asteroids; N₂ is scarce')]
y=512
for n,a,b,c in rows:
    ctx.new_path(); ctx.arc(462,y-5,12,0,2*math.pi); rgb('#f0b860'); ctx.fill(); text(ctx,n,462,y-.5,13,'#1a1206',anchor='c',bold=True)
    text(ctx,a,484,y,15,GOLD,bold=True); text(ctx,b,484,y+22,13.5,FG); text(ctx,c,484,y+42,13,MUT)
    y+=62
text(ctx,'~300 Mt in all, mostly lunar',484,y+2,14,CY); text(ctx,'built in 6,060 bays of 18 m by 6 bay factories',484,y+22,13,CY)
surf.write_to_png('img/onering.png'); print('ok')
