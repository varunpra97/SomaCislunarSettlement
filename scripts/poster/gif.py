import json, subprocess, os, sys
P=json.load(open('plan.json')); ks=list(P); T=8
def build(W,fps,out):
    k=W/3840
    args=['ffmpeg','-v','error','-y','-loop','1','-framerate',str(fps),'-i','bg.png']
    FILE={'B':'B8.mp4','D':'D8.mp4','E':'E.mov'}
    for key in ks: args+=['-stream_loop','-1','-i',FILE.get(key,f'{key}.mp4')]
    f=[f'[0:v]trim=duration={T},scale={W}:-2:flags=lanczos[b0]']; prev='b0'
    for i,key in enumerate(ks,1):
        p=P[key]; w=round(p['w']*k); h=round(p['h']*k)
        f.append(f'[{i}:v]fps={fps},trim=duration={T},setpts=PTS-STARTPTS,scale={w}:{h}:flags=lanczos[c{i}]')
        f.append(f'[{prev}][c{i}]overlay={round(p["x"]*k)}:{round(p["y"]*k)}:eof_action=repeat[b{i}]'); prev=f'b{i}'
    n=len(ks)+1; args[args.index('-filter_complex') if '-filter_complex' in args else len(args):len(args)]=[]
    args+=['-loop','1','-framerate',str(fps),'-i','wm.png']
    f.append(f'[{n}:v]scale={W}:-2:flags=lanczos,format=rgba[wm]'); f.append(f'[{prev}][wm]overlay=0:0:shortest=1[wmo]'); prev='wmo'
    f.append(f'[{prev}]split[x][y];[x]palettegen=max_colors=256:stats_mode=diff[pal];[y][pal]paletteuse=dither=none:diff_mode=rectangle')
    args+=['-filter_complex',';'.join(f),'-t',str(T),'-loop','0','tmp.gif']
    subprocess.run(args,check=True); os.replace('tmp.gif',out); print(out,os.path.getsize(out))
import sys
if len(sys.argv)>1: build(int(sys.argv[1]),int(sys.argv[2]),sys.argv[3])
else: build(1920,15,'../soma-poster-animated.gif'); build(3840,15,'../soma-poster-animated-3840.gif')
