"""Audit merged dates, missing URLs, stale details and verbatim numeric preservation. No network."""
import csv, collections, hashlib, json, re, sys
from pathlib import Path
from urllib.parse import urlparse
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kbcommon import load_raw, clean
ROOT = Path(__file__).resolve().parent.parent
DATE = "2026-11-08"
CATS = ["Classes","Skills","Stats","Combat_Mechanics","Weapons","Equipment","Affixes","Cards","Pets","Monsters","Maps","Items","Blacksmith","Game_Systems","Region_Sets"]
merge = json.loads((ROOT/"Sources/SNAPSHOT_MERGE.json").read_text(encoding="utf-8"))
rows = list(csv.DictReader((ROOT/"Sources/URL_MANIFEST.csv").open(encoding="utf-8",newline="")))
raws, organized = {}, {}
for file in sorted((ROOT/"Raw/Original_Wiki_Pages").rglob("*.md")):
    meta, body = load_raw(str(file))
    p = urlparse(meta["source_url"]).path.rstrip("/") or "/"
    raws[p] = {"meta":meta,"body":body,"file":file.relative_to(ROOT).as_posix()}
for category in CATS:
    for file in (ROOT/category).rglob("*.md"):
        text = file.read_text(encoding="utf-8")
        source = re.search(r"> \*\*Source:\*\* (https://\S+)",text)
        if source:
            p = urlparse(source.group(1)).path.rstrip("/") or "/"
            organized[p] = {"file":file.relative_to(ROOT).as_posix(),"text":text}
aliases = {"/skills","/refine","/skills/novice","/gem-exchange"}
errors = []
for p, raw in raws.items():
    if p in aliases: continue
    if p not in organized:
        errors.append({"path":p,"error":"missing organized page"}); continue
    expected = collections.Counter(re.findall(r"\d+(?:\.\d+)?",clean(raw["body"])))
    actual = collections.Counter(re.findall(r"\d+(?:\.\d+)?",organized[p]["text"].split("\n---\n",1)[-1]))
    missing = expected-actual
    if missing: errors.append({"path":p,"missing_tokens":dict(missing)})
stale = [{"url":r["meta"]["source_url"],"path":p,"last_crawled":r["meta"]["crawled_date"],"raw_file":r["file"],"kb_file":organized.get(p,{}).get("file"),"priority":"high" if p.startswith(("/mob/","/skill/")) or p in {"/item/rapier_t10","/item/dagger_t10","/item/moth_mask"} else "normal"} for p,r in sorted(raws.items()) if r["meta"]["crawled_date"]<DATE and p not in aliases]
missing = [{"url":r["url"],"path":r["path"],"category":r["category"],"status":"not_fetched","listing_data_available":r["path"].startswith("/item/"),"priority":"normal" if r["path"].startswith(("/npc/","/map/","/tools/")) else "low"} for r in rows if r["path"] not in raws]
counts, conflicts = {}, []
for file in sorted((ROOT/"Structured_Data").glob("*.json")):
    payload = json.loads(file.read_text(encoding="utf-8")); records = payload.get("records",[])
    if payload["count"] != len(records): raise SystemExit("Count mismatch: "+file.name)
    for record in records:
        raw = raws.get(urlparse(record.get("source_url","")).path)
        if raw: record["freshness_status"] = "snapshot_2026-11-08" if raw["meta"]["crawled_date"]>=DATE else "not_refreshed_after_2026-11-07"
        elif record.get("data_source")=="listing_table_only": record["freshness_status"]="listing_only_2026-11-08_detail_not_fetched"
        if record.get("listing_source"): record["listing_last_crawled"]=DATE
        if file.name in {"equipment.json","weapons.json"}:
            props=record.get("properties",{}); detail=props.get("detail_stats",{})
            for key in ["ATK","MATK","DEF"]:
                a,b=props.get(key),detail.get(key)
                if a not in (None,"—","") and b not in (None,"—","") and str(a)!=str(b):
                    conflict={"slug":record["slug"],"field":key,"listing":a,"detail":b,"listing_date":DATE,"detail_date":record.get("last_crawled"),"kb_file":record.get("kb_file")}
                    conflicts.append(conflict)
                    flag=f"TO_VERIFY: {key} listing ({DATE})={a}, detail ({record.get('last_crawled')})={b}"
                    if flag not in record.setdefault("flags",[]): record["flags"].append(flag)
        if record.get("kb_file") and not (ROOT/record["kb_file"]).is_file(): raise SystemExit("Broken record path: "+record["kb_file"])
    counts[file.name]=len(records)
    if file.name=="maps.json": payload["_about"]="55 map detail pages captured 2026-11-07; fresh listing has 56 maps. Copperbell Arena detail not fetched."
    if file.name=="npcs.json": payload["_about"]="71 NPC detail pages captured 2026-11-07; fresh listing has 77 NPCs. Six arena NPC details not fetched."
    file.write_text(json.dumps(payload,ensure_ascii=False,indent=1)+"\n",encoding="utf-8")
for entry in merge["pages"]:
    if hashlib.sha256((ROOT/entry["snapshot_file"]).read_bytes()).hexdigest()!=entry["sha256"]: raise SystemExit("Snapshot modified")
report={"snapshot_date":DATE,"merged_on":"2026-11-09","policy":"available_snapshot_only_no_new_crawl","fresh_pages":merge["fresh_pages"],"fresh_hubs":merge["hubs"],"fresh_item_details":merge["new_item_details"],"raw_pages":len(raws),"organized_pages":len(organized),"older_detail_pages":len(stale),"not_fetched_pages":len(missing),"structured_counts":counts,"numeric_preservation":{"checked_pages":len(raws)-len(aliases),"errors":errors},"listing_detail_conflicts":conflicts,"stale_details":stale,"not_fetched":missing,"missing_by_category":dict(collections.Counter(r["category"] for r in missing)),"note":"Fresh hubs do not refresh old details. Missing data is unknown, never zero."}
(ROOT/"Sources/DATA_FRESHNESS.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
with (ROOT/"Sources/REFRESH_QUEUE.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.writer(f,lineterminator="\n"); w.writerow(["url","status","last_crawled","priority","reason"])
    for r in stale: w.writerow([r["url"],"stale_detail",r["last_crawled"],r["priority"],"Not refreshed after snapshot"])
    for r in missing: w.writerow([r["url"],"not_fetched","",r["priority"],"Listing only" if r["listing_data_available"] else "Detail not fetched"])
md=["# ข้อมูลที่ยังต้องดึงหรือยืนยัน","",f"รวม snapshot {DATE} เมื่อ 2026-11-09 โดยไม่ดึง Wiki เพิ่ม","",
    "| กลุ่ม | จำนวน | สถานะ |","|---|---:|---|",f"| หน้ารวม/ระบบ/อาชีพ | {merge['hubs']} | รวมแล้ว |",f"| รายละเอียดไอเท็มใหม่ | {merge['new_item_details']} | รวมแล้ว |",f"| รายละเอียดเดิม | {len(stale)} | ยังเป็นข้อมูล 2026-11-07 |",f"| URL ที่ยังไม่ได้ดึง | {len(missing)} | บางส่วนมีเพียงตารางรวม |","",
    "## ลำดับแนะนำ","","1. มอนใน Shellforge และสกิล Rogue","2. รายละเอียดอุปกรณ์เดิมของ Taru: ค่าตีบวก/ออฟอาจต่างจากระบบใหม่","3. หน้ามอนอื่น: การ์ด ★1/★5 ยังมาจากรายละเอียดเดิม","4. Copperbell Arena และ NPC ใหม่ 6 ตัว","5. ไอเท็มขั้นต่ำ/แฟชั่นและรายการนอกขอบเขตเดิม","",
    "ไม่ต้องรอสรุปจาก Claude เพื่อรวมส่วนที่มีแล้ว สรุปหรือ raw เพิ่มเติมใช้เติมเฉพาะช่องว่าง โดยแนบ URL และวันที่ต้นทาง","",
    "[รายการ URL](Sources/REFRESH_QUEUE.csv) · [รายงานเครื่องอ่าน](Sources/DATA_FRESHNESS.json)"]
(ROOT/"MISSING_DATA.md").write_text("\n".join(md)+"\n",encoding="utf-8")
print(json.dumps({k:report[k] for k in ["fresh_pages","raw_pages","organized_pages","older_detail_pages","not_fetched_pages","missing_by_category"]},ensure_ascii=False))
print("numeric preservation errors:",len(errors),"listing/detail conflicts:",len(conflicts))
if errors:
    print(json.dumps(errors[:4],ensure_ascii=False)); raise SystemExit(1)
