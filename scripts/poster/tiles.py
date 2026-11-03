import json, subprocess, os, sys, shutil
d=json.load(open('anim/rects.json')); K=d['K']; P=json.load(open('anim/plan.json'))
P.pop('DF',None); P={k:v for k,v in P.items() if k in d['R']}
X264=['-c:v','libx264','-preset','veryfast','-crf','14','-pix_fmt','yuv420p']
def enc(inp,vf,out,extra=X264):
    ext=os.path.splitext(out)[1]; subprocess.run(['ffmpeg','-v','error','-y','-framerate','15','-i',inp,'-vf',vf]+extra+[out+'.tmp'+ext],check=True); os.replace(out+'.tmp'+ext,out)
def rect(k): r=d['R'][k]; return r,round(r['width']*K/2)*2,round(r['height']*K/2)*2
r,W,H=rect('C'); enc('anim/lf/f%d.png',f'scale={W}:-2:flags=lanczos,crop={W}:{H}','anim/C.mp4'); P['C']=dict(x=round(r['x']*K),y=round(r['y']*K),w=W,h=H,dur=4)
for key,script,fd in (('GS','spoketele.py','sf'),('GP','podsanim.py','pf'),('F','trainanim.py','tf')):
    r,W,H=rect(key); shutil.rmtree(f'anim/{fd}',ignore_errors=True); subprocess.run([sys.executable,script,'anim',str(W*2)],check=True)
    enc(f'anim/{fd}/f%03d.png',f'scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}',f'anim/{key}.mp4'); P[key]=dict(x=round(r['x']*K),y=round(r['y']*K),w=W,h=H,dur=8)
r,W,H=rect('E'); P['E']=dict(x=round(r['x']*K),y=round(r['y']*K),w=W,h=H,dur=8)
json.dump(P,open('anim/plan.json','w')); print(sorted(P))
