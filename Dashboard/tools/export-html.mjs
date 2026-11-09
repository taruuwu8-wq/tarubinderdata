import {readFile,writeFile,mkdir} from 'node:fs/promises';
const root=new URL('../dist/',import.meta.url);
let html=await readFile(new URL('index.html',root),'utf8');
const css=(await readFile(new URL('style.css',root),'utf8')).replace('@import url("mobile.css");','')+'\n'+await readFile(new URL('mobile.css',root),'utf8')+'\n'+await readFile(new URL('repo-policy.css',root),'utf8')+'\n'+await readFile(new URL('wiki-media.css',root),'utf8');
const policy=(await readFile(new URL('repo-policy.js',root),'utf8')).replaceAll('export ','');
const core=(await readFile(new URL('core.js',root),'utf8')).replace(/^import[^\n]+\n/gm,'').replaceAll('export ','').replace('function validateProfile(','function parseProfile(');
let app=await readFile(new URL('app.js',root),'utf8');
app=app.replace(/^import[^\n]+\n/gm,'');
const data=JSON.stringify(JSON.parse(await readFile(new URL('data.json',root),'utf8'))).replaceAll('</','<\\/');
const repo=JSON.stringify(JSON.parse(await readFile(new URL('repo-items.json',root),'utf8'))).replaceAll('</','<\\/');
const media=JSON.parse(await readFile(new URL('wiki-media.json',root),'utf8'));
for(const group of ['items','mobs','skills','classes'])for(const entry of Object.values(media[group])){if(entry.src.startsWith('data:'))continue;const bytes=await readFile(new URL(entry.src.slice(2),root));entry.src='data:'+entry.type+';base64,'+bytes.toString('base64');}
app=app.replace(/const \[DATA,REPO,MEDIA\]=await Promise[^\n]+\n/,()=>`const DATA=${data},REPO=${repo},MEDIA=${JSON.stringify(media)};\n`);
html=html.replace('<link rel="stylesheet" href="style.css">',()=>'<style>'+css+'</style>').replace('<link rel="stylesheet" href="mobile.css">','').replace('<link rel="stylesheet" href="repo-policy.css">','').replace('<link rel="stylesheet" href="wiki-media.css">','').replace('<script type="module" src="app.js"></script>',()=>'<script type="module">'+policy+'\n'+core+'\n'+app+'</script>');
const out=new URL('../exports/',import.meta.url);await mkdir(out,{recursive:true});
await writeFile(new URL('Taru-Build-Lab.html',out),html,'utf8');
console.log('Standalone dashboard written to Dashboard/exports/Taru-Build-Lab.html');
