"""Phase 2 discovery: BFS over hub/listing pages only (not detail pages).
Each scrape result is cached in Progress/discovery_scrapes/ so nothing is re-scraped."""
import json, os, re, subprocess, sys, time, urllib.parse as up, collections
BASE = "https://wiki.bindertowngame.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "Progress", "discovery_scrapes")
DETAIL = {"item", "skill", "mob", "map", "card", "pet", "npc", "quest", "class"}  # single-entity pages
MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 60
def norm(u):
    p = up.urlparse(u)
    if p.netloc and p.netloc != "wiki.bindertowngame.com": return None
    path = re.sub(r"/+$", "", p.path) or ""
    if re.search(r"\.(png|jpe?g|gif|webp|svg|ico|css|js|mp4|webm|pdf|zip|json|xml)$", path, re.I): return None
    return BASE + path
def fname(u):
    s = up.urlparse(u).path.strip("/").replace("/", "__") or "_root"
    return os.path.join(CACHE, s + ".json")
def scrape(u):
    f = fname(u)
    if not os.path.exists(f):
        time.sleep(9)  # free plan rate limit (~10 req/min)
        r = subprocess.run(["firecrawl", "scrape", u, "--format", "markdown,links", "--json", "-o", f],
                           capture_output=True, text=True, timeout=180)
        if r.returncode != 0 or not os.path.exists(f):
            return None, (r.stderr or r.stdout)[-300:]
    d = json.load(open(f)); d = d.get("data", d)
    return d, None
def is_hub(u):
    seg = up.urlparse(u).path.strip("/").split("/")
    return seg[0] not in DETAIL
seed = [BASE] + [l["url"] for l in json.load(open(os.path.join(ROOT, "Progress/map_raw.json")))["data"]["links"]]
found = {}  # url -> set of hub pages linking to it
for s in seed:
    n = norm(s)
    if n: found.setdefault(n, set()).add("MAP")
queue = [u for u in found if is_hub(u)]; seen = set(); errors = {}; n_scraped = 0
while queue and n_scraped < MAX:
    u = queue.pop(0)
    if u in seen: continue
    seen.add(u); new_scrape = not os.path.exists(fname(u))
    d, err = scrape(u); n_scraped += new_scrape
    if err: errors[u] = err; continue
    for l in d.get("links", []):
        n = norm(up.urljoin(u + "/", l))
        if not n: continue
        if n not in found and is_hub(n): queue.append(n)
        found.setdefault(n, set()).add(u)
json.dump({"found": {k: sorted(v) for k, v in found.items()}, "hubs_scraped": sorted(seen),
           "errors": errors, "queue_left": queue}, open(os.path.join(ROOT, "Progress/discovery_state.json"), "w"),
          ensure_ascii=False, indent=1)
print("hubs scraped:", len(seen), "new scrapes this run:", n_scraped, "errors:", len(errors), "queue left:", len(queue))
print("total URLs:", len(found))
print(collections.Counter(up.urlparse(k).path.strip("/").split("/")[0] or "(root)" for k in found).most_common())
for e in errors: print("ERR", e, errors[e])
