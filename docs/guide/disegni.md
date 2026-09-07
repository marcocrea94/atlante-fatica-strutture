# Disegni dei dettagli

Le 245 schede dell’atlante sono illustrate con disegni tecnici SVG a colori. Ogni immagine si può aprire e scaricare dalla propria scheda, ingrandire senza perdita di nitidezza e riutilizzare nei limiti applicabili alle fonti. Le anteprime del catalogo mostrano la geometria; il disegno completo include titolo, riferimento e legenda.

| Colore | Significato |
| --- | --- |
| Blu | Elementi metallici; le tonalità distinguono le facce |
| Arancio | Saldature e sezioni del materiale d’apporto |
| Turchese | Azioni e direzioni della sollecitazione |
| Viola | Radice, ripresa o zona evidenziata, quando indicata |

I disegni sono schemi non in scala, con proporzioni semplificate. Non si ricavano dimensioni dalla figura. La classificazione dipende anche da finitura, processo di saldatura, controlli, spessore e altri requisiti che possono distinguere schede con la stessa geometria. Occorre leggere le condizioni nella scheda e confrontarle con il PDF originale. Le quote limite non sono tutte ripetute nella figura: rimangono nella trascrizione e nella fonte.

## Provenienza e ricostruzione

I diagrammi sono costruiti da geometrie vettoriali parametrizzate; non contengono screenshot, immagini raster incorporate o tracciati grafici estratti dal PDF. Il manifesto [illustrations.json](../../data/illustrations.json) associa esplicitamente ogni scheda alla famiglia geometrica, alla variante e alla pagina di origine. L’identificativo della scheda rimane stabile.

Per **IIW 731, pagina PDF 70**, e **IIW 912, pagina PDF 73**, la cella grafica è vuota nel documento fornito. I relativi disegni sono ricostruzioni editoriali dalla descrizione: questa condizione è dichiarata nelle due schede e nei dati, con `review: editorial_from_source_description`.

Gli originali PDF e i ritagli della prima estrazione restano conservati per tracciabilità. Il sito rimanda direttamente al PDF per vedere le figure della fonte e presenta i disegni nuovi nelle schede. Per le tabelle si consultano le celle Markdown e il rimando al PDF, senza screenshot incorporati.

## Lettura tramite AI

`data/details.json`, JSONL e CSV indicano il nuovo SVG nel campo `image`; `source_image` identifica il vecchio ritaglio documentale. `bbox` continua a descrivere il rettangolo della fonte in punti PDF, non le coordinate del disegno nuovo. `illustration` contiene titolo, testo alternativo, anteprima, metodo, stato e impronta SHA-256. Le coordinate SVG non sono misure di progetto.

## Controlli

La copertura automatica richiede un disegno e un’anteprima per ogni scheda, assenza di raster incorporati, integrità dei PDF originali e collegamenti risolti. È stato confrontato il catalogo grafico con i ritagli delle fonti e sono stati controllati i disegni renderizzati. Il controllo riguarda la rappresentazione documentale e non costituisce una validazione ingegneristica delle classi o delle verifiche.
