# Phase 3 — Cost Estimate (Binder Town Wiki)

- **Date:** 2026-11-07
- **Pricing source:** https://www.firecrawl.dev/pricing (scraped 2026-11-07, saved at `Progress/firecrawl_pricing.md`)
- **Account balance:** read from the API via `firecrawl --status`

## 1. Official pricing used (from the pricing page)

- **Credit cost:** 1 credit = 1 page on a basic scrape or crawl. A Map call costs 1 credit. The JSON/Question/Highlight formats add 4 credits per page, so they are **not used here**: markdown + links only.
- **Failed requests:** a scrape that returns no result is not charged. A page with an error status (403/404) still costs 1 credit.
- **Free plan:** 1,000 credits/month, refreshed monthly. Rate limit 10/min for scrape/map; 2/min for crawl and batch-scrape jobs.
- **Hobby:** $19/month billed monthly, or $16/month billed annually. 5,000 credits/month; rate limit 100/min.
- **Observed cost matches:** 3 Map calls plus 63 + 6 scrapes reduced the balance from 1,000 to 928. Rate-limited (rejected) requests cost nothing.

## 2. Account

| Item | Value | Verified |
|---|---|---|
| Plan credits | 1,000 / cycle (Free) | ✅ API |
| Remaining | **928** | ✅ API |
| Billing period | 2026-11-07 → 2026-12-07 | ✅ API |
| Concurrency | 2 parallel jobs | ✅ CLI status |

## 3. Pages left to crawl

63 hub pages and 5 sample detail pages are already saved.

| Group | Pages | Credits |
|---|---|---|
| Monsters `/mob/` | 159 | 159 |
| Skills `/skill/` | 128 | 128 |
| NPCs `/npc/` | 71 | 71 |
| Maps `/map/` | 54 | 54 |
| Pets `/pet/` | 31 | 31 |
| **Subtotal: non-item** | **443** | **443** |
| Items: cards 3 + orphans 4 + potions/food 49 + materials 156 + monster drops 160 + fashion 69 | 441 | 441 |
| Items: gear | 1,001 | 1,001 |
| Items: headgear/face/mouth | 331 | 331 |
| **Total** | **2,216** | **2,216** |

**Shortfall on the current balance:** 2,216 − 928 = **1,288 credits** (plus a retry reserve).

## 4. Why item detail pages cannot be skipped

From the samples, detail pages contain data the listing tables do not:
- Drop sources and per-kill drop rates
- Crafting recipes
- Refine (+5) average cost
- Sell price by rarity (Normal/Magic/Rare/Epic)
- Equippable classes, stat bonuses, weight
- Monster element weakness/resistance, DEF/MDEF/FLEE, day/night multipliers
- Skill per-level tables

The listing tables only carry Lv / tier / ATK / MATK / DEF / sell price (Normal).

## 5. Batching

- **Method:** `firecrawl batch-scrape` with markdown + links, 50 URLs per job, saved one file per page, with a progress record per URL.
- **Recommended batch size:** 50. This keeps resume granularity small and stays inside the 2-jobs/min crawl limit.
- **Batches:** about 9 for the non-item pages, about 9 for the first item group, and about 27 for gear + headgear.
- **Order** (per user request, items last):
  1. Pets
  2. Maps
  3. Skills
  4. NPCs
  5. Monsters
  6. Items: cards/orphans/use/mat/drop/fashion
  7. Items: gear
  8. Items: headgear

## 6. Claude token estimate (rough)

- **Sample page sizes** (markdown chars): skill 0.7k · map 3.3k · material 10k · gear 17.6k · monster 38k.
- **Raw corpus estimate:** about 30–35 million characters. Much of this is image-link markup, which will be stripped when organizing.
- Organization will be done by local scripts. Claude reads only samples for parser design plus spot checks, never the whole corpus.
- **Estimated Claude usage for the whole project:** about 0.5–1.5M tokens. This is an estimate, not a measurement.

## 7. Options

| Option | Cost | Result |
|---|---|---|
| **A. Free plan, staged** (recommended if no spend) | $0 | Now: all 443 non-item + 441 smaller-category items (884 credits; about 44 kept for retries). Dec 7 reset: gear (~1,000). Jan 7 reset: the rest of gear + headgear (~330). Complete in about 2 months. |
| B. Hobby plan, 1 month | $19 (official price) | Everything now (2,216 of 5,000 credits). Faster rate limits. |
| C. Direct HTTP fetch of the Wiki (no Firecrawl) | 0 credits | Requires allowing `wiki.bindertowngame.com` in this cloud environment's network. Local HTML→Markdown conversion may differ from Firecrawl's output. Deviates from the "Firecrawl primary" rule, so it needs your approval. |
