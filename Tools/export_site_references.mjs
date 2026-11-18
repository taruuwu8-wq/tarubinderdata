import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'..');
const dir=path.join(root,'Raw/Snapshots/2026-11-18');
const dest=process.argv[2];
if(!dest)throw Error('Pass destination JSON');
const records=[];
for(const file of fs.readdirSync(dir).sort()){
 if(!/^(skill__|mob__|systems__|pet__|item__|guide__|build\.|dmg\.)/.test(file))continue;
 const d=JSON.parse(fs.readFileSync(path.join(dir,file),'utf8'));
 if(!d.markdown)continue;
 const url=d.requestedURL||d.metadata?.sourceURL;
 if(!url)continue;
 const parts=new URL(url).pathname.split('/').filter(Boolean),id=parts.at(-1);
 const category=parts[0]==='mob'?'mobs':parts[0]==='skill'?'skills':parts[0]==='pet'?'pets':parts[0]==='item'?'items':'systems';
 records.push({id,name:id.replaceAll('_',' ').replaceAll('-',' '),category,source:url,capturedAt:d.capturedAt||'2026-11-18',markdown:d.markdown});
}
fs.writeFileSync(dest,JSON.stringify({capturedAt:'2026-11-18',records}));
console.log(JSON.stringify({references:records.length,bytes:fs.statSync(dest).size}));
