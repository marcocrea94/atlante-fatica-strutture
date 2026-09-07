# Mappa ragionata dell'analisi a fatica

Sintesi editoriale dei documenti forniti, con riferimenti per ritrovare le prescrizioni complete.

## Dal carico al danno

**Storia dei carichi → storia delle tensioni nel dettaglio → conteggio dei cicli → spettro → curva di resistenza coerente → verifica.**

L'intervallo di tensione normale è `Δσ = σmax − σmin`. Per il taglio si usa `Δτ`. Il numero di cicli associato a ogni intervallo è parte del dato di ingresso: il solo massimo della tensione non descrive uno spettro di fatica.

Riferimenti: Circolare [C4.2.4.1.4.1–2, PDF 123–125](../pages/ntc-123.md); IIW [§2.1, PDF 18](../pages/iiw-018.md) e [§2.3, PDF 39–41](../pages/iiw-039.md); EC3 [§1.3, PDF 9–10](../pages/ec3-009.md).

## Scegliere la definizione di tensione

| Metodo | Che cosa rappresenta | Dove approfondire |
| --- | --- | --- |
| Nominale | Tensione associata alla sezione e alla classificazione del particolare; gli effetti già inclusi nella FAT non vanno conteggiati due volte | IIW §2.2.2, PDF 22–24; EC3 §§5–6 |
| Geometrico, hot spot | Effetto strutturale della geometria presso la potenziale cricca, con procedure specifiche di estrapolazione | IIW §2.2.3, PDF 25–34; EC3 appendice B, PDF 41 |
| Intaglio efficace | Modello locale con geometria di intaglio convenzionale e resistenza coerente | IIW §2.2.4, PDF 35–36; §3.4 |
| Propagazione della cricca | Evoluzione di una cricca mediante fattore di intensificazione delle tensioni e legge di crescita | IIW §2.2.5, PDF 37–38; §§3.6 e 4.4 |

La somiglianza del disegno non basta per classificare un dettaglio. Occorre controllare direzione del carico, posizione di innesco, saldatura, penetrazione, finitura, controlli, spessore e geometria. Un particolare può avere più modalità di rottura da valutare separatamente.

## Curve S–N dell'Eurocodice fornito

Queste formule sono state riscontrate visivamente in **EN 1993-1-9:2005, §7.1, pagina stampata 12 / PDF 17**. La notazione seguente è una riscrittura editoriale in LaTeX; si riferisce alle curve nominali descritte in quel paragrafo, prima dei coefficienti di progetto e delle correzioni applicabili.

```math
N_C = 2\cdot10^6,\quad N_D = 5\cdot10^6,\quad N_L = 10^8
```

```math
\Delta\sigma_D = \left(\frac{2}{5}\right)^{1/3}\Delta\sigma_C
\simeq 0.737\,\Delta\sigma_C
```

```math
\Delta\sigma_L = \left(\frac{5}{100}\right)^{1/5}\Delta\sigma_D
\simeq 0.549\,\Delta\sigma_D
```

Per lo spettro variabile cui si applica il §7.1(3):

```math
\Delta\sigma_R^3 N_R = \Delta\sigma_C^3\,2\cdot10^6
\quad (N_R\leq5\cdot10^6)
```

```math
\Delta\sigma_R^5 N_R = \Delta\sigma_D^5\,5\cdot10^6
\quad (5\cdot10^6 < N_R\leq10^8)
```

Per le tensioni tangenziali del §7.1(2):

```math
\Delta\tau_R^5 N_R = \Delta\tau_C^5\,2\cdot10^6,
\qquad \Delta\tau_L = \left(\frac{2}{100}\right)^{1/5}\Delta\tau_C
\simeq0.457\,\Delta\tau_C
```

Il rapporto `ΔσL / ΔσC ≈ 0.405` è un valore **derivato** dalle due relazioni EC3 precedenti. Non va confuso con `0.549`, che moltiplica `ΔσD`. Le incongruenze visibili nel PDF della Circolare sono registrate [separatamente](qualita.md).

[Testo e immagine della pagina EC3 17](../pages/ec3-017.md) · [curve normali, PDF 18](../pages/ec3-018.md) · [curve tangenziali, PDF 19](../pages/ec3-019.md).

## Conteggio e accumulo

Rainflow e reservoir trasformano una storia irregolare in cicli o semicicli. Il trattamento dei residui, la durata rappresentata e la ripetizione della storia devono rimanere espliciti. Vedere Circolare [PDF 124–125](../pages/ntc-124.md) e IIW [appendice 6.1, PDF 122](../pages/iiw-122.md).

La somma lineare di Palmgren–Miner usa:

```math
D=\sum_i\frac{n_i}{N_i}
```

`ni` indica i cicli applicati nella classe dello spettro; `Ni` indica i cicli resistenti secondo la curva e il metodo adottati. Il valore ammissibile del danno e i coefficienti di sicurezza si ricavano dalla fonte applicabile; **non si impone un limite universale comune ai tre documenti**. Vedere EC3 [appendice A, PDF 38–40](../pages/ec3-038.md) e IIW [§4.3, PDF 108–112](../pages/iiw-108.md).

## Carichi sui ponti nella Circolare

| Sezione | Contenuto estratto | Rinvii che richiedono altri documenti |
| --- | --- | --- |
| C5.1.4.3, PDF 171–172 | Modelli 1–2 per vita illimitata; modelli 3–4 per danneggiamento; collocazione sulle corsie; interazione dei veicoli; amplificazione presso i giunti | NTC §5.1.4.3 e tabelle dei modelli; EN 1992-2, EN 1993-2, EN 1994-2 per coefficienti equivalenti |
| C5.2.3.2.3, PDF 176 | Spettri ferroviari, coefficienti dinamici e uso del modello LM71 con coefficienti coerenti | EN 1991-2 e norme dei ponti |

Le NTC 2018 complete e gli Eurocodici sui ponti richiamati **non fanno parte dei tre PDF forniti**. I dati non presenti non sono stati ricostruiti.
