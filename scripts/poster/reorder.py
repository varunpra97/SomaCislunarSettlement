import re, sys
p='poster.html'; s=open(p).read(); order=sys.argv[1].split(',')
pat=r'<div class="step"><img src="img/([a-z0-9_]+)\.png".*?</div>'
ms=list(re.finditer(pat,s)); blocks={m.group(1):m.group(0) for m in ms}
assert set(order)==set(blocks), set(blocks)
a=ms[0].start(); b=ms[-1].end()
s=s[:a]+'\n    '.join(re.sub(r'<b>\d</b>',f'<b>{i}</b>',blocks[k],count=1) for i,k in enumerate(order,1))+s[b:]
open(p,'w').write(s); print(re.findall(r'<b>(\d)</b>([^<]+)</h3>',s))
