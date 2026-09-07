# Registro di qualità e ambito

## Edizioni conservate

| Fonte | Identificazione e selezione |
| --- | --- |
| Circolare | Circolare 21 gennaio 2019, n. 7, Gazzetta Ufficiale 11 febbraio 2019. Estratte soltanto C4.2.4.1.4 (PDF 123–134), C5.1.4.3 (171–172) e C5.2.3.2.3 (176). Le pagine di confine sono ritagliate per escludere altri argomenti. Il PDF completo rimane come fonte. |
| EC3 | UNI EN 1993-1-9:2005, versione italiana maggio 2008, comprendente AC:2005 secondo la copertina. Estratte pagine PDF 6–41, cioè pagine stampate 1–36, incluse appendici A e B. Copertine, indice editoriale e pagine finali rimangono nel PDF originale. |
| IIW | Doc. XIII-1965-03/XV-1127-03, Update June 2005. Tutte le 145 pagine. La copertina dichiara provvisori impaginazione, revisione tipografica e numerazione; intestazioni interne riportano anche febbraio 2005 e febbraio 2004. Non è identificato come un'edizione IIW successiva. |

## Problemi della fonte e dell'estrazione

### NTC-01 — Formule C4.2.94 e C4.2.95

Nell'immagine della [pagina PDF 125 / stampata 121](../pages/ntc-125.md), il secondo ramo della C4.2.94 riporta `2·10^6` al numeratore accanto a `ΔσD`. La C4.2.95 riporta `ΔσL = 0,549 ΔσC`. Questi elementi non coincidono con le relazioni EC3 della [pagina PDF 17 / stampata 12](../pages/ec3-017.md), dove compaiono rispettivamente `5·10^6` e `0,549 ΔσD`.

**Trattamento:** riscontro visivo conservato; nessuna correzione silenziosa del testo della Circolare. Le formule EC3 riscritte nella guida dichiarano fonte e ambito. Questa segnalazione documentale non è un'errata corrige ufficiale.

### NTC-02 — Testo assente o codifica corrotta

La pagina PDF 125 ha contenuto visibile ma quasi nessun testo estraibile. Altre pagine contengono simboli e intere celle con codifica corrotta. Per le 15 pagine selezionate è stato eseguito OCR con coordinate e punteggi di confidenza, conservato in `data/ocr/`. Le formule restano da confrontare con la fonte.

### EC3-01 — Caratteri del font SymbolMT

Il PDF non contiene una mappa Unicode per `SymbolMT-Identity-H`: l'estrazione diretta restituisce, per esempio, `V` al posto di σ e `t` al posto di ≥. È stata ricostruita la corrispondenza dei glifi osservati, registrata in `data/symbol-map.json`, e applicata **solo alla copia in memoria** durante l'estrazione. Il PDF originale è invariato. Restano da verificare l'ordine di apici, pedici, frazioni e i frammenti di parentesi grandi.

### IIW-01 — Indice e segnalibri

Parte dei segnalibri del PDF rimanda alle pagine dell'indice, invece che alle sezioni. La navigazione dell'archivio usa i titoli riscontrati nel corpo e i numeri delle pagine PDF. La pagina 46 è prevalentemente grafica ed è stata sottoposta a OCR; l'immagine è il riscontro.

### TABLE-01 — Celle unite e varianti

La rilevazione dei bordi può dividere una tabella in colonne aggiuntive o segmenti. Le schede conservano celle unite, disegno vettoriale del dettaglio e rimando alla tabella completa nel PDF. I ritagli della prima estrazione restano come provenienza nei dati e nei file di archivio. I numeri recuperati dalle descrizioni possono includere richiami ad altri particolari. Non viene inferita una corrispondenza numerica fra varianti e classi ambigue. Alcune immagini rappresentano un gruppo di varianti condivise nella fonte.

## Verifica eseguita e limiti

Sono controllati integrità SHA-256 degli originali, copertura delle pagine selezionate, esistenza delle immagini, unicità degli ID e collegamenti locali del sito. Sono stati ispezionati esempi di tabelle e dettagli per ogni fonte e le formule EC3 §7.1 e Circolare C4.2.94–95 citate sopra. Non è stata eseguita una revisione ingegneristica riga per riga dell'intero corpus.

## Diritti e bibliografia

I diritti restano ai rispettivi titolari. Il PDF UNI riporta espressamente limitazioni alla riproduzione e all'uso in rete; la conservazione qui non attribuisce una licenza di riutilizzo. La repository non applica una licenza aperta ai PDF, alle trascrizioni o alle immagini derivate. Vedere la [bibliografia](bibliografia.md).


## Ridisegno del catalogo — 7 settembre 2026

Tutte le 245 schede usano SVG nativi a colori; nessuna scheda o pagina di consultazione incorpora screenshot del PDF. I disegni sono schemi semplificati non in scala: quote limite e condizioni non ripetute nell’immagine si leggono nella trascrizione e nel PDF. La corrispondenza è registrata in `data/illustrations.json`; la copertura in `data/illustration-coverage.json`. [Metodo, legenda e limiti](disegni.md).

Il confronto grafico ha permesso di correggere cinque numerazioni della Circolare recuperate male dall’OCR: `ntc-128-t02-d06` → 9; `ntc-132-t01-d01` → 5; `ntc-133-t01-d02` → 3; `ntc-133-t01-d05` → 6; `ntc-133-t01-d06` → 7. Il dato estratto precedente è conservato in `extracted_detail_numbers`. Le classi di fatica non sono state modificate.

Nelle celle IIW 731 e 912 il PDF non presenta una figura. I due schemi sono ricostruzioni editoriali dalla descrizione, dichiarate separatamente nel campo `review` del manifesto e nelle schede. Non sono figure normative recuperate.
