import json, subprocess
F='/tmp/claude-0/-home-claude/2aa3f404-8de0-56e4-b320-595de06df08e/scratchpad/film/soma-construction-film.mp4'
d=json.load(open('anim/rects.json')); K=d['K']; R=d['R']
R['D']=dict(R['D'],height=448); R['DF']=R['D']
# key: (start, end, region x0,y0,x1,y1 in 1280x720 film frame)
C={'B':(314.0,326.4,(0,75,1280,595)),'D':(251.0,255.0,(0,75,1280,595)),'DF':(273.0,277.0,(0,75,1280,595)),
   'G1':(9.0,13.0,(0,75,1280,595)),'G2':(100.0,104.0,(0,75,1280,595)),'G3':(155.0,171.4,(300,70,980,500)),
   'G4':(113.0,117.0,(0,75,1280,595)),'G5':(125.0,129.0,(40,90,700,502)),'GS':(215.0,223.8,(276,70,1004,590)),
   'G6':(240.0,244.0,(0,75,1280,595)),'G7':(55.0,59.0,(0,75,1280,595))}
SPEED={'B':3.1,'G3':2.05,'GS':1.1}
plan={}
for k,(a,b,(x0,y0,x1,y1)) in C.items():
    r=R[k]; W=round(r['width']*K/2)*2; H=round(r['height']*K/2)*2
    rw,rh=x1-x0,y1-y0; ta=W/H
    if rw/rh>ta: cw=rh*ta; cx=x0+(rw-cw)/2; cy=y0; ch=rh
    else: ch=rw/ta; cy=y0+(rh-ch)/2; cx=x0; cw=rw
    out=f'anim/{k}.mp4'
    sp=f'setpts=PTS/{SPEED[k]},' if k in SPEED else ''
    vf=sp+f'crop={cw:.0f}:{ch:.0f}:{cx:.0f}:{cy:.0f},scale={W}:{H}:flags=lanczos,setsar=1,fps=30,format=yuv420p'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-t',str(b-a),'-i',F,'-vf',vf,'-an','-c:v','libx264','-preset','veryfast','-crf','16',out+'.tmp.mp4'],check=True)
    import os; os.replace(out+'.tmp.mp4',out)
    plan[k]=dict(x=round(r['x']*K),y=round(r['y']*K),w=W,h=H,dur=(b-a)/SPEED.get(k,1)); print(k,plan[k])
json.dump(plan,open('anim/plan.json','w'))
