"""Import captured Firecrawl JSON without making network requests.

Usage: python Tools/import_live_capture.py <capture-directory>
Original 2026-11-08 snapshot and player inventory remain unchanged.
"""
import csv, hashlib, json, re, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parent.parent
capture=Path(sys.argv[1]).resolve()
if not (ROOT/'.git').exists() or not capture.is_dir(): raise SystemExit('Select a valid checkout and captured JSON directory')
manifest_path=ROOT/'Sources/URL_MANIFEST.csv'
with manifest_path.open(encoding='utf-8',newline='') as f:
    reader=csv.DictReader(f); fields=reader.fieldnames; rows=list(reader)
manifest={r['path']:r for r in rows}; imported=[]
for file in sorted(capture.glob('*.json')):
    data=json.loads(file.read_text(encoding='utf-8')); meta=data.get('metadata',{})
    url=meta.get('sourceURL') or meta.get('url'); parsed=urlparse(url or '')
    if parsed.scheme!='https' or parsed.netloc!='wiki.bindertowngame.com' or not data.get('markdown') or meta.get('statusCode',200)!=200: raise SystemExit('Invalid capture '+file.name)
    path=parsed.path.rstrip('/') or '/'
    timestamp=data['captured_at']; date=datetime.fromisoformat(timestamp.replace('Z','+00:00')).astimezone(timezone(timedelta(hours=7))).date().isoformat()
    data['captured_date']=date
    name=path.strip('/').replace('/','__') or '_root'; section=path.strip('/').split('/')[0] if '/' in path.strip('/') else '_hub'
    raw=Path('Raw/Original_Wiki_Pages')/section/(name+'.md')
    snapshot=Path('Raw/Snapshots')/date/'live'/(name+'.json')
    body=json.dumps(data,ensure_ascii=False,indent=1)+'\n'; target=ROOT/snapshot;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(body,encoding='utf-8',newline='\n')
    title=str(meta.get('title') or path).replace('"',"'").replace('\n',' ')
    header=f'---\nsource_url: "{url}"\nsource_title: "{title}"\nhttp_status: 200\ncrawled_date: "{date}"\ncrawler: "Firecrawl scrape (markdown), maxAge=0"\nverification_status: "WIKI"\n---\n\n'
    target=ROOT/raw; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(header+data['markdown'],encoding='utf-8',newline='\n')
    category={'item':'Items','map':'Maps','mob':'Monsters'}.get(section,section)
    row=manifest.setdefault(path,{k:'' for k in fields});row.update(url=url,path=path,title=title,category=category,page_type='hub' if section in {'_hub','items','systems'} else 'detail',crawl_status='crawled',raw_file=raw.as_posix(),http_status='200',notes='Fresh Firecrawl capture '+date+'; no early-level item crawl')
    imported.append({'url':url,'crawled_date':date,'captured_at':timestamp,'snapshot_file':snapshot.as_posix(),'raw_file':raw.as_posix(),'sha256':hashlib.sha256(body.encode()).hexdigest(),'credits_used':meta.get('creditsUsed',0)})
with manifest_path.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(manifest[k] for k in sorted(manifest))
report={'pages':imported,'count':len(imported),'latest_capture_date':max(p['crawled_date'] for p in imported),'credits_used':sum(p['credits_used'] for p in imported),'scope':'New Tier 10 items, Tidehaven maps, Copperbell Arena, equipped items, affix rules and Shellforge monsters; no Tier 1-9 item details'}
(ROOT/'Sources/LIVE_CAPTURE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='pages'}))
