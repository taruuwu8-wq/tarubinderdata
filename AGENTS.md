# Working on Taru's knowledge base and dashboard

- Read `CLOUD_HANDOFF.md` first for current state and commands. Prefer concise Thai replies.
- `Dashboard/` is a buildless Node.js/HTML application. Node 22+ is sufficient; it has no npm dependencies. Run `cd Dashboard && npm test` after behavior or data changes.
- Preserve the live Site identity in `Dashboard/.openai/hosting.json`. The GitHub copy does not automatically deploy to Sites. Use the connected Sites workflow for the existing private site; do not create another site or change its audience.
- `Structured_Data/` and organized Markdown are the dashboard's source. `Raw/Snapshots/` preserves capture evidence. Keep capture dates and URLs. Missing data is unknown, never zero; a fresh listing does not refresh older details.
- Original crawl scope: equipment/headgear detail pages for Tier 10 only, important materials and high-level consumables; skip Tier 1–9 detail pages, fashion and vendor junk unless the user expands scope. Do not crawl all URLs in the missing-data queue.
- Preserve player-owned inventory and overrides: `My_Cards/card_inventory.md`, `My_Cards/card_db_backup.json`, `My_Cards/tracker/overrides.json`. Preserve original Nov 8 snapshot JSON. Ask only if a requested change actually conflicts with current authorization.
- Observed ATK/HP/DPS-related totals in the dashboard are a player screenshot snapshot. Do not claim they are recalculated when swapping gear. Compare raw gear bonuses separately. Conditional effects remain references.
- Keep the Moth Mask 245% Crit DMG transcription flagged and excluded; do not guess 24.5%. Offhand usage requires explicit sandbox confirmation.
- Item IDs, slot/class restrictions, refine tables, affix pools/ranges and rarity limits must remain validated. Preserve browser-local saved-build import/export compatibility.
- `npm run sync:data` rebuilds from existing KB files without network calls. It is not a Wiki refresh. Keep the compact registry schema and hydrate pools in memory; expanding all item pools in JSON can exceed hosting file limits.
- Use Firecrawl only for requested fresh pages, reuse successful captures and record credits. Never commit credentials, authorization URLs, local browser state or `.env` values.
