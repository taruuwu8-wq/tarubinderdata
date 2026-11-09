"""Phase 5-6: organize Raw/Original_Wiki_Pages into category folders + Structured_Data/*.json.
No network. Text and numbers are copied verbatim from the Wiki markdown (images stripped).
Every record carries source_url, source_title, last_crawled and verification_status."""
import os, re, json, glob, csv, shutil, collections, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kbcommon import ROOT, RAW, BASE, load_raw, clean, tables, plain, name_from_title

def relative_path(*args):
    return os.path.relpath(*args).replace(os.sep, "/")

SD = f"{ROOT}/Structured_Data"
CATS = ["Classes", "Skills", "Stats", "Combat_Mechanics", "Weapons", "Equipment", "Affixes", "Cards", "Pets",
        "Monsters", "Maps", "Items", "Blacksmith", "Game_Systems", "Region_Sets", "Patch_Notes"]
# Refuse regeneration outside an explicitly selected checkout or through symlinks.
from pathlib import Path
_root = Path(ROOT).resolve()
_expected = os.environ.get("KB_WORKSPACE_ROOT")
if not _expected or Path(_expected).resolve() != _root or not (_root / ".git").exists():
    raise SystemExit("Set KB_WORKSPACE_ROOT to the selected repository checkout before regeneration")
for _category in CATS + ["Structured_Data"]:
    _target = (_root / _category).resolve()
    if _target == _root or not _target.is_relative_to(_root):
        raise SystemExit("Refusing regeneration outside the selected checkout")
for c in CATS + ["Structured_Data"]:
    if c == "Patch_Notes": os.makedirs(f"{ROOT}/{c}", exist_ok=True); continue  # user-provided patch notes are kept
    shutil.rmtree(f"{ROOT}/{c}", ignore_errors=True); os.makedirs(f"{ROOT}/{c}", exist_ok=True)

# ---------- load everything ----------
pages = {}  # wiki path -> dict(meta, body, md)
for f in glob.glob(f"{RAW}/*/*.md"):
    meta, body = load_raw(f)
    path = "/" + meta["source_url"].replace(BASE, "").strip("/")
    pages[path if path != "/" else "/"] = {"meta": meta, "body": body, "md": clean(body), "raw_file": relative_path(f, ROOT)}
ALIASES = {"/skills": "/jobs", "/refine": "/systems/refine", "/skills/novice": "/job/novice", "/gem-exchange": "/systems/gem-exchange"}
manifest = {r["path"]: r for r in csv.DictReader(open(f"{ROOT}/Sources/URL_MANIFEST.csv", encoding="utf-8"))}

def listing(path):
    out = {}
    for t in tables(pages[path]["md"]):
        for r in t["rows"]:
            m = re.search(r"\]\((/item/[^)\s]+)\)", r[0])
            if m: out[m.group(1)] = dict(zip(t["header"], [plain(c) for c in r]))
    return out
L = {k: listing(f"/items/{k}") for k in ["gear", "look", "use", "mat", "drop", "fashion"]}
CARD_ITEMS = {"/item/loose_spirit", "/item/spirit_card", "/item/spirit_coin"}

# ---------- skill -> class ----------
CLASS_ORDER = ["knight", "warrior", "scout", "rogue", "mage", "acolyte", "summoner", "novice"]
skill_classes = collections.defaultdict(list)
for j in CLASS_ORDER:
    for s in sorted(set(re.findall(r"\]\((/skill/[^)\s#]+)\)", pages[f"/job/{j}"]["md"]))):
        skill_classes[s].append(j)
def skill_folder(p):
    cl = skill_classes.get(p, [])
    if not cl: return "Skills/_Unassigned"
    if len(cl) > 1 and "novice" in cl: return "Skills/Binder"
    return "Skills/" + ("Binder" if cl[0] == "novice" else cl[0].capitalize())

SYSMAP = {"stats": "Stats", "statuses": "Combat_Mechanics", "class-resources": "Combat_Mechanics", "classes": "Combat_Mechanics",
          "threats": "Combat_Mechanics", "weapon-rules": "Combat_Mechanics", "affix": "Affixes", "smith": "Blacksmith",
          "refine": "Blacksmith", "crafting": "Blacksmith", "uniques": "Blacksmith", "region-sets": "Region_Sets",
          "pets": "Pets", "bosses": "Monsters", "world-boss": "Monsters", "oils-foods": "Items"}
def target(p):
    """Organized file path (relative to ROOT) for a wiki path, or None if not stored."""
    p = ALIASES.get(p, p)
    if p not in pages: return None
    seg = p.strip("/").split("/"); slug = seg[-1] if seg[-1] else "home"
    if p == "/": return "Game_Systems/Wiki_Home.md"
    if seg[0] == "job": return f"Classes/{'Binder' if slug == 'novice' else slug.capitalize()}.md"
    if seg[0] == "jobs": return "Classes/_All_Classes.md"
    if seg[0] == "skill": return f"{skill_folder(p)}/{slug}.md"
    if seg[0] == "mob": return f"Monsters/{slug}.md"
    if seg[0] == "mobs": return "Monsters/_All_Monsters.md"
    if seg[0] == "map": return f"Maps/{slug}.md"
    if seg[0] == "maps": return "Maps/_All_Maps.md"
    if seg[0] == "npc": return f"Game_Systems/NPCs/{slug}.md"
    if seg[0] == "npcs": return "Game_Systems/NPCs/_All_NPCs.md"
    if seg[0] == "pet": return f"Pets/{slug}.md"
    if seg[0] == "cards": return "Cards/Cards_and_Spirits.md"
    if seg[0] == "glossary": return "Game_Systems/Glossary.md"
    if seg[0] == "guide": return f"Game_Systems/Guides/{slug if len(seg) > 1 else '_Guide_Index'}.md"
    if seg[0] == "items": return f"Items/_Listings/{slug if len(seg) > 1 else 'items_index'}.md"
    if seg[0] == "systems":
        if len(seg) == 1: return "Game_Systems/_Systems_Index.md"
        return f"{SYSMAP.get(slug, 'Game_Systems')}/{slug}.md"
    if seg[0] == "item":
        if p in CARD_ITEMS: return f"Cards/{slug}.md"
        if p in L["gear"]: return f"{'Weapons' if L['gear'][p]['ช่อง'] == 'อาวุธ' else 'Equipment'}/{slug}.md"
        if p in L["look"]: return f"Equipment/Headgear/{slug}.md"
        if p in L["use"]: return f"Items/Consumables/{slug}.md"
        if p in L["mat"]: return f"Items/Materials/{slug}.md"
        if re.search(r"(greatsword|bow|dagger)_t\d+_alt", slug): return f"Weapons/{slug}.md"
        return f"Items/Unlisted/{slug}.md"
    return f"Game_Systems/{slug}.md"

def relink(md, here):
    def rep(m):
        txt, p, frag = m.group(1), m.group(2), m.group(3) or ""
        t = target(p.rstrip("/") or "/")
        if t: return f"[{txt}]({relative_path(f'{ROOT}/{t}', os.path.dirname(f'{ROOT}/{here}'))}{frag})"
        return f"[{txt}]({BASE}{p}{frag})"
    return re.sub(r"\[([^\]]*)\]\((/[^)\s#]*)(#[^)\s]*)?\)", rep, md)

# ---------- write organized markdown ----------
written = {}
for p, pg in sorted(pages.items()):
    if p in ALIASES: continue
    t = target(p); written[p] = t
    m = pg["meta"]; os.makedirs(os.path.dirname(f"{ROOT}/{t}"), exist_ok=True)
    rel_raw = relative_path(f"{ROOT}/{pg['raw_file']}", os.path.dirname(f"{ROOT}/{t}"))
    alias = [a for a, c in ALIASES.items() if c == p]
    head = (f"# {name_from_title(m['source_title'])}\n\n"
            f"> **Source:** {m['source_url']}  \n> **Source title:** {m['source_title']}  \n"
            f"> **Last crawled:** {m['crawled_date']} · **Status:** [WIKI] (verbatim Wiki text, images removed)  \n"
            f"> **Raw original:** [{os.path.basename(pg['raw_file'])}]({rel_raw})"
            + (f"  \n> **Alias URLs (identical content):** {', '.join(BASE + a for a in alias)}" if alias else "") + "\n\n---\n\n")
    open(f"{ROOT}/{t}", "w", encoding="utf-8").write(head + relink(pg["md"], t).strip() + "\n")

# ---------- structured data helpers ----------
def section(md, title):
    m = re.search(rf"^## {re.escape(title)}[^\n]*\n(.*?)(?=^## |\Z)", md, re.S | re.M)
    return m.group(1).strip() if m else None
def tabs_plain(md):
    return [{"section": plain(t["section"] or ""), "header": [plain(h) for h in t["header"]],
             "rows": [[plain(c.replace("<br>", " / ")) for c in r] for r in t["rows"]]} for t in tables(md)]
def bold_pairs(text):
    return {plain(k).strip(): plain(v).strip() for k, v in re.findall(r"^([^*\n|#-][^*\n]*?)\s\*\*([^*\n]+)\*\*\s*$", text or "", re.M)}
def base_rec(p, category):
    pg = pages.get(p); m = pg["meta"] if pg else {}
    return {"name": name_from_title(m.get("source_title")) if pg else None, "slug": p.rsplit("/", 1)[-1], "category": category,
            "tier": None, "level": None, "properties": {}, "effects": [], "requirements": [], "conditions": [], "related": [],
            "source_url": BASE + p, "source_title": m.get("source_title"), "last_crawled": m.get("crawled_date"),
            "kb_file": written.get(p), "verification_status": "WIKI",
            "data_source": "detail_page" if pg else "listing_table_only"}
def related(md): return sorted(set(re.findall(r"\]\((/(?:item|mob|map|skill|pet|job|npc|systems)/[^)\s#]+)", md)))
def detail(rec, p):
    if p in pages:
        md = pages[p]["md"]
        rec["summary_text"] = section(md, "ตอบให้ก่อน")
        rec["tables"] = tabs_plain(md)
        rec["related"] = related(md)
    return rec
def dump(name, data, note):
    json.dump({"_about": note, "count": len(data), "records": data}, open(f"{SD}/{name}", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{name}: {len(data)}")

LISTING_URL = "listing table at {}"
# ---------- equipment & weapons (all 1,002 gear + 331 headgear from listings; T10 with detail) ----------
weapons, equipment = [], []
for kind, src in [("gear", "/items/gear"), ("look", "/items/look")]:
    for p, row in L[kind].items():
        is_w = kind == "gear" and row["ช่อง"] == "อาวุธ"
        r = base_rec(p, "weapon" if is_w else ("headgear" if kind == "look" else "equipment"))
        name_cell = row["ไอเท็ม"]
        r["name"] = r["name"] or name_cell
        r["listing_name"] = name_cell
        r["tier"] = row["ขั้น"]; r["level"] = row["Lv"]
        r["properties"] = {"slot": row["ช่อง"], "ATK": row["ATK"], "MATK": row["MATK"], "DEF": row["DEF"],
                           "sell_npc_normal": row["ขาย NPC (Normal)"]}
        r["listing_source"] = BASE + src
        if p in pages:
            md = pages[p]["md"]
            st = next((t for t in tabs_plain(md) if t["header"][:2] == ["ค่า", "ตัวเลข"]), None)
            if st: r["properties"]["detail_stats"] = {row_[0]: row_[1] for row_ in st["rows"] if len(row_) > 1}
            s = section(md, "ตอบให้ก่อน") or ""
            mm = re.search(r"ใครใส่ได้(.*)$", plain(s), re.M)
            if mm: r["requirements"].append(mm.group(1).strip())
            for line in md.split("\n"):
                if "ใส่มือรองได้" in line or line.startswith("ความหายากสุ่มตอนดรอป"): r["conditions"].append(plain(line))
            detail(r, p)
        (weapons if is_w else equipment).append(r)
for p in sorted(k for k in pages if re.search(r"/item/(greatsword|bow|dagger)_t\d+_alt$", k) and k not in L["gear"]):
    r = detail(base_rec(p, "weapon"), p); r["listing_name"] = r["name"]
    r["properties"] = {"slot": None, "ATK": None, "MATK": None, "DEF": None, "sell_npc_normal": None}
    st = next((t for t in r.get("tables", []) if t["header"][:2] == ["ค่า", "ตัวเลข"]), None)
    if st: r["properties"]["detail_stats"] = {x[0]: x[1] for x in st["rows"] if len(x) > 1}
    r["verification_status"] = "WIKI"; r["flags"] = ["TO_VERIFY: soft-404 — page returns HTTP 200 but only the generic item index (no item data). Not linked from any listing; found only by Firecrawl Map, whose cached title/description (Progress/map_raw.json) suggests a removed item."]
    weapons.append(r)
dump("weapons.json", weapons, "All weapons from /items/gear listing (slot อาวุธ). Tier 10 entries have detail-page data; others are listing_table_only by user scope. Values verbatim; '—' = not applicable per Wiki.")
dump("equipment.json", equipment, "Non-weapon gear (armor, off-hand, accessories, boots, necklace, belt) + headgear/face/mouth (/items/look). Tier 10 entries have detail-page data.")
# Also tier-split CSV for quick lookup
with open(f"{SD}/equipment_all_tiers.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["slug", "name", "category", "slot", "tier", "level", "ATK", "MATK", "DEF", "sell_npc_normal", "data_source", "source_url"])
    for r in weapons + equipment:
        pr = r["properties"]; w.writerow([r["slug"], r["listing_name"], r["category"], pr["slot"], r["tier"], r["level"], pr["ATK"], pr["MATK"], pr["DEF"], pr["sell_npc_normal"], r["data_source"], r["source_url"]])

# ---------- items: consumables, materials, drops, fashion, cards items ----------
items = []
for kind, cat in [("use", "consumable"), ("mat", "material"), ("drop", "monster_drop"), ("fashion", "fashion")]:
    for p, row in L[kind].items():
        r = base_rec(p, cat); r["name"] = r["name"] or row["ไอเท็ม"]; r["listing_name"] = row["ไอเท็ม"]
        r["properties"] = {k: v for k, v in row.items() if k != "ไอเท็ม"}
        if row.get("ผล"): r["effects"].append(row["ผล"])
        r["listing_source"] = f"{BASE}/items/{kind}"
        items.append(detail(r, p))
for p in sorted(CARD_ITEMS | {k for k in pages if k.startswith("/item/") and target(k) and target(k).startswith("Items/Unlisted")}):
    r = detail(base_rec(p, "card_item" if p in CARD_ITEMS else "unlisted_item"), p)
    if p not in CARD_ITEMS: r["flags"] = ["TO_VERIFY: soft-404 — page returns HTTP 200 but only the generic item index (no item data); found only by Firecrawl Map."]
    items.append(r)
dump("items.json", items, "Consumables, materials, monster drops, fashion (listing data for all; detail pages only for the user-scoped subset), card/spirit items, unlisted items.")

# ---------- monsters + cards ----------
mobs, cards = [], []
EQDROPS = []
for p in sorted(k for k in pages if k.startswith("/mob/")):
    md = pages[p]["md"]; r = detail(base_rec(p, "monster"), p)
    r["properties"]["matchups"] = bold_pairs(section(md, "แพ้ทาง / ชนะทาง"))
    lv = next((t for t in r["tables"] if t["header"][:2] == ["Lv", "HP"]), None)
    if lv: r["properties"]["stats_by_level"] = [dict(zip(lv["header"], x)) for x in lv["rows"]]
    loc = section(md, "อยู่ที่ไหน") or ""
    r["properties"]["locations"] = [plain(x) for x in re.findall(r"\[\*\*[^\]]+\]\([^)]*\)", loc)] or [plain(loc)]
    keep = []
    for t in r["tables"]:
        if t["header"][:2] == ["ชิ้น", "ขั้น"]:
            for row in t["rows"]:
                if len(row) == len(t["header"]): EQDROPS.append([r["slug"], r["name"]] + row + [r["source_url"]])
                elif row: grp = row[0]
            r["properties"]["equipment_drop_list"] = f"{len(t['rows'])} rows moved to Structured_Data/monster_equipment_drops.csv"
        else: keep.append(t)
    r["tables"] = keep
    mobs.append(r)
    cs = section(md, "การ์ดของมอนนี้")
    if cs:
        c = base_rec(p, "card"); c["name"] = f"{r['name']} card"; c["monster"] = r["name"]; c["kb_file"] = r["kb_file"]
        hdr = re.search(r"สี\s+(\S+)\s+·\s+Spirit Load\s+(\S+)", cs)
        c["properties"] = {"colour": hdr.group(1) if hdr else None, "spirit_load": hdr.group(2) if hdr else None}
        st = next((t for t in tabs_plain(cs) if t["header"] == ["ดาว", "ผล"]), None)
        c["star_effects"] = {x[0]: x[1] for x in st["rows"]} if st else {}
        c["star5_effect"] = c["star_effects"].get("★5")
        c["conditions"] = [plain(l) for l in cs.split("\n") if l.startswith("แลกด้วย") or "ได้วิญญาณ" in l]
        c["note"] = "The Wiki shows ★1 and ★5 values only; intermediate stars are not listed. [UNKNOWN] for ★2-★4."
        cards.append(c)
with open(f"{SD}/monster_equipment_drops.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["mob_slug", "mob_name", "item", "tier", "chance_per_kill", "equip_level", "classes", "source_url"]); w.writerows(EQDROPS)
print("monster_equipment_drops.csv:", len(EQDROPS))
dump("monsters.json", mobs, "All 160 monsters (detail pages). matchups = bold label/value pairs from 'แพ้ทาง / ชนะทาง'. Drops/equipment-drop tables are under tables[].")
dump("cards.json", cards, "One card per monster, taken from each monster page's 'การ์ดของมอนนี้' section (★1 and ★5 as stated by the Wiki). Card system rules: Cards/Cards_and_Spirits.md.")

# ---------- skills ----------
skills = []
for p in sorted(k for k in pages if k.startswith("/skill/")):
    md = pages[p]["md"]; r = detail(base_rec(p, "skill"), p)
    r["classes"] = skill_classes.get(p, [])
    s = plain(r.get("summary_text") or "")
    mm = re.search(r"ปลดล็อก(.*?)$", s, re.M); r["requirements"] = [mm.group(1).strip()] if mm else []
    r["skill_type"] = "passive" if "Passive" in s else ("active" if re.search(r"คูลดาวน์|MP", s) else None)
    evo = section(md, "Evolution A / B (เปิดที่สกิล Lv 5)") or section(md, "Evolution A / B")
    if evo: r["properties"]["evolutions"] = [plain(l) for l in evo.split("\n") if l.startswith("ทางเลือก")]
    bp = section(md, "Breakpoint")
    if bp: r["properties"]["breakpoints"] = [plain(l) for l in bp.split("\n") if l.strip()]
    lvt = next((t for t in r["tables"] if t["header"] and t["header"][0] == "Lv"), None)
    if lvt: r["properties"]["per_level"] = [dict(zip(lvt["header"], x)) for x in lvt["rows"]]
    skills.append(r)
dump("skills.json", skills, "All 129 skills. classes = job pages that link the skill. per_level = 'ค่าตามเลเวลสกิล' table rows verbatim. Evolution/Breakpoint lines verbatim.")

# ---------- pets ----------
pets_md = pages["/systems/pets"]["md"]
pet_list = {u: (rar, plain(txt)) for txt, rar, u in re.findall(r"\[\*\*([^\]]+?)(Legendary|Epic|Rare|Common)\]\((/pet/[^)]+)\)", pets_md)}
pets = []
for p, (rar, txt) in sorted(pet_list.items()):
    r = detail(base_rec(p, "pet"), p); r["tier"] = rar
    r["listing_text"] = txt.strip(); r["listing_source"] = BASE + "/systems/pets"
    if not r["name"]: r["name"] = txt.split(" ")[0]
    pets.append(r)
dump("pets.json", pets, "All 31 pets from /systems/pets (rarity + bonus text). Legendary/Epic have detail-page data; Rare/Common are listing_table_only by user scope.")

# ---------- maps, classes, npcs ----------
maps_ = [detail(base_rec(p, "map"), p) for p in sorted(k for k in pages if k.startswith("/map/"))]
for r in maps_:
    md = pages["/map/" + r["slug"]]["md"]
    r["monsters"] = sorted(set(re.findall(r"\]\((/mob/[^)\s]+)\)", section(md, "มอนสเตอร์") or "")))
dump("maps.json", maps_, "All 55 maps. summary_text holds level range / EXP cap / exits / matchup notes verbatim.")
classes = [detail(base_rec(p, "class"), p) for p in sorted(k for k in pages if k.startswith("/job/"))]
for r in classes: r["skills"] = [s for s, cl in skill_classes.items() if r["slug"] in cl]
dump("classes.json", classes, "8 classes (Binder/novice + 7). Class trait, resource mechanic and recommended pets are in tables/summary_text; full text in Classes/*.md.")
npcs = [detail(base_rec(p, "npc"), p) for p in sorted(k for k in pages if k.startswith("/npc/"))]
dump("npcs.json", npcs, "All 71 NPCs.")

# ---------- system pages: table dumps ----------
def sysdump(name, paths, note):
    out = []
    for p in paths:
        r = base_rec(p, "system_page"); r["tables"] = tabs_plain(pages[p]["md"]); r["summary_text"] = section(pages[p]["md"], "ตอบให้ก่อน"); out.append(r)
    dump(name, out, note)
sysdump("affixes.json", ["/systems/affix"], "Affix & Reroll page: every affix table (tier ranges per affix family) verbatim. Per-item affix pools for tier-10 gear are in weapons.json/equipment.json tables.")
sysdump("stats.json", ["/systems/stats", "/systems/statuses"], "Stat effects per point, stat cost, combat caps, unlocks, EXP / Job EXP tables; status effects.")
sysdump("blacksmith.json", ["/systems/smith", "/systems/refine", "/systems/crafting", "/systems/uniques", "/systems/weapon-rules"], "Infusion, Inscription, Pact (smith), Refine table, Craft recipes, Uniques, weapon Property/Focused/Grip rules.")
sysdump("combat_mechanics.json", ["/systems/class-resources", "/systems/classes", "/systems/threats"], "Class resources (Rage/Combo/Mark...), class traits & dash, per-map monster threat traits.")
sysdump("region_sets.json", ["/systems/region-sets"], "Region Set bonuses.")
sysdump("game_systems.json", sorted(k for k in pages if k.startswith("/systems/") and k.split("/")[-1] not in SYSMAP and k != "/systems/affix") + ["/cards", "/glossary"], "Remaining system pages (shop, pass, premium, auto, gathering, pvp, social, events, rules, windows, fashion, gem-exchange) plus card rules and glossary.")

print("organized md files:", len(written))
