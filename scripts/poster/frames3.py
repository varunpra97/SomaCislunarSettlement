"""Strip frames with every in-picture label removed (captions on the poster carry the words)."""
import sys, cairo
sys.path.insert(0,'../stack'); sys.path.insert(0,'../video')
import vid
noop=lambda *a,**k: None
vid.text=noop
import common, hubspine, solarrad
from PIL import Image
NAMES=('text','caption','head','header','hdr','tag','label','label_pill','readout','card')
for m in (vid, common, hubspine, solarrad):
    for n in NAMES:
        if hasattr(m,n): setattr(m,n,noop)
def shot(name, fn, t, dur, S=4, crop=(0,75,1280,595)):
    surf=cairo.ImageSurface(cairo.FORMAT_ARGB32,1280*S,720*S); ctx=cairo.Context(surf); ctx.scale(S,S); fn(ctx,t,dur)
    surf.write_to_png('img/tmp.png'); x0,y0,x1,y1=crop
    Image.open('img/tmp.png').crop((x0*S,y0*S,x1*S,y1*S)).save(f'img/{name}.png'); print(name)
D={n:d for n,_,d in vid.SCENES}
shot('f1_spine', hubspine.c1, 11.0, 12)
shot('f2_setup', vid.scene4, 0.9*D['s4'], D['s4'])
shot('f3_build', vid.scene5, 0.55*D['s5'], D['s5'])
shot('f5_solar', solarrad.b1, 9.5, 12)
shot('drums', hubspine.c4b, 10.0, 10.5)
import spokes
for n in NAMES:
    if hasattr(spokes,n): setattr(spokes,n,noop)
shot('f_spokes', spokes.a3, 8.6, 10, crop=(276,70,1004,590))
