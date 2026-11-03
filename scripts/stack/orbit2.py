import numpy as np, json
from scipy.integrate import solve_ivp
exec(open('scan2.py').read().split("for dkm in")[0])
dkm=30000; x0=1-mu-dkm/LU; vy=0.4861
from scipy.optimize import brentq
vy=brentq(lambda v:half(v,x0),0.47,0.50,xtol=1e-13)
VU=LU/TU
yr=365.25*86400/TU
# one period CR3BP for clean loop
sol=solve_ivp(f,[0,20],[x0,0,0,vy],args=(None,),rtol=1e-11,atol=1e-12,dense_output=True)
# baseline 20 years with Sun
Y=20*yr
base=solve_ivp(f,[0,Y],[x0,0,0,vy],args=(0.0,),rtol=1e-10,atol=1e-11,max_step=0.05,dense_output=True)
# kicked: 2 m/s random kicks when rings are added
rng=np.random.default_rng(7); adds=[2,5,8,11,14,17]
s=[x0,0,0,vy]; t0=0; segs=[]
for a in adds+[20]:
    seg=solve_ivp(f,[t0,a*yr],s,args=(0.0,),rtol=1e-10,atol=1e-11,max_step=0.05,dense_output=True); segs.append(seg)
    s=seg.y[:,-1].copy(); t0=a*yr
    if a<20:
        ang=rng.uniform(0,2*np.pi); s[2]+=0.002/1.0245*np.cos(ang)*1; s[3]+=0.002/1.0245*np.sin(ang)
def sample(seg,t): return seg.sol(t)[:2]
tt=np.linspace(0,Y,24000)
B=base.sol(tt)[:2]
K=np.hstack([sg.sol(tt[(tt>=sg.t[0])&(tt<=sg.t[-1])])[:2] for sg in segs])[:, :len(tt)]
dmB=np.hypot(B[0]-(1-mu),B[1])*LU; dmK=np.hypot(K[0]-(1-mu),K[1])*LU
print('base',dmB.min(),dmB.max(),' kicked',dmK.min(),dmK.max(), 'period d', 'speed rel moon km/s', vy*VU)
# 2 months detailed (rotating frame & time) with Sun
t2=np.linspace(0,60*86400/TU,1800); P2=base.sol(t2)[:2]
json.dump(dict(mu=mu,LU=LU,TU=TU,ws=ws,yr=yr,
  t2=list(map(float,t2)),p2=P2.T.tolist(),
  tt=list(map(float,tt[::6])),B=B[:,::6].T.tolist(),K=K[:,::6].T.tolist(),adds=adds),open('orbit.json','w'))
