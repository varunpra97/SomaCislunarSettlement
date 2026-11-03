import json, re
d=json.load(open('../stack/cost.json')); O={r['k']:r['pp_spine'] for r in d['opt']}; C={r['k']:r['pp_spine'] for r in d['cons']}
ks=[1,2,3,5,10,25,50,100]; ks=[k for k in ks if k in O]
W,H=564,290; L,R,T,B=66,8,70,52; pw=W-L-R; ph=H-T-B; mx=700e3
o=[f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="IBM Plex Mono, monospace" role="img" aria-label="Build cost per resident for each new ring, optimistic and conservative">']
for v in (0,200e3,400e3,600e3):
    y=T+ph-ph*v/mx; o.append(f'<line x1="{L}" x2="{W-R}" y1="{y:.1f}" y2="{y:.1f}" stroke="#2c2a24"/><text x="{L-10}" y="{y+6:.1f}" text-anchor="end" font-size="16" fill="#b8ab8e">${int(v/1e3)}k</text>')
n=len(ks); bw=pw/n
for i,k in enumerate(ks):
    x=L+i*bw; c=C[k]; op=O[k]
    yc=T+ph-ph*c/mx; yo=T+ph-ph*op/mx
    o.append(f'<rect x="{x+bw*.18:.1f}" y="{yc:.1f}" width="{bw*.64:.1f}" height="{T+ph-yc:.1f}" fill="#3a5f80"/>')
    o.append(f'<rect x="{x+bw*.18:.1f}" y="{yo:.1f}" width="{bw*.64:.1f}" height="{T+ph-yo:.1f}" fill="#f0b860"/>')
    o.append(f'<text x="{x+bw/2:.1f}" y="{T+ph+24}" text-anchor="middle" font-size="16" fill="#ece6d8">{k}</text>')
o.append(f'<text x="{L+pw/2}" y="{H-4}" text-anchor="middle" font-size="16" fill="#b8ab8e" letter-spacing="2">RING NUMBER</text>')
o.append(f'<rect x="{L}" y="8" width="16" height="16" fill="#f0b860"/><text x="{L+24}" y="22" font-size="17" fill="#ece6d8">optimistic: ${O[1]/1e3:.0f}k → ${O[ks[-1]]/1e3:.0f}k</text>')
o.append(f'<rect x="{L}" y="36" width="16" height="16" fill="#3a5f80"/><text x="{L+24}" y="50" font-size="17" fill="#ece6d8">conservative: ${C[1]/1e3:.0f}k → ${C[ks[-1]]/1e3:.0f}k</text>')
o.append('</svg>')
svg=''.join(o)
p=open('poster.html').read()
p=re.sub(r'<img src="img/cost.png"[^>]*>|<svg viewBox="0 0 [0-9]+ 290".*?</svg>',lambda m: svg,p,count=1,flags=re.S)
open('poster.html','w').write(p); print(ks)
