// usage: node extract.js <htmlfile> <mode slide|dc> <out.json> [sectionWidthPx]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [file,mode,out,secW]=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:2000,height:1400}});
let src=fs.readFileSync(file,'utf8');
let html;
if(mode==='slide'){src=src.replace(/<aside>[\s\S]*?<\/aside>/,'');
 html='<html><head><meta charset="utf-8"><style>body{margin:0}p,ul,h1,h2,h3{margin:0}ul{padding-left:1.1em}x-icon{display:none}section{width:'+secW+'px !important;box-sizing:border-box;height:auto !important}</style></head><body>'+src+'</body></html>';}
else{const m=src.match(/<x-dc>([\s\S]*?)<\/x-dc>/)[1].replace(/<helmet>[\s\S]*?<\/helmet>/,'');
 html='<html><head><meta charset="utf-8"><style>body{margin:0}p{margin:0}</style></head><body><div id="root">'+m+'</div></body></html>';}
await p.setContent(html);await p.waitForTimeout(300);
const items=await p.evaluate((mode)=>{
 const root=mode==='slide'?document.querySelector('section'):document.querySelector('#root>div');
 const R0=root.getBoundingClientRect();const out=[];
 const rgb=s=>{const m=s&&s.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/);if(!m)return null;if(m[4]!==undefined&&+m[4]<0.05)return null;return [m[1],m[2],m[3]].map(v=>(+v|0).toString(16).padStart(2,'0')).join('').toUpperCase()};
 const rel=r=>({x:r.left-R0.left,y:r.top-R0.top,w:r.width,h:r.height});
 const isBlock=e=>{const d=getComputedStyle(e).display;return !(d==='inline'||d==='contents')};
 root.querySelectorAll('*').forEach(e=>{
  if(e.closest('svg')&&e.tagName.toLowerCase()!=='svg'){return}
  const cs=getComputedStyle(e);const r=e.getBoundingClientRect();if(r.width<0.5||r.height<0.5)return;
  if(e.tagName.toLowerCase()==='svg'){const vb=e.viewBox.baseVal;const sx=r.width/(vb&&vb.width||r.width),sy=r.height/(vb&&vb.height||r.height);
    e.querySelectorAll('polygon').forEach(pg=>{const c=rgb(getComputedStyle(pg).fill);if(!c)return;const pts=pg.getAttribute('points').trim().split(/\s+/).map(t=>t.split(',').map(Number)).map(([a,b2])=>[a*sx,b2*sy]);
     out.push({k:'poly',...rel(r),pts,fill:c});});return}
  // background
  let fill=rgb(cs.backgroundColor);const bi=cs.backgroundImage;let hl=null;
  if(bi&&bi!=='none'){const cols=[...bi.matchAll(/rgba?\([^)]*\)/g)].map(m=>m[0]);
    const m=bi.match(/linear-gradient\((?:180deg,\s*)?rgba\([^)]*,\s*0\)\s*([\d.]+)%,\s*(rgb\([^)]*\))/);
    if(m){hl={p:+m[1],c:rgb(m[2])}} else {const c=cols.map(rgb).filter(Boolean);if(c.length&&!fill)fill=bi.startsWith('repeating')?c[c.length-1]:c[0];}}
  const disp=cs.display;
  if(hl){if(disp==='inline'){for(const cr of e.getClientRects()){const q=rel(cr);out.push({k:'rect',x:q.x,y:q.y+q.h*hl.p/100,w:q.w,h:q.h*(1-hl.p/100),fill:hl.c})}}
   else{const q=rel(r);const tw=Math.min(q.w,(()=>{const rg=document.createRange();rg.selectNodeContents(e);return rg.getBoundingClientRect().width})());out.push({k:'rect',x:q.x,y:q.y+q.h*hl.p/100,w:tw,h:q.h*(1-hl.p/100),fill:hl.c})}}
  const bw=['Top','Right','Bottom','Left'].map(s=>parseFloat(cs['border'+s+'Width'])||0);const bc=['Top','Right','Bottom','Left'].map(s=>rgb(cs['border'+s+'Color']));
  const uni=bw.every(v=>v===bw[0])&&bc.every(v=>v===bc[0])&&bw[0]>0&&bc[0]&&cs.borderTopStyle!=='none';
  if((fill&&disp!=='inline')||uni){const q=rel(r);out.push({k:'rect',...q,fill:disp!=='inline'?fill:null,line:uni?bc[0]:null,lw:uni?bw[0]:0})}
  else if(fill&&disp==='inline'){for(const cr of e.getClientRects()){out.push({k:'rect',...rel(cr),fill})}}
  if(!uni){const q=rel(r);[[0,q.x,q.y,q.w,bw[0]],[1,q.x+q.w-bw[1],q.y,bw[1],q.h],[2,q.x,q.y+q.h-bw[2],q.w,bw[2]],[3,q.x,q.y,bw[3],q.h]].forEach(([i,x,y,w,h])=>{if(bw[i]>0&&bc[i]&&cs['border'+['Top','Right','Bottom','Left'][i]+'Style']!=='none')out.push({k:'rect',x,y,w,h,fill:bc[i]})})}
  // text
  if(disp==='inline')return;
  const hasDirect=[...e.childNodes].some(n=>(n.nodeType===3&&n.textContent.trim())||(n.nodeType===1&&!isBlock(n)&&n.textContent.trim()));
  if(!hasDirect)return;
  const pre=/pre/.test(cs.whiteSpace);
  const paras=[[]];
  const walk=(n,st)=>{for(const c of n.childNodes){if(c.nodeType===3){let t=c.textContent;if(!pre)t=t.replace(/\s+/g,' ');const parts=t.split('\n');parts.forEach((pt,i)=>{if(i>0)paras.push([]);if(pt)paras[paras.length-1].push({t:pt,...st})})}
   else if(c.nodeType===1){const tg=c.tagName.toLowerCase();if(tg==='br'){paras.push([]);continue}if(isBlock(c)&&getComputedStyle(c).display!=='inline-flex'&&getComputedStyle(c).display!=='inline-block')continue;const s2=getComputedStyle(c);walk(c,{sz:parseFloat(s2.fontSize),b:(+s2.fontWeight>=600)||/Bold/.test(s2.fontFamily),c:rgb(s2.color),ls:parseFloat(s2.letterSpacing)||0})}}};
  walk(e,{sz:parseFloat(cs.fontSize),b:(+cs.fontWeight>=600)||/Bold/.test(cs.fontFamily),c:rgb(cs.color),ls:parseFloat(cs.letterSpacing)||0});
  // trim
  paras.forEach(pa=>{if(pa.length){pa[0].t=pa[0].t.replace(/^ +/,'');pa[pa.length-1].t=pa[pa.length-1].t.replace(/ +$/,'')}});
  while(paras.length&&!paras[paras.length-1].some(x=>x.t))paras.pop();
  if(!paras.length)return;
  if(e.tagName.toLowerCase()==='li'&&paras[0].length)paras[0].unshift({...paras[0][0],t:'• '});
  const pl=parseFloat(cs.paddingLeft),pr=parseFloat(cs.paddingRight),pt=parseFloat(cs.paddingTop),pb=parseFloat(cs.paddingBottom);
  const q=rel(r);let x=q.x+pl+bw[3],w=q.w-pl-pr-bw[1]-bw[3],y=q.y+pt+bw[0],h=q.h-pt-pb-bw[0]-bw[2];
  if(e.tagName.toLowerCase()==='li'){const ind=parseFloat(getComputedStyle(e.parentElement).paddingLeft)||0;x-=ind*0.9;w+=ind*0.9}
  const fs=parseFloat(cs.fontSize);const lh=cs.lineHeight==='normal'?1.2:parseFloat(cs.lineHeight)/fs;
  let al=cs.textAlign;if(disp==='flex'&&cs.justifyContent==='center'&&cs.flexDirection!=='column')al='center';if(disp==='flex'&&cs.justifyContent==='flex-end')al='right';
  const anchor=(disp==='flex'&&cs.alignItems==='center'&&cs.flexDirection!=='column')||(disp==='flex'&&cs.flexDirection==='column'&&cs.justifyContent==='center')?'ctr':'t';
  out.push({k:'text',x,y,w,h,paras,al,lh,anchor});
 });
 return {items:out,W:R0.width,H:R0.height};
},mode);
fs.writeFileSync(out,JSON.stringify(items));await (await p.$(mode==='slide'?'section':'#root>div')).screenshot({path:out.replace('.json','.png'),scale:'css'});console.log(out,items.items.length,'items',Math.round(items.W),'x',Math.round(items.H));await b.close()})();
