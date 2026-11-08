# DATA_COVERAGE — completeness audit (Phase 8)

- **Audit date:** 2026-11-07
- **Basis:** local files only. Counts are compared with the Wiki's own counters (home page: "อาชีพ 8 · สกิล 129 · ไอเท็ม 1,771 · มอน 160 · แมพ 55" and each listing's "แสดง X จาก X").

**This knowledge base is NOT 100% complete.** Detail pages for about 68% of item URLs were deliberately deferred by the user. All non-item categories are complete.

## Audit checks

| Check | Result |
|---|---|
| Every discovered URL has a crawl status | ✅ 2,284/2,284 (`Sources/URL_MANIFEST.csv`) |
| Every successful crawl has a saved original file | ✅ 726/726 (`raw_file` column verified to exist) |
| Every organized page shows its source URL | ✅ 722/722 (header `> **Source:**`) |
| Numeric values preserved, raw → organized | ✅ every number token in the 722 raw pages is present in the organized files (automated comparison, 0 missing) |
| Tables preserved | ✅ organized files keep the full markdown tables; JSON keeps every table as header + rows (verbatim cell text) |
| Listing vs detail consistency (tier-10 ATK/MATK/DEF/slot) | ✅ 122 values compared, 0 conflicts |
| Skills / equipment not merged | ✅ one record per URL; variants (e.g. `_keen`, `_quickdraw`, `_weighted`, `_alt`) are separate records |
| Tiers / levels distinguished | ✅ each gear record has its own `tier` (ขั้น 1–10) and `level`; never combined |
| Internal links | ✅ 17,934 relative links, 0 broken. Links to un-crawled pages point to the live Wiki URL. |
| Failed URLs documented | ✅ none failed |

## Coverage by category

| Category | Wiki count | Detail pages saved | Status |
|---|---|---|---|
| Classes (`Classes/`) | 8 | 8 | ✅ Complete |
| Skills (`Skills/`) | 129 | 129 | ✅ Complete (all 8 classes) |
| Monsters (`Monsters/`) | 160 | 160 | ✅ Complete (+ bosses, world-boss pages) |
| Cards (`Cards/`) | 160 monster cards | 160 (from monster pages) | ✅ ★1 and ★5 complete. **[UNKNOWN] ★2–★4:** the Wiki does not list those values per card. |
| Maps (`Maps/`) | 55 | 55 | ✅ Complete |
| NPCs (`Game_Systems/NPCs/`) | 71 | 71 | ✅ Complete |
| Stats (`Stats/`) | — | stats + statuses pages | ✅ Complete |
| Combat mechanics (`Combat_Mechanics/`) | — | class resources, traits/dash, threats, statuses, weapon rules | ✅ Complete |
| Affixes (`Affixes/`) | — | `/systems/affix` (53 tables) + per-item affix pools on tier-10 gear | ✅ Affix system complete. Per-item pools exist only for tier-10 items. |
| Blacksmith (`Blacksmith/`) | — | smith (Infusion, Inscription, Pact), refine, crafting, uniques | ✅ Complete. Reforge: no page named "Reforge" exists; the Affix **Reroll** at the smith is on `Affixes/affix.md` [TO_VERIFY whether "Reforge" means Reroll]. |
| Region Sets (`Region_Sets/`) | — | 1 page | ✅ Complete |
| Game systems & guides | — | 15 system pages, 7 guides, glossary, home | ✅ Complete |
| Pets (`Pets/`) | 31 | 14 (Legendary 10, Epic 4) | ⚠️ Partial: Rare 8 / Common 9 have listing data only (bonus text, rarity) |
| Weapons (`Weapons/`) | 334 | 37 tier-10 + 3 unlisted `_alt` variants [TO_VERIFY] + 1 sample (iron_sword, tier 2) | ⚠️ Partial: tiers 1–9 listing data only |
| Equipment (`Equipment/`) | 668 gear + 331 headgear | 69 gear + 54 headgear (tier 10) | ⚠️ Partial: tiers 1–9 listing data only |
| Materials (`Items/Materials/`) | 157 | 62 key materials | ⚠️ Partial: basic gathering mats, gathering tools, cosmetic tickets → listing only |
| Consumables (`Items/Consumables/`) | 49 | 4 top-tier | ⚠️ Partial: all 49 effects are in the listing table; detail (sources, crafting) only for 4 |
| Monster drops | 160 | 0 | ⚠️ Excluded by user (vendor items, empty effect column); drop chances are on each monster page |
| Fashion (Cash) | 69 | 0 | ⚠️ Deferred; listing data only |
| Patch notes (`Patch_Notes/`) | — | 2 user-provided patches (47 entries) | ⚠️ The Wiki has no patch-notes page. 2 patches added (47 entries): official Discord admin announcement (received 2026-11-07) and update of 8 Nov 2026 (build 20261108-135133). 38 affected files carry a notice. |

## What "listing data only" contains

| Group | Listing columns preserved |
|---|---|
| Gear / headgear | name, slot, Lv, tier, ATK, MATK, DEF, NPC sell price (Normal) |
| Materials / consumables / drops / fashion | name, effect text, NPC sell price |
| Pets | name, Thai name, bonus, rarity |

Missing for deferred items: drop sources and rates, crafting recipes, refine cost, sell price by rarity, equippable classes, stat bonus lines, per-item affix pools.

## Data requiring manual verification

| Item | Label | Note |
|---|---|---|
| 4 orphan pages (`greatsword_t4_alt`, `bow_t4_alt`, `dagger_t10_alt`, `remnant_shard`) | [TO_VERIFY] | **Soft-404:** HTTP 200, but the page shows only the generic item index (no item data). Not linked from any listing. Firecrawl Map's cached title suggests removed items. Treat as non-existent. |
| Card ★2–★4 values | [UNKNOWN] | Not stated per card |
| "Reforge" system | [TO_VERIFY] | No page with this name; closest is Affix Reroll at the smith |
| Wiki claim "ดึงจากโค้ดเกมโดยตรง ตัวเลขตรงกับในเกม" | [WIKI] claim | Not independently verified |
| Monster single-level stats | note | 63 monsters (mostly Elite/boss) have no per-level table; their EXP / HP / damage are in `summary_text` |
| 3 universal passives (`keen_edge`, `light_step`, `tough_skin`) | note | Linked from all 8 class pages; filed under `Skills/Binder/` |

## Source conflicts

- **Wiki vs Wiki:** none. Listing and detail values agree for all compared fields.
- **Wiki vs patch (received 2026-11-07):** mount speed (+15% on the Wiki vs 50% in the patch); Oathbound Band (patch adds MATK = ATK, INT = STR); fashion count (69 on the Wiki vs 106 new in the patch). Both versions are kept: Wiki text unchanged, patch in `Patch_Notes/`. See [Patch_Notes/patch_received_2026-11-07.md](Patch_Notes/patch_received_2026-11-07.md).
- **Wiki vs patch (8 Nov 2026, build 20261108-135133):** PvP damage cap (Wiki: ≤40% max HP per hit and per second) removed; PvP armour cap (Wiki: ≤40%) replaced by PvE-style defence; base HP raised (new values [UNKNOWN]). **New content not in this KB:** Tidebound sea-themed gear and 24 new headgear/face/mouth items (Nacreon only). See [Patch_Notes/patch_2026-11-08_build-20261108-135133.md](Patch_Notes/patch_2026-11-08_build-20261108-135133.md).
