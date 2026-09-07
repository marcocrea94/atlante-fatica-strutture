"""Integrity and traceability checks; does not validate engineering classifications."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,sys,re
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ('src','href') and v:self.links.append(v)
def main():
 errors=[];sources=load('data/sources.json');details=load('data/details.json')
 pages=[json.loads(l) for l in (ROOT/'data/pages.jsonl').read_text(encoding='utf8').splitlines()]
 for s in sources:
  if hashlib.sha256((ROOT/s['file']).read_bytes()).hexdigest()!=s['sha256']:errors.append('Hash: '+s['id'])
  expected={n for a,b,_ in s['sections'] for n in range(a,b+1)}
  actual={p['pdf_page'] for p in pages if p['source']==s['id']}
  if actual!=expected:errors.append('Coverage: '+s['id'])
 for records in [pages,details,load('data/tables.json')]:
  if len({r['id'] for r in records})!=len(records):errors.append('Duplicate IDs')
  for r in records:
   if not (ROOT/r['image']).is_file():errors.append('Image: '+r['id'])
   b=r['bbox']
   if b[2]<=b[0] or b[3]<=b[1]:errors.append('Rectangle: '+r['id'])
 if re.search(r'^C4\.2\.9(?:\s|$)',next(p['text'] for p in pages if p['id']=='ntc-134'),re.M):errors.append('NTC unrelated chapter included')
 if 'C5.1.4.5' in next(p['text'] for p in pages if p['id']=='ntc-172'):errors.append('NTC deformation chapter included')
 for src,n in [('ec3',37),('ec3',33)]:
  if not any(r['source']==src and r['pdf_page']==n for r in details):errors.append('Missing detail page '+str(n))
 r=next(r for r in details if r['id']=='iiw-048-t01-d01')
 if r['fat_steel_mpa']!=125 or r['fat_aluminium_mpa']!=40:errors.append('IIW 122 material mapping')
 e=next(p for p in pages if p['id']=='ec3-023')
 if '≥' not in e['text'] or '∆σ' not in e['text']:errors.append('EC3 Symbol mapping')
 for f in (ROOT/'site').rglob('*.html'):
  parser=Links();parser.feed(f.read_text(encoding='utf8'))
  for link in parser.links:
   u=urlsplit(link)
   if u.scheme or u.netloc or not u.path:continue
   target=(f.parent/unquote(u.path)).resolve()
   if not target.exists():errors.append(f'Broken link: {f.relative_to(ROOT)} -> {link}')
 print(json.dumps({'source_pdfs':len(sources),'pages':len(pages),'details':len(details),'html_pages':sum(1 for _ in (ROOT/'site').rglob('*.html')),'errors':errors},ensure_ascii=False,indent=2))
 if errors:sys.exit(1)
if __name__=='__main__':main()
