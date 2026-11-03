const { chromium } = require('playwright');
(async () => {
  const K=3840/3600;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 3600, height: 2160 }, deviceScaleFactor: K });
  await p.goto('file://'+__dirname+'/poster.html'); await p.waitForTimeout(2000); await p.addStyleTag({content:'.watermark{display:none!important}'});
  const sel={E:'img.fx',C:'img[src="img/lunarind.png"]',B:'img[src="img/orbitview.png"]',D:'img[src="img/onering.png"]',F:'img[src="img/f_train.png"]',
    G1:'img[src="img/f1_spine.png"]',G2:'img[src="img/f2_setup.png"]',G3:'img[src="img/f_panels.png"]',G4:'img[src="img/f3_build.png"]',
    G5:'img[src="img/f_halftorus.png"]',GS:'img[src="img/f_spokes.png"]',GP:'img[src="img/f_pods.png"]',G6:'img[src="img/f5_solar.png"]',G7:'img[src="img/drums.png"]'};
  const R={};
  for (const [k,s] of Object.entries(sel)) { const e=await p.$(s); const r=await e.boundingBox(); R[k]=r;
    if (k!=='D') await e.evaluate(el=>{el.style.visibility='hidden'}); }
  await p.screenshot({path:'anim/bg.png'});
  require('fs').writeFileSync('anim/rects.json',JSON.stringify({K,R}));
  console.log(JSON.stringify(R)); await b.close();
})();
