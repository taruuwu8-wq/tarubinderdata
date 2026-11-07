"""Build Progress/crawl_queue.csv: the approved Phase-4 page list (user-scoped 2026-11-07), in crawl order.
Selection is derived only from already-cached hub pages (no network)."""
import json, re, csv, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "https://wiki.bindertowngame.com"
def hub(n):
    d = json.load(open(f"{ROOT}/Progress/discovery_scrapes/{n}.json")); return d.get("data", d)
def md(n): return re.sub(r"!\[[^\]]*\]\([^)]*\)", "", hub(n)["markdown"])
def table(n):
    out = []
    for l in md(n).split("\n"):
        if l.startswith("| ["):
            c = [x.strip() for x in l.strip("|").split("|")]
            out.append((re.search(r"\]\((https://[^)\s]+)", c[0]).group(1).rstrip("/"), c))
    return out
def links(n, seg): return sorted({l.rstrip("/") for l in hub(n)["links"] if f"/{seg}/" in l})
Q = []
def add(group, urls, rule):
    for u in urls:
        if u not in {q[1] for q in Q}: Q.append((group, u, rule))
pets = re.findall(r"(Legendary|Epic|Rare|Common)\]\((https://[^)]+/pet/[^)]+)\)", md("systems__pets"))
add("1_pets", sorted(u for r, u in pets if r in ("Legendary", "Epic")), "pet rarity Legendary/Epic")
add("2_maps", links("maps", "map"), "all maps")
for j in ["novice", "rogue", "scout", "knight", "acolyte", "mage", "warrior", "summoner"]:
    add("3_skills", links("job__" + j, "skill"), f"skills linked from /job/{j}")
add("4_npcs", links("npcs", "npc"), "all NPCs")
add("5_mobs", links("mobs", "mob"), "all monsters (includes card ★1-★5 data)")
add("6_items_cards", [f"{B}/item/{k}" for k in ("loose_spirit", "spirit_card", "spirit_coin")], "card/spirit items")
add("6_items_orphans", [f"{B}/item/{k}" for k in ("greatsword_t4_alt", "bow_t4_alt", "dagger_t10_alt", "remnant_shard")], "Map-only orphan pages")
add("7_items_gear_t10", [u for u, c in table("items__gear") if c[3] == "ขั้น 10"], "gear tier 10")
add("7_items_look_t10", [u for u, c in table("items__look") if c[3] == "ขั้น 10"], "headgear tier 10")
IMP = re.compile(r"/item/(essence_|core_|.*_core$|refine_ward|repair|hone_stone|scribe_ink|bindmark|unique_shard)")
mats = table("items__mat")
add("8_items_mat_key", [u for u, c in mats if IMP.search(u) or "Core" in c[0] or "ยันต์กันลดขั้น" in c[0] or "ชุดซ่อม" in c[0]], "key materials (essence/core/ward/repair/hone/ink/bindmark/unique shard)")
add("9_items_use_top", [f"{B}/item/{k}" for k in ("sovereign_elixir", "sovereign_ether", "spirit_feast", "sanctum_lotus_feast")], "top potions/food")
with open(f"{ROOT}/Progress/crawl_queue.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["order", "group", "url", "selection_rule"])
    for i, (g, u, r) in enumerate(Q, 1): w.writerow([i, g, u, r])
import collections; print(len(Q), collections.Counter(q[0] for q in Q))
