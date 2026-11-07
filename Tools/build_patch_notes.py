"""Build Patch_Notes pages + Structured_Data/patch_notes.json from user-provided patch text, and add patch notices
to affected organized files. Wiki text is never edited: a notice block is inserted after each file's header.
Run after organize.py. Idempotent."""
import os, re, json, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATCH_ID = "patch_received_2026-11-07"
SRC = f"{ROOT}/Patch_Notes/_source/{PATCH_ID}.txt"
PROVENANCE = ("Official Binder Town Discord announcement posted by a game admin (per the user, who copied it into chat on 2026-11-07). "
              "Exact post date/link not archived here. Not present on the Wiki (no patch-notes page).")

# entry index (1-based, in source order) -> (system, affected KB files, wiki comparison note)
MAP = {
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

lines = [l.rstrip("\n") for l in open(SRC, encoding="utf-8") if l.strip()]
header, raw_entries = lines[0], lines[1:]
entries, group = [], None
for i, l in enumerate(raw_entries, 1):
    top = l.startswith("•  ")                      # double space after bullet = new topic in the source layout
    text = re.sub(r"^•\s+", "", l)
    if top or group is None: group = text
    system, files, note = MAP[i]
    entries.append({"id": f"{PATCH_ID}#{i}", "index": i, "text_verbatim": text, "source_line": l,
                    "topic_line": group, "is_topic_line": top or i == 1, "system": system,
                    "affected_kb_files": [f for f in files if os.path.exists(f"{ROOT}/{f}")],
                    "missing_kb_files": [f for f in files if not os.path.exists(f"{ROOT}/{f}")],
                    "wiki_comparison": note, "verification_status": "PATCH",
                    "provenance": PROVENANCE})
assert len(entries) == len(MAP), (len(entries), len(MAP))

os.makedirs(f"{ROOT}/Structured_Data", exist_ok=True)
json.dump({"_about": "Patch notes from the official Discord (admin post, copied by the user). Each entry is verbatim. topic_line groups continuation bullets under the preceding "
           "topic per the source's bullet indentation [INFERENCE for grouping only]. Wiki data is NOT modified; conflicts are listed in wiki_comparison.",
           "patch_id": PATCH_ID, "provenance": PROVENANCE, "count": len(entries), "records": entries},
          open(f"{ROOT}/Structured_Data/patch_notes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def esc(s): return s.replace("|", "\\|")
md = [f"# Patch notes — received 2026-11-07", "",
      f"> **Status:** [PATCH] · **Provenance:** {PROVENANCE}  ",
      f"> **Verbatim source:** [_source/{PATCH_ID}.txt](_source/{PATCH_ID}.txt)  ",
      "> **Precedence:** where this patch contradicts Wiki text crawled on 2026-11-07, the patch is newer. The Wiki text is kept unchanged; affected files carry a notice.", "",
      "## Conflicts / items needing attention", ""]
for e in entries:
    if e["wiki_comparison"].startswith(("CONFLICT", "[UNKNOWN]", "[TO_VERIFY]")):
        md.append(f"- **#{e['index']}** {e['text_verbatim']} — {e['wiki_comparison']}")
md += ["", "## All changes", "", "| # | Change (verbatim) | Topic | System | Affected KB files | Wiki comparison |", "|---|---|---|---|---|---|"]
for e in entries:
    files = " · ".join(f"[{os.path.basename(f)}](../{f})" for f in e["affected_kb_files"]) or "—"
    md.append(f"| {e['index']} | {esc(e['text_verbatim'])} | {'—' if e['is_topic_line'] else esc(e['topic_line'][:40])} | {e['system']} | {files} | {esc(e['wiki_comparison'])} |")
open(f"{ROOT}/Patch_Notes/{PATCH_ID}.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
open(f"{ROOT}/Patch_Notes/README.md", "w", encoding="utf-8").write(
    "# Patch Notes\n\nThe Wiki (https://wiki.bindertowngame.com/) has **no patch-notes page** (checked 2026-11-07). Patch notes here are added from other sources and labelled [PATCH] with their provenance.\n\n"
    f"| Patch | Received | Entries | Provenance |\n|---|---|---|---|\n| [{PATCH_ID}]({PATCH_ID}.md) | 2026-11-07 | {len(entries)} | official Discord (admin post), copied by user; exact post date not recorded |\n\n"
    "Structured form: [../Structured_Data/patch_notes.json](../Structured_Data/patch_notes.json). "
    "Verbatim text: `_source/`. Affected organized files carry a `Patch notice` block linking back here; Wiki text itself is not edited.\n")

# ---- notices in affected files ----
by_file = {}
for e in entries:
    for f in e["affected_kb_files"]: by_file.setdefault(f, []).append(e)
START, END = "<!-- PATCH-NOTICES:START -->", "<!-- PATCH-NOTICES:END -->"
for f, es in by_file.items():
    path = f"{ROOT}/{f}"; t = open(path, encoding="utf-8").read()
    t = re.sub(rf"\n?{re.escape(START)}.*?{re.escape(END)}\n?", "\n", t, flags=re.S)
    rel = os.path.relpath(f"{ROOT}/Patch_Notes/{PATCH_ID}.md", os.path.dirname(path))
    block = [START, "> ⚠️ **Patch notice [PATCH]** — a later patch (official Discord announcement, received 2026-11-07) changes this topic. "
             f"The Wiki text below may be outdated. See [{PATCH_ID}]({rel}).", ">"]
    for e in es: block.append(f"> - #{e['index']}: {e['text_verbatim']}" + (f" — *{e['wiki_comparison']}*" if e["wiki_comparison"].startswith("CONFLICT") else ""))
    block.append(END)
    t = t.replace("\n---\n", "\n" + "\n".join(block) + "\n\n---\n", 1)
    open(path, "w", encoding="utf-8").write(t)
print(f"entries {len(entries)} | files with notices {len(by_file)} | missing files {sorted({m for e in entries for m in e['missing_kb_files']})}")
