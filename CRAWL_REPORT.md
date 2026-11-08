# CRAWL_REPORT — Binder Town Wiki

- **Source:** https://wiki.bindertowngame.com/ (official Wiki, Thai language)
- **Crawl date:** 2026-11-07
- **Tool:** Firecrawl CLI 1.29.0 (`map`, `scrape`, `batch-scrape`; markdown + links formats only)

## Totals

| Metric | Value |
|---|---|
| Unique URLs discovered | **2,284** (see [Sources/URL_DISCOVERY_REPORT.md](Sources/URL_DISCOVERY_REPORT.md)) |
| Pages saved (raw originals) | **726** = 63 hub/listing pages + 663 detail pages |
| Alias URLs (identical content, kept once in organized output) | 4 |
| Failed pages | **0** ([Sources/FAILED_URLS.csv](Sources/FAILED_URLS.csv) is empty apart from its header) |
| HTTP status of every saved page | 200 |
| Deferred by user scope (not crawled, listing data only) | 1,558 |
| Organized Markdown files | 722 pages + `Patch_Notes/` (README + 2 patch pages) |
| Structured data files | 18 (16 JSON + 2 CSV) |

Every one of the 2,284 URLs has a `crawl_status` in [Sources/URL_MANIFEST.csv](Sources/URL_MANIFEST.csv): `crawled`, `scraped_during_discovery`, or `deferred_by_user_scope`.

## Scope approved by the user (2026-11-07)

| Group | Rule | Pages |
|---|---|---|
| Hub/listing/system/guide pages | all | 63 |
| Classes | all 8 | 8 (hubs) |
| Skills | all 8 classes | 129 |
| Monsters | all | 160 |
| Maps | all | 55 |
| NPCs | all | 71 |
| Pets | Legendary + Epic only | 14 of 31 |
| Cards | ★5 data comes from monster pages; card/spirit/coin item pages | 3 |
| Weapons & equipment | tier 10 (ขั้น 10) only | 106 of 1,002 |
| Headgear / face / mouth | tier 10 only | 54 of 331 |
| Materials | key only: 49 Essences, 6 elemental Cores, Refine Ward, Repair Kit, Hone Stone, Scribe's Ink, Bindmark, Unique Shard (+ copper_ore sample) | 62 of 157 |
| Potions & food | top only: Sovereign Elixir, Sovereign Ether, Spirit Feast, Sanctum Lotus Feast | 4 of 49 |
| Monster drops (vendor junk) | excluded (the Wiki's effect column is empty for all 160) | 0 of 160 |
| Fashion (Cash) | deferred | 0 of 69 |
| Orphan pages (found by Map only) | all — all 4 turned out to be soft-404s (no item data) | 4 |
| Phase 3 sample outside scope | iron_sword (tier 2, kept) | 1 |

Check: 63 + 129 + 160 + 55 + 71 + 14 + 3 + 106 + 54 + 62 + 4 + 4 + 1 = 726 saved pages. The 8 class pages are among the 63 hubs.

Deferred pages still have their **listing-table values** (name, slot, level, tier, ATK/MATK/DEF, sell price or effect text) in `Structured_Data/` with `data_source: "listing_table_only"`.

## Firecrawl credits

| Phase | Credits | Notes |
|---|---|---|
| Phase 2 discovery | 66 | 3 Map calls + 63 hub scrapes |
| Phase 3 estimate | 6 | 5 sample pages + the official pricing page |
| Phase 4 crawl | 658 | 14 + 13 batch jobs; exactly 1 credit per page |
| **Total used** | **730** | |
| Balance after the crawl | 670 | Firecrawl added 400 bonus credits during the run (1,000 + 400 − 730) |

Rejected (rate-limited) requests cost nothing. Estimate (Phase 3) and actual usage match: 1 credit per page.

## Method and resumability

- **Discovery:** Map, then a breadth-first scrape of hub pages only (`Tools/discover_hubs.py`). The Wiki has no sitemap; Map alone found just 57 URLs.
- **Crawl:** `Tools/crawl_batches.py` sends `batch-scrape` jobs of 50 URLs. It caches every result under `Progress/page_cache/`, logs each URL to `Progress/crawl_log.csv`, and skips cached URLs on re-run.
- **Export:** `Tools/export_raw.py` writes `Raw/Original_Wiki_Pages/<section>/<page>.md`. Each file has a source header and unmodified Firecrawl markdown.
- **Organization:** `Tools/organize.py` builds the category folders and `Structured_Data/`. `Tools/build_docs.py` builds `INDEX.md` and `ALL_DATA.md`.

## Incremental updates later

1. Re-run discovery with `python3 Tools/discover_hubs.py`. Delete the hub cache first only if you want fresh listings.
2. Add new or deferred URLs to `Progress/crawl_queue.csv`, then run `python3 Tools/crawl_batches.py`. Only uncached URLs are fetched.
3. Re-run `export_raw.py`, `organize.py` and `build_docs.py`. These are local only and free.

To re-crawl a changed page, delete its file in `Progress/page_cache/` first.
