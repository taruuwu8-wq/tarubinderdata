"""Write each crawled page to Raw/Original_Wiki_Pages/<section>/<slug>.md, unmodified markdown + source header.
Sources: Progress/discovery_scrapes (hub pages) and Progress/page_cache (detail pages). No network."""
import json, os, glob, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/Raw/Original_Wiki_Pages"
n = 0
for f in sorted(glob.glob(f"{ROOT}/Progress/discovery_scrapes/*.json") + glob.glob(f"{ROOT}/Progress/page_cache/*.json")):
    d = json.load(open(f)); d = d.get("data", d); m = d.get("metadata", {})
    k = os.path.basename(f)[:-5]
    parts = k.split("__"); section = parts[0] if len(parts) > 1 else "_hub"
    if k == "_root": section = "_hub"
    url = "https://wiki.bindertowngame.com/" + ("" if k == "_root" else k.replace("__", "/"))
    url = url.rstrip("/")
    crawled = datetime.datetime.fromtimestamp(os.path.getmtime(f), datetime.timezone.utc).strftime("%Y-%m-%d")
    title = (m.get("title") or "").replace('"', "'")
    os.makedirs(f"{OUT}/{section}", exist_ok=True)
    with open(f"{OUT}/{section}/{k}.md", "w", encoding="utf-8") as o:
        o.write(f'---\nsource_url: "{url}"\nsource_title: "{title}"\nhttp_status: {m.get("statusCode")}\n'
                f'crawled_date: "{crawled}"\ncrawler: "Firecrawl scrape (markdown)"\nverification_status: "WIKI"\n---\n\n')
        o.write(d.get("markdown", ""))
    n += 1
print("exported", n, "pages")
