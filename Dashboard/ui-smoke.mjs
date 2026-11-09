import vm from 'node:vm';import assert from 'node:assert/strict';import {readFile} from 'node:fs/promises';
const data=JSON.parse(await readFile('dist/data.json','utf8')),repo=JSON.parse(await readFile('dist/repo-items.json','utf8')),media=JSON.parse(await readFile('dist/wiki-media.json','utf8'));
let core=(await readFile('dist/core.js','utf8')).replace(/^import[^\n]+\n/gm,'').replaceAll('export ','').replace('function validateProfile(','function parseProfile(');
const policy=(await readFile('dist/repo-policy.js','utf8')).replaceAll('export ','');
let app=(await readFile('dist/app.js','utf8')).replace(/^import[^\n]+\n/gm,'').replace(/^const \[DATA,REPO,MEDIA\]=await Promise[^\n]+\n/m,`const DATA=${JSON.stringify(data)},REPO=${JSON.stringify(repo)},MEDIA=${JSON.stringify(media)};\n`);
const nodes=new Map();const node=selector=>{if(!nodes.has(selector))nodes.set(selector,{innerHTML:'',textContent:'',value:'',classList:{toggle(){},add(){},remove(){}},querySelectorAll(){return []},addEventListener(){},showModal(){this.open=true},close(){this.open=false}});return nodes.get(selector)};
const context=vm.createContext({structuredClone,console,Intl,crypto:globalThis.crypto,setTimeout:()=>1,clearTimeout(){},document:{querySelector:node,querySelectorAll(){return []},addEventListener(){}},window:{scrollTo(){}},localStorage:{getItem(){return null},setItem(){}},URL,Blob});
vm.runInContext(policy+'\n'+core+'\n'+app,context);
assert.ok(node('#content').innerHTML.includes('ฐานข้อมูล: repo snapshot'));
assert.ok(node('#content').innerHTML.includes(media.items.rapier_t10.src));
assert.ok(node('#content').innerHTML.includes(media.mobs.forge_hermit.src));
for(const page of ['overview','equipment','cards','skills','compare']){vm.runInContext(`view='${page}';render()`,context);assert.ok(node('#content').innerHTML.length>2000);}
vm.runInContext("view='equipment';render()",context);assert.ok(node('#content').innerHTML.includes('rapier_t10'));assert.ok(node('#content').innerHTML.includes('245% · ไม่รวม'));
vm.runInContext("preset('thorn');view='cards';render()",context);assert.ok(node('#content').innerHTML.includes('Bramble Pact'));
assert.ok(node('#content').innerHTML.includes(media.mobs.thornling.src));
vm.runInContext("view='skills';render()",context);assert.ok(node('#content').innerHTML.includes(media.skills.flurry.src));
vm.runInContext("openEditor('face')",context);assert.ok(node('#editorContent').innerHTML.includes('id="editItem"'));assert.ok(node('#editorContent').innerHTML.includes('data-affix-choice'));
console.log('UI smoke passed: all 5 views render, repo status, excluded conflict, preset and editor provenance');

vm.runInContext('showDataGaps()',context);assert.ok(node('#gapDialog').open);assert.ok(node('#gapContent').innerHTML.includes('640'));assert.ok(node('#gapContent').innerHTML.includes('1,671'));assert.ok(node('#gapContent').innerHTML.includes('REFRESH_QUEUE.csv'));

vm.runInContext("view='maps';render()",context);assert.ok(node('#content').innerHTML.includes('Copperbell Arena'));assert.ok(node('#content').innerHTML.includes('Shellforge Basin'));
