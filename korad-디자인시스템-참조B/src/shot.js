const {chromium}=require('playwright');
const path=require('path');
(async()=>{
  const ids=process.argv.slice(2);
  const b=await chromium.launch({args:['--allow-file-access-from-files']});
  const pg=await b.newPage({viewport:{width:960,height:900},deviceScaleFactor:2});
  for(const id of ids){
    await pg.goto('file://'+path.resolve('render/'+id+'.html'));
    await pg.waitForTimeout(500);
    const h=await pg.evaluate(()=>document.body.firstElementChild.offsetHeight);
    await pg.setViewportSize({width:960,height:h});
    await pg.screenshot({path:`render/${id}.png`,clip:{x:0,y:0,width:960,height:Math.min(h,540)}});
    const bad=await pg.evaluate(()=>{const o=[];document.querySelectorAll('.ko-slide *').forEach(e=>{if(e.closest('.gd'))return;const r=e.getBoundingClientRect();const p=e.parentElement.getBoundingClientRect();if(e.parentElement.classList.contains('ko-slide'))return;const cs=getComputedStyle(e);if(e.scrollHeight>e.clientHeight+1&&e.clientHeight>0&&cs.overflow!=='visible')o.push(e.className+' '+e.scrollHeight+'>'+e.clientHeight)});
      // text overflow vs parent box for ko-b-* containers
      document.querySelectorAll('.ko-b-tt td, .ko-b-rp .bd, .ko-b-nr .tx, .ko-b-ob, .ko-b-def, .ko-b-ph .h, .ko-b-rc > div').forEach(e=>{if(e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1)o.push('OVF '+e.className+' '+e.scrollWidth+'x'+e.scrollHeight+' > '+e.clientWidth+'x'+e.clientHeight+' "'+e.textContent.slice(0,20)+'"')});return o});
    console.log(id,JSON.stringify(bad));
  }
  // measure header title widths
  await pg.goto('file://'+path.resolve('render/L49.html'));
  const w=await pg.evaluate(()=>{const t=document.querySelector('.ko-header-title');return [t.textContent,t.getBoundingClientRect().width]});
  console.log('title',w);
  await b.close();
})();
