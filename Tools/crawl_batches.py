"""Phase 4 crawler. Resumable: a URL with a cached result in Progress/page_cache/ is never re-requested.
Usage: python3 crawl_batches.py [max_batches] [group_prefix]"""
import csv, json, os, subprocess, sys, time, datetime, urllib.parse as up
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = f"{ROOT}/Progress/page_cache"; BATCH_DIR = f"{ROOT}/Progress/batches"; LOG = f"{ROOT}/Progress/crawl_log.csv"
os.makedirs(CACHE, exist_ok=True); os.makedirs(BATCH_DIR, exist_ok=True)
SIZE = 50
max_batches = int(sys.argv[1]) if len(sys.argv) > 1 else 999
prefix = sys.argv[2] if len(sys.argv) > 2 else ""
def key(u): return up.urlparse(u).path.strip("/").replace("/", "__") or "_root"
def log(u, status, note=""):
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new: w.writerow(["timestamp_utc", "url", "status", "note"])
        w.writerow([datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z", u, status, note])
queue = [r for r in csv.DictReader(open(f"{ROOT}/Progress/crawl_queue.csv")) if r["group"].startswith(prefix)]
todo = [r["url"] for r in queue if not os.path.exists(f"{CACHE}/{key(r['url'])}.json")]
print(f"queue {len(queue)} | already cached {len(queue)-len(todo)} | to do {len(todo)}")
for b in range(min(max_batches, (len(todo) + SIZE - 1) // SIZE)):
    chunk = todo[b * SIZE:(b + 1) * SIZE]
    stamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    uf = f"{BATCH_DIR}/{stamp}_urls.txt"; of = f"{BATCH_DIR}/{stamp}_result.json"
    open(uf, "w").write("\n".join(chunk) + "\n")
    for attempt in range(4):
        r = subprocess.run(["firecrawl", "batch-scrape", "--urls-file", uf, "--format", "markdown,links", "--wait",
                            "--poll-interval", "5", "--timeout", "1500", "-o", of], capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(of): break
        err = (r.stderr or r.stdout)[-300:]; print("batch error, retry in 65s:", err.strip()[:200]); time.sleep(65)
    else:
        for u in chunk: log(u, "failed", "batch job error: " + err.replace("\n", " ")[:200])
        continue
    res = json.load(open(of)); data = res.get("data", res if isinstance(res, list) else [])
    got = set()
    for d in data:
        m = d.get("metadata", {}); src = (m.get("sourceURL") or m.get("url") or "").rstrip("/")
        match = next((u for u in chunk if u == src or key(u) == key(src)), None)
        if not match: print("unmatched result", src); continue
        code = m.get("statusCode")
        if not d.get("markdown") or (code and int(code) >= 400):
            log(match, "failed", f"status {code}; empty={not d.get('markdown')}"); continue
        json.dump({"data": d}, open(f"{CACHE}/{key(match)}.json", "w"), ensure_ascii=False)
        got.add(match); log(match, "success", f"status {code}")
    for u in chunk:
        if u not in got and not any(row for row in [] ): pass
    missing = [u for u in chunk if u not in got]
    for u in missing:
        if not os.path.exists(f"{CACHE}/{key(u)}.json"): log(u, "failed", "no result returned in batch")
    print(f"batch {b+1}: requested {len(chunk)}, saved {len(got)}, missing {len(missing)} | status={res.get('status')} credits={res.get('creditsUsed')}")
    time.sleep(31)  # free plan: 2 batch jobs/min
