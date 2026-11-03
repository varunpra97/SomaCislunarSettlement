const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 3600, height: 2160 }, deviceScaleFactor: 2.5 });
  await p.goto('file://'+process.cwd()+'/poster.html'); await p.waitForTimeout(3000);
  await p.screenshot({ path: 'soma-poster-60x36in-150dpi.png' });
  await p.pdf({ path: 'soma-poster-60x36in.pdf', width: '60in', height: '36in', printBackground: true, scale: 1.6, pageRanges: '1' });
  await b.close();
})();
