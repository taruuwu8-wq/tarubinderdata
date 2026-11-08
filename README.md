# Binder Town Wiki — AI Knowledge Base

A file-based, source-traceable copy of the official **Binder Town Wiki** (https://wiki.bindertowngame.com/), organized so AI assistants (Claude, ChatGPT, others) can answer questions without reading the whole Wiki. No database, no app: Markdown, JSON and CSV only.

- **Crawled:** 2026-11-07 (Firecrawl).
- **Language:** the Wiki is in **Thai**. All game text, numbers and terms are kept exactly as written; proper names (classes, maps, monsters, many items) are in English.
- **Coverage:** see [DATA_COVERAGE.md](DATA_COVERAGE.md). Non-item categories are complete. Items are partial: tier-10 gear plus key materials have detail pages; everything else has listing-table data only.

## Layout

| Path | What it holds |
|---|---|
| [INDEX.md](INDEX.md) | Categorized index of every file. **Start here.** |
| [ALL_DATA.md](ALL_DATA.md) | One-file quick-reference tables (skills, pets, cards ★1/★5, monster matchups, tier-10 gear…), linking to full files |
| `Classes/` `Skills/<Class>/` `Monsters/` `Maps/` `Pets/` `Cards/` `Weapons/` `Equipment/` (`Headgear/`) `Items/` | One Markdown file per Wiki page, verbatim text and tables (images removed) |
| `Stats/` `Combat_Mechanics/` `Affixes/` `Blacksmith/` `Region_Sets/` `Game_Systems/` (`Guides/`, `NPCs/`) | System and mechanics pages |
| `Patch_Notes/` | The Wiki has no patch notes; official patches (e.g. Discord announcements) are added here as [PATCH], with notices in affected files |
| [Structured_Data/](Structured_Data/) | JSON and CSV for lookups and filtering (see below) |
| `Raw/Original_Wiki_Pages/` | Unmodified crawl output, one file per URL. Use it as the source of truth. |
| [Sources/](Sources/) | URL manifest (2,284 URLs with crawl status), discovery report, cost estimate, failed URLs |
| [CRAWL_REPORT.md](CRAWL_REPORT.md) · [DATA_COVERAGE.md](DATA_COVERAGE.md) | Crawl statistics; completeness audit and gaps |
| `Tools/` `Progress/` | Scripts and crawl cache for resumable and incremental updates |

Every organized file starts with a header giving **Source URL · Source title · Last crawled · Status · link to the raw original**. Links inside a file point to other files in this knowledge base. Links to pages that were not crawled point to the live Wiki.

## Structured data

| File | Records |
|---|---|
| `classes.json` | 8 classes (incl. Binder/novice) |
| `skills.json` | 129 skills: class, type, unlock, per-level table, Evolution A/B, Breakpoints |
| `monsters.json` | 160 monsters: matchups (element weakness/resistance, DEF/MDEF/FLEE…), stats by level, drop tables |
| `monster_equipment_drops.csv` | 21,955 rows: monster → equipment piece, tier, chance per kill, equip level, classes |
| `cards.json` | 160 monster cards: colour, Spirit Load, ★1 and ★5 effects, soul exchange |
| `weapons.json` · `equipment.json` | All 1,002 gear + 331 headgear (listing values); tier-10 items add detail stats, requirements, drop sources, affix pools, refine table |
| `equipment_all_tiers.csv` | Flat table of all gear/headgear: slot, tier, Lv, ATK, MATK, DEF, sell price |
| `items.json` | Consumables, materials, monster drops, fashion, card items |
| `pets.json` | 31 pets: rarity, bonus; Legendary/Epic have detail data |
| `maps.json` · `npcs.json` | 55 maps, 71 NPCs |
| `affixes.json` · `stats.json` · `blacksmith.json` · `combat_mechanics.json` · `region_sets.json` · `game_systems.json` | System pages as tables (header + rows, verbatim) |

Record fields include `name`, `slug`, `category`, `tier`, `level`, `properties`, `effects`, `requirements`, `conditions`, `related`, `tables`, `summary_text`, `source_url`, `source_title`, `last_crawled`, `kb_file`, `verification_status`, and `data_source` (`detail_page` or `listing_table_only`). Unknown values are `null`; nothing is guessed. A Wiki "—" means not applicable.

## Reliability labels

| Label | Meaning |
|---|---|
| **[WIKI]** | Directly stated by the official Wiki. Applies to all crawled content in this knowledge base. |
| [PATCH] | Stated in patch notes (`Patch_Notes/`, `Structured_Data/patch_notes.json`). Newer than the Wiki crawl where they conflict. Patches so far: official Discord admin announcement (received 2026-11-07, 36 entries) and update of 8 Nov 2026, build 20261108-135133 (11 entries). Newer patches override older ones. |
| [CALCULATED] | Derived from an explicit Wiki formula and documented inputs. The formula and inputs must be shown. |
| [INFERENCE] | Interpretation, not confirmed by the Wiki. Never present it as fact. |
| [UNKNOWN] | The Wiki does not say (e.g. card ★2–★4 values). |
| [TO_VERIFY] | Ambiguous, incomplete or conflicting (e.g. the 4 soft-404 orphan pages). |

Note: the Wiki states its numbers come directly from the game code. That is the Wiki's claim, not independently verified.

## Using it with an AI assistant

**General rules to give the assistant**
1. Read `INDEX.md` (or `ALL_DATA.md`) first to locate the right files. Do not load everything.
2. Answer from the specific files, quote numbers exactly, and cite the `source_url`.
3. If a file shows a ⚠️ Patch notice, the patch overrides the older Wiki text for that point.
4. Label anything not directly stated as [INFERENCE] or [UNKNOWN]. Check `DATA_COVERAGE.md` before saying something does not exist: it may be a deferred page.

**Claude** (Claude Code, Claude Projects, claude.ai)
- *Claude Code:* open this folder and ask questions. Claude can `grep` the files, e.g. `grep -ril "Bulwark" Skills Classes`, or open `Structured_Data/skills.json`.
- *Claude Projects:* upload `README.md`, `INDEX.md`, `ALL_DATA.md` and the category folders or JSON you need. Project knowledge has size limits, so prefer the relevant folders over `Raw/`.

**ChatGPT** (Custom GPT / Projects / file upload)
- Upload `ALL_DATA.md` and the needed `Structured_Data/*.json` or CSV; Code Interpreter can filter JSON/CSV.
- For detailed questions, also upload the relevant category folder (zip it).
- Put the general rules above in the GPT's instructions.

**Other assistants / RAG pipelines:** chunk the organized Markdown files. Each is one Wiki page, and most are under 20 KB. Keep the header lines as metadata.

**Example prompts**
- "Using Skills/Knight/ and skills.json, list every Knight skill with its unlock requirement and Lv 10 value. Cite source URLs."
- "From monsters.json, which monsters are weak to Holy (แสง)? Include the multiplier exactly as written."
- "Which tier-10 weapons can a Scout equip? Use weapons.json `requirements`."

## Updating

See "Incremental updates later" in [CRAWL_REPORT.md](CRAWL_REPORT.md). Crawled pages are cached and never re-fetched unless their cache file is deleted. Organization scripts run locally for free:

```bash
python3 Tools/export_raw.py && python3 Tools/organize.py && python3 Tools/build_patch_notes.py && python3 Tools/build_docs.py
```

Firecrawl commands in this environment need `FIRECRAWL_API_KEY` set (a placeholder is fine when a proxy injects the key) and `NODE_USE_ENV_PROXY=1`.
