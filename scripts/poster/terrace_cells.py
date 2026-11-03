"""Rewrite the cross-sections of cells where people live or work as step terraces."""
import re, math
A='/tmp/claude-0/-home-claude/2aa3f404-8de0-56e4-b320-595de06df08e/scratchpad/repo/designs/html/assets/'
B='/tmp/claude-0/-home-claude/2aa3f404-8de0-56e4-b320-595de06df08e/scratchpad/cellbak/'
Y0=156.1; LV=3.4667; L=6.8; Rr=173.2; C=90.0
def r(x,y,w,h,f,o=1): return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{f}" opacity="{o}"/>'
def circ(x,y,rr,f,o=1): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr}" fill="{f}" opacity="{o}"/>'

def terraces(key,c,ht,n,col,y0=Y0,tread=None,garden='#6f8b52',glass='#bfe0f0',lights=None,trees=True,roof=True):
    """Two stepped blocks either side of a canyon of half-width c, n steps up to height ht."""
    out=[]; rise=ht/n
    if tread is None: tread=(C-c-L-8)/(n-1)
    for side in (-1,1):
        pts=[]; edge=lambda dx: C+side*dx
        pts.append((edge(c),y0))
        for i in range(n):
            yt=y0-rise*(i+1); xi=edge(c+tread*i)
            pts.append((xi,y0-rise*i)); pts.append((xi,yt))
            pts.append((edge(c+tread*(i+1)) if i<n-1 else (L if side<0 else Rr),yt))
        pts.append((L if side<0 else Rr,y0))
        cid=f'{key}{"l" if side<0 else "r"}'
        P=' '.join(f'{x:.1f},{y:.1f}' for x,y in pts)
        out.append(f'<clipPath id="{cid}"><polygon points="{P}"/></clipPath>')
        out.append(f'<polygon points="{P}" fill="{col}"/>')
        g=[f'<g clip-path="url(#{cid})">']
        y=y0-LV
        while y>y0-ht: g.append(f'<line x1="{L}" y1="{y:.1f}" x2="{Rr}" y2="{y:.1f}" stroke="#0a0b10" stroke-width="0.5" opacity="0.4"/>'); y-=LV
        g.append('</g>'); out+=g
        for i in range(n):
            yb=y0-rise*i; yt=y0-rise*(i+1); xi=edge(c+tread*i)
            # glass front on each riser
            out.append(r(xi-(1.4 if side>0 else 0),yt,1.4,rise,glass,.95))
            if lights:
                for k in range(int(rise//2.6)):
                    out.append(r(xi+side*2.2-0.9,yb-2-k*2.6,1.8,1.4,lights,.9))
            # garden on the tread above this riser
            x0=xi; x1=edge(c+tread*(i+1)) if i<n-1 else (L if side<0 else Rr)
            if garden and (i<n-1 or roof):
                out.append(r(min(x0,x1),yt-1.0,abs(x1-x0),1.0,garden))
                if trees and i<n-1 and i%2==0: out.append(circ((x0+x1)/2,yt-2.6,1.9,'#4f7a3e'))
    return out

def write(name,inner):
    s=open(B+f'cell-{name}.svg').read()
    head=s[:s.index('<g clip-path')]; g0=s[s.index('<g clip-path'):]
    gopen=g0[:g0.index('>')+1]
    base=re.search(r'<rect x="6.8" y="156.1"[^>]*>(?:<line[^>]*stroke="#6b6252"[^>]*>)*',g0).group(0)
    tail=g0[g0.index('<rect x="6.8" y="14.0"'):]
    defs=[e for e in inner if e.startswith('<clipPath')]
    body=[e for e in inner if not e.startswith('<clipPath')]
    head=head.replace('</defs>',''.join(defs)+'</defs>')
    open(A+f'cell-{name}.svg','w').write(head+gopen+base+''.join(body)+tail)

# HOME: 10 steps L5-L31 either side of a 40 m green canyon
e=terraces('res',20.8,90.1,10,'#e6b85c',lights='#ffe29a')
e+= [r(C-20.8,Y0-3.1,41.6,3.1,'#6f8b52')]+[circ(x,Y0-4.1,3,'#6f8b52') for x in (77.5,85.8,96.2,104.6)]
write('res',e)
# LAB: heavy labs on the hull (L5-8), then 8 steps of labs and offices round a 20 m light well
e=[r(L,142.3,166.4,13.8,'#6d7fa8')]
e+=terraces('lab',10.4,69.4,8,'#9fb7e8',y0=142.3,garden='#7fae5a',trees=False)
e+=[r(75.4,128.4,29.1,13.9,'#ffffff',.85)]
write('lab',e)
# CIVIC: 6 steps to L20 around a 52 m plaza
e=terraces('civ',26.0,55.5,6,'#d8a0b8',garden='#7fae5a')
e+=[r(64.0,154.1,52.0,2.0,'#c9c5ba')]+[circ(x,150.8,2.6,'#4f8a3a') for x in (72,84,96,108)]
write('civ',e)
# FOOD AND NIGHT: 5 lit steps to L15 around the concert plaza
e=terraces('food',26.0,41.6,5,'#e07a5f',garden='#c98a3a',lights='#ffe29a',trees=False)
e+=[r(64.0,154.6,52.0,1.5,'#c9c5ba')]
for i in range(13):
    x=65+i*(50/12); y=133+4*math.sin(i*1.3)+3
    e.append(circ(x,y,1.5,'#ffe29a'))
write('food',e)
# HUB: stepped concourse round the spoke elevators
e=terraces('hub',14.0,41.6,4,'#66c2d4',garden=None,lights='#e9fbff')
e+=[r(83.8,0,12.5,Y0,'#66c2d4'),r(85.6,0,8.9,Y0,'#2b6f80',.6)]
write('hub',e)
# PLAY: the sloped stands become stepped seating with gyms inside; fields and climbing wall stay
s=open(B+'cell-park.svg').read()
pts=[(L,Y0)]; n=12; rise=48.6/n; run=54.1/n
for i in range(n):
    x=L+run*i; y=Y0-48.6+rise*i
    pts+= [(x,y),(x+run,y)]
pts+=[(L+54.1,Y0)]
Lp=' '.join(f'{x:.1f},{y:.1f}' for x,y in pts)
Rp=' '.join(f'{2*C-x:.1f},{y:.1f}' for x,y in pts)
s=re.sub(r'<polygon points="[^"]*" fill="#c98a3a" opacity="0.9"/>',
         f'<polygon points="{Lp}" fill="#c98a3a" opacity="0.9"/><polygon points="{Rp}" fill="#c98a3a" opacity="0.9"/>',s)
open(A+'cell-park.svg','w').write(s)
print('ok')
