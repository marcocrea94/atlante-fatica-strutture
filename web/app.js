'use strict';
const $=id=>document.getElementById(id);
const names={ntc:'Circolare NTC',ec3:'Eurocodice 3',iiw:'IIW'};
const state={details:[],pages:[],limit:24};
const norm=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n};
function card(r,isPage){
 const a=el('a','card');a.href=isPage?`docs/pages/${r.id}.html`:`docs/details/${r.id}.html`;
 const frame=el('div','card-image'),img=el('img');img.src=r.image;img.alt=isPage?`${names[r.source]}, pagina ${r.pdf_page}`:`Disegno del dettaglio ${r.id}`;img.loading='lazy';img.decoding='async';frame.append(img);
 const body=el('div','card-body'),meta=el('div','card-meta'),badge=el('span','badge');badge.append(el('i',`dot ${r.source}`),document.createTextNode(names[r.source]));meta.append(badge,el('span','',`PDF ${r.pdf_page}`));body.append(meta);
 body.append(el('h2','',isPage?r.section:(r.description||`Dettaglio ${r.table}`).replace(/\s+/g,' ').slice(0,190)));
 if(isPage)body.append(el('p','card-description',r.text.slice(0,180)));
 const bottom=el('div','card-class');bottom.append(el('b','',isPage?`Stampata ${r.printed_page}`:(r.class_text||`Tabella ${r.table}`).replace(/\s+/g,' ').slice(0,105)),el('span','','→'));body.append(bottom);a.append(frame,body);return a;
}
function render(reset=true){
 if(reset)state.limit=24;
 const isPage=$('view').value==='pages',source=$('source').value,query=norm($('search').value).trim(),terms=query.split(/\s+/).filter(Boolean);
 const list=(isPage?state.pages:state.details).filter(r=>(source==='all'||r.source===source)&&terms.every(t=>r.search.includes(t)));
 $('results-count').textContent=`${list.length} ${isPage?'pagine':'schede illustrate'}${query?' trovate':''}`;
 const frag=document.createDocumentFragment();list.slice(0,state.limit).forEach(r=>frag.append(card(r,isPage)));
 if(!list.length)frag.append(el('p','empty','Nessun risultato. Prova un termine più breve, una classe o un’altra fonte.'));
 $('results').replaceChildren(frag);$('more').hidden=state.limit>=list.length;
 const p=new URLSearchParams();if(query)p.set('q',$('search').value);if(source!=='all')p.set('source',source);if(isPage)p.set('view','pages');history.replaceState(null,'',location.pathname+(p.size?'?'+p:''));
}
async function init(){
 try{
  const responses=await Promise.all([fetch('data/catalog.json'),fetch('data/page-index.json')]);
  if(responses.some(r=>!r.ok))throw Error('catalog');
  [state.details,state.pages]=await Promise.all(responses.map(r=>r.json()));
  for(const r of state.details)r.search=norm([r.id,names[r.source],r.table,r.class_text,r.description,r.requirements,...r.original_detail_numbers].join(' '));
  for(const r of state.pages)r.search=norm([r.id,names[r.source],r.section,r.text].join(' '));
  const p=new URLSearchParams(location.search);$('search').value=p.get('q')||'';if(['ntc','ec3','iiw'].includes(p.get('source')))$('source').value=p.get('source');if(p.get('view')==='pages')$('view').value='pages';
  $('corpus-count').textContent=`${state.details.length} schede · ${state.pages.length} pagine`;render();
  let timer;$('search').addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(()=>render(),120)});$('source').addEventListener('change',()=>render());$('view').addEventListener('change',()=>render());$('more').addEventListener('click',()=>{state.limit+=24;render(false)});
  document.addEventListener('keydown',e=>{if(e.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){e.preventDefault();$('search').focus()}});
 }catch(e){$('results-count').textContent='Il catalogo non è disponibile.';$('results').append(el('p','empty','Apri una delle tre fonti dal menu. La consultazione delle pagine statiche resta disponibile.'))}
}
init();
