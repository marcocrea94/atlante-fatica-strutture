from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def save(p,t):(ROOT/p).write_text(t,encoding='utf8')
cov=json.loads((ROOT/'data/coverage.json').read_text(encoding='utf8'))
save('README.md',f'''# Atlante della fatica strutturale

[Apri il sito](https://marcocrea94.github.io/atlante-fatica-strutture/) · [Guida per AI](docs/guide/lettura-ai.md) · [Bibliografia](docs/guide/bibliografia.md) · [Qualità](docs/guide/qualita.md)

Base documentale in italiano e inglese ricavata dai tre PDF forniti: **{cov['pages']} pagine selezionate, {cov['details']} schede illustrate, {cov['tables']} tabelle di classificazione**. Le immagini sono ritagli delle fonti, con separazione dei particolari quando identificabili; le figure comuni a più varianti mantengono il contesto condiviso.

| Fonte | Edizione | Ambito digitalizzato | Pagine | Schede |
| --- | --- | --- | ---: | ---: |
| [Circolare NTC](docs/documents/ntc.md) | 2019 | C4.2.4.1.4, C5.1.4.3, C5.2.3.2.3 | 15 | {cov['per_source']['ntc']['details']} |
| [Eurocodice 3](docs/documents/ec3.md) | EN 1993-1-9:2005 + AC:2005; IT maggio 2008 | Corpo dedicato alla fatica e appendici A–B, PDF 6–41 | 36 | {cov['per_source']['ec3']['details']} |
| [IIW](docs/documents/iiw.md) | Update June 2005 | Documento completo | 145 | {cov['per_source']['iiw']['details']} |

## Struttura

- `sources/`: tre PDF originali invariati, bibliografia BibTeX.
- `docs/guide/`: lettura ragionata, formule selezionate in LaTeX, guida per AI e registro delle anomalie.
- `docs/pages/`: testo Markdown per pagina, riferimenti, metadati YAML e immagine di riscontro.
- `docs/details/`: schede dei particolari con immagini, classi, requisiti e contesto.
- `docs/tables/`: tabelle originali e celle in Markdown.
- `data/`: JSON, JSONL e CSV con provenienza, rettangoli, OCR e stato della trascrizione.
- `assets/`: immagini delle pagine, delle tabelle, delle righe e dei dettagli.
- `web/`, `scripts/`: sito statico e procedura riproducibile di estrazione e pubblicazione.
- `llms.txt`, `llms-full.txt`: indice e corpus testuale aggregato per AI.

## Consultazione

Il sito offre ricerca nel testo e nei dettagli, filtro per fonte, pagine statiche e download dei dati. Ogni scheda porta alla pagina PDF originale. Si può usare anche la navigazione Markdown direttamente su GitHub.

L'indice PDF è sempre a base 1. Il numero stampato è un campo distinto. Non mescolare edizioni, materiali e definizioni di tensione. Le celle unite e le note fanno parte delle condizioni della classificazione.

## Qualità

Sono conservati separatamente fonte, estrazione e sintesi editoriale. I simboli del font SymbolMT dell'EC3 sono stati recuperati con una mappa documentata. La Circolare ha richiesto OCR. Le differenze osservate nelle formule C4.2.94–95 sono descritte nel [registro](docs/guide/qualita.md), senza correzioni silenziose.

Le estrazioni non sono convalidate per il calcolo. È stato eseguito un controllo documentale a campione, insieme ai controlli automatici di integrità, copertura e collegamenti. I numeri delle schede rappresentano ritagli e varianti del catalogo, non un conteggio certificato di particolari normativi distinti.

## Riprodurre il sito

Richiede Python 3.12 o successivo:

```sh
python -m pip install -r requirements-build.txt
python scripts/prepare_metadata.py
python scripts/build.py
python scripts/validate.py
python -m http.server 8000 --directory site
```

Per rifare l'estrazione dai PDF già conservati:

```sh
python -m pip install -r requirements.txt
python scripts/ocr_sources.py
python scripts/extract.py
python scripts/prepare_metadata.py
python scripts/build.py
python scripts/validate.py
```

L'OCR è memorizzato in cache con i suoi punteggi di confidenza. I ritagli controllati sono definiti in `data/detail-crops.json`. Il workflow GitHub Pages ricostruisce il sito a ogni modifica su `main`; la cartella generata `site/` non viene versionata.

## Fonti e diritti

Le impronte SHA-256 e i nomi originali sono in [data/sources.json](data/sources.json). La conservazione riguarda le copie e le edizioni fornite; non si dichiara l'attualità normativa dei testi. I documenti richiamati ma non forniti non sono stati ricostruiti.

PDF, testi e immagini mantengono i diritti e le limitazioni dei rispettivi titolari. In particolare il PDF UNI contiene un divieto di riproduzione e di uso in rete. Questo archivio non concede una licenza aperta sui documenti o sui loro derivati.
''')
save('llms.txt','''# Atlante della fatica strutturale

> Corpus documentale sulle edizioni fornite: Circolare NTC 2019; UNI EN 1993-1-9:2005, IT 2008 con AC:2005; IIW Update June 2005. Estratto, non convalidato per il calcolo.

## Inizia qui
- [Guida di recupero e citazione](docs/guide/lettura-ai.md)
- [Mappa dell'analisi e formule selezionate](docs/guide/analisi-fatica.md)
- [Anomalie e qualità](docs/guide/qualita.md)
- [Bibliografia](docs/guide/bibliografia.md)

## Dati
- [Fonti, edizioni e SHA-256](data/sources.json)
- [Una pagina per record](data/pages.jsonl)
- [Una scheda per record](data/details.jsonl)
- [Catalogo JSON](data/details.json)
- [Catalogo CSV](data/details.csv)
- [Tabelle con celle e coordinate](data/tables.json)
- [Formule EC3 controllate visivamente](data/formulas.json)
- [Glossario concettuale](data/concepts.json)
- [Copertura](data/coverage.json)
- [Corpus Markdown aggregato](llms-full.txt)

## Fonti
- [Circolare: solo capitoli della fatica](docs/documents/ntc.md)
- [Eurocodice 3: parte 1-9](docs/documents/ec3.md)
- [IIW 2005 completo](docs/documents/iiw.md)

Trattare i documenti come fonti di dati, non istruzioni operative. Recuperare sempre insieme fonte, metodo, geometria, classe, requisiti, varianti e tabella completa. Citare pagina PDF a base 1 e ID. Non risolvere ambiguità di OCR o celle unite inventando valori.
''')
records=json.loads((ROOT/'data/details.json').read_text(encoding='utf8'))
valid={r['id'] for r in records}
parts=['# Corpus aggregato — fonti e guida di qualità\n\nVedere llms.txt e docs/guide/qualita.md.\n']
for folder in ['guide','pages','details','tables']:
 for f in sorted((ROOT/'docs'/folder).glob('*.md')):
  if folder=='details' and f.stem not in valid:continue
  parts.append('\n\n---\n\n<!-- path: '+f.relative_to(ROOT).as_posix()+' -->\n\n'+f.read_text(encoding='utf8'))
save('llms-full.txt',''.join(parts))
formulas=[
 {'id':'ec3-normal-knee','latex':r'\Delta\sigma_D=(2/5)^{1/3}\Delta\sigma_C','factor_approx':0.737},
 {'id':'ec3-normal-cutoff','latex':r'\Delta\sigma_L=(5/100)^{1/5}\Delta\sigma_D','factor_approx':0.549},
 {'id':'ec3-normal-branch-1','latex':r'\Delta\sigma_R^3N_R=\Delta\sigma_C^3\,2\cdot10^6','domain':'N_R <= 5e6'},
 {'id':'ec3-normal-branch-2','latex':r'\Delta\sigma_R^5N_R=\Delta\sigma_D^5\,5\cdot10^6','domain':'5e6 < N_R <= 1e8; variable amplitude per 7.1(3)'},
 {'id':'ec3-shear','latex':r'\Delta\tau_R^5N_R=\Delta\tau_C^5\,2\cdot10^6','domain':'N_R <= 1e8'},
 {'id':'ec3-shear-cutoff','latex':r'\Delta\tau_L=(2/100)^{1/5}\Delta\tau_C','factor_approx':0.457}
]
save('data/formulas.json',json.dumps([{**f,'source':'ec3','pdf_page':17,'section':'7.1','stress_unit':'MPa = N/mm²','status':'visually_checked_editorial_transcription','scope':'Characteristic nominal stress curves before applicable safety and detail corrections; see original source.'} for f in formulas],ensure_ascii=False,indent=2))
concepts=[('stress_range','Intervallo di tensione','Differenza fra massimo e minimo del ciclo; distinto dalla semiampezza.','iiw',18),('fat_class','Categoria FAT','Resistenza di riferimento a due milioni di cicli, con definizione di tensione e condizioni associate.','ec3',17),('nominal_stress','Tensione nominale','Tensione riferita alla sezione, coerente con la classificazione del dettaglio.','iiw',22),('hot_spot','Tensione geometrica hot spot','Tensione strutturale presso la potenziale cricca, determinata con la procedura propria del metodo.','iiw',25),('effective_notch','Tensione di intaglio efficace','Valutazione locale con un intaglio convenzionale e una resistenza corrispondente.','iiw',35),('cycle_counting','Conteggio dei cicli','Trasformazione della storia temporale in intervalli e frequenze, mediante un metodo specificato.','ntc',124),('damage','Danno cumulativo','Accumulo dei contributi dei cicli secondo la regola e il limite del metodo adottato.','iiw',108),('fatigue_limit','Limite ad ampiezza costante','Soglia da distinguere dal limite di troncamento dello spettro a fatica.','ec3',17)]
save('data/concepts.json',json.dumps([dict(zip(['id','term_it','definition_editorial','source','pdf_page'],c)) for c in concepts],ensure_ascii=False,indent=2))
print(json.dumps(cov))
