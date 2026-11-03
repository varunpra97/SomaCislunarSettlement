import sys
sys.path.insert(0,'../stack'); sys.path.insert(0,'../video')
import vid
def install(floor):
    orig=vid.text
    def text(ctx,s,x,y,size,*a,**k): return orig(ctx,s,x,y,max(size,floor),*a,**k)
    vid.text=text
