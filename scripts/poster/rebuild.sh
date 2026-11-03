set -e
node shot.js 0.5 check.png | tr ']' '\n' | grep -i torus
node animbg.js >/dev/null; python3 animclips.py >/dev/null; python3 tiles.py
cd anim
ffmpeg -v error -y -i B.mp4 -i Bzoom.mp4 -filter_complex "[0:v]fps=15,trim=duration=4,setpts=PTS-STARTPTS[a];[1:v]fps=15,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1[o]" -map "[o]" -c:v libx264 -preset veryfast -crf 14 -pix_fmt yuv420p B8.tmp.mp4 && mv B8.tmp.mp4 B8.mp4
ffmpeg -v error -y -i D.mp4 -i DF.mp4 -filter_complex "[0:v]fps=15,trim=duration=4,setpts=PTS-STARTPTS[a];[1:v]fps=15,trim=duration=4,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1[o]" -map "[o]" -c:v libx264 -preset veryfast -crf 14 -pix_fmt yuv420p D8.tmp.mp4 && mv D8.tmp.mp4 D8.mp4
python3 gif.py 1920 15 ../soma-poster-animated.gif; python3 gif.py 3840 12 ../soma-poster-animated-3840.gif
cd ..
node export.js; rm -f soma-poster-60x36in-150dpi.zip; zip -q soma-poster-60x36in-150dpi.zip soma-poster-60x36in-150dpi.png
node xshot.js; python3 -c "
from PIL import Image; Image.open('x/native.png').convert('RGB').save('soma-poster-x.jpg',quality=97,subsampling=0,optimize=True)
im=Image.open('soma-poster-animated-3840.gif'); im.seek(60); im.convert('RGB').crop((40,1660,3000,2000)).resize((1480,170)).save('anim/stripg.png')"
