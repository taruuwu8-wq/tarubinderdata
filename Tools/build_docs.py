"""Phase 8-9: generate INDEX.md, ALL_DATA.md, DATA_COVERAGE.md, CRAWL_REPORT.md from local files (no network)."""
import os, re, json, glob, csv, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def relative_path(*args):
    return os.path.relpath(*args).replace(os.sep, "/")

J = lambda n: json.load(open(f"{ROOT}/Structured_Data/{n}", encoding="utf-8"))["records"]
CATS = ["Classes", "Skills", "Stats", "Combat_Mechanics", "Weapons", "Equipment", "Affixes", "Cards", "Pets",
        "Monsters", "Maps", "Items", "Blacksmith", "Game_Systems", "Region_Sets", "Patch_Notes"]
def title(f):
    for l in open(f, encoding="utf-8"):
        if l.startswith("# "): return l[2:].strip()
    return os.path.basename(f)
def md_files(c): return sorted(glob.glob(f"{ROOT}/{c}/**/*.md", recursive=True))
def esc(s): return (s or "").replace("|", "\\|").replace("\n", " ")
def link(r): return f"[{esc(r['name'])}]({r['kb_file']})" if r.get("kb_file") else f"{esc(r['name'])} ([wiki]({r['source_url']}))"

# ---------------- INDEX.md ----------------
out = ["# INDEX — Binder Town Wiki Knowledge Base", "",
       "Categorized index of every organized file. Each file starts with its source URL. "
       "Structured data: [Structured_Data/](Structured_Data/). Raw originals: [Raw/Original_Wiki_Pages/](Raw/Original_Wiki_Pages/).", ""]
out.append("## Categories\n\n| Category | Files |\n|---|---|")
for c in CATS: out.append(f"| [{c}](#{c.lower().replace('_', '_')}) | {len(md_files(c))} |")
out.append("")
for c in CATS:
    out.append(f"## {c}\n")
    groups = collections.defaultdict(list)
    for f in md_files(c):
        rel = relative_path(f, ROOT); sub = os.path.dirname(rel)
        groups[sub].append(f"[{title(f)}]({rel})")
    for sub in sorted(groups):
        if sub != c: out.append(f"**{sub.split('/', 1)[1]}**\n")
        out.append(" · ".join(groups[sub]) + "\n")
out.append("## Structured data files\n")
for f in sorted(glob.glob(f"{ROOT}/Structured_Data/*")):
    n = os.path.basename(f)
    if n.endswith(".json"):
        d = json.load(open(f, encoding="utf-8")); out.append(f"- [{n}](Structured_Data/{n}) — {d['count']} records. {d['_about']}")
    else: out.append(f"- [{n}](Structured_Data/{n})")
open(f"{ROOT}/INDEX.md", "w", encoding="utf-8").write("\n".join(out) + "\n")

# ---------------- ALL_DATA.md ----------------
A = ["# ALL_DATA — consolidated quick reference", "",
     "Generated from Structured_Data/*.json. **This is a lookup index, not a replacement for the source files**: every row links to its organized file, which holds the full verbatim Wiki text and tables. All values are [WIKI] unless stated. Text is in the Wiki's original Thai.", ""]
A.append("## Classes\n\n| Class | Skills linked | File |\n|---|---|---|")
for r in J("classes.json"): A.append(f"| {esc(r['name'])} | {len(r['skills'])} | {link(r)} |")
A.append("\n## Skills\n\n| Skill | Class(es) | Type | Unlock | Lv rows |\n|---|---|---|---|---|")
for r in sorted(J("skills.json"), key=lambda r: (r["classes"][0] if r["classes"] else "", r["name"] or "")):
    A.append(f"| {link(r)} | {', '.join(r['classes'])} | {r['skill_type'] or ''} | {esc('; '.join(r['requirements']))} | {len(r['properties'].get('per_level', []))} |")
A.append("\n## Pets\n\n| Pet | Rarity | Bonus (listing text) | Data |\n|---|---|---|---|")
for r in sorted(J("pets.json"), key=lambda r: ["Legendary", "Epic", "Rare", "Common"].index(r["tier"])):
    A.append(f"| {link(r)} | {r['tier']} | {esc(r['listing_text'])} | {r['data_source']} |")
A.append("\n## Cards (one per monster; ★1 / ★5 as stated by the Wiki)\n\n| Monster | Colour | Spirit Load | ★1 | ★5 |\n|---|---|---|---|---|")
for r in sorted(J("cards.json"), key=lambda r: r["monster"] or ""):
    A.append(f"| [{esc(r['monster'])}]({r['kb_file']}) | {r['properties']['colour']} | {r['properties']['spirit_load']} | {esc(r['star_effects'].get('★1'))} | {esc(r['star5_effect'])} |")
A.append("\n## Monsters\n\n| Monster | Type | Weak to | Resists | DEF | MDEF | FLEE |\n|---|---|---|---|---|---|---|")
for r in sorted(J("monsters.json"), key=lambda r: r["name"] or ""):
    m = r["properties"]["matchups"]
    A.append(f"| {link(r)} | {esc(m.get('ประเภท'))} | {esc(m.get('แพ้ธาตุ'))} | {esc(m.get('ต้านธาตุ'))} | {esc(m.get('เกราะกายภาพ (DEF)'))} | {esc(m.get('ต้านเวท (MDEF)'))} | {esc(m.get('หลบ (FLEE)'))} |")
A.append("\n## Maps\n\n| Map | Monsters linked |\n|---|---|")
for r in J("maps.json"): A.append(f"| {link(r)} | {len(r['monsters'])} |")
A.append("\n## Tier-10 weapons & equipment (detail pages)\n\nAll tiers 1–10 (listing values only) are in [Structured_Data/equipment_all_tiers.csv](Structured_Data/equipment_all_tiers.csv).\n")
A.append("| Item | Slot | Lv | ATK | MATK | DEF | Stat / bonus (detail) | Who can equip |\n|---|---|---|---|---|---|---|---|")
for r in sorted([x for x in J("weapons.json") + J("equipment.json") if x["data_source"] == "detail_page"], key=lambda r: (r["properties"]["slot"] or "", r["slug"])):
    p = r["properties"]; ds = p.get("detail_stats", {})
    A.append(f"| {link(r)} | {p['slot']} | {r['level']} | {p['ATK']} | {p['MATK']} | {p['DEF']} | {esc(' · '.join(f'{k} {v}' for k, v in ds.items() if k not in ('ATK', 'MATK', 'DEF', 'ช่อง', 'น้ำหนัก')))} | {esc('; '.join(r['requirements']))} |")
A.append("\n## Items with detail pages (key materials, top consumables, card items)\n\n| Item | Category | Effect / listing data |\n|---|---|---|")
for r in [x for x in J("items.json") if x["data_source"] == "detail_page"]:
    A.append(f"| {link(r)} | {r['category']} | {esc('; '.join(r['effects']) or ' · '.join(f'{k}: {v}' for k, v in r['properties'].items()))} |")
A.append("\n## System pages\n")
for n in ["affixes.json", "stats.json", "blacksmith.json", "combat_mechanics.json", "region_sets.json", "game_systems.json"]:
    for r in J(n): A.append(f"- {link(r)} — {len(r['tables'])} tables ({n})")
open(f"{ROOT}/ALL_DATA.md", "w", encoding="utf-8").write("\n".join(A) + "\n")

# ---------------- coverage numbers ----------------
man = list(csv.DictReader(open(f"{ROOT}/Sources/URL_MANIFEST.csv", encoding="utf-8")))
st = collections.Counter(r["crawl_status"] for r in man)
def cov(prefix):
    rs = [r for r in man if r["path"].startswith(prefix)]
    return len(rs), sum(r["crawl_status"] != "deferred_by_user_scope" for r in rs)
print("INDEX/ALL_DATA written;", dict(st))
for p in ["/item/", "/mob/", "/skill/", "/npc/", "/map/", "/pet/", "/job/", "/systems/", "/guide/"]: print(p, cov(p))
