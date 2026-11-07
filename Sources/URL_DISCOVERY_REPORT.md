# URL Discovery Report — Binder Town Wiki

- **Source:** https://wiki.bindertowngame.com/
- **Discovery date:** 2026-11-07
- **Tools:** Firecrawl CLI 1.29.0 (`map`, `scrape --format markdown,links`)
- **Wiki language:** Thai (with English proper names for classes, maps, monsters, and some items)
- **Manifest:** `Sources/URL_MANIFEST.csv` (one row per unique URL)

## 1. Method

1. **Firecrawl Map** (sitemap include) returned only **57 URLs**.
   - A sitemap-only map returned **0**. The site has no usable sitemap.
   - A no-sitemap map returned the same 57.
2. Because Map was clearly incomplete, discovery continued with a **breadth-first scrape of hub/listing pages only**:
   - Scraped: home, `/items/*`, `/mobs`, `/maps`, `/npcs`, `/jobs`, `/job/*`, `/systems/*`, `/guide/*`, `/cards`, `/glossary`.
   - Their links were harvested.
   - Detail pages (`/item/`, `/mob/`, `/skill/`, `/npc/`, `/map/`, `/pet/`) were **not** scraped.
3. The 63 hub pages scraped here are cached in `Progress/discovery_scrapes/` (markdown + links). They will be reused in Phase 4 and not crawled again.
4. URLs were normalized: same host only, trailing slash removed, fragments (`#...`) dropped. Image and asset URLs were excluded.

Script: `Tools/discover_hubs.py` (resumable; skips cached pages). Manifest builder: `Tools/build_manifest.py`.

## 2. Totals

| Metric | Count |
|---|---|
| Raw link occurrences harvested from hub pages | 3,522 |
| URLs from Firecrawl Map | 57 (all also covered below) |
| **Unique internal page URLs** | **2,284** |
| Hub/listing pages (already scraped during discovery) | 63 |
| Detail pages (pending crawl) | 2,221 |
| Alias URLs with identical content to another URL | 4 |
| External-domain links | 0 |
| Asset links (images etc.) in link lists | 0 (images appear only inline in markdown and are excluded) |
| Pages that returned an HTTP error | 0 (all 63 hub scrapes returned 200) |

## 3. URLs by category

| Category | Path pattern | Unique URLs | Wiki-stated count | Match |
|---|---|---|---|---|
| Items (detail) | `/item/*` | 1,775 | 1,771 (home page) | +4 extra, see §5 |
| ↳ Gear | `/items/gear` | 1,002 | 1,002 | ✅ |
| ↳ Headgear / face / mouth | `/items/look` | 331 | 331 | ✅ |
| ↳ Potions & food | `/items/use` | 49 | 49 | ✅ |
| ↳ Materials | `/items/mat` | 157 | 157 | ✅ |
| ↳ Monster drops | `/items/drop` | 160 | 160 | ✅ |
| ↳ Fashion (Cash) | `/items/fashion` | 69 | 69 | ✅ |
| ↳ Cards & spirits | `/cards` | 3 | 3 | ✅ |
| Monsters | `/mob/*` | 160 | 160 | ✅ |
| Skills | `/skill/*` | 129 | 129 | ✅ |
| NPCs | `/npc/*` | 71 | 71 | ✅ |
| Maps | `/map/*` | 55 | 55 | ✅ |
| Pets | `/pet/*` | 31 | 31 | ✅ |
| Classes | `/job/*` | 8 | 8 | ✅ (Binder/Novice + Knight, Warrior, Scout, Rogue, Mage, Acolyte, Summoner) |
| Game systems | `/systems/*` | 31 | — | — |
| Guides | `/guide/*` | 7 | — | — |
| Listing / index pages | `/`, `/items`, `/mobs`, `/maps`, `/npcs`, `/jobs`, `/skills`, `/cards`, `/glossary`, `/refine`, `/gem-exchange` | 12 (incl. `/items` hub) | — | — |

Wiki-stated counts come from the home page ("อาชีพ 8 · สกิล 129 · ไอเท็ม 1,771 · มอน 160 · แมพ 55") and from each listing's "แสดง X จาก X" counter.

### System and guide pages found (all scraped during discovery)

- **Blacksmith:** `/systems/smith` (ช่างตีเหล็ก), `/systems/refine` (ตีบวก), `/systems/affix` (Affix & Reroll), `/systems/crafting`, `/systems/weapon-rules` (Property · Focused · Grip), `/systems/uniques`
- **Stats & combat:** `/systems/stats`, `/systems/statuses`, `/systems/class-resources`, `/systems/classes` (Class Trait & Dash), `/systems/threats`
- **World:** `/systems/bosses`, `/systems/world-boss`, `/systems/region-sets`, `/systems/rules`, `/systems/events`, `/systems/pvp`
- **Economy / meta:** `/systems/shop`, `/systems/gem-exchange`, `/systems/premium`, `/systems/pass`, `/systems/fashion`, `/systems/social`, `/systems/auto`, `/systems/windows`
- **Gathering / consumables:** `/systems/gathering`, `/systems/gathering-50`, `/systems/oils-foods`
- **Pets:** `/systems/pets`
- **Guides:** `/guide`, `/guide/start`, `/guide/daily`, `/guide/leveling`, `/guide/gold`, `/guide/power`, `/guide/faq`

## 4. Duplicate URLs

Each URL appears only once in the manifest, because it was deduplicated after normalization. The following **alias pairs** return byte-identical markdown. Only the canonical one needs to be organized; both are recorded (`duplicate_of` column).

| Alias | Canonical |
|---|---|
| `/skills` | `/jobs` |
| `/skills/novice` | `/job/novice` |
| `/refine` | `/systems/refine` |
| `/gem-exchange` | `/systems/gem-exchange` |

## 5. Excluded, suspicious, and missing

**Excluded:**
- Image URLs under `/img/...` (item/mob/map art), embedded inline in markdown. Excluded per the no-assets rule.
- URL fragments such as `/guide/faq#death`, folded into their base page.
- No external domains were linked.

**Suspicious (included, flagged):** these 4 item pages were returned by Firecrawl Map but are **not linked from any listing page**. They may be legacy or alternate variants. **Phase 4 result:** all 4 are soft-404s (HTTP 200, generic item index only, no item data).
- `/item/greatsword_t4_alt` (title: "ดาบสองมือเหล็กกล้า (เวท)")
- `/item/bow_t4_alt`
- `/item/dagger_t10_alt`
- `/item/remnant_shard`

**Not found on the Wiki:**
- **No patch-notes / changelog page exists.** `/systems/windows` mentions an in-game patch-notes window ("แพตช์ ล่าสุดอยู่บนสุด"), but the Wiki does not host patch notes. `Patch_Notes/` will stay empty unless another official source is provided.
- No separate pages for individual affixes, cards, or region sets. That data lives inside `/systems/affix`, `/cards`, and `/systems/region-sets` (already scraped).

**Inaccessible:** none. Rate-limit refusals during discovery (free-plan limit of about 10 requests/min) were retried successfully. They consumed no credits.

## 6. Limitations

- Detail pages may link to further pages not reachable from any hub (e.g. pages like the 4 orphans above). The Phase 4 crawl will record any newly seen internal links and add them to the manifest incrementally.
- The site says its data is extracted directly from game code ("ดึงจากโค้ดเกมโดยตรง ตัวเลขตรงกับในเกม"). This is the Wiki's own claim, not independently verified.

## 7. Credits used in Phase 2

| Step | Credits |
|---|---|
| Map ×3 (include / only / skip sitemap) | 3 |
| Hub-page scrapes (63 pages) | 63 |
| **Total** | **66** (balance 1,000 → 934, per `firecrawl --status`) |
