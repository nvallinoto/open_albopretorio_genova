import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import glob
import json

# Configuration
PUB_DIR = "pub"
MESSAGE_DELAY = 3  # seconds
STATE_FILE = f"{PUB_DIR}/processing_state.json"  # Tracks processed files and records

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def load_processing_state():
    try:
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
            return {
                'processed_files': set(state.get('processed_files', [])),
                'published_records': set(state.get('published_records', []))
            }
    except (FileNotFoundError, json.JSONDecodeError):
        return {'processed_files': set(), 'published_records': set()}

def save_processing_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            'processed_files': list(state['processed_files']),
            'published_records': list(state['published_records'])
        }, f)

def get_record_id(entry):
    """Create a unique ID for each record using publication number and adoption date"""
    return f"{entry['pubblicazioneNumero']}"

def parse_albo_file(file_path):
    # Try multiple common encodings for Italian/European files
    encodings = ['utf-8', 'latin-1', 'windows-1252', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                entries = []
                rows = soup.find_all('tr')[1:]  # Skip header row
                
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 7:
                        entry = {
                            'pubblicazioneNumero': cols[0].text.strip(),
                            'attoNumero': cols[1].text.strip(),
                            'dataInizioPubbl': cols[2].text.strip(),
                            'dataFinePubbl': cols[3].text.strip(),
                            'oggetto': cols[4].text.strip(),
                            'dataAdozione': cols[5].text.strip(),
                            'url': cols[6].text.strip()
                        }
                        entries.append(entry)
                return entries
                
        except UnicodeDecodeError:
            continue
        except Exception as e:
            logger.error(f"Error parsing file {file_path} with encoding {encoding}: {e}")
            continue
    
    logger.error(f"Failed to parse file {file_path} with all attempted encodings")
    return []

def format_message(entry):
    title = f"Pubblicazione n. {entry['pubblicazioneNumero']} del {entry['dataInizioPubbl']} - {entry['attoNumero']}"
    description = entry['oggetto']
    url = entry['url']
    
    return f"<b>{title}</b>\n\n{description}\n\n<a href='{url}'>Leggi di più</a>"

async def process_new_files(bot, channel_id):
    try:
        logger.info(f"Starting processing at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Load processing state
        state = load_processing_state()
        logger.info(f"Loaded state: {len(state['processed_files'])} processed files, {len(state['published_records'])} published records")

        # Find all albo files
        all_files = set(glob.glob(f"{PUB_DIR}/albo_*.html"))
        new_files = all_files - state['processed_files']
        
        if not new_files:
            logger.info("No new files to process")
            return True

        new_records_count = 0

        # Process only new files
        for file_path in sorted(new_files):
            file_name = os.path.basename(file_path)
            logger.info(f"Processing new file: {file_name}")

            # Parse the HTML file
            entries = parse_albo_file(file_path)
            if not entries:
                logger.info("No entries found in the file")
                state['processed_files'].add(file_path)
                continue

            # Process entries
            file_records = 0
            for entry in entries:
                record_id = get_record_id(entry)
                
                if record_id not in state['published_records']:
                    try:
                        message = format_message(entry)
                        await bot.send_message(
                            chat_id=channel_id,
                            text=message,
                            parse_mode='HTML'
                        )
                        state['published_records'].add(record_id)
                        new_records_count += 1
                        file_records += 1
                        logger.info(f"Posted new record: {record_id}")
                        await asyncio.sleep(MESSAGE_DELAY)
                    except TelegramError as e:
                        logger.error(f"Failed to send message: {e}")
                        await asyncio.sleep(10)  # Wait longer on Telegram errors

            # Mark file as processed even if no new records were found
            state['processed_files'].add(file_path)
            logger.info(f"Processed {file_records} new records from {file_name}")

        # Save updated state
        save_processing_state(state)
        logger.info(f"Processing complete. Added {new_records_count} new records from {len(new_files)} files")
        return True

    except Exception as e:
        logger.error(f"Error processing files: {e}")
        return False

async def cleanup_old_files():
    """Optional: Clean up files older than 14 days from the state"""
    state = load_processing_state()
    cutoff_date = datetime.now() - timedelta(days=14)
    
    files_to_remove = set()
    for file_path in state['processed_files']:
        try:
            date_str = os.path.basename(file_path)[5:-5]  # Extract YYYYMMDD
            file_date = datetime.strptime(date_str, "%Y%m%d")
            if file_date < cutoff_date:
                files_to_remove.add(file_path)
        except ValueError:
            continue
    
    if files_to_remove:
        state['processed_files'] -= files_to_remove
        save_processing_state(state)
        logger.info(f"Cleaned up {len(files_to_remove)} old files from state")

async def main():
    # Load environment variables
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHANNEL_ID = os.getenv("CHANNEL_CONIPIEDIPERTERRA_ID")

    if not BOT_TOKEN or not CHANNEL_ID:
        logger.error("Please set BOT_TOKEN and CHANNEL_ID environment variables")
        return

    bot = Bot(token=BOT_TOKEN)
    
    # Optional: Clean up old files from state (run occasionally)
    # await cleanup_old_files()
    
    # Process new files
    success = await process_new_files(bot, CHANNEL_ID)
    if success:
        logger.info("Processing completed successfully")
    else:
        logger.warning("Processing completed with errors")

if __name__ == "__main__":
    asyncio.run(main())