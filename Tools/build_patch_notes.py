"""Build Patch_Notes pages + Structured_Data/patch_notes.json from user-provided patch texts, and add patch notices
to affected organized files. Wiki text is never edited: one notice block (covering all patches) is inserted after each
file's header. Run after organize.py. Idempotent. To add a patch: save its verbatim text in Patch_Notes/_source/, then
append an entry to PATCHES below (id, received date, provenance, map of entry index -> (system, files, note))."""
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# entry index (1-based, in source order) -> (system, affected KB files, wiki comparison note)
MAP_0 = {
 1: ("Maps", ["Maps/_All_Maps.md"], "[TO_VERIFY] Which 28 maps form the 'first continent' is not named in the patch; map sizes and spawn layouts on the Wiki may predate this change."),
 2: ("Maps", ["Maps/_All_Maps.md"], "Channel counts / spawn spread: not compared."),
 3: ("Monsters (AI)", ["Monsters/_All_Monsters.md"], "No Wiki statement found to compare."),
 4: ("Maps", ["Maps/_All_Maps.md"], "No Wiki statement found to compare."),
 5: ("Server", [], "Not a game-data change."),
 6: ("UI", ["Game_Systems/shop.md", "Game_Systems/premium.md", "Game_Systems/pass.md", "Game_Systems/social.md", "Game_Systems/windows.md"], "Performance fix; no data impact."),
 7: ("Fashion", ["Game_Systems/fashion.md", "Items/_Listings/fashion.md", "Game_Systems/shop.md"], "CONFLICT-LIKELY: Wiki crawl (2026-11-07) lists 69 fashion items; the 106 new items are not in this knowledge base."),
 8: ("Fashion / Dye", ["Game_Systems/fashion.md", "Items/_Listings/mat.md"], "Wiki dye item text describes hair/outfit colour; hat/weapon dyeing is new per patch."),
 9: ("Fashion / Mounts", ["Game_Systems/fashion.md", "Items/_Listings/fashion.md", "Game_Systems/shop.md"], "CONFLICT: Wiki states mount run speed '+15%'; patch states 50% (was 15%). Patch is newer."),
 10: ("Bank", ["Game_Systems/rules.md"], "New UI feature; Wiki Bank rules otherwise unaffected."),
 11: ("Social", ["Game_Systems/social.md"], "New feature."),
 12: ("Social / Profile", ["Game_Systems/social.md", "Game_Systems/windows.md"], "New feature."),
 13: ("Guild War", ["Game_Systems/pvp.md", "Game_Systems/social.md"], "No Wiki statement found to compare."),
 14: ("Guild War", ["Game_Systems/pvp.md"], "No Wiki statement found to compare."),
 15: ("Class: Warrior (PvP)", ["Classes/Warrior.md", "Skills/Warrior/rend.md", "Skills/Warrior/gash.md"], "PvP trait changes; Wiki class traits may predate this patch."),
 16: ("Class: Warrior (PvP)", ["Classes/Warrior.md"], "PvP trait change."),
 17: ("Class: Warrior (PvP)", ["Classes/Warrior.md"], "PvP trait change."),
 18: ("Class: Rogue (PvP)", ["Classes/Rogue.md", "Skills/Rogue/assassinate.md"], "PvP trait change."),
 19: ("Class: Rogue (PvP)", ["Classes/Rogue.md", "Skills/Rogue/fade.md"], "PvP trait change."),
 20: ("Class: Rogue (PvP)", ["Classes/Rogue.md"], "PvP trait change."),
 21: ("Class: Mage (PvP)", ["Classes/Mage.md"], "New PvP trait. Note: on the Wiki 'Frost Nova' is also the name of Nova's Evolution A (Skills/Mage/nova.md) — different mechanic."),
 22: ("Class: Scout (PvP)", ["Classes/Scout.md"], "PvP trait change."),
 23: ("Class: Scout (PvP)", ["Classes/Scout.md"], "PvP trait change."),
 24: ("Class: Scout (PvP)", ["Classes/Scout.md"], "PvP trait change."),
 25: ("Affixes", ["Affixes/affix.md", "Classes/Scout.md"], "[TO_VERIFY] DEX on armor/boots/headgear is new per patch; the tier-10 per-item affix pools in this KB may not include it yet."),
 26: ("Class: Acolyte (PvP)", ["Classes/Acolyte.md"], "PvP rule change."),
 27: ("Class: Acolyte (PvP)", ["Classes/Acolyte.md", "Skills/Warrior/rend.md", "Skills/Warrior/gash.md", "Skills/Rogue/assassinate.md"], "Grouping under Acolyte follows the bullet layout of the source text [INFERENCE]; the effect itself names Rend, Gash, Assassinate."),
 28: ("Class: Summoner", ["Classes/Summoner.md", "Combat_Mechanics/class-resources.md"], "Class resource rule change."),
 29: ("Unique item", ["Equipment/oathbound_band.md", "Blacksmith/uniques.md"], "CONFLICT-LIKELY: Wiki shows Oathbound Band as 'ATK +10% · MATK +10% · Block +5%' with Twin Oath; the patch adds MATK = ATK and INT = STR."),
 30: ("Bug fix: Fear status", ["Combat_Mechanics/statuses.md"], "Bug fix."),
 31: ("Bug fix: class change", ["Classes/_All_Classes.md"], "Bug fix."),
 32: ("Bug fix: PvP", ["Game_Systems/pvp.md"], "Bug fix."),
 33: ("Bug fix: PvP lifesteal", ["Game_Systems/pvp.md"], "Bug fix."),
 34: ("Bug fix: Soulforge", [], "[UNKNOWN] 'Soulforge' does not appear anywhere in the crawled Wiki."),
 35: ("Bug fix: monster spawn", ["Monsters/gate_brute.md", "Monsters/golden_sentinel.md"], "Bug fix (spawn restored)."),
 36: ("Cards / World Boss", ["Monsters/world-boss.md", "Cards/Cards_and_Spirits.md"], "Card delivery change."),
}

MAP_1 = {
 1: ("Server", [], "Not a game-data change."),
 2: ("PvP", ["Game_Systems/pvp.md"], "CONFLICT: Wiki says a single hit deals at most 40% of the target's max HP and at most 40% within 1 second. The patch removes the damage cap."),
 3: ("Stats / PvP", ["Stats/stats.md", "Game_Systems/pvp.md"], "CONFLICT: Wiki says armour reduces player damage by at most 40% in PvP; the patch makes PvP defence work like PvE. New base HP values are not in the patch, so HP numbers on the Wiki may be outdated [UNKNOWN new values]."),
 4: ("Monsters (Mini-boss)", ["Monsters/_All_Monsters.md", "Maps/_All_Maps.md"], "No Wiki statement found to compare."),
 5: ("Equipment / Nacreon", ["Region_Sets/region-sets.md", "Cards/Cards_and_Spirits.md", "Items/_Listings/gear.md", "Items/_Listings/look.md"], "NEW CONTENT NOT IN KB: the Tidebound gear and the 24 new headgear/face/mouth items are not in the 2026-11-07 crawl. On the Wiki, 'Tidebound' is the name of the Nacreon card set (Cards_and_Spirits.md), and the Region Set page lists 12 sets for Regions A–D only. [TO_VERIFY] whether the new Tidebound gear is a Region Set."),
 6: ("Cards / Codex", ["Cards/Cards_and_Spirits.md"], "New feature. The Wiki describes duplicate cards only as upgrade material (merged at 100% value); clearing/refunding them and feeding them to the Codex is new."),
 7: ("Fashion / Dye", ["Game_Systems/fashion.md"], "Extends patch_received_2026-11-07 #8 (hat/weapon dyeing) to every fashion piece, including glow."),
 8: ("Minimap / AUTO", ["Game_Systems/auto.md", "Game_Systems/windows.md"], "Display change. [TO_VERIFY] may affect the Duskhunter Region Set 2-piece minimap bonus (Region_Sets/region-sets.md)."),
 9: ("Bug fix: boss respawn timer", ["Monsters/_All_Monsters.md", "Monsters/world-boss.md"], "Bug fix (display only)."),
 10: ("Maps", ["Maps/_All_Maps.md"], "Spawn layouts on the Wiki may predate this change."),
 11: ("Event: top-up", ["Game_Systems/events.md", "Game_Systems/shop.md"], "Time-limited event, 9–15 Nov 2026 (2569 BE). Separate from the shop's permanent first-purchase ×2 bonus on the Wiki."),
}

PATCHES = [
 {"id": "patch_received_2026-11-07", "title": "Patch notes — received 2026-11-07", "received": "2026-11-07",
  "posted": None, "build": None, "header_lines": 1, "bullet_grouping": True,
  "provenance": ("Official Binder Town Discord announcement posted by a game admin (per the user, who copied it into chat on 2026-11-07). "
                 "Exact post date/link not archived here. Not present on the Wiki (no patch-notes page)."),
  "map": MAP_0},
 {"id": "patch_2026-11-08_build-20261108-135133", "title": "Patch notes — 8 Nov 2026 (build 20261108-135133)", "received": "2026-11-08",
  "posted": "8 พ.ย. 2569 20:53 (= 2026-11-08 20:53, time zone not stated)", "build": "20261108-135133", "header_lines": 0, "footer_lines": 1,
  "bullet_grouping": False,
  "provenance": ("Update announcement pasted by the user into chat on 2026-11-08 (same official source as the previous patch per the user's context; "
                 "channel/link not archived) [TO_VERIFY]. Footer of the post: '8 พ.ย. 2569 20:53 · build 20261108-135133'. Not present on the Wiki."),
  "map": MAP_1},
]

def esc(s): return s.replace("|", "\\|")
all_entries, by_file = [], {}
for P in PATCHES:
    pid, MAP = P["id"], P["map"]
    lines = [l.rstrip("\n") for l in open(f"{ROOT}/Patch_Notes/_source/{pid}.txt", encoding="utf-8") if l.strip()]
    raw_entries = lines[P.get("header_lines", 0): len(lines) - P.get("footer_lines", 0)]
    entries, group = [], None
    for i, l in enumerate(raw_entries, 1):
        top = l.startswith("•  ") if P["bullet_grouping"] else True   # patch 1: double space after bullet = new topic
        text = re.sub(r"^\s*•?\s*", "", l)
        if top or group is None: group = text
        system, files, note = MAP[i]
        entries.append({"id": f"{pid}#{i}", "patch_id": pid, "index": i, "text_verbatim": text, "source_line": l,
                        "topic_line": group, "is_topic_line": top or i == 1, "system": system,
                        "affected_kb_files": [f for f in files if os.path.exists(f"{ROOT}/{f}")],
                        "missing_kb_files": [f for f in files if not os.path.exists(f"{ROOT}/{f}")],
                        "wiki_comparison": note, "verification_status": "PATCH", "provenance": P["provenance"]})
    assert len(entries) == len(MAP), (pid, len(entries), len(MAP))
    P["entries"] = entries; all_entries += entries
    for e in entries:
        for f in e["affected_kb_files"]: by_file.setdefault(f, []).append(e)
    flag = ("CONFLICT", "NEW CONTENT", "[UNKNOWN]", "[TO_VERIFY]")
    md = [f"# {P['title']}", "",
          f"> **Status:** [PATCH] · **Received:** {P['received']}" + (f" · **Posted:** {P['posted']}" if P.get("posted") else "") +
          (f" · **Build:** {P['build']}" if P.get("build") else "") + "  ",
          f"> **Provenance:** {P['provenance']}  ",
          f"> **Verbatim source:** [_source/{pid}.txt](_source/{pid}.txt)  ",
          "> **Comparison basis:** wiki_comparison is a historical audit against the 2026-11-07 crawl, not a claim that every conflict remains after the 2026-11-08 snapshot merge. Check Sources/DATA_FRESHNESS.json for current page dates.", "",
          "## Conflicts / items needing attention", ""]
    for e in entries:
        if e["wiki_comparison"].startswith(flag) or "CONFLICT" in e["wiki_comparison"] or "[TO_VERIFY]" in e["wiki_comparison"]:
            md.append(f"- **#{e['index']}** {e['text_verbatim']} — {e['wiki_comparison']}")
    md += ["", "## All changes", "", "| # | Change (verbatim) | Topic | System | Affected KB files | Historical comparison (2026-11-07) |", "|---|---|---|---|---|---|"]
    for e in entries:
        fl = " · ".join(f"[{os.path.basename(f)}](../{f})" for f in e["affected_kb_files"]) or "—"
        md.append(f"| {e['index']} | {esc(e['text_verbatim'])} | {'—' if e['is_topic_line'] else esc(e['topic_line'][:40])} | {e['system']} | {fl} | {esc(e['wiki_comparison'])} |")
    open(f"{ROOT}/Patch_Notes/{pid}.md", "w", encoding="utf-8").write("\n".join(md) + "\n")

os.makedirs(f"{ROOT}/Structured_Data", exist_ok=True)
json.dump({"_about": "Patch notes from official game announcements (copied by the user). Each entry is verbatim. topic_line groups continuation bullets under the preceding "
           "topic per the source's bullet indentation [INFERENCE for grouping only]. Wiki data is NOT modified; wiki_comparison is the historical 2026-11-07 audit. Refreshed pages may already resolve entries; inspect page dates. "
           "Later patches are newer than earlier ones.",
           "patches": [{k: P.get(k) for k in ("id", "title", "received", "posted", "build", "provenance")} | {"count": len(P["entries"])} for P in PATCHES],
           "count": len(all_entries), "records": all_entries},
          open(f"{ROOT}/Structured_Data/patch_notes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

rows = "".join(f"| [{P['id']}]({P['id']}.md) | {P['received']} | {P.get('posted') or 'not recorded'} | {P.get('build') or '—'} | {len(P['entries'])} |\n" for P in PATCHES)
open(f"{ROOT}/Patch_Notes/README.md", "w", encoding="utf-8").write(
    "# Patch Notes\n\nThe Wiki (https://wiki.bindertowngame.com/) has **no patch-notes page** (checked 2026-11-07). Patch notes here are added from official announcements "
    "copied by the user and labelled [PATCH] with their provenance. **Use dated sources: historical comparisons refer to the 2026-11-07 crawl; refreshed Wiki pages may incorporate these changes.**\n\n"
    "| Patch | Received | Posted | Build | Entries |\n|---|---|---|---|---|\n" + rows + "\n"
    "Structured form: [../Structured_Data/patch_notes.json](../Structured_Data/patch_notes.json). "
    "Verbatim text: `_source/`. Affected organized files carry a `Patch notice` block linking back here; Wiki text itself is not edited.\n")

# ---- notices in affected files (one block per file, grouped by patch, newest first) ----
START, END = "<!-- PATCH-NOTICES:START -->", "<!-- PATCH-NOTICES:END -->"
title = {P["id"]: P for P in PATCHES}
for f, es in by_file.items():
    path = f"{ROOT}/{f}"; t = open(path, encoding="utf-8").read()
    t = re.sub(rf"\n?{re.escape(START)}.*?{re.escape(END)}\n?", "\n", t, flags=re.S)
    page_date = re.search(r"Last crawled:\*\* ([0-9-]+)", t)
    page_date = page_date.group(1) if page_date else "unknown"
    block = [START, f"> **Patch reference [PATCH]** — Wiki page captured {page_date}. Comparisons below were originally audited against 2026-11-07; refreshed pages may already incorporate them.", ">"]
    for P in reversed(PATCHES):
        pe = [e for e in es if e["patch_id"] == P["id"]]
        if not pe: continue
        rel = os.path.relpath(f"{ROOT}/Patch_Notes/{P['id']}.md", os.path.dirname(path)).replace(os.sep, "/")
        block.append(f"> **[{P['title']}]({rel})**")
        for e in pe:
            c = e["wiki_comparison"]
            block.append(f"> - #{e['index']}: {e['text_verbatim']}" + (f" — *{c}*" if c.startswith(("CONFLICT", "NEW CONTENT")) else ""))
        block.append(">")
    block[-1] = END
    t = t.replace("\n---\n", "\n" + "\n".join(block) + "\n\n---\n", 1)
    t = re.sub(r"\n{3,}(?=<!-- PATCH-NOTICES:START)", "\n\n", t, count=1)   # keep reruns idempotent
    open(path, "w", encoding="utf-8").write(t)
print(f"patches {len(PATCHES)} | entries {len(all_entries)} | files with notices {len(by_file)} | missing files {sorted({m for e in all_entries for m in e['missing_kb_files']})}")
