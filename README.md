# Ricerca degli atti dell'Albo Pretorio del Comune di Genova e pubblicazione su un canale Telegram dedicato

Seleziona gli atti in pubblicazione dell'Albo Pretorio del Comune di Genova in base a determinate parole e/o sequenze di parole chiave (formato di output: html o csv).

Pubblica gli atti sul canale Telegram non ufficiale https://t.me/AlboPOPComuneGenova

Il sito dell'albo pretorio del Comune di Genova (https://alboonline.comune.genova.it/albopretorio/) attualmente non consente: 

- lo scarico dei dati in un formato tabellare. Alcuni Comuni forniscono la possibilità di esportare i dati in un formato aperto e con una licenza di open data come per esempio il Comune di Biella (https://www.comune.biella.it/servizi-on-line/biella-open-data). 

- la ricerca per parole e/o sequenze di parole chiave alternative. La ricerca con l’operatore logico OR consente infatti di estrarre più dati rispetto alle ricerche con l’operatore logico AND. 

Come affermano i promotori del progetto AlboPOP.it realizzato dall'associazione onData: "Gli Albi Pretori sono una fonte preziosissima di informazioni, che le PA devono pubblicare in una sezione specifica dei loro siti internet. All'interno, ad esempio, si trovano: avvisi pubblici, bandi di concorso, determine dirigenziali, avvisi ed esiti di gare, notifiche, ordinanze del sindaco, pubblicazioni di matrimonio, ecc. Si tratta di elementi molto utili a chi vuole vivere il proprio territorio in modo consapevole e attivo."

E aggiungono: "Gli Albi pretori online attualmente non forniscono quasi mai strumenti che consentano ai cittadini di essere avvisati in modo automatico per ogni nuova pubblicazione. Inoltre non esiste un formato Standard per le Pubbliche Amministrazioni."

Questo programma nasce da una richiesta specifica di aiuto proveniente dal comitato genovese Con i piedi per terra che ha la necessità di monitorare giornalmente gli atti pubblicati dall'Albo pretorio.

Siccome la stessa esigenza può accomunare altri comitati locali, ma anche singoli cittadini, abbiamo voluto generalizzare il programma di ricerca degli atti in pubblicazione mettendo a disposizione di tutti gli interessati il relativo codice con una licenza di software libero. 

Il programma vuole essere uno strumento di ricerca per aiutare quei cittadini (o gruppi di cittadini) che hanno necessità di trovare periodicamente atti su un determinato argomento in modo semplificato.

Inoltre vorrebbe essere uno sprone per l'amministrazione locale affinchè agevoli la ricerca degli atti e li metta a disposizione in un formato aperto con una licenza di open data. 

Il programma (scritto in python) esegue le seguenti operazioni:

•  Seleziona i dati (numero di pubblicazione e dell'atto, data di inizio e di fine pubblicazione, oggetto e data di adozione) degli atti in pubblicazione che contengono determinate parole e/o sequenze di parole chiave nella colonna oggetto 
    
•  Aggiunge una colonna (urlAtto) con il link all'atto sul sito del Comune di Genova
    
•  Salva i dati selezionati in formato html/csv (a scelta)

•  Salva tutti gli atti in pubblicazione in un feed rss (in formato xml).

Per eseguire lo script occorre installare Python e alcune librerie. Meglio in un ambiente virtuale.

```
# creare ambiente virtuale
python -m venv .venv
# attivarlo
source .venv/bin/activate
# installare i requisiti
pip install -r requirements.txt
```

Clonando questo repository, verranno anche create le sottocartelle necessarie (temp e pub). Di queste, solo una e' pensata per essere esposta sul web (pub), mentre l'accesso alla sua sottocartella archive dovrebbe essere protetto. 

Da linea di comando digitare:
```
py download_and_search.py formato_file_output parola_chiave_1 parola_chiave_2 ... parola_chiave_N
```
(formato_file_output = csv,html - per cercare una sequenza esatta di parole aggiungere la sequenza tra parentesi "...")

Esempi:
```
py download_and_search.py csv cantiere marassi
```
(ritorna gli atti in pubblicazione che contengono le parole "cantiere" e "marassi" in formato "csv")
```    
py download_and_search.py html "stazione principe" lavori
```
(ritorna gli atti in pubblicazione che contengono le parole "stazione principe" e "lavori" in formato "html")
    
```
py download_and_search.py
```
(ritorna gli atti in pubblicazione in formato "html" - il formato di default)
     
```
py download_and_search.py html
```
(ritorna gli atti in pubblicazione in formato "html")
    
```
py download_and_search.py csv 
```
(ritorna gli atti in pubblicazione in formato "csv")

Se le ricerche sono ricorrenti e prevedono la selezione di atti che hanno sempre le stesse parole e/o sequenze di parole chiave, queste ultime possono essere memorizzate nel file download_and_search.py impostando la variabile RECURRENT_SEARCH_TERMS (nel file .env). Ciò evita di dover digitare le parole e/o sequenze di parole chiave da ricercare sulla linea di comando.

Un secondo script (upd_alboge_channel_async.py) si occupa di:

•  leggere il feed rss (prodotto dal primo script) con gli atti dell'albo pretorio del Comune di Genova in pubblicazione e

•  pubblicare gli atti sul canale Telegram non ufficiale degli atti dell'albo pretorio del Comune di Genova (https://t.me/AlboPOPComuneGenova)
