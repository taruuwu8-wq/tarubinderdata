#!/usr/bin/env python3
"""Rebuild the card tracker's game data from this repo.

Usage (from the repo root):
    python3 My_Cards/tracker/build.py

Writes:
    My_Cards/tracker/catalog.json      -> card catalog (one row per monster card)
    My_Cards/tracker/catalog_doc.json  -> same data shaped as the web page's DB doc meta/catalog
    My_Cards/tracker/card-vault.html   -> the full page with the catalog embedded (fallback)
"""
import datetime, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))

def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()

def regions():
    region, cur = {}, None
    for line in read("Maps/_All_Maps.md").splitlines():
        m = re.match(r"## Region [A-Z] · (\w+)", line)
        if m:
            cur = m.group(1); continue
        if line.startswith("## "):
            cur = None
        if cur:
            for s in re.findall(r"\]\(([a-z_]+)\.md\)", line):
                region[s] = cur
    return region

def build():
    region = regions()
    out, problems = [], []
    mon_dir = os.path.join(ROOT, "Monsters")
    for fn in sorted(os.listdir(mon_dir)):
        if not fn.endswith(".md") or fn.startswith("_"):
            continue
        t = read(os.path.join("Monsters", fn))
        sec = re.search(r"## การ์ดของมอนนี้(.*?)(\n## |\Z)", t, re.S)
        if not sec:
            continue
        s = sec.group(1)
        col = re.search(r"สี (\w+) · Spirit Load (\d)", s)
        s1 = re.search(r"\| ★1 \| (.*?) \|", s)
        s5 = re.search(r"\| ★5 \| (.*?) \|", s)
        if not (col and s5):
            problems.append(fn); continue
        name = re.search(r"^# (.+)", t, re.M).group(1).strip()
        typ = re.search(r"ประเภท \*\*([A-Za-z' -]+?) ·", t)
        maps = re.findall(r"\]\(\.\./Maps/([a-z_]+)\.md\)", t)
        regs = sorted({region[m] for m in maps if m in region})
        lv = re.search(r"\(ที่ Lv (\d+)", t)
        mp = re.findall(r"\[\*\*([^*]+)\*\* Lv [^]]*\]\(\.\./Maps/", t)
        cost = re.search(r"แลกด้วยวิญญาณ ([\d,]+) ดวง · โอกาสได้วิญญาณต่อตัว ([\d.]+)%", s)
        row = dict(s=fn[:-3], n=name, c=col.group(1), l=int(col.group(2)),
                   t=typ.group(1).strip() if typ else "", r=regs[0] if regs else "",
                   lv=int(lv.group(1)) if lv else None, m=mp[0] if mp else "",
                   e1=s1.group(1) if s1 else "", e5=s5.group(1))
        if cost:
            row["cost"] = int(cost.group(1).replace(",", "")); row["sc"] = float(cost.group(2))
        out.append(row)
    ov = json.loads(open(os.path.join(HERE, "overrides.json"), encoding="utf-8").read())
    by = {r["s"]: r for r in out}
    for slug, patch in ov.items():
        if slug.startswith("_") or slug not in by:
            continue
        by[slug].update({k: v for k, v in patch.items() if not k.startswith("_")})
    return out, problems

def main():
    rows, problems = build()
    if len(rows) < 100:
        sys.exit(f"only {len(rows)} cards parsed — check Monsters/*.md format")
    today = datetime.date.today().isoformat()
    js = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(HERE, "catalog.json"), "w", encoding="utf-8") as f:
        f.write(js)
    with open(os.path.join(HERE, "catalog_doc.json"), "w", encoding="utf-8") as f:
        json.dump({"updatedAt": today, "count": len(rows), "source": "tarubinderdata repo (Monsters/*.md + overrides.json)", "items": rows}, f, ensure_ascii=False, separators=(",", ":"))
    tpl = open(os.path.join(HERE, "card-vault.template.html"), encoding="utf-8").read()
    html = tpl.replace("__CATALOG__", js).replace("__CATALOG_DATE__", today)
    with open(os.path.join(HERE, "card-vault.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"{len(rows)} cards · built {today}" + (f" · skipped {problems}" if problems else ""))

if __name__ == "__main__":
    main()
