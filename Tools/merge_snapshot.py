"""Merge an existing local snapshot without crawling or changing player inventory.

Usage: python Tools/merge_snapshot.py 2026-11-08
Raw snapshot JSON stays immutable. Only available pages replace older raw pages;
the manifest retains deferred URLs and records newly discovered gaps.
"""
import csv, hashlib, json, os, re, sys
from pathlib import Path
from urllib.parse import urlparse, urldefrag

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://wiki.bindertowngame.com"
DATE = sys.argv[1] if len(sys.argv) > 1 else "2026-11-08"
if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", DATE):
    raise SystemExit("Use an ISO snapshot date")
SNAP = ROOT / "Raw" / "Snapshots" / DATE
if not SNAP.is_dir() or not (ROOT / ".git").exists():
    raise SystemExit("Run inside the selected knowledge-base checkout")

def normalized(url):
    parsed = urlparse(urldefrag(url)[0])
    if parsed.scheme != "https" or parsed.netloc != "wiki.bindertowngame.com":
        return None
    p = parsed.path.rstrip("/") or "/"
    if p != "/" and p.split("/")[1] not in {"item", "items", "mob", "mobs", "map", "maps", "npc", "npcs", "pet", "job", "jobs", "skill", "skills", "systems", "guide", "cards", "glossary", "refine", "gem-exchange", "tools"}:
        return None
    return p

def raw_path(p):
    key = p.strip("/").replace("/", "__") or "_root"
    section = key.split("__")[0] if "__" in key else "_hub"
    return Path("Raw/Original_Wiki_Pages") / section / (key + ".md")

manifest_path = ROOT / "Sources/URL_MANIFEST.csv"
with manifest_path.open(encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    fields = list(reader.fieldnames)
    manifest = {r["path"].rstrip("/") or "/": r for r in reader}

fresh = {}
discovered = {}
for folder in ["hubs", "new_items"]:
    for file in sorted((SNAP / folder).glob("*.json")):
        raw = file.read_bytes()
        payload = json.loads(raw)
        data = payload.get("data", payload)
        md = data.get("markdown")
        meta = data.get("metadata", {})
        url = meta.get("sourceURL") or meta.get("url") or (BASE + "/" + file.stem.replace("__", "/"))
        if file.stem == "_root":
            url = BASE
        p = normalized(url)
        if not p or not md or int(meta.get("statusCode") or 200) >= 400:
            raise SystemExit(f"Invalid snapshot page: {file.relative_to(ROOT)}")
        if p in fresh:
            raise SystemExit(f"Duplicate snapshot path: {p}")
        target = ROOT / raw_path(p)
        if not target.resolve().is_relative_to((ROOT / "Raw/Original_Wiki_Pages").resolve()):
            raise SystemExit("Raw output outside the knowledge base")
        title = str(meta.get("title") or p).replace('"', "'").replace("\n", " ")
        header = (f'---\nsource_url: "{BASE}{"" if p == "/" else p}"\nsource_title: "{title}"\n'
                  f'http_status: {meta.get("statusCode") or 200}\ncrawled_date: "{DATE}"\n'
                  'crawler: "Firecrawl scrape (markdown)"\nverification_status: "WIKI"\n---\n\n')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(header + md, encoding="utf-8", newline="\n")
        fresh[p] = {"source_url": BASE + ("" if p == "/" else p), "snapshot_file": file.relative_to(ROOT).as_posix(),
                    "raw_file": target.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(raw).hexdigest(),
                    "crawled_date": DATE, "folder": folder, "title": title}
        links = data.get("links", []) + re.findall(r"\]\((https://wiki\.bindertowngame\.com/[^\s)]+)", md)
        for link in links:
            path = normalized(link.get("url", "") if isinstance(link, dict) else link)
            if path:
                discovered.setdefault(path, set()).add(p)

for p in sorted(set(discovered) | set(fresh)):
    if p not in manifest:
        first = p.strip("/").split("/")[0]
        manifest[p] = {k: "" for k in fields}
        manifest[p].update(url=BASE + ("" if p == "/" else p), path=p,
                           category={"item": "Items", "map": "Maps", "npc": "NPCs", "mob": "Monsters", "skill": "Skills"}.get(first, first),
                           page_type="detail", found_by_map="no", linked_from_hubs=str(len(discovered.get(p, []))),
                           crawl_status="deferred_by_user_scope", notes=f"Discovered in snapshot {DATE}; detail not fetched")
    row = manifest[p]
    if p in fresh:
        info = fresh[p]
        row.update(title=info["title"], page_type="hub" if info["folder"] == "hubs" else "detail",
                   crawl_status="scraped_during_discovery" if info["folder"] == "hubs" else "crawled",
                   raw_file=info["raw_file"], http_status="200")
        note = f"Fresh snapshot {DATE} merged"
        if note not in row.get("notes", ""):
            row["notes"] = "; ".join(x for x in [row.get("notes", ""), note] if x)

with manifest_path.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(manifest[p] for p in sorted(manifest))

out = {"snapshot_date": DATE, "policy": "merge_available_only_no_network", "source_snapshot_preserved": True,
       "fresh_pages": len(fresh), "hubs": sum(v["folder"] == "hubs" for v in fresh.values()),
       "new_item_details": sum(v["folder"] == "new_items" for v in fresh.values()),
       "pages": list(fresh.values()), "manifest_urls": len(manifest)}
(ROOT / "Sources/SNAPSHOT_MERGE.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in out.items() if k != "pages"}, ensure_ascii=False))
