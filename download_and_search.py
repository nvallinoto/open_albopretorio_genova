import requests
import json
import csv
import re
import pandas as pd 
import datetime
import os
from datetime import datetime
import sys
# config
ALBO_URL = "https://alboonline.comune.genova.it/albopretorio/dispatcher/alboPretorioServlet/invoke"
TEMP_DIR = "temp"
PUB_DIR = "pub"
RECURRENT_SEARCH_TERMS = []
# RECURRENT_SEARCH_TERMS = [
#    'cantiere',
#    'lavori',
#    'interventi di manutenzione'
#    ]
# argv[1] = filetype (csv or html)
# argv[2:] = parole chiave
if not os.path.exists(PUB_DIR):
    raise Exception(
        f"La cartella {PUB_DIR} non esiste."
    )
if not os.path.exists(TEMP_DIR):
    raise Exception(
        f"La cartella {TEMP_DIR} non esiste."
    )
if len(sys.argv) < 2:
    download_typefile = "html"
    SEARCH_TERMS = []
else:
    download_typefile = sys.argv[1]
    SEARCH_TERMS = sys.argv[2:]
if (download_typefile != 'csv' and download_typefile != 'html'):
    print("Indicare il formato del file di output: csv oppure html")
    sys.exit()
SEARCH_TERMS = SEARCH_TERMS + RECURRENT_SEARCH_TERMS 
today = datetime.today().strftime('%Y%m%d')
json_file = "{}/albo_{}.json".format(TEMP_DIR, today)
csv_file = "{}/albo_{}.csv".format(TEMP_DIR, today)
html_file = "{}/albo_{}.html".format(PUB_DIR, today)
csv_pub_file = "{}/albo_{}.csv".format(PUB_DIR, today)
# Query API and save response as temporary JSON
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
payload = 'dataInputXml=<?xml version="1.0" encoding="UTF-8" ?><filtriAlboPretorio><filtroAlbo><name>TIPO_DOC</name><value /></filtroAlbo><filtroAlbo><name>NASCONDI_ANNULLATE</name><value>VALIDA</value></filtroAlbo><filtroAlbo><name>FULL_TEXT</name><value /></filtroAlbo></filtriAlboPretorio>&nameService=search'
req = requests.post(ALBO_URL, data = payload, headers=headers)
req.raise_for_status() # ensure we notice bad responses
response = req.text
if req.status_code != 200:
    raise Exception(
        f"Error getting data from {link}. Status code: {response.status_code}"
    )
file = open(json_file, "w")
file.write(response)
file.close()
# Converte il file JSON in formato CSV
if not os.path.isfile(json_file):
    raise Exception("JSON file not found")
with open(json_file) as json_file_content:
    data = json.load(json_file_content) 
albo_data = data['data']
# rimuove colonna esecutivoDal presente solo in alcune righe
for index, doc in enumerate(albo_data):
    if 'esecutivoDal' in doc:
        del doc['esecutivoDal']
# Salva in formato csv
data_file = open(csv_file, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(data_file)
# estrae gli atti con le parole chiave
count = 0
for atto in albo_data:
    if count == 0:
        header = atto.keys() 
        csv_writer.writerow(header)
    count += 1
    row = atto.values()
    # sostituisci le newlines 
    row = [v.replace("\n", " ").strip() for v in atto.values()]    
    # prepare search pattern
    search_pattern = re.compile(r'\b(?:%s)\b' % '|'.join(SEARCH_TERMS), re.I)
    # check search matches in object column
    if re.search(search_pattern, row[7]):
        csv_writer.writerow(row)
data_file.close()
# Rimuovi le colonne inutili e crea la colonna con il link all'atto
columns_to_be_removed = ['idUdRettifica','tsPubblicazione','motivoAnnullamento','formaPubblicazione','idDocType','dataAtto','statoPubblicazione','tipo','flgImmediatamenteEsegiubile']
df = pd.read_csv(csv_file).drop(columns_to_be_removed, axis = 'columns')
pd.set_option('display.max_colwidth', None)
# crea una nuova colonna con il link all'atto
df['urlAtto'] = "https://alboonline.comune.genova.it/albopretorio/#/albo/atto/" + df['idUd'].map(str) + "/" + df['idPubblicazione']
def make_clickable(val):
    return '<a target="_blank" href="{}">ATTO</a>'.format(val)
df.style.format({'urlAtto': make_clickable})
columns_to_be_removed_after = ['idUd','idPubblicazione','richiedente']
df = df.drop(columns_to_be_removed_after, axis = 'columns') 
if download_typefile == "html":
    # Convert the DataFrame to an HTML table 
    html_table = df.to_html(border=10, index=False, justify='left', col_space=100, render_links=True, notebook=True)
    # Save the HTML table
    with open(html_file, 'w') as f: 
        f.write(html_table)
    f.close
elif download_typefile == "csv":
    # Convert the DataFrame to a CSV file 
    csv_table = df.to_csv()
    # Save the CSV file
    with open(csv_pub_file, 'w', newline='',encoding='utf-8') as f: 
        f.write(csv_table)
    f.close
# clear up
os.remove(json_file)
os.remove(csv_file)
