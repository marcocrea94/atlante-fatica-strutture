"""Build a self-contained static GitHub Pages site, without remote runtime libraries."""
from pathlib import Path
import html,json,re,shutil,sys
import markdown,yaml
from latex2mathml.converter import convert
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'site'
REPO='https://github.com/marcocrea94/atlante-fatica-strutture'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
def save(path,text):
 p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf8')
def main():
 OUT.mkdir(exist_ok=True)
 for folder in ['assets','sources','data']:
  shutil.copytree(ROOT/folder,OUT/folder,dirs_exist_ok=True)
 for f in (ROOT/'web').iterdir():shutil.copy2(f,OUT/f.name)
 pages=[json.loads(l) for l in (ROOT/'data/pages.jsonl').read_text(encoding='utf8').splitlines()]
 records=load('data/details.json');valid_details={r['id'] for r in records}
 keep=['id','source','pdf_page','printed_page','table','class_text','description','requirements','original_detail_numbers','image']
 save('data/catalog.json',json.dumps([{k:r[k] for k in keep} for r in records],ensure_ascii=False))
 save('data/page-index.json',json.dumps(pages,ensure_ascii=False))
 header=(ROOT/'web/index.html').read_text(encoding='utf8').split('<main id="main">')[0]
 footer='</main></div><footer>ATLANTE DELLA FATICA <span>Edizioni dei documenti forniti · Diritti dei rispettivi titolari</span></footer></body></html>'
 for f in (ROOT/'docs').rglob('*.md'):
  if f.parent.name=='details' and f.stem not in valid_details:continue
  rel=f.relative_to(ROOT);prefix='../'*(len(rel.parts)-1);raw=f.read_text(encoding='utf8');meta={}
  if raw.startswith('---\n'):
   front,raw=raw[4:].split('\n---\n',1);meta=yaml.safe_load(front)
  title=re.search(r'^# (.+)',raw,re.M).group(1)
  body=markdown.markdown(raw,extensions=['tables','fenced_code','sane_lists'])
  body=re.sub(r'<pre><code class="language-math">(.*?)</code></pre>',lambda m:'<div class="math-block">'+convert(html.unescape(m[1]),display='block')+'</div>',body,flags=re.S)
  body=re.sub(r'href="([^"]+)\.md([#?][^"]*)?"',lambda m:f'href="{m[1]}.html{m[2] or ""}"',body)
  body=body.replace('<img ','<img loading="lazy" decoding="async" ')
  top=header.replace('<title>Atlante della fatica — dettagli, metodi e fonti</title>',f'<title>{html.escape(title)} — Atlante della fatica</title>').replace('<script defer src="app.js"></script>','')
  top=re.sub(r'(href|src)="(?!https?:|#)([^"]+)"',lambda m:f'{m[1]}="{prefix}{m[2]}"',top)
  tools=f'<div class="doc-tools"><a href="{prefix}{rel.as_posix()}">Leggi il Markdown ↓</a><a href="{REPO}/blob/main/{rel.as_posix()}">Apri su GitHub ↗</a></div>'
  nav=''
  if meta.get('pdf_page') and meta.get('source'):
   ids=[p['id'] for p in pages if p['source']==meta['source']]
   if f.stem in ids:
    i=ids.index(f.stem);nav='<nav class="page-step" aria-label="Pagine della fonte">'
    if i>0:nav+=f'<a href="{ids[i-1]}.html">← Pagina precedente</a>'
    if i+1<len(ids):nav+=f'<a href="{ids[i+1]}.html">Pagina successiva →</a>'
    nav+='</nav>'
  save(rel.with_suffix('.html'),top+f'<main id="main" class="doc-main"><div class="breadcrumbs"><a href="{prefix}index.html">Archivio</a> / {html.escape(f.parent.name)}</div>'+tools+'<article class="article">'+body+'</article>'+nav+footer)
  save(rel, f.read_text(encoding='utf8'))
 for name in ['README.md','llms.txt','llms-full.txt']:
  if (ROOT/name).exists():shutil.copy2(ROOT/name,OUT/name)
 save('.nojekyll','')
 print(json.dumps({'html_pages':sum(1 for _ in OUT.rglob('*.html')),'catalog_records':len(records),'document_pages':len(pages),'output':str(OUT)},ensure_ascii=False))
if __name__=='__main__':main()
