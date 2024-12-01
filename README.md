# albopretorio-genova

Scarica e filtra gli atti dell'albo pretorio del Comune di Genova in base a determinate parole chiave.

Il sito dell'albo pretorio del Comune di Genova (https://alboonline.comune.genova.it/albopretorio/) attualmente non consente la ricerca degli atti per parole chiave nè lo scarico in formato tabellare (es: csv). La ricerca avanzata testuale non funziona (da una prova effettuata il 17 novembre 2024) e restituisce "Nessun atto trovato" per qualsiasi parola inserita.

Come afferma il progetto AlboPOP.it promosso dall'associazione onData: "Gli Albi Pretori sono una fonte preziosissima di informazioni, che le PA devono pubblicare in una sezione specifica dei loro siti internet. All'interno, ad esempio, si trovano: avvisi pubblici, bandi di concorso, determine dirigenziali, avvisi ed esiti di gare, notifiche, ordinanze del sindaco, pubblicazioni di matrimonio, ecc. Si tratta di elementi molto utili a chi vuole vivere il proprio territorio in modo consapevole e attivo." 

E aggiunge: "Gli Albi pretori online attualmente non forniscono quasi mai strumenti che consentano ai cittadini di essere avvisati in modo automatico per ogni nuova pubblicazione. Inoltre non esiste un formato Standard per le Pubbliche Amministrazioni."

Questo programma vuole essere uno strumento di ricerca per aiutare quei cittadini (o gruppi di cittadini) che hanno necessità di trovare atti su un determinato argomento in modo semplificato. 

Il programma (scritto in python) esegue le seguenti operazioni
- Scarica gli atti in pubblicazione dell'albo pretorio in formato json
- Seleziona gli atti che contengono determinate parole chiave nella colonna oggetto
- Cancella le colonne superflue e ne aggiunge una con il link all'atto sul sito del Comune di Genova
- Converte il file con i dati selezionati (e le colonne: pubblicazioneNumero,	attoNumero,	dataInizioPubbl,	dataFinePubbl,	oggetto,	dataAdozione,	urlAtto) in formato html/csv (a scelta)

Per eseguire lo script occorre installare Python e la libreria pandas.

Creare due sottocartelle temp e pub nella cartella dove avete scaricato il progetto.

Da linea di comando digitare: 

- python download_and_search.py format_output_file parola_chiave_1 parola_chiave_2 ... parola_chiave_N (format_output_file = csv,html)

Esempi:
  
- python download_and_search.py csv cantiere marassi (ritorna gli atti in pubblicazione che contengono le parole "cantiere" e "marassi" in formato "csv")
- python download_and_search.py html stazione principe brignole (ritorna gli atti in pubblicazione che contengono le parole "stazione", "principe" e "brignole" in formato "html")
- python download_and_search.py (ritorna gli atti in pubblicazione in formato "html" - il formato di default)
- python download_and_search.py html (ritorna gli atti in pubblicazione in formato "html")
- python download_and_search.py csv (ritorna gli atti in pubblicazione in formato "csv")
  
Se le ricerche sono ricorrenti e prevedono la ricerca di atti che hanno sempre le stesse parole chiave, queste ultime possono essere memorizzate nel file download_and_search.py impostando la variabile SEARCH_TERMS. Ciò evita di dover digitare le parole chiave da ricercare sulla linea di comando.
