# albopretorio-genova

Scarica e filtra gli atti dell'albo pretorio del Comune di Genova in base a determinate parole chiave.
Il sito dell'albo pretorio del Comune di Genova (https://alboonline.comune.genova.it/albopretorio/) non consente la ricerca degli atti nè lo scarico in formato tabellare (es: csv). 
La ricerca avanzata non funziona (al 17/11/2024) e restituisce "Nessun atto trovato" per qualsiasi parola inserita.

Lo script scritto in python esegue le seguenti operazioni
- Scarica la pagina con gli atti in pubblicazione dell'albo pretorio in formato json
- Filtra i dati cercando gli atti che contengono determinate parole chiave e salva il file in formato csv
- Converte il file in formato html/csv, cancella le colonne inutili e aggiunge una colonna con il link all'atto sul sito del Comune di Genova

Per eseguire lo script occorre installare Python e la libreria pandas.
Da linea di comando: 
- python download_and_search.py format_output_file parolachiave1 parolachiave2 ... parolachiaveN
- format_output_file = csv,html
- Esempi:
- python download_and_search.py csv cantiere marassi (ritorna gli atti che contengono le parole "cantiere" e "marassi" in formato "csv")
- python download_and_search.py html stazione principe brignole (ritorna gli atti che contengono le parole "stazione", "principe" e "brignole" in formato "html")
- python download_and_search.py (ritorna gli atti in pubblicazione in formato "html" - il formato di default)
- python download_and_search.py html (ritorna gli atti in pubblicazione in formato "html")
- python download_and_search.py csv (ritorna gli atti in pubblicazione in formato "csv")
  
Se le ricerche sono ricorrenti e prevedono la ricerca di atti che hanno sempre le stesse parole chiave, queste ultime possono essere memorizzate nel file download_and_search.php impostando la variabile SEARCH_TERMS. Ciò evita di dover digitare le parole chiave da ricercare sulla linea di comando.
