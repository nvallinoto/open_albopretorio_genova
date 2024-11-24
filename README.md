# albopretorio-genova

Scarica e filtra gli atti dell'albo pretorio del Comune di Genova in base a determinate parole chiave.
Il sito dell'albo pretorio del Comune di Genova (https://alboonline.comune.genova.it/albopretorio/) non consente la ricerca degli atti nè lo scarico in formato tabellare (es: csv). 
La ricerca avanzata non funziona (al 17/11/2024) e restituisce "Nessun atto trovato" per qualsiasi parola inserita.

Lo script scritto in python esegue le seguenti operazioni
- Scarica la pagina con gli atti in pubblicazione dell'albo pretorio in formato json
- Filtra i dati cercando gli atti che contengono determinate parole chiave e salva il file in formato csv
- Converte il file in formato html, cancella le colonne inutili e aggiunge una colonna con il link all'atto sul sito del Comune di Genova

Per eseguire lo script occorre installare Python e la libreria pandas.
