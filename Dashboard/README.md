# Taru Build Lab

Portable source of the live Binder Town build dashboard, migrated from the existing Sites source into this GitHub repository. Data and code now travel together for Cloud tasks.

## Run

Node.js 22 or later. No dependencies or installation step.

```sh
cd Dashboard
npm test
npm run preview
```

Preview: `http://127.0.0.1:4173`. For a Cloud preview service that requires external binding:

```sh
HOST=0.0.0.0 PORT=4173 npm run preview
```

On PowerShell, set `$env:HOST='0.0.0.0'` and `$env:PORT='4173'` before starting preview. The default remains loopback.

## Data and exports

```sh
npm run sync:data
npm test
npm run export:html
```

`sync:data` reads the repository's existing structured/Markdown KB and pins the registry to the checked-out commit. It makes no network requests and spends no Firecrawl credits. Original player inventory is preserved. `export:html` creates `exports/Taru-Build-Lab.html`, with assets embedded. The website can also serve the tracked `dist/` directory directly.

The compact registry stores each affix definition once. `hydrateRegistry` expands per-item pools in memory. `compact-registry.mjs` preserves this format after a rebuild.

## Current functionality

- 279 Tier 10 items with actual Wiki images; 138 meet Rogue requirements, filtered further by equipment slot.
- Gear selection, refine levels, rarity, per-item affix selection, roll checks, duplicate-family and prefix/suffix limits.
- Card editing/resonance, attribute and skill experiments, saved build comparison and JSON import/export.
- Eight freshly captured maps: Tidehaven, six field maps and Copperbell Arena.
- Source capture dates and missing-data disclosure. Conditional effects and unknown text remain references.

Observed combat totals are the player's screenshot snapshot, not a final-stat/DPS simulation. Browser-local saved profiles are not stored in GitHub; use the website's JSON export/import to move them between browsers.

## Publication

Live URL: https://taru-build-lab-1109.tallraisin4.chatgpt.site

The current Site remains private. `Dashboard/.openai/hosting.json` retains its existing project ID. This GitHub migration does not change hosting, create a new Site, or configure automatic deployment. If the Cloud task has Sites available, follow its skill to open the existing Site source, carry the reviewed `Dashboard/` changes into that checkout, test/package/push the matching source and deploy it. If Sites is unavailable, finish and commit the code here, then publish from a connected session. Do not assume a GitHub commit alone updated the live website.

See `../CLOUD_HANDOFF.md` for data history, gaps and Cloud setup.

Image bytes are embedded as data URLs in dist/wiki-media.json, with their original source attribution and byte-length checks. This keeps the Cloud checkout self-contained without hundreds of individual image uploads.
