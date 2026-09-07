"""Render and integrate every authored SVG in data/illustrations.json.

Safe to run after extract.py or before a site build. Source PDFs and extracted
technical data are not modified; original crop coordinates remain provenance.
"""
from pathlib import Path
import csv,json,re,hashlib
import yaml
from drawing_catalog import render

ROOT=Path(__file__).resolve().parents[1]
def save(p,t):
 path=ROOT/p;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(t.encode('utf8'))
def main():
 records=json.loads((ROOT/'data/details.json').read_text(encoding='utf8'))
 specs=json.loads((ROOT/'data/illustrations.json').read_text(encoding='utf8'))
 assert set(specs)=={r['id'] for r in records},'Every record needs an explicit illustration specification'
 for r in records:
  s=specs[r['id']]
  if s.get('display_detail_numbers') and r['original_detail_numbers']!=s['display_detail_numbers']:
   r['extracted_detail_numbers']=r['original_detail_numbers']
   r['original_detail_numbers']=s['display_detail_numbers'];r['detail_number_status']='visually_checked'
   r['notes']=[n for n in r['notes'] if not n.startswith('Numerazione della figura')]+['Numerazione della figura corretta durante il ridisegno mediante confronto visivo con il PDF; il valore estratto precedente è conservato in extracted_detail_numbers.']
  n=', '.join(r['original_detail_numbers']) or 'riferimento nella scheda'
  label=f"{r['source'].upper()} · {r['table']} · dettaglio {n}"
  diagram=render(s)
  target=f"assets/illustrations/{r['id']}.svg"
  preview=f"assets/illustrations/previews/{r['id']}.svg"
  save(preview,diagram.finish(s['title'],label,s['alt'],compact=True))
  svg=diagram.finish(s['title'],label,s['alt'])
  save(target,svg)
  r['source_image']=s['reference_image'];r['image']=target
  r['illustration']={'specification':f"data/illustrations.json#{r['id']}",'title':s['title'],'thumbnail':preview,'method':s['method'],'scope':s['scope'],'review':s['review'],'alt':s['alt'],'sha256':hashlib.sha256(svg.encode('utf8')).hexdigest()}
  front=yaml.safe_dump({k:v for k,v in r.items() if k not in ['context_cells','description','requirements']},allow_unicode=True,sort_keys=False)
  md=f'---\n{front}---\n\n# {label}\n\n'
  md+=f'[Pagina estratta](../pages/{r["source"]}-{r["pdf_page"]:03}.md) · [PDF originale](../../sources/{r["source"]}.pdf#page={r["pdf_page"]})\n\n'
  md+=f'![{s["alt"]}](../../{target})\n\n'
  md+=f'**{s["title"]}.** Disegno vettoriale non in scala. [Apri / scarica il disegno SVG](../../{target}).\n\n'
  if s.get('note'):md+=f'> {s["note"]}\n\n'
  md+='Il blu rappresenta gli elementi metallici, l’arancio le saldature e il turchese le azioni. Simboli e proporzioni hanno funzione schematica; classi, dimensioni limite e condizioni applicabili sono quelle riportate nella fonte.\n\n'
  md+=f'## Classificazione riportata\n\n{r["class_text"] or "Consultare la tabella originale."}\n\n## Descrizione e condizioni\n\n{r["description"]}\n\n## Requisiti e note\n\n{r["requirements"]}\n\n'
  md+='> Estrazione documentale da verificare. Le categorie non sono valori di progetto pronti per il calcolo. Celle condivise e varianti non vanno separate dalle condizioni.\n\n'
  md+=f'## Contesto della classificazione\n\n[Celle della tabella in Markdown](../tables/{r["table_id"]}.md) · [Tabella nel PDF di riferimento](../../sources/{r["source"]}.pdf#page={r["pdf_page"]}).\n'
  save(f'docs/details/{r["id"]}.md',md)
 save('data/details.json',json.dumps(records,ensure_ascii=False,indent=2)+'\n')
 save('data/details.jsonl',''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
 fields=['id','source','pdf_page','table','original_detail_numbers','class_text','description','requirements','image','source_image','status']
 with (ROOT/'data/details.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader()
  for r in records:w.writerow({**r,'original_detail_numbers':','.join(r['original_detail_numbers'])})
 # Historical source rasters stay in the repository as extraction evidence.
 # Reader-facing documents use the direct PDF for source-image inspection.
 for folder in ['pages','tables']:
  for p in (ROOT/'docs'/folder).glob('*.md'):
   raw=p.read_text(encoding='utf8')
   raw=re.sub(r'!\[[^\]]*\]\(../../assets/(?:pages|tables)/[^)]+\)',lambda m:'[Consulta la figura nel PDF originale](../../sources/'+p.stem.split('-')[0]+'.pdf#page='+str(int(p.stem.split('-')[1]))+')',raw)
   raw=raw.replace('## Pagina di riscontro','## Riscontro sulla fonte')
   p.write_text(raw,encoding='utf8')
 save('data/illustration-coverage.json',json.dumps({'details':len(records),'svg_drawings':len(records),'source_screenshots_in_detail_pages':0,'editorial_from_description':[k for k,s in specs.items() if s['review']=='editorial_from_source_description'],'method':'authored_parametric_svg','original_pdf_unchanged':True,'validation_scope':'documental and visual; not certified for engineering design'},ensure_ascii=False,indent=2)+'\n')
 print(f'{len(records)} SVG diagrams generated and integrated')
if __name__=='__main__':main()
