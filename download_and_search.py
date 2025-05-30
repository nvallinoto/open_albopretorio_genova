import requests
import json
import csv
import re
import pandas as pd 
import os
from datetime import datetime, timezone
import pytz
import sys
import time
import html
from dateutil import parser
from dotenv import load_dotenv
import ast

# argv[1] = filetype (csv or html)
# argv[2:] = parole chiave

def convert_to_rfc822(data_input):
    #parsed_date = datetime.strptime(data_input, "%b %d, %Y %I:%M:%S %p")
    # Aggiunta del fuso orario UTC
    # utc_date = parsed_date.replace(tzinfo=pytz.utc)
    utc_date = datetime.strptime(data_input, "%b %d, %Y %I:%M:%S %p").replace(tzinfo=pytz.utc)
    # Conversione nel formato RFC-822
    formatted_tsPubblicazione = utc_date.strftime("%a, %d %b %Y %H:%M:%S +0000")
    return formatted_tsPubblicazione

def convert_to_rfc822_from_ddmmyyyy(data_input):
    # parsed_date = parser.parse(data_input)
    # formatted_dataInizioPubbl = parsed_date.strftime("%a, %d %b %Y %H:%M:%S +0000")
    formatted_dataInizioPubbl = parser.parse(data_input).strftime("%a, %d %b %Y %H:%M:%S +0000")
    return formatted_dataInizioPubbl

def generate_rss(data):
    # Ottieni la data corrente
    # current_date = datetime.now(timezone.utc)
    # Conversione nel formato RFC-822
    formatted_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    rss = """\
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
 xmlns:atom="http://www.w3.org/2005/Atom"
 xmlns:creativeCommons="http://backend.userland.com/creativeCommonsRssModule"
 xmlns:xhtml="http://www.w3.org/1999/xhtml">
<channel>
<title>AlboPOP - Comune - Genova</title>
<atom:link href="https://ospiti.peacelink.it/albogenova/albogenova_rss.xml" rel="self"  type="application/rss+xml" />
<link>https://ospiti.peacelink.it/albogenova/albogenova_rss.xml</link>
<description>*non ufficiale* RSS feed dell'Albo Pretorio del Comune di Genova</description>
<language>it</language>
<pubDate>{}</pubDate>
<webMaster>nicola.vallinoto@gmail.com (Nicola Vallinoto)</webMaster>
<docs>https://github.com/nvallinoto/albopop_genova_feedrss</docs>
<copyright>Copyright 2025 Comune di Genova</copyright>
<xhtml:meta name="robots" content="noindex" />    
<category domain="http://albopop.it/specs#channel-category-country">Italia</category>
    <category domain="http://albopop.it/specs#channel-category-region">Liguria</category>
    <category domain="http://albopop.it/specs#channel-category-province">Genova</category>
    <category domain="http://albopop.it/specs#channel-category-municipality">Genova</category>
    <category domain="http://albopop.it/specs#channel-category-latitude">44.414165</category>
    <category domain="http://albopop.it/specs#channel-category-longitude">8.942184</category>
    <category domain="http://albopop.it/specs#channel-category-type">Comune</category>
    <category domain="http://albopop.it/specs#channel-category-name">Comune di Genova</category>
    <category domain="http://albopop.it/specs#channel-category-uid">istat:010025</category>
""".format(
            f"{formatted_date}"
           )
    for i in data:
        # crea una nuova colonna con il link all'atto
        urlAtto = "https://alboonline.comune.genova.it/albopretorio/#/albo/atto/" + i['idUd'] + "/" + i['idPubblicazione']
        titolo = "Pubblicazione n. " + i['pubblicazioneNumero'] + " del " + i['dataInizioPubbl'] + " - " + i['attoNumero']      
        #Parsing di dataInizioPubbl
        formatted_dataInizioPubbl = convert_to_rfc822_from_ddmmyyyy(i['dataInizioPubbl'])     
        #Parsing di dataFinePubbl
        formatted_dataFinePubbl = convert_to_rfc822_from_ddmmyyyy(i['dataFinePubbl'])
        # Parsing di tsPubblicazione
        formatted_tsPubblicazione = convert_to_rfc822(i['tsPubblicazione'])
        # Parsing di dataAtto
        formatted_dataAtto = convert_to_rfc822(i['dataAtto'])
        # Parsing di dataAdozione
        formatted_dataAdozione = convert_to_rfc822(i['dataAdozione']) if 'dataAdozione' in i else ""
        clean_oggetto = html.escape(i['oggetto'])
        rss += """\
        <item>
            <title>{}</title>
            <link>{}</link>
            <description>{}</description>
            <pubDate>{}</pubDate>
            <guid isPermaLink="true">{}</guid>
            <category domain="http://albopop.it/specs#item-category-uid">{}</category>
            <category domain="http://albopop.it/specs#item-category-type">{}</category>
            <category domain="http://albopop.it/specs#item-category-pubStart">{}</category>
            <category domain="http://albopop.it/specs#item-category-pubEnd">{}</category>
            <category domain="http://albopop.it/specs#item-category-relStart">{}</category>
            <category domain="http://albopop.it/specs#item-category-exeStart">{}</category>
            <category domain="http://albopop.it/specs#item-category-chapter">{}</category>
            <category domain="http://albopop.it/specs#item-category-unit">{}</category>
        </item>
""".format(
            f"{titolo}",
            f"{urlAtto}",
            f"{clean_oggetto}",
            f"{formatted_tsPubblicazione}",
            f"{urlAtto}",  
            f"{i['attoNumero']}",
            f"{i['tipo']}",
            f"{formatted_dataInizioPubbl}",
            f"{formatted_dataFinePubbl}",
            f"{formatted_dataAtto}",
            f"{formatted_dataAdozione}",
            f"{i['idDocType']}",
            f"{i['richiedente']}"
        )
    rss += "\n</channel>\n</rss>"
    return rss

def make_clickable(val):
    return '<a target="_blank" href="{}">ATTO</a>'.format(val)

if __name__ == '__main__':
    # Load environment variables if not already present
    if os.getenv("ALBO_PRETORIO_API") is None:
        load_dotenv()
    ALBO_URL = os.getenv("ALBO_PRETORIO_API")
    TEMP_DIR = "temp"
    PUB_DIR = "pub"
    RECURRENT_SEARCH_TERMS = os.getenv("RECURRENT_SEARCH_TERMS")
    # Convert string to list
    RECURRENT_SEARCH_TERMS = ast.literal_eval(RECURRENT_SEARCH_TERMS)    
    
    if not os.path.exists(PUB_DIR):
        os.mkdir(PUB_DIR)
    if not os.path.exists(TEMP_DIR):
        os.mkdir(TEMP_DIR)
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
    rss_pub_file = "{}/albogenova_rss.xml".format(PUB_DIR)
    # Query API and save response as temporary JSON
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = 'dataInputXml=<?xml version="1.0" encoding="UTF-8" ?><filtriAlboPretorio><filtroAlbo><name>TIPO_DOC</name><value /></filtroAlbo><filtroAlbo><name>NASCONDI_ANNULLATE</name><value>VALIDA</value></filtroAlbo><filtroAlbo><name>FULL_TEXT</name><value /></filtroAlbo></filtriAlboPretorio>&nameService=search'
    req = requests.post(ALBO_URL, data = payload, headers=headers)
    req.raise_for_status() # ensure we notice bad responses
    response = req.text
    if req.status_code != 200:
        raise Exception(
            f"Error getting data from {ALBO_URL}. Status code: {response.status_code}"
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
    
    with open(rss_pub_file, 'w') as f_out:
        print(generate_rss(albo_data), file=f_out)
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
