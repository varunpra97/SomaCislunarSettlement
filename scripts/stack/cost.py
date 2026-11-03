import math, json
# kit = Earth high-tech kit excluding 'own' (the report's $30B/$60B kit includes it)
POP=550_000; HOMES=220_000; S=6
cases={
 'opt': dict(lunar_prog=500, kit=27, n2=30, power=9, robots=5, design=10, lr=0.80, own=3, head=6, seg=0.5, mid=1.5),
 'cons':dict(lunar_prog=1900, kit=51, n2=200, power=42, robots=15, design=20, lr=0.90, own=9, head=15, seg=1.5, mid=5),
}
# 'own' = what a standalone ring pair needs per ring: its own port/docks, gas reserve store, control centre, pointing propulsion, ring-to-ring shuttles.
# On a spine these move into a shared spine head (once per stack) plus a short spine segment per ring.
def ring(k,c,mode):
    f=k**math.log2(c['lr'])
    x=dict(lunar=c['lunar_prog']/100, n2=c['n2'])
    if mode=='flat':
        x.update(kit=c['kit'],power=c['power'],robots=c['robots'],design=c['design'],own=c['own'])
    else:
        x.update(kit=c['kit']*f,power=c['power']*f,robots=c['robots']*(1 if k==1 else .3),design=c['design']*(1 if k==1 else .25))
        if mode=='learn': x['own']=c['own']*f
        if mode=='spine': x['spine']=(c['head'] if (k-1)%S==0 else 0)+c['seg']
    return sum(x.values())
out={}
for name,c in cases.items():
    rows=[];cum=0
    for k in range(1,101):
        fl,le,sp=(ring(k,c,m) for m in ('flat','learn','spine'))
        cum+=sp-c['lunar_prog']/100
        rows.append(dict(k=k,flat=fl,learn=le,spine=sp,pp_flat=fl*1e9/POP,pp_learn=le*1e9/POP,pp_spine=sp*1e9/POP,
                         home=sp*1e9*.6*1.4/HOMES, avgN=(c['lunar_prog']+cum)*1e9/k/POP))
    out[name]=rows
    T=lambda key:sum(r[key] for r in rows)
    print(name, f"100-ring totals: flat {T('flat')/1e3:.2f}T  learning {T('learn')/1e3:.2f}T  learning+spine {T('spine')/1e3:.2f}T  mid ring adds {sum(c['mid']*k**math.log2(c['lr']) for k in range(1,101))/1e3:.2f}T")
    for r in rows:
        if r['k'] in (1,2,3,6,7,12,13,25,50,100):
            print(f"  {r['k']:3d} flat {r['flat']:6.1f} learn {r['learn']:6.1f} spine {r['spine']:6.1f} | pp {r['pp_spine']/1e3:5.0f}k home {r['home']/1e6:.2f}M | avgN {r['avgN']/1e3:,.0f}k")
json.dump(out,open('cost.json','w'))
