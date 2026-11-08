"""Fetch URLs FRESH (Firecrawl --max-age 0, never Firecrawl's cache) with batch-scrape and write each result into a
cache dir, overwriting older copies. Snapshot the old cache first if you want to diff.
Usage: python3 Tools/refresh_batch.py <urls.txt> <Progress/page_cache|Progress/discovery_scrapes>"""
import csv, json, os, subprocess, sys, time, datetime, urllib.parse as up
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urls = [l.strip() for l in open(sys.argv[1]) if l.strip()]; out = os.path.join(ROOT, sys.argv[2]); os.makedirs(out, exist_ok=True)
BATCH_DIR = f"{ROOT}/Progress/batches"; LOG = f"{ROOT}/Progress/crawl_log.csv"; os.makedirs(BATCH_DIR, exist_ok=True)
def key(u): return up.urlparse(u).path.strip("/").replace("/", "__") or "_root"
def log(u, s, n):
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds") + "Z", u, s, n])
for b in range(0, len(urls), 50):
    chunk = urls[b:b + 50]; stamp = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).strftime("%Y%m%dT%H%M%S")
    uf, of = f"{BATCH_DIR}/{stamp}_fresh_urls.txt", f"{BATCH_DIR}/{stamp}_fresh_result.json"
    open(uf, "w").write("\n".join(chunk) + "\n")
    for attempt in range(4):
        r = subprocess.run(["firecrawl", "batch-scrape", "--urls-file", uf, "--format", "markdown,links", "--max-age", "0",
                            "--wait", "--poll-interval", "5", "--timeout", "1500", "-o", of], capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(of): break
        print("batch error, retry in 65s:", (r.stderr or r.stdout)[-200:].strip()); time.sleep(65)
    else:
        for u in chunk: log(u, "failed", "fresh batch error")
        continue
    res = json.load(open(of)); got = set()
    for d in res.get("data", []):
        m = d.get("metadata", {}); src = (m.get("sourceURL") or m.get("url") or "").rstrip("/")
        u = next((u for u in chunk if key(u) == key(src)), None)
        if not u or not d.get("markdown") or int(m.get("statusCode") or 200) >= 400:
            if u: log(u, "failed", f"fresh status {m.get('statusCode')}"); continue
            print("unmatched", src); continue
        json.dump({"data": d}, open(f"{out}/{key(u)}.json", "w"), ensure_ascii=False); got.add(u); log(u, "success", f"fresh status {m.get('statusCode')} cache={m.get('cacheState')}")
    print(f"batch {b//50+1}: {len(chunk)} requested, {len(got)} saved, missing {[key(u) for u in chunk if u not in got]} credits={res.get('creditsUsed')}")
    time.sleep(31)
