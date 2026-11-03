import math
R=75; PX=78/75; CX=90; CY=92; r=78
def y(h): return CY+r-h*PX
def x(m): return CX+m*PX
def lv(l): return (l-1)*150/45  # bottom of level l in m
def w(h): return math.sqrt(max(0,R*R-(R-h)**2))
SKY='#16233a'; BASE='#3a3530'
def band(h0,h1,c,op=1,x0=-80,x1=80):
    return f'<rect x="{x(x0):.1f}" y="{y(h1):.1f}" width="{(x1-x0)*PX:.1f}" height="{(h1-h0)*PX:.1f}" fill="{c}" opacity="{op}"/>'
def floors(h0,h1,x0,x1,step=3.333,c='#0a0b10',op=.5):
    s=''
    h=h0+step
    while h<h1-0.1:
        s+=f'<line x1="{x(x0):.1f}" y1="{y(h):.1f}" x2="{x(x1):.1f}" y2="{y(h):.1f}" stroke="{c}" stroke-width="0.6" opacity="{op}"/>'
        h+=step
    return s
def card(key,inner):
    return (f'<svg width="180" height="184" viewBox="0 0 180 184" role="img" aria-label="{key} cell cross-section">'
      f'<defs><clipPath id="c{key}"><circle cx="{CX}" cy="{CY}" r="{r}"/></clipPath></defs>'
      f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="{SKY}"/>'
      f'<g clip-path="url(#c{key})">{band(0,lv(5),BASE)}{floors(0,lv(5),-80,80,c="#6b6252",op=.8)}{inner}'
      f'{band(lv(44),150,"#7fd6ec",.25)}</g>'
      f'<path d="M{x(-22):.1f} {y(146.6):.1f} A{r} {r} 0 0 1 {x(22):.1f} {y(146.6):.1f}" fill="none" stroke="#7fd6ec" stroke-width="5"/>'
      f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="#f0b860" stroke-width="2.5"/></svg>')
out={}
L5=lv(5)
# residence
out['res']=card('res',band(L5,lv(31),'#e6b85c',1,-80,-20)+band(L5,lv(31),'#e6b85c',1,20,80)+floors(L5,lv(31),-80,-20)+floors(L5,lv(31),20,80)+band(L5,L5+3,'#6f8b52',1,-20,20)+band(lv(31),lv(31)+2,'#6f8b52',1,-80,-20)+band(lv(31),lv(31)+2,'#6f8b52',1,20,80)+''.join(f'<circle cx="{x(xx):.1f}" cy="{y(L5+4):.1f}" r="3" fill="#6f8b52"/>' for xx in (-12,-4,6,14)))
# research
out['lab']=card('lab',band(L5,lv(29),'#9fb7e8',1,-80,-10)+band(L5,lv(29),'#9fb7e8',1,10,80)+floors(L5,lv(29),-80,-10)+floors(L5,lv(29),10,80)+band(L5,lv(9),'#6d7fa8',1,-80,80)+band(lv(9),lv(13),'#ffffff',.85,-14,14))
# farm
s=''
for i in range(9):
    h=L5+5*i
    s+=band(h,h+1.2,'#5b4630',1,-80,80)+band(h+1.2,h+2.6,'#7fbf5a',1,-80,80)
s+=band(L5+45,L5+47,'#5b4630',1)+''.join(f'<rect x="{x(xx)-2:.1f}" y="{y(L5+52):.1f}" width="4" height="{8*PX:.1f}" fill="#4f8a3a"/><circle cx="{x(xx):.1f}" cy="{y(L5+53):.1f}" r="5" fill="#6f9e4a"/>' for xx in (-50,-30,-10,10,30,50))
s+=''.join(f'<line x1="{x(xx):.1f}" y1="{y(146):.1f}" x2="{x(xx):.1f}" y2="{y(L5+47):.1f}" stroke="#ffe29a" stroke-width="1" opacity=".55"/>' for xx in (-40,0,40))
out['farm']=card('farm',s)
# hardware plant
s=band(L5,lv(21),'#7d756a',1)+floors(L5,lv(21),-80,80,step=10,c='#0a0b10',op=.6)
s+=''.join(f'<rect x="{x(xx):.1f}" y="{y(hh+8):.1f}" width="{14*PX:.1f}" height="{8*PX:.1f}" fill="#9a917f" stroke="#0a0b10" stroke-width=".6"/>' for xx,hh in ((-60,L5+2),(-38,L5+2),(-16,L5+2),(6,L5+2),(28,L5+2),(-50,L5+22),(-20,L5+22),(10,L5+22),(40,L5+22)))
s+=''.join(f'<circle cx="{x(xx):.1f}" cy="{y(L5+38):.1f}" r="{6*PX:.1f}" fill="#9a917f" stroke="#0a0b10" stroke-width=".6"/>' for xx in (-40,-20,0,20,40))
out['hw']=card('hw',s)
# industry
out['ind']=card('ind',band(L5,lv(17),'#c98a3a',1)+floors(L5,lv(17),-80,80,step=8.3)+band(lv(17),lv(17)+1.5,'#9a917f',1)+''.join(f'<rect x="{x(xx):.1f}" y="{y(L5+7):.1f}" width="{10*PX:.1f}" height="{6*PX:.1f}" fill="#0a0b10" opacity=".5"/>' for xx in (-50,-25,0,25)))
# civic & health
out['civ']=card('civ',band(L5,lv(21),'#d8a0b8',1,-80,-25)+band(L5,lv(21),'#d8a0b8',1,25,80)+floors(L5,lv(21),-80,-25)+floors(L5,lv(21),25,80)+band(L5,L5+2,'#c9c5ba',1,-25,25)+band(lv(13),lv(21),'#d8a0b8',.7,-25,25)+floors(lv(13),lv(21),-25,25))
# spoke hub
out['hub']=card('hub',band(L5,lv(17),'#66c2d4',.8)+floors(L5,lv(17),-80,80)+f'<rect x="{x(-6):.1f}" y="0" width="{12*PX:.1f}" height="{y(lv(17)):.1f}" fill="#66c2d4"/>')
# great outdoors
def terrain(fn,c,op=1):
    pts=' '.join(f'{x(m):.1f},{y(L5+fn(m)):.1f}' for m in range(-80,81,4))
    return f'<polygon points="{x(-80):.1f},{y(L5):.1f} {pts} {x(80):.1f},{y(L5):.1f}" fill="{c}" opacity="{op}"/>'
hills=lambda m: max(0,(abs(m)-12)*0.95)+6*math.sin(m/7)**2
s=terrain(hills,'#4f7a3e')+terrain(lambda m:max(0,(abs(m)-30)*0.7),'#3d6331')
s+=band(L5,L5+2,'#3f8fbf',1,-9,9)
s+=''.join(f'<circle cx="{x(m):.1f}" cy="{y(L5+hills(m)+3):.1f}" r="3.2" fill="#2f5226"/>' for m in (-52,-44,-36,-26,24,32,40,50))
out['out']=card('out',s)
# waterfront
s=band(L5-4,L5+4,'#2e7fb8',1,-55,55)+terrain(lambda m:max(0,(abs(m)-55)*1.6),'#d9c38f')+terrain(lambda m:max(0,(abs(m)-62)*3.2),'#8a806c')
s+=band(L5+4,L5+5,'#7fd6ec',.6,-55,55)+band(L5+4,L5+5.5,'#e8d6a6',1,-62,-55)+band(L5+4,L5+5.5,'#e8d6a6',1,55,62)
out['wat']=card('wat',s)
# food & night
s=''.join(band(L5,L5+hh,'#e07a5f',1,a,b)+floors(L5,L5+hh,a,b) for a,b,hh in ((-80,-50,40),(-50,-25,25),(25,50,25),(50,80,40)))
s+=band(L5,L5+1.5,'#c9c5ba',1,-25,25)
s+=''.join(f'<circle cx="{x(m):.1f}" cy="{y(L5+18+3*math.sin(m)):.1f}" r="1.6" fill="#ffe29a"/>' for m in range(-24,25,4))
s+=''.join(f'<rect x="{x(m):.1f}" y="{y(L5+h):.1f}" width="2.4" height="2.4" fill="#ffe29a"/>' for m in range(-76,-28,8) for h in (8,16,24))
out['food']=card('food',s)
# parks & sports
s=band(L5,L5+1.5,'#6fae4f',1,-60,60)+band(L5,lv(26),'#b8ad98',1,60,80)+''.join(f'<line x1="{x(60):.1f}" y1="{y(L5+k):.1f}" x2="{x(80):.1f}" y2="{y(L5+k):.1f}" stroke="#0a0b10" stroke-width=".6"/>' for k in range(6,70,8))
s+=band(L5,L5+14,'#c9c5ba',1,-80,-62)+''.join(f'<line x1="{x(-80):.1f}" y1="{y(L5+k):.1f}" x2="{x(-62):.1f}" y2="{y(L5+k):.1f}" stroke="#0a0b10" stroke-width=".6"/>' for k in range(3,14,3))
s+=f'<line x1="{x(0):.1f}" y1="{y(L5+1.5):.1f}" x2="{x(0):.1f}" y2="{y(L5+1.5)-0:.1f}" stroke="#fff"/>'
s+=f'<circle cx="{x(0):.1f}" cy="{y(L5+1.5)-1:.1f}" r="0.1" fill="#fff"/>'
out['park']=card('park',s)
import json; json.dump(out,open('cards.json','w'))
# district strip: 20 cells
seq=['out','res','farm','res','lab','farm','wat','res','civ','farm','out','res','hw','food','farm','res','lab','park','ind','out']
cw=104; H=150; base_y=170
col={'res':'#e6b85c','lab':'#9fb7e8','farm':'#7fbf5a','hw':'#7d756a','ind':'#c98a3a','civ':'#d8a0b8','out':'#4f7a3e','wat':'#2e7fb8','food':'#e07a5f','park':'#6fae4f'}
top={'res':100,'lab':93,'farm':58,'hw':67,'ind':53,'civ':67,'out':45,'wat':10,'food':40,'park':20}
names={'res':'HOME','lab':'LAB','farm':'FARM','hw':'PLANT','ind':'MAKE','civ':'CIVIC','out':'WILD','wat':'WATER','food':'FOOD','park':'PLAY'}
s=f'<rect x="0" y="{base_y-H}" width="{cw*20}" height="{H}" fill="#16233a"/>'
s+=f'<rect x="0" y="{base_y-H}" width="{cw*20}" height="4" fill="#7fd6ec" opacity=".7"/>'
for i,k in enumerate(seq):
    x0=i*cw; t=top[k]
    if k=='out':
        pts=' '.join(f'{x0+j*cw/12:.1f},{base_y-13-(25+18*math.sin(j*0.9+i))*(1 if 0<j<12 else .4):.1f}' for j in range(13))
        s+=f'<polygon points="{x0},{base_y-13} {pts} {x0+cw},{base_y-13}" fill="#4f7a3e"/>'
        s+=f'<rect x="{x0+cw*0.42:.1f}" y="{base_y-15}" width="{cw*0.16:.1f}" height="3" fill="#3f8fbf"/>'
    elif k=='wat':
        s+=f'<rect x="{x0+8}" y="{base_y-18}" width="{cw-16}" height="8" fill="#2e7fb8"/><rect x="{x0}" y="{base_y-20}" width="8" height="8" fill="#e8d6a6"/><rect x="{x0+cw-8}" y="{base_y-20}" width="8" height="8" fill="#e8d6a6"/>'
    elif k=='farm':
        for j in range(9): s+=f'<rect x="{x0+3}" y="{base_y-13-5*j-3:.1f}" width="{cw-6}" height="2.6" fill="#7fbf5a"/>'
    elif k=='food':
        for a,b,hh in ((0,.3,40),(.3,.42,25),(.58,.7,25),(.7,1,40)): s+=f'<rect x="{x0+a*cw:.1f}" y="{base_y-13-hh}" width="{(b-a)*cw:.1f}" height="{hh}" fill="#e07a5f"/>'
        s+=''.join(f'<circle cx="{x0+cw*.42+k2*4:.1f}" cy="{base_y-30}" r="1.5" fill="#ffe29a"/>' for k2 in range(5))
    elif k=='park':
        s+=f'<rect x="{x0+4}" y="{base_y-15}" width="{cw-20}" height="2" fill="#6fae4f"/><rect x="{x0+cw-14}" y="{base_y-13-70}" width="10" height="70" fill="#b8ad98"/>'
    else:
        s+=f'<rect x="{x0+3}" y="{base_y-13-(t-13)}" width="{cw-6}" height="{t-13}" fill="{col[k]}"/>'
        if k in('res','lab'): s+=f'<rect x="{x0+cw/2-8}" y="{base_y-13-(t-13)}" width="16" height="{t-13}" fill="#16233a"/>'
    s+=f'<line x1="{x0}" y1="{base_y-H}" x2="{x0}" y2="{base_y}" stroke="#0a0b10" stroke-width="1.5"/>'
    s+=f'<text x="{x0+cw/2}" y="{base_y+18}" text-anchor="middle" font-size="11" fill="{col[k]}" letter-spacing="1">{names[k]}</text>'
s+=f'<rect x="0" y="{base_y-13}" width="{cw*20}" height="13" fill="#3a3530"/>'
s+=f'<rect x="0" y="{base_y-H}" width="{cw*20}" height="{H}" fill="none" stroke="#f0b860" stroke-width="2"/>'
open('strip.svg','w').write(s)
print({k:len(v) for k,v in out.items()}, len(s))
# --- improved waterfront and parks ---
s=terrain(lambda m:max(0,(abs(m)-38)*0.55)+max(0,(abs(m)-58)*1.8),'#d9c38f')
s+=terrain(lambda m:max(0,(abs(m)-60)*2.6),'#8a806c')
s+=band(L5,L5+4,'#2e7fb8',1,-38,38)+band(L5+4,L5+4.8,'#7fd6ec',.7,-38,38)
s+=''.join(f'<rect x="{x(m)-1:.1f}" y="{y(L5+4+max(0,(abs(m)-38)*0.55)+9):.1f}" width="2" height="{9*PX:.1f}" fill="#8a6a3a"/><circle cx="{x(m):.1f}" cy="{y(L5+4+max(0,(abs(m)-38)*0.55)+10):.1f}" r="4" fill="#4f8a3a"/>' for m in (-52,-46,46,52))
s+=f'<rect x="{x(-4):.1f}" y="{y(L5+22):.1f}" width="{8*PX:.1f}" height="{1.2*PX:.1f}" fill="#c9c5ba"/><line x1="{x(0):.1f}" y1="{y(L5+22):.1f}" x2="{x(0):.1f}" y2="{y(L5+4):.1f}" stroke="#c9c5ba" stroke-width="1.5"/>'
s+=''.join(f'<rect x="{x(m):.1f}" y="{y(L5+h):.1f}" width="2.4" height="2.4" fill="#ffe29a"/>' for m in (-70,-66,64,68) for h in (24,30))
out['wat']=card('wat',s)
s=band(L5,L5+1.5,'#6fae4f',1,-45,45)
s+=''.join(f'<line x1="{x(m):.1f}" y1="{y(L5+1.5):.1f}" x2="{x(m):.1f}" y2="{y(L5+1.6):.1f}" stroke="#ffffff"/>' for m in (-45,0,45))
s+=band(L5+1.5,L5+1.9,'#ffffff',.8,-45,45)
for sgn in (-1,1):
    pts=' '.join(f'{x(sgn*(45+k*4)):.1f},{y(L5+k*4):.1f} {x(sgn*(49+k*4)):.1f},{y(L5+k*4):.1f}' for k in range(5))
    s+=terrain(lambda m,sg=sgn:(max(0,(m*sg)-45)*1.0) if m*sg>45 else 0,'#c98a3a',.9)
s+=band(L5,lv(28),'#b8ad98',1,66,80)+''.join(f'<rect x="{x(68+(k%3)*3):.1f}" y="{y(L5+6+k*6):.1f}" width="2.2" height="2.2" fill="#e07a5f"/>' for k in range(11))
s+=''.join(f'<circle cx="{x(m):.1f}" cy="{y(L5+5):.1f}" r="3.5" fill="#4f8a3a"/>' for m in (-62,-56))
out['park']=card('park',s)
import json; json.dump(out,open('cards.json','w'))
for k,v in out.items():
    open(f'cell-{k}.svg','w').write(v.replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" ',1))
# --- v3 waterfront / parks fitted inside the walls ---
shore=lambda m: 0 if abs(m)<30 else ((abs(m)-30)*0.7 if abs(m)<38 else 5.6+(abs(m)-38)*1.4)
s=terrain(shore,'#d9c38f')+terrain(lambda m: 0 if abs(m)<38 else (abs(m)-38)*1.4,'#8a806c')
s+=band(L5,L5+3,'#2e7fb8',1,-30,30)+band(L5+3,L5+3.8,'#7fd6ec',.7,-30,30)
s+=''.join(f'<rect x="{x(m)-1:.1f}" y="{y(L5+shore(m)+9):.1f}" width="2" height="{9*PX:.1f}" fill="#8a6a3a"/><circle cx="{x(m):.1f}" cy="{y(L5+shore(m)+10):.1f}" r="4" fill="#4f8a3a"/>' for m in (-35,35))
s+=f'<rect x="{x(-4):.1f}" y="{y(L5+20):.1f}" width="{8*PX:.1f}" height="{1.2*PX:.1f}" fill="#c9c5ba"/><line x1="{x(0):.1f}" y1="{y(L5+20):.1f}" x2="{x(0):.1f}" y2="{y(L5+3):.1f}" stroke="#c9c5ba" stroke-width="1.5"/>'
s+=''.join(f'<rect x="{x(sg*m):.1f}" y="{y(L5+5.6+(m-38)*1.4+3):.1f}" width="2.6" height="2.6" fill="#ffe29a"/>' for sg in (-1,1) for m in (44,50,56))
out['wat']=card('wat',s)
stands=lambda m: 0 if abs(m)<28 else (abs(m)-28)*0.9
s=band(L5,L5+1.2,'#6fae4f',1,-28,28)+band(L5+1.2,L5+1.6,'#ffffff',.8,-28,28)
s+=terrain(stands,'#c98a3a',.9)
s+=''.join(f'<line x1="{x(sg*m):.1f}" y1="{y(L5+stands(m)):.1f}" x2="{x(sg*(m+3)):.1f}" y2="{y(L5+stands(m)):.1f}" stroke="#0a0b10" stroke-width=".8"/>' for sg in (-1,1) for m in range(30,60,3))
s+=f'<rect x="{x(44):.1f}" y="{y(L5+70):.1f}" width="{8*PX:.1f}" height="{55*PX:.1f}" fill="#b8ad98"/>'+''.join(f'<rect x="{x(45+(k%3)*2.2):.1f}" y="{y(L5+20+k*4.5):.1f}" width="2" height="2" fill="#e07a5f"/>' for k in range(11))
s+=''.join(f'<circle cx="{x(m):.1f}" cy="{y(L5+stands(m)+4):.1f}" r="3.2" fill="#4f8a3a"/>' for m in (-50,-44))
out['park']=card('park',s)
json.dump(out,open('cards.json','w'))
for k,v in out.items():
    open(f'cell-{k}.svg','w').write(v.replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" ',1))
