# Strumento per facilitare la ricerca degli atti dell'Albo Pretorio del Comune di Genova

Seleziona gli atti in pubblicazione dell'Albo Pretorio del Comune di Genova in base a determinate parole e/o sequenze di parole chiave.

Il sito dell'albo pretorio del Comune di Genova (https://alboonline.comune.genova.it/albopretorio/) attualmente non consente lo scarico dei dati in un formato tabellare. Alcuni Comuni forniscono la possibilità di esportare i dati in un formato aperto e con una licenza di open data come per esempio il Comune di Biella (https://www.comune.biella.it/servizi-on-line/biella-open-data). Inoltre non consente la ricerca per parole e/o sequenze di parole chiave alternative. La ricerca con l’operatore logico OR consente infatti di estrarre più dati rispetto alle ricerche con l’operatore logico AND. 

Come affermano i promotori del progetto AlboPOP.it realizzato dall'associazione onData: "Gli Albi Pretori sono una fonte preziosissima di informazioni, che le PA devono pubblicare in una sezione specifica dei loro siti internet. All'interno, ad esempio, si trovano: avvisi pubblici, bandi di concorso, determine dirigenziali, avvisi ed esiti di gare, notifiche, ordinanze del sindaco, pubblicazioni di matrimonio, ecc. Si tratta di elementi molto utili a chi vuole vivere il proprio territorio in modo consapevole e attivo."

E aggiungono: "Gli Albi pretori online attualmente non forniscono quasi mai strumenti che consentano ai cittadini di essere avvisati in modo automatico per ogni nuova pubblicazione. Inoltre non esiste un formato Standard per le Pubbliche Amministrazioni."

Questo programma nasce da una richiesta specifica di aiuto proveniente dal comitato genovese Con i piedi per terra che ha la necessità di monitorare giornalmente gli atti pubblicati dall'Albo pretorio.

Siccome la stessa esigenza può accomunare altri comitati locali, ma anche singoli cittadini, abbiamo voluto generalizzare il programma di ricerca degli atti in pubblicazione.  

Per questo motivo il codice del programma viene ora messo a disposizione di tutti con una licenza di software libero. 

Il programma vuole essere uno strumento di ricerca per aiutare quei cittadini (o gruppi di cittadini) che hanno necessità di trovare periodicamente atti su un determinato argomento in modo semplificato.

Inoltre vorrebbe essere uno sprone per l'amministrazione locale affinchè agevoli la ricerca degli atti e li metta a disposizione in un formato aperto con una licenza di open data. 

Il programma (scritto in python) esegue le seguenti operazioni:

•  Seleziona i dati (numero di pubblicazione e dell'atto, data di inizio e di fine pubblicazione, oggetto e data di adozione) degli atti in pubblicazione che contengono determinate parole e/o sequenze di parole chiave nella colonna oggetto 
    
•  Aggiunge una colonna (urlAtto) con il link all'atto sul sito del Comune di Genova
    
•  Salva i dati selezionati in formato html/csv (a scelta)

Per eseguire lo script occorre installare Python e la libreria pandas. E creare due sottocartelle temp (dove vengono memorizzati temporaneamente i dati in formato json e csv) e pub (dove viene salvato il file con il risultato finale) nella cartella dove avete scaricato il progetto.

Da linea di comando digitare:

•  py download_and_search.py formato_file_output parola_chiave_1 parola_chiave_2 ... parola_chiave_N (formato_file_output = csv,html - per cercare una sequenza esatta di parole aggiungere la sequenza tra parentesi "...")

Esempi:

•  py download_and_search.py csv cantiere marassi (ritorna gli atti in pubblicazione che contengono le parole "cantiere" e "marassi" in formato "csv")
    
•  py download_and_search.py html "stazione principe" lavori (ritorna gli atti in pubblicazione che contengono le parole "stazione principe" e "lavori" in formato "html")
    
•  py download_and_search.py (ritorna gli atti in pubblicazione in formato "html" - il formato di default)
    
•  py download_and_search.py html (ritorna gli atti in pubblicazione in formato "html")
    
•  py download_and_search.py csv (ritorna gli atti in pubblicazione in formato "csv")

Se le ricerche sono ricorrenti e prevedono la selezione di atti che hanno sempre le stesse parole e/o sequenze di parole chiave, queste ultime possono essere memorizzate nel file download_and_search.py impostando la variabile RECURRENT_SEARCH_TERMS. Ciò evita di dover digitare le parole e/o sequenze di parole chiave da ricercare sulla linea di comando.
