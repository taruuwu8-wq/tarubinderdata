import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
const dest=process.argv[2]||path.join(root,'Structured_Data/farming-2026-11-18.json');
const raw=path.join(root,'Raw/Snapshots/2026-11-18');
const base=JSON.parse(fs.readFileSync(path.join(root,'Raw/Snapshots/2026-11-16/build-data.json'),'utf8'));
const read=name=>{try{return JSON.parse(fs.readFileSync(path.join(raw,name+'.json'),'utf8'));}catch{return null;}};
const clean=s=>String(s||'').replace(/!\[[^\]]*\]\([^)]*\)/g,'').replace(/\*\*/g,'').replace(/\\([+.*])/g,'$1');
const plain=s=>clean(s).replace(/\[([^\]]*)\]\([^)]*\)/g,'$1').replace(/<br\s*\/?>/g,' · ').trim();
const num=s=>{const t=String(s??'').replaceAll(',','').trim();return /^\d+(\.\d+)?$/.test(t)?Number(t):null;};
const section=(md,title)=>md.split('## '+title)[1]?.split('\n## ')[0]?.trim()||'';
const seals={};
for(const line of section(clean(read('systems__soul-seal')?.markdown),'แต่ละแผนที่ต้องใช้พลังเท่าไร').split('\n')){
 const id=line.match(/\/map\/([a-z0-9_]+)/)?.[1];if(!id)continue;const cells=line.split('|').slice(1,-1).map(plain);
 seals[id]={normal:cells[2]==='ไม่ต้องใช้'?0:num(cells[2]),miniboss:num(cells[3]),frenziedElite:num(cells[4]),source:'https://wiki.bindertowngame.com/systems/soul-seal'};
}
function mobDetail(id){
 const recent=read('mob__'+id);let md=recent?.markdown,date=recent?'2026-11-18':null;
 if(!md){try{md=fs.readFileSync(path.join(root,'Raw/Snapshots/2026-11-16/mobs',id+'.md'),'utf8');date='2026-11-16';}catch{}}
 if(!md){try{md=fs.readFileSync(path.join(root,'Monsters',id+'.md'),'utf8');date=md.match(/Last crawled:\*\* (\d{4}-\d{2}-\d{2})/)?.[1]||null;}catch{}}
 const s=plain(md),summary=s.split('## อยู่ที่ไหน')[0];
 const rewards=summary.match(/EXP\s*([\d,.]+)\s*·\s*Job EXP\s*([\d,.]+)\s*·\s*Gold\s*([\d,.]+)(?:[–−-]([\d,.]+))?/);
 const hp=summary.match(/\bHP\s*([\d,.]+)/),lv=summary.match(/ที่ Lv\s*(\d+)/);
 const family=s.match(/ประเภท\s+([^·\n]+)/)?.[1]?.trim()||null;
 return {mobAggressive:/เห็นแล้ววิ่งเข้ามาตี/.test(summary)?true:/ไม่ตีก่อน|ไม่โจมตีก่อน/.test(summary)?false:null,source:'https://wiki.bindertowngame.com/mob/'+id,capturedAt:date,family,referenceLevel:num(lv?.[1]),hp:num(hp?.[1]),exp:num(rewards?.[1]),goldMin:num(rewards?.[3]),goldMax:num(rewards?.[4]||rewards?.[3]),def:num(s.match(/เกราะกายภาพ \(DEF\)[^\n]*?·\s*([\d,.]+)/)?.[1]),mdef:num(s.match(/ต้านเวท \(MDEF\)[^\n]*?·\s*([\d,.]+)/)?.[1]),card5:s.match(/\|\s*★5\s*\|([^\n]+)/)?.[1]?.replace(/\|/g,'').trim()||null};
}
const records=base.maps.map(m=>{
 const d=read('map__'+m.id),md=clean(d?.markdown),body=section(md,'มอนสเตอร์');
 const aggroSection=md.split('มอนตีก่อนไหม')[1]?.split('Elite / บอส')[0];
 const aggro=aggroSection===undefined?null:[...aggroSection.matchAll(/\/mob\/([a-z0-9_]+)/g)].map(x=>x[1]);
 const encounters=[...body.matchAll(/\[([^\]]*?)\]\(https:\/\/wiki\.bindertowngame\.com\/mob\/([a-z0-9_]+)\)/g)].map(x=>{
  const text=x[1],lev=text.match(/Lv\s*(\d+)(?:[–−-](\d+))?/),count=text.match(/·\s*([\d,.]+)\s*ตัว/),special=/Elite|[Bb]oss|บอส/.test(text);
  return{id:x[2],name:text.split(/\s*Lv/)[0].trim(),levelMin:num(lev?.[1]),levelMax:num(lev?.[2]||lev?.[1]),count:num(count?.[1]),special,role:text.split('ตัว')[1]?.trim()||null,aggressive:aggro===null||special?null:aggro.includes(x[2]),...mobDetail(x[2])};
 });
 for(const e of encounters){if(e.mobAggressive!==null)e.aggressive=e.mobAggressive;delete e.mobAggressive;}
 const normal=encounters.filter(e=>!e.special),complete=!!body&&encounters.length>0&&encounters.every(e=>e.count!==null);
 const sum=arr=>complete?arr.reduce((s,e)=>s+e.count,0):null;
 return {...m,source:'https://wiki.bindertowngame.com/map/'+m.id,capturedAt:d?'2026-11-18':null,status:d?(complete?'complete':'no_population_table'):'missing',encounters,normalCount:sum(normal),specialCount:sum(encounters.filter(e=>e.special)),levelMin:normal.length?Math.min(...normal.map(e=>e.levelMin)):null,levelMax:normal.length?Math.max(...normal.map(e=>e.levelMax)):null,seal:seals[m.id]||null,fullExpThrough:num(md.match(/ถึง\s*Lv\s*(\d+)/)?.[1]),gathering:plain(section(md,'Gathering')),respawnSeconds:null,spawnCoordinates:null};
});
const result={version:1,capturedAt:'2026-11-18',notes:['Population is the Wiki count, not kills/hour or density per unit area.','Monster rewards are base values at the reference level; not adjusted for build, night, seal or party.','Missing values are null; older monster details retain their dates.'],records};
fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,JSON.stringify(result));
console.log(JSON.stringify({maps:records.length,complete:records.filter(r=>r.status==='complete').length,missing:records.filter(r=>r.status==='missing').map(r=>r.id),noTable:records.filter(r=>r.status==='no_population_table').map(r=>r.id)}));
