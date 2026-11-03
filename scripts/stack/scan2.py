import numpy as np, sys
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
mu=0.01215058; LU=384400.0; TU=375190.0
ms=328900.54; as_=388.81114; ws=0.92519598
def f(t,s,ph):
    x,y,vx,vy=s
    r1=np.hypot(x+mu,y); r2=np.hypot(x-1+mu,y)
    ax=2*vy+x-(1-mu)*(x+mu)/r1**3-mu*(x-1+mu)/r2**3
    ay=-2*vx+y-(1-mu)*y/r1**3-mu*y/r2**3
    if ph is not None:
        th=ph-ws*t; xs,ys=as_*np.cos(th),as_*np.sin(th); dx,dy=x-xs,y-ys; rs=np.hypot(dx,dy)
        ax+=-ms*dx/rs**3-ms*xs/as_**3; ay+=-ms*dy/rs**3-ms*ys/as_**3
    return [vx,vy,ax,ay]
def half(vy,x0):
    ev=lambda t,s,ph: s[1]; ev.terminal=True; ev.direction=-1
    sol=solve_ivp(f,[1e-6,10],[x0,0,0,vy],args=(None,),events=ev,rtol=1e-11,atol=1e-12)
    if len(sol.t_events[0])==0: return np.nan
    return sol.y_events[0][0][2]
for dkm in (25000,30000,35000):
    x0=1-mu-dkm/LU; vs=np.linspace(0.3,0.7,41); fv=[half(v,x0) for v in vs]
    vy=None
    for i in range(40):
        if np.isfinite(fv[i]) and np.isfinite(fv[i+1]) and fv[i]<0<fv[i+1] and abs(fv[i])<.5: vy=brentq(lambda v:half(v,x0),vs[i],vs[i+1],xtol=1e-13);break
    out=[]
    for ph in (0,np.pi/2,np.pi,3*np.pi/2):
        Y=20*365.25*86400/TU
        esc=lambda t,s,ph: np.hypot(s[0]-(1-mu),s[1])-0.6; esc.terminal=True
        sl=solve_ivp(f,[0,Y],[x0,0,0,vy],args=(ph,),rtol=1e-10,atol=1e-11,max_step=0.05,events=esc)
        dm=np.hypot(sl.y[0]-(1-mu),sl.y[1])*LU
        out.append(f"{sl.t[-1]*TU/86400/365.25:.0f}y {dm.min()/1e3:.0f}-{dm.max()/1e3:.0f}k")
    print(dkm, round(vy,4), out, flush=True)
