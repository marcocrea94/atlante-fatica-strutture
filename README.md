# Atlante della fatica strutturale

[Apri il sito](https://marcocrea94.github.io/atlante-fatica-strutture/) · [Guida per AI](docs/guide/lettura-ai.md) · [Bibliografia](docs/guide/bibliografia.md) · [Qualità](docs/guide/qualita.md)

Base documentale in italiano e inglese ricavata dai tre PDF forniti: **196 pagine selezionate, 245 schede illustrate, 64 tabelle di classificazione**. Le immagini sono ritagli delle fonti, con separazione dei particolari quando identificabili; le figure comuni a più varianti mantengono il contesto condiviso.

| Fonte | Edizione | Ambito digitalizzato | Pagine | Schede |
| --- | --- | --- | ---: | ---: |
| [Circolare NTC](docs/documents/ntc.md) | 2019 | C4.2.4.1.4, C5.1.4.3, C5.2.3.2.3 | 15 | 68 |
| [Eurocodice 3](docs/documents/ec3.md) | EN 1993-1-9:2005 + AC:2005; IT maggio 2008 | Corpo dedicato alla fatica e appendici A–B, PDF 6–41 | 36 | 94 |
| [IIW](docs/documents/iiw.md) | Update June 2005 | Documento completo | 145 | 83 |

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
