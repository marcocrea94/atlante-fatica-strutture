"""Deterministic corpus extraction; coordinates are PDF points in displayed orientation."""
from pathlib import Path
import csv, hashlib, json, re, sys, unicodedata
import pymupdf as pdf
import yaml

ROOT=Path(__file__).resolve().parents[1]
SOURCES={
 'ntc': {'title':'Circolare 21 gennaio 2019, n. 7 — sezioni sulla fatica','edition':'2019','language':'it','total_pages':348,'sections':[(123,134,'C4.2.4.1.4 — Stato limite di fatica'),(171,172,'C5.1.4.3 — Fatica dei ponti stradali'),(176,176,'C5.2.3.2.3 — Fatica dei ponti ferroviari')],'original_filename':'Circolare-7-2019-NTC.pdf','printed_offset':-4},
 'ec3': {'title':'UNI EN 1993-1-9:2005 — Fatica','edition':'2005 + AC:2005; versione italiana maggio 2008','language':'it','total_pages':44,'sections':[(6,7,'Premessa e appendice nazionale'),(8,11,'1 — Generalità, definizioni e simboli'),(12,13,'2–3 — Requisiti e metodi di valutazione'),(14,16,'4–6 — Azioni e calcolo delle tensioni'),(17,21,'7–8 — Resistenza e verifiche a fatica'),(22,37,'8 — Catalogo dei particolari costruttivi'),(38,40,'Appendice A — Carico di fatica e verifiche'),(41,41,'Appendice B — Tensione geometrica hot spot')],'original_filename':'UNI EN 1993-1-9 (2005 IT) - Fatica.pdf','printed_offset':-5},
 'iiw': {'title':'IIW — Recommendations for Fatigue Design of Welded Joints and Components','edition':'XIII-1965-03 / XV-1127-03, Update June 2005','language':'en','total_pages':145,'sections':[(1,6,'Copertina, prefazione e indice'),(7,17,'1 — General'),(18,41,'2 — Fatigue actions (loading)'),(42,76,'3.1–3.2 — Fatigue resistance and classified details'),(77,106,'3.3–3.8 — Local methods, modifications and imperfections'),(107,117,'4 — Fatigue assessment'),(118,121,'5 — Safety considerations'),(122,145,'6 — Appendices')],'original_filename':'79001845-Recommendations-for-Fatigue-Design-of-Welded-Joints-and-Components.pdf','printed_offset':0}
}
CROPS=json.loads((ROOT/'data/detail-crops.json').read_text(encoding='utf8'))

def write(path,text):
 p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding='utf-8')
def js(path,data): write(path,json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def clean(t):
 t=unicodedata.normalize('NFKC',t)
 return re.sub(r'[\x00-\x08\x0b-\x1f]','',t).strip()
def serial_rect(r): return [round(float(v),2) for v in r]
def ocr_lines(src,n):
 p=ROOT/f'data/ocr/{src}-{n:03}.json'
 return json.loads(p.read_text(encoding='utf8')) if p.exists() else []
def rect_text(p,r,ocr=None):
 if ocr:
  lines=[l for l in ocr if r.contains(pdf.Point((l['bbox'][0]+l['bbox'][2])/2,(l['bbox'][1]+l['bbox'][3])/2))]
  return '\n'.join(clean(l['text']) for l in sorted(lines,key=lambda l:(round(l['bbox'][1]/5),l['bbox'][0])))
 return clean(p.get_text(clip=r,sort=True))
def render(p,r,path,dpi=180):
 target=ROOT/path; target.parent.mkdir(parents=True,exist_ok=True)
 p.get_pixmap(clip=r,dpi=dpi,alpha=False).save(str(target))
def scope(src,n,p):
 if src=='ntc':
  start={123:476,171:532,176:260}.get(n,85)
  end={134:420,172:452}.get(n,745)
  return pdf.Rect(42,start,554,end)
 if src=='ec3': return pdf.Rect(35,48,p.rect.width-35,795)
 return pdf.Rect(40,90 if p.rect.width>700 else 45,p.rect.width-35,p.rect.height-48)
def caption(p,t,ocr,src,n,ti):
 r=pdf.Rect(t.bbox[0],max(0,t.bbox[1]-32),t.bbox[2],t.bbox[1])
 txt=' '.join(rect_text(p,r,ocr).split())
 pat=r'C4\.2\.[XVI]+(?:\.[a-d])?' if src=='ntc' else r'(?:prospetto\s*)?((?:8|B)\.\d+)'
 m=re.search(pat,txt,re.I)
 return (m.group(0) if src=='ntc' else m.group(1)) if m else ('3.2-1' if src=='iiw' else f'PDF-{n}-T{ti}')

def extract_tables(p,src,n,ocr):
 records=[]; tables=[]
 for ti,t in enumerate(p.find_tables().tables,1):
  if t.bbox[3]<100 or t.bbox[1]>745 and src=='ntc': continue
  cells=[pdf.Rect(c) for c in t.cells if c is not None]
  cap=caption(p,t,ocr,src,n,ti)
  raw=[[clean(c or '') for c in row] for row in t.extract()]
  tid=f'{src}-{n:03}-t{ti:02}'
  timg=f'assets/tables/{tid}.png'; render(p,pdf.Rect(t.bbox),timg)
  table_cells=[{'bbox':serial_rect(c),'text':rect_text(p,c,ocr)} for c in cells]
  tables.append({'id':tid,'source':src,'pdf_page':n,'table':cap,'bbox':serial_rect(t.bbox),'cells':table_cells,'raw_rows':raw,'image':timg,'status':'extracted_not_engineering_validated'})
  # Locate the real column boundaries from header cells, avoiding false lines inside drawings.
  headers=[(c,rect_text(p,c,ocr).lower()) for c in cells if c.y0<t.bbox[1]+60]
  desc=next((c for c,v in headers if ('description' in v or 'descrizione' in v) and c.height<60),None)
  pic=next((c for c,v in headers if any(k in v for k in ['structural detail','dettaglio costruttivo','particolare costruttivo']) and c.height<60),None)
  description_inside=False
  if desc is None and pic is not None and src=='ec3':
   desc=next((c for c,v in headers if 'requisiti' in v and c.height<60),None)
   description_inside=True
  if desc is None or pic is None: continue
  x0=pic.x0; x1=desc.x0; header_bottom=max(pic.y1,desc.y1)
  def context_at(r):
   # Include complete merged cells that intersect the detail's vertical extent.
   relevant=[c for c in cells if c.y1>r.y0+1 and c.y0<r.y1-1 and c.y0>=header_bottom-1]
   return [{'bbox':serial_rect(c),'text':rect_text(p,c,ocr)} for c in relevant if c.x1<=x0+1 or c.x0>=x1-1]
  candidates=[]
  if src=='iiw':
   for c in cells:
    val=rect_text(p,c)
    if c.x1<=x0+1 and c.y0>=header_bottom-1 and re.fullmatch(r'\d{3}',val) and not val.endswith('00'):
     candidates.append((pdf.Rect(x0,c.y0,x1,c.y1),val))
  elif src=='ntc':
   for info in p.get_image_info():
    r=pdf.Rect(info['bbox'])
    if r.x0>=x0-2 and r.x1<=x1+3 and r.y0>=header_bottom and r.y1<=t.bbox[3]+1 and r.width>25 and r.height>12:
     candidates.append((r+(-2,-2,2,2),''))
  else:
   seen=set()
   for c in cells:
    if c.x0>=x0-1 and c.x1<=x1+1 and c.width>(x1-x0)*.42 and c.height>22 and c.y0>=header_bottom-1:
     key=(round(c.y0,1),round(c.y1,1))
     if key not in seen:
      seen.add(key); candidates.append((pdf.Rect(x0,c.y0,x1,c.y1),''))
  for di,(r,original_id) in enumerate(candidates,1):
   rid=f'{src}-{n:03}-t{ti:02}-d{di:02}'
   ctx=context_at(r)
   class_cells=[c for c in ctx if c['bbox'][2]<=x0+1]
   right=[c for c in ctx if c['bbox'][0]>=x1-1]
   description=rect_text(p,r,ocr) if description_inside else '\n\n'.join(c['text'] for c in right if c['bbox'][0]<desc.x1-1 and c['text'])
   req='\n\n'.join(c['text'] for c in right if (description_inside or c['bbox'][0]>=desc.x1-1) and c['text'])
   class_text='\n'.join(c['text'] for c in class_cells if c['text'])
   numbers=sorted(set(re.findall(r'\b(\d{1,2})\)',description)),key=int) if src!='iiw' else [original_id]
   if src=='iiw':
    fat_headers=[(c,v) for c,v in headers if 'fat' in v]
    vals={}
    for hc,v in fat_headers:
     vals['steel' if 'st' in v else 'aluminium']=rect_text(p,pdf.Rect(hc.x0,r.y0,hc.x1,r.y1))
    class_text='; '.join(k+': '+v for k,v in vals.items())
    req=rect_text(p,pdf.Rect(max(c.x1 for c,v in fat_headers),r.y0,t.bbox[2],r.y1)) if fat_headers else req
   else: vals={}
   img=f'assets/details/{rid}.png'; render(p,r,img,260)
   rowimg=f'assets/rows/{rid}.png'; render(p,pdf.Rect(t.bbox[0],r.y0,t.bbox[2],r.y1),rowimg,180)
   record={'id':rid,'source':src,'pdf_page':n,'printed_page':str(n+SOURCES[src]['printed_offset']),'table':cap,'original_detail_numbers':numbers,'description':description,'requirements':req,'class_text':class_text,'fat_by_material_text':vals,'image':img,'context_image':rowimg,'table_image':timg,'table_id':tid,'bbox':serial_rect(r),'context_cells':ctx,'extraction':'ocr' if ocr else 'pdf_text','status':'extracted_not_engineering_validated','notes':['Leggere la tabella completa per condizioni condivise, varianti e note. Le celle unite sono conservate integralmente; nessuna assegnazione numerica inferita.']}
   record['detail_number_status']='not_checked'
   record['fat_steel_mpa']=int(vals['steel']) if re.fullmatch(r'\d+',vals.get('steel','')) else None
   record['fat_aluminium_mpa']=int(vals['aluminium']) if re.fullmatch(r'\d+',vals.get('aluminium','')) else None
   if rid in CROPS:
    for ci,(label,a,b,c,e) in enumerate(CROPS[rid],1):
     item={**record,'original_detail_numbers':label.split(','),'detail_number_status':'visually_checked','context_group_id':rid}
     if len(CROPS[rid])>1:
      item['id']=rid+f'-{ci:02}'
      cr=pdf.Rect(r.x0+a*r.width,r.y0+b*r.height,r.x0+c*r.width,r.y0+e*r.height)
      item['bbox']=serial_rect(cr); item['image']=f'assets/details/{item["id"]}.png';render(p,cr,item['image'],260)
     records.append(item)
   else: records.append(record)
 return tables,records

def main():
 sys.stdout.reconfigure(encoding='utf8')
 pages=[]; tables=[]; details=[]; manifest=[]
 for src,meta in SOURCES.items():
  path=ROOT/f'sources/{src}.pdf'; original=path.read_bytes(); d=pdf.open(path)
  assert len(d)==meta['total_pages']
  if src=='ec3':
   sm=json.loads((ROOT/'data/symbol-map.json').read_text(encoding='utf8'))['mapping']
   cmap='/CIDInit /ProcSet findresource begin\n12 dict begin\nbegincmap\n/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def\n/CMapName /RecoveredSymbol def\n/CMapType 2 def\n1 begincodespacerange\n<0000> <FFFF>\nendcodespacerange\n'+str(len(sm))+' beginbfchar\n'+'\n'.join(f'<{int(k):04X}> <{v.encode("utf-16-be").hex().upper()}>' for k,v in sm.items())+'\nendbfchar\nendcmap\nCMapName currentdict /CMap defineresource pop\nend\nend'
   ref=d.get_new_xref(); d.update_object(ref,'<<>>');d.update_stream(ref,cmap.encode('ascii'))
   for font in {f[0]:f for p in d for f in p.get_fonts()}.values():
    if 'SymbolMT' in font[3] and font[5]=='Identity-H':d.xref_set_key(font[0],'ToUnicode',f'{ref} 0 R')
  source={**meta,'id':src,'file':f'sources/{src}.pdf','sha256':hashlib.sha256(original).hexdigest(),'bytes':len(original),'rights':'Diritti dei rispettivi titolari; nessuna licenza sui documenti è conferita da questo archivio.'}
  manifest.append(source); source_pages=[]
  for first,last,section in meta['sections']:
   for num in range(first,last+1):
    p=d[num-1]; p.remove_rotation(); clip=scope(src,num,p); ocr=ocr_lines(src,num)
    native=rect_text(p,clip); txt=rect_text(p,clip,ocr) if ocr else native
    pid=f'{src}-{num:03}'; img=f'assets/pages/{pid}.png'; render(p,clip,img,145)
    issue=['Formule, simboli e associazioni delle tabelle non sono convalidati per il calcolo.']
    if ocr: issue.append('Testo ottenuto con OCR; verificare simboli greci, apici, pedici e disuguaglianze sulla pagina.')
    pr={'id':pid,'source':src,'pdf_page':num,'printed_page':str(num+meta['printed_offset']),'section':section,'bbox':serial_rect(clip),'coordinate_system':'PDF points, origin top-left, displayed orientation','text':txt,'extraction':'ocr' if ocr else 'pdf_text','image':img,'markdown':f'docs/pages/{pid}.md','status':'extracted_not_engineering_validated','warnings':issue}
    pages.append(pr); source_pages.append(pr)
    tm,ds=extract_tables(p,src,num,ocr) if (src=='ntc' and 127<=num<=133) or (src=='ec3' and (22<=num<=37 or num==41)) or (src=='iiw' and 47<=num<=74) else ([],[])
    tables.extend(tm); details.extend(ds)
    front=yaml.safe_dump({k:v for k,v in pr.items() if k!='text'},allow_unicode=True,sort_keys=False)
    md=f'---\n{front}---\n\n# {section} — pagina PDF {num}\n\nFonte: [{meta["title"]}](../../sources/{src}.pdf#page={num}). Pagina stampata: {pr["printed_page"]}.\n\n> '+ ' '.join(issue)+'\n\n## Testo estratto\n\n'
    # Reflow prose at blank paragraphs; keep formula-like / layout-sensitive blocks fenced.
    for block in re.split(r'\n\s*\n',txt):
     lines=[line.strip() for line in block.splitlines()]
     if len(lines)>2 and (sum(len(l)<25 for l in lines)>len(lines)*.5 or any('  ' in l for l in lines)):
      md+='```text\n'+block+'\n```\n\n'
     else: md+=' '.join(lines)+'\n\n'
    if tm:
     md+='## Tabelle e dettagli\n\n'
     md+='\n'.join(f'- [{x["id"]}](../details/{x["id"]}.md) — {x["class_text"].replace(chr(10),"; ")}' for x in ds)+'\n\n'
    md+=f'## Pagina di riscontro\n\n![Pagina PDF {num}: {section}](../../{img})\n'
    write(pr['markdown'],md)
    write(f'data/native/{pid}.txt',native+'\n')
    print(src,num,'details',len(ds),flush=True)
  index=f'# {meta["title"]}\n\nEdizione: {meta["edition"]}. Lingua: {meta["language"]}.\n\n[PDF originale](../../sources/{src}.pdf) · [Manifesto e impronte SHA-256](../../data/sources.json)\n\n'
  index+='\n'.join(f'- [{p["section"]} — PDF {p["pdf_page"]}, stampata {p["printed_page"]}](../pages/{p["id"]}.md)' for p in source_pages)+'\n'
  write(f'docs/documents/{src}.md',index)
 for t in tables:
  md=f'# {t["source"].upper()} — Tabella {t["table"]}\n\n[Pagina PDF {t["pdf_page"]}](../pages/{t["source"]}-{t["pdf_page"]:03}.md)\n\n![Tabella originale](../../{t["image"]})\n\n## Celle estratte\n\n| Rettangolo (punti PDF) | Testo della cella |\n| --- | --- |\n'
  for c in t['cells']:
   md+='| '+str(c['bbox'])+' | '+c['text'].replace('|','\\|').replace('\n','<br>')+' |\n'
  write(f'docs/tables/{t["id"]}.md',md)
 for r in details:
  front=yaml.safe_dump({k:v for k,v in r.items() if k not in ['context_cells','description','requirements']},allow_unicode=True,sort_keys=False)
  md=f'---\n{front}---\n\n# {r["source"].upper()} · {r["table"]} · dettaglio {", ".join(r["original_detail_numbers"]) or r["id"]}\n\n'
  md+=f'[Pagina estratta](../pages/{r["source"]}-{r["pdf_page"]:03}.md) · [PDF originale](../../sources/{r["source"]}.pdf#page={r["pdf_page"]})\n\n'
  md+=f'![Dettaglio costruttivo](../../{r["image"]})\n\n## Classificazione riportata\n\n{r["class_text"] or "Consultare la tabella originale."}\n\n## Descrizione e condizioni\n\n{r["description"]}\n\n## Requisiti e note\n\n{r["requirements"]}\n\n'
  md+='> Estrazione documentale da verificare. Le categorie non sono valori di progetto pronti per il calcolo. Celle condivise e varianti non vanno separate dalle condizioni.\n\n'
  md+=f'## Tabella completa\n\n![Contesto completo, comprese celle unite](../../{r["table_image"]})\n'
  write(f'docs/details/{r["id"]}.md',md)
 js('data/sources.json',manifest); js('data/tables.json',tables); js('data/details.json',details)
 write('data/pages.jsonl',''.join(json.dumps(p,ensure_ascii=False)+'\n' for p in pages))
 write('data/details.jsonl',''.join(json.dumps(p,ensure_ascii=False)+'\n' for p in details))
 with (ROOT/'data/details.csv').open('w',encoding='utf-8-sig',newline='') as f:
  fields=['id','source','pdf_page','table','original_detail_numbers','class_text','description','requirements','image','status']
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader()
  for r in details: w.writerow({**r,'original_detail_numbers':','.join(r['original_detail_numbers'])})
 js('data/coverage.json',{'pages':len(pages),'tables':len(tables),'details':len(details),'per_source':{s:{'pages':sum(p['source']==s for p in pages),'details':sum(p['source']==s for p in details),'tables':sum(p['source']==s for p in tables)} for s in SOURCES}})

if __name__=='__main__': main()
