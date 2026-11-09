// Store each affix definition once; expand item pools in memory at runtime.
import {readFile,writeFile} from 'node:fs/promises';
const path='dist/repo-items.json',r=JSON.parse(await readFile(path,'utf8'));
r.families=[...new Set(r.affixRules.map(rule=>rule.section))];
for(const item of Object.values(r.items)){if(item.allowedAffixes){const seen=new Set();item.affixPool=[];for(const rule of item.allowedAffixes){const family=r.families.indexOf(rule.section),key=rule.anchor+':'+family;if(!seen.has(key)){seen.add(key);item.affixPool.push([rule.anchor,family]);}}delete item.allowedAffixes;}}
r.schemaVersion=2;await writeFile(path,JSON.stringify(r)+'\n');console.log('Compact registry: '+Buffer.byteLength(JSON.stringify(r))+' bytes');
