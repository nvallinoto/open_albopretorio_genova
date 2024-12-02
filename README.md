# Strumento per facilitare la ricerca degli atti dell'Albo Pretorio del Comune di Genova

Seleziona gli atti in pubblicazione dell'Albo Pretorio del Comune di Genova in base a determinate parole chiave.

Il sito dell'albo pretorio del Comune di Genova (https://alboonline.comune.genova.it/albopretorio/) attualmente non consente lo scarico in formato tabellare (per esempio csv/html). 

Come affermano i promotori del progetto AlboPOP.it (realizzato dall'associazione onData): "Gli Albi Pretori sono una fonte preziosissima di informazioni, che le PA devono pubblicare in una sezione specifica dei loro siti internet. All'interno, ad esempio, si trovano: avvisi pubblici, bandi di concorso, determine dirigenziali, avvisi ed esiti di gare, notifiche, ordinanze del sindaco, pubblicazioni di matrimonio, ecc. Si tratta di elementi molto utili a chi vuole vivere il proprio territorio in modo consapevole e attivo." 

E aggiungono: "Gli Albi pretori online attualmente non forniscono quasi mai strumenti che consentano ai cittadini di essere avvisati in modo automatico per ogni nuova pubblicazione. Inoltre non esiste un formato Standard per le Pubbliche Amministrazioni."

Questo programma vuole essere uno strumento di ricerca per aiutare quei cittadini (o gruppi di cittadini) che hanno necessità di trovare atti su un determinato argomento in modo semplificato. 

Il programma (scritto in python) esegue le seguenti operazioni
- Seleziona i dati (numero di pubblicazione e dell'atto, data di inizio e di fine pubblicazione, oggetto e data di adozione) degli atti in pubblicazione che contengono determinate parole chiave nella colonna oggetto
- Aggiunge una colonna (urlAtto) con il link all'atto sul sito del Comune di Genova
- Salva i dati selezionati in formato html/csv (a scelta)

Per eseguire lo script occorre installare Python e la libreria pandas. E creare due sottocartelle temp (dove vengono memorizzati temporaneamente i dati in formato json e csv) e pub (dove viene salvato il file con il risultato finale) nella cartella dove avete scaricato il progetto.

Da linea di comando digitare: 

- python download_and_search.py formato_file_output parola_chiave_1 parola_chiave_2 ... parola_chiave_N (formato_file_output = csv,html - per cercare una sequenza esatta di parole aggiungere la sequenza tra parentesi "")

Esempi:
  
- python download_and_search.py csv cantiere marassi (ritorna gli atti in pubblicazione che contengono le parole "cantiere" e "marassi" in formato "csv")
- python download_and_search.py html "stazione principe" lavori (ritorna gli atti in pubblicazione che contengono le parole "stazione principe" e "lavori" in formato "html")
- python download_and_search.py (ritorna gli atti in pubblicazione in formato "html" - il formato di default)
- python download_and_search.py html (ritorna gli atti in pubblicazione in formato "html")
- python download_and_search.py csv (ritorna gli atti in pubblicazione in formato "csv")
  
Se le ricerche sono ricorrenti e prevedono la selezione di atti che hanno sempre le stesse parole chiave, queste ultime possono essere memorizzate nel file download_and_search.py impostando la variabile RECURRENT_SEARCH_TERMS. Ciò evita di dover digitare le parole chiave da ricercare sulla linea di comando.
