import {readFile,writeFile} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const base=new URL('../../',import.meta.url),site=new URL('../',import.meta.url);
const read=async p=>JSON.parse(await readFile(new URL(p,base),'utf8'));
const registry=JSON.parse(await readFile(new URL('dist/repo-items.json',site),'utf8'));
registry.ref=execFileSync('git',['rev-parse','HEAD'],{cwd:fileURLToPath(base),encoding:'utf8'}).trim();
const all=(await read('Structured_Data/equipment.json')).records.concat((await read('Structured_Data/weapons.json')).records);
const affix=(await read('Structured_Data/affixes.json')).records[0],norm=s=>String(s).replace(/^of /i,'').trim().toLowerCase();
const number=s=>{const m=String(s).replaceAll(',','').match(/[+-]?\d+(?:\.\d+)?/);return m?Number(m[0]):null;};
registry.affixLastCrawled=affix.last_crawled;
registry.affixRules=affix.tables.filter(t=>t.header[0]==='Tier').flatMap(t=>t.rows.map(row=>({name:row[1],norm:norm(row[1]),tier:row[0],min:number(row[3]),max:number(row[4]),minText:row[3],maxText:row[4],section:t.section})));
const metrics={ATK:'atk',MATK:'matk',DEF:'def',STR:'str',AGI:'agi',VIT:'vit',INT:'int',DEX:'dex',LUK:'luk',HIT:'hit',FLEE:'flee',HP:'hp',MP:'mp','คริ':'crit','คริติคอล':'crit','สปีดตี':'attackSpeed','สปีดวิ่ง':'speed','ร่ายไว':'castSpeed','Crit DMG':'critDamage','Skill CDR':'cdr','HP regen/s':'hpRegen','MP regen/s':'mpRegen'};
registry.items={};
const missing=[];let unsupported=0;
for(const r of all.filter(r=>r.data_source==='detail_page'&&r.tier==='ขั้น 10')){
 const markdown=await readFile(new URL(r.kb_file,base),'utf8');
 const statRows=r.tables.find(t=>t.section==='ค่าพลังของชิ้นนี้')?.rows,table=r.tables.find(t=>t.header[0]==='ตีไปขั้น');
 if(!statRows||!table){missing.push(r.slug);continue;}
 const baseStats=[],referenceStats=[];
 for(const [key,value] of statRows){
  if(['ATK','MATK','DEF'].includes(key)&&number(value)!==null){baseStats.push({key:metrics[key],value:number(value),kind:'flat'});continue;}
  if(!['สเตตัส','โบนัส'].includes(key))continue;
  for(const part of value.split(' · ')){
   const m=part.replace(/Max /g,'').match(/^([+-]?\d+(?:\.\d+)?)\s*(%)?\s*(.+)$/u),key=m&&metrics[m[3]];
   if(!m||!key){referenceStats.push(part);unsupported++;continue;}
   baseStats.push({key:key+(m[2]&&['atk','matk','hp','mp'].includes(key)?'Pct':''),value:Number(m[1]),kind:m[2]?'percent':'flat'});
  }
 }
 const columns=table.header.map((h,i)=>({h,i})).filter(x=>/ATK|MATK|^DEF$/.test(x.h));
 if(!columns.length){missing.push(r.slug);continue;}
 const {h,i}=columns[0],refineKeys=columns.length>1?columns.map(x=>metrics[x.h]):/ATK.*MATK/.test(h)?['atkPct','matkPct']:[metrics[h]];
 if(!refineKeys[0]){missing.push(r.slug);continue;}
 const refine=Object.fromEntries(table.rows.map(row=>[number(row[0]),columns.length>1?Object.fromEntries(columns.map(c=>[metrics[c.h],number(row[c.i])])):number(row[i])]));
 const allowedAffixes=[];
 for(const match of markdown.matchAll(/\[([^\]]+)\]\([^)]*Affixes\/affix\.md#([^)]*)\)/g)){
  const rule=registry.affixRules.find(a=>a.norm===norm(match[1]));if(!rule)throw Error('Missing global rule '+match[1]);
  for(const a of registry.affixRules.filter(x=>x.section===rule.section))if(!allowedAffixes.some(x=>x.norm===a.norm))allowedAffixes.push({...a,anchor:match[2],kind:match[2].startsWith('p_')?'trigger':'passive',family:rule.section});
 }
 registry.items[r.slug]={slug:r.slug,path:r.kb_file,name:r.name,sourceUrl:`https://github.com/${registry.repo}/blob/${registry.ref}/${r.kb_file}`,baseStats,referenceStats,refine,refineKeys,allowedAffixes,lastCrawled:r.last_crawled,slot:r.properties.slot,level:Number(r.level),requirements:r.requirements,compatibleRogue:r.requirements.some(s=>/ทุกอาชีพ|Rogue/.test(s)),freshnessStatus:r.freshness_status||'capture_'+r.last_crawled};
}
registry.catalogPolicy='Tier 10 details only; slots and class requirements from source; unknown effects remain reference text.';
await writeFile(new URL('dist/repo-items.json',site),JSON.stringify(registry,null,2)+'\n');
const eligible=Object.values(registry.items).filter(r=>r.compatibleRogue);console.log(JSON.stringify({items:Object.keys(registry.items).length,eligibleRogue:eligible.length,unsupportedStats:unsupported,skipped:missing,anchors:[...new Set(eligible.flatMap(r=>r.allowedAffixes.map(a=>a.anchor)))].sort()}));

const {hydrateRegistry,reconcileProfile}=await import('../dist/repo-policy.js');
const {execFileSync:runNode}=await import('node:child_process');
runNode(process.execPath,['compact-registry.mjs'],{cwd:fileURLToPath(site),stdio:'inherit'});
const compact=JSON.parse(await readFile(new URL('dist/repo-items.json',site),'utf8'));hydrateRegistry(compact);
const data=JSON.parse(await readFile(new URL('dist/data.json',site),'utf8')),freshness=await read('Sources/DATA_FRESHNESS.json');
const cardRecords=(await read('Structured_Data/cards.json')).records,catalog=(await read('My_Cards/tracker/catalog_doc.json')).items;
data.catalog=catalog.map(c=>({...c,lastCrawled:cardRecords.find(r=>r.slug===c.s)?.last_crawled||null}));
data.baseline=reconcileProfile(data.baseline,compact);data.repoCommit=registry.ref;
data.sources.commit='https://github.com/'+registry.repo+'/tree/'+registry.ref;
data.sources.gaps='https://github.com/'+registry.repo+'/blob/'+registry.ref+'/MISSING_DATA.md';
data.sources.queue='https://github.com/'+registry.repo+'/blob/'+registry.ref+'/Sources/REFRESH_QUEUE.csv';
data.repoCrawled='ข้อมูลหลายวัน · รายละเอียดล่าสุด '+freshness.latest_capture_date;
data.coverage={...data.coverage,freshPages:freshness.fresh_pages,olderDetails:freshness.older_detail_pages,notFetched:freshness.not_fetched_pages,conflicts:freshness.listing_detail_conflicts.length,latestCapture:freshness.latest_capture_date,liveCapturePages:freshness.live_capture_pages,liveCredits:freshness.live_capture_credits};
await writeFile(new URL('dist/data.json',site),JSON.stringify(data,null,2)+'\n');
await writeFile(new URL('dist/data-freshness.json',site),JSON.stringify({...data.coverage,missingByCategory:freshness.missing_by_category,listingDetailConflicts:freshness.listing_detail_conflicts},null,2)+'\n');
console.log('Synced existing KB data without network calls; player inventory and user builds are preserved.');
