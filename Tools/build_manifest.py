"""Build Sources/URL_MANIFEST.csv from discovery state (no network)."""
import json, csv, os, glob, urllib.parse as up
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
st = json.load(open(f"{ROOT}/Progress/discovery_state.json"))
mp = {l["url"].rstrip("/"): l for l in json.load(open(f"{ROOT}/Progress/map_raw.json"))["data"]["links"]}
titles = {}
for f in glob.glob(f"{ROOT}/Progress/discovery_scrapes/*.json"):
    d = json.load(open(f)); d = d.get("data", d); m = d.get("metadata", {})
    u = (m.get("sourceURL") or m.get("url") or "").rstrip("/")
    titles[os.path.basename(f)[:-5]] = (m.get("title"), m.get("statusCode"))
ALIAS = {"/skills": "/jobs", "/refine": "/systems/refine", "/skills/novice": "/job/novice", "/gem-exchange": "/systems/gem-exchange"}
CAT = {"item": "Items", "mob": "Monsters", "skill": "Skills", "npc": "NPCs", "map": "Maps", "pet": "Pets", "job": "Classes",
       "items": "Items (listing)", "guide": "Guides", "systems": "Game_Systems", "mobs": "Monsters (listing)", "maps": "Maps (listing)",
       "jobs": "Classes (listing)", "skills": "Skills (listing)", "cards": "Cards", "glossary": "Glossary", "refine": "Blacksmith",
       "gem-exchange": "Game_Systems", "npcs": "NPCs (listing)", "": "Home"}
ORPHAN = {"/item/greatsword_t4_alt", "/item/bow_t4_alt", "/item/dagger_t10_alt", "/item/remnant_shard"}
hubs = {h.rstrip("/") for h in st["hubs_scraped"]}
rows = []
for u, src in sorted(st["found"].items()):
    path = up.urlparse(u).path or "/"
    seg = path.strip("/").split("/")[0]
    key = path.strip("/").replace("/", "__") or "_root"
    t, code = titles.get(key, (None, None))
    if not t and u in mp: t = mp[u].get("title")
    linked = [s for s in src if s != "MAP"]
    notes = []
    if path in ALIAS: notes.append(f"identical content to {ALIAS[path]}")
    if path in ORPHAN: notes.append("found only by Map; not linked from any listing page")
    rows.append({"url": u, "path": path, "category": CAT.get(seg, seg), "page_type": "hub" if u in hubs else "detail",
        "title": t or "", "found_by_map": "yes" if "MAP" in src else "no", "linked_from_hubs": len(linked),
        "duplicate_of": ("https://wiki.bindertowngame.com" + ALIAS[path]) if path in ALIAS else "",
        "crawl_status": "scraped_during_discovery" if u in hubs else ("crawled" if os.path.exists(f"{ROOT}/Progress/page_cache/{key}.json") else "deferred_by_user_scope"),
        "raw_file": (f"Raw/Original_Wiki_Pages/{key.split('__')[0] if '__' in key else '_hub'}/{key}.md") if (u in hubs or os.path.exists(f"{ROOT}/Progress/page_cache/{key}.json")) else "",
        "http_status": code or "", "notes": "; ".join(notes)})
with open(f"{ROOT}/Sources/URL_MANIFEST.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), "rows")
