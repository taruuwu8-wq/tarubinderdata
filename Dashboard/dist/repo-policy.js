// Repo is authoritative for item definitions, refine values and affix limits.
export const normalizeAffix=s=>String(s||'').replace(/^of /i,'').trim().toLowerCase();
export function hydrateRegistry(registry){for(const item of Object.values(registry.items)){if(item.allowedAffixes)continue;item.allowedAffixes=(item.affixPool||[]).flatMap(([anchor,family])=>registry.affixRules.filter(rule=>rule.section===registry.families[family]).map(rule=>({...rule,anchor,family:rule.section,kind:anchor.startsWith('p_')?'trigger':'passive'})));}return registry;}
const anchorKeys={atk:'atk',atkpct:'atkPct',matkpct:'matkPct',crit:'crit',critdmg:'critDamage',cdr:'cdr',vsdebuff:'ccDamage',str:'str',agi:'agi',vit:'vit',int:'int',dex:'dex',luk:'luk',hp:'hp',hppct:'hpPct',hit:'hit',flee:'flee',leech:'lifesteal',armorpen:'armorPierce',mp:'mp',softdef:'softDef',sturdy:'softDef',guard:'def',evasive:'flee',aspd:'attackSpeed',move:'speed',regen:'hpRegen',castspd:'castSpeed',mending:'healPower',block:'block',matk:'matk'};
export function repoStats(item,enchant){const stats=structuredClone(item.baseStats);const value=Number(enchant)===0?null:item.refine[Number(enchant)];if(Number(enchant)>0&&value===undefined)return null;if(value!==null){for(const key of item.refineKeys){const s=stats.find(s=>s.key===key);const next=typeof value==='object'?value[key]:value;if(s)s.value=next;else stats.push({key,value:next,kind:key.endsWith('Pct')?'percent':'flat'});}}return stats;}
export function checkAffix(affix,item,registry,gear){
 const rule=item.allowedAffixes.find(r=>r.norm===normalizeAffix(affix.name));
 if(!rule)return {status:'conflict',message:'ไม่พบออฟชื่อนี้ในรายการที่ชิ้นนี้สุ่มได้'};
 if(affix.key==='trigger'||affix.key==='reference')return {status:'reference',message:'อ้างอิงคำอธิบาย Trigger ใน repo · ไม่รวมเป็นโบนัสถาวร',rule};
 const expected=anchorKeys[rule.anchor]||(/Unyielding|Stonewall/i.test(rule.name)?'softDef':null);
 if(!expected||expected!==affix.key)return {status:'conflict',message:'ชนิดโบนัสไม่ตรงกับออฟใน repo',rule};
 let min=rule.min,max=rule.max;
 if(gear.rarity==='Magic'&&gear.affixes.length<=2){const cap=registry.affixRules.find(r=>r.norm===rule.norm.replace(/^mythic /,'eternal '))?.max;const factor=gear.affixes.length===1?1.8:1.35;max=Math.min(max*factor,cap??max*factor);min=Math.min(min,Math.min(min*factor,cap??min*factor));}
 const value=Number(affix.value);if(!Number.isFinite(value)||value<min-0.0001||value>max+0.0001)return {status:'conflict',message:`ค่าอยู่นอกช่วง repo ${min}–${max}`,min,max,rule};
 return {status:'range_checked',message:`ค่าผู้เล่นอยู่ในช่วง repo ${min}–${max} (ไม่ใช่การยืนยันของในเกม)`,min,max,rule};
}
export function reconcileProfile(profile,registry){const result=structuredClone(profile);for(const gear of result.gear){const slug=gear.itemSlug||registry.mapping[gear.id];const item=registry.items[slug];gear.itemSlug=slug||null;gear.sourceUrl=item?.sourceUrl||null;gear.sourceCommit=registry.ref;gear.sourceLastCrawled=item?.lastCrawled||null;gear.repoStatus=item?'matched':'unmatched';gear.repoIssues=[];
 if(item&&!itemFitsSlot(item,gear.id,registry)){gear.repoStatus='unmatched';gear.repoIssues.push('ไอเท็มไม่ตรงช่องหรืออาชีพ Rogue · ไม่นำมารวมโบนัส');continue;}if(!item){gear.repoIssues.push('ไม่พบรหัสไอเท็มนี้ใน snapshot repo · ไม่นำค่ามารวมโบนัส');continue;}
 gear.name=item.name;gear.level=item.level;const cap=affixCapacity(gear.rarity);if(gear.affixes.length>cap)gear.repoIssues.push('จำนวนออฟเกินความหายาก');const families=new Set();let prefixes=0,suffixes=0;for(const a of gear.affixes){const r=item.allowedAffixes.find(r=>r.norm===normalizeAffix(a.name));if(!r)continue;if(families.has(r.family))gear.repoIssues.push('ออฟซ้ำตระกูล');families.add(r.family);if(/^of /i.test(r.name))suffixes++;else prefixes++;}gear.affixLayoutValid=gear.affixes.length<=cap&&families.size===gear.affixes.length&&prefixes<=2&&suffixes<=3;if(prefixes>2||suffixes>3)gear.repoIssues.push('เกิน 2 Prefix / 3 Suffix');
 const stats=repoStats(item,gear.enchant);gear.refineVerified=!!stats;
 if(stats)gear.stats=stats;else{gear.repoIssues.push('ไม่มีค่าตีบวกระดับนี้ใน repo · ไม่นำชิ้นนี้มารวมโบนัส');}
 if(gear.id==='offhand'&&gear.roleConfirmed!==true)gear.repoIssues.push('ยังไม่ยืนยันว่าเป็นอาวุธที่ใส่จริง · ไม่นำมารวมโบนัส');
 for(const affix of gear.affixes){const audit=checkAffix(affix,item,registry,gear);affix.sourceStatus=audit.status;affix.sourceMessage=audit.message;affix.repoMin=audit.min??audit.rule?.min;affix.repoMax=audit.max??audit.rule?.max;affix.repoText=audit.rule?.maxText||'';if(audit.rule)affix.tier=audit.rule.tier;if(audit.status==='conflict')gear.repoIssues.push(`${affix.name}: ${audit.message}`);}
 }return result;}
export function canCountGear(g){return g.enabled&&g.repoStatus!=='unmatched'&&g.refineVerified!==false&&!(g.id==='offhand'&&g.roleConfirmed!==true);}

export const AFFIX_LIMITS={Normal:0,Magic:2,Rare:3,Epic:4};
export const affixCapacity=rarity=>AFFIX_LIMITS[rarity]??4;
const SLOT_TYPES={weapon:'อาวุธ',offhand:'มือรอง',head:'หมวก',face:'หน้า',mouth:'ปาก',neck:'สร้อยคอ',armor:'เกราะ',belt:'เข็มขัด',ring1:'เครื่องประดับ',ring2:'เครื่องประดับ',boots:'รองเท้า'};
export function itemFitsSlot(item,id,registry){return !!item&&item.compatibleRogue!==false&&(item.slot===SLOT_TYPES[id]||(id==='offhand'&&['dagger_t10','dagger_t10_tide'].includes(item.slug))||(!item.slot&&registry.mapping[id]===item.slug));}
export function makeAffix(rule){const key=rule.kind==='trigger'?'trigger':anchorKeys[rule.anchor]||'reference';return {name:rule.name,key,value:['trigger','reference'].includes(key)?0:rule.min,kind:['trigger','reference'].includes(key)?key:rule.minText.includes('%')?'percent':'flat',tier:rule.tier};}
export function selectGearItem(gear,slug,registry){const item=registry.items[slug];if(!itemFitsSlot(item,gear.id,registry))throw Error('อุปกรณ์ไม่ตรงช่องหรืออาชีพ');const result=structuredClone(gear);result.itemSlug=slug;result.name=item.name;result.level=item.level;result.affixes=[];result.notes=(item.referenceStats||[]).join(' · ');result.set='';result.roleConfirmed=false;result.enchant=Math.min(15,Math.max(0,Math.round(result.enchant||0)));result.stats=repoStats(item,result.enchant)||item.baseStats;return reconcileProfile({gear:[result]},registry).gear[0];}
