# Snapshot 2026-11-08 — merged on 2026-11-09

- **Fetched:** 2026-11-08, Firecrawl `--max-age 0` (fresh from the live Wiki, no cache; every file has `cacheState` ≠ `hit`).
- **Current status:** 63 hubs and 119 new item pages are merged into the organized KB. Original JSON is unchanged. Existing 663 detail pages remain dated 2026-11-07; see the root MISSING_DATA.md.
- **Status:** [WIKI] captured source, locally organized and audited; not independently verified against the game.

| Folder | Files | Contents |
|---|---|---|
| `hubs/` | 63 | All hub/listing/system/guide/class pages (same set as `Progress/discovery_scrapes/` on 2026-11-07). 33 of them changed. |
| `new_items/` | 119 | Detail pages of items new since 2026-11-07: 95 Tidebound tier-10 gear (`*_t10*_tide`) + 24 tier-10 headgear/face/mouth (Lv 100+). |
| `fresh_hubs.txt` · `fresh_new_items.txt` | — | URL lists used |

Each JSON file is Firecrawl output `{"data": {"markdown", "links", "metadata"}}`; the file name is the URL path with `/` → `__`.

## What changed on the Wiki (hub diff vs 2026-11-07)

- Counts: items 1,771 → 1,996 · gear 1,002 → 1,097 · headgear 331 → 355 · fashion 69 → 175 · maps 55 → 56 · NPCs 71 → 77 · glossary 166 → 167.
- New pages (not fetched): `map/copperbell_arena` (Lv 1–115), 6 arena NPCs (`npc/arena_exit`, `npc/arena_portal_*`), `tools/stats`, 106 new fashion items.
- Changed: monster stats (e.g. Sprout Lv 1–2 HP 249 → Lv 1–3 HP 345), threat table, refine and smith costs, weapon rules (Bow/Crossbow now one-handed; two-handed bonuses changed),
  PvP rules (damage cap removed, DEF same as PvE), new PvP traits on Acolyte/Mage/Rogue/Scout/Warrior pages, market tax, card Codex tiers, statuses, world-boss rewards, affix slots, pass, shop.
- **Not re-fetched:** the 663 detail pages from 2026-11-07 (monsters, maps, skills, NPCs, pets, old tier-10 items, materials). They are likely outdated.

## Merging later (when patches settle)

1. Copy `hubs/*.json` → `Progress/discovery_scrapes/` and `new_items/*.json` → `Progress/page_cache/` (or refetch the hubs fresh).
2. Refresh detail pages with `python3 Tools/refresh_batch.py <urls.txt> Progress/page_cache`, add new URLs to the manifest.
3. Run the rebuild pipeline (README.md → Updating), then `My_Cards/tracker/build.py` and `My_Cards/tracker/UPDATE.md`.
