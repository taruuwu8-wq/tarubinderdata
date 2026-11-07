"""Shared helpers for organizing raw pages (no network)."""
import re, os, json, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = f"{ROOT}/Raw/Original_Wiki_Pages"
BASE = "https://wiki.bindertowngame.com"
def load_raw(path):
    t = open(path, encoding="utf-8").read()
    fm, body = t.split("\n---\n", 1)
    meta = dict(re.findall(r'^(\w+): "?(.*?)"?$', fm, re.M))
    return meta, body.lstrip("\n")
def clean(md):
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)                       # drop image embeds (assets excluded)
    md = re.sub(r'\]\(https://wiki\.bindertowngame\.com(/[^)\s]*)?(?: "[^"]*")?\)', lambda m: "](" + (m.group(1) or "/") + ")", md)
    md = re.sub(r"[ \t]+\n", "\n", md)
    return md
def tables(md):
    """Return list of {heading, header, rows} for every markdown table, cells kept verbatim."""
    out, head, lines = [], None, md.split("\n")
    i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("#"): head = l.lstrip("# ").strip()
        if l.startswith("|") and i + 1 < len(lines) and re.match(r"^\|\s*-{3}", lines[i + 1]):
            hdr = [c.strip() for c in l.strip().strip("|").split("|")]; rows = []; i += 2
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            out.append({"section": head, "header": hdr, "rows": rows}); continue
        i += 1
    return out
def plain(cell):
    return re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", cell).replace("**", "").replace("\\+", "+").strip()
def name_from_title(t): return re.sub(r"\s*[·|]\s*Binder Town Wiki\s*$", "", t or "").strip()
