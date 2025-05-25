import os
import asyncio
import feedparser
from telegram import Bot
from telegram.error import TelegramError
import logging
from datetime import datetime
from dotenv import load_dotenv
import calendar

# Configuration
PUB_DIR = "pub"
RSS_FILE = os.path.join(PUB_DIR, "albogenova_rss.xml")
MESSAGE_DELAY = 3  # seconds
LAST_ENTRY_FILE = os.path.join(PUB_DIR, "last_entry.txt")

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_last_publication_date():
    try:
        with open(LAST_ENTRY_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return None
            return int(content)
    except FileNotFoundError:
        logger.error(f"File not found: {LAST_ENTRY_FILE}")
        return None
    except Exception as e:
        logger.error(f"Error reading last publication date: {e}")
        return None

def save_last_publication_date(timestamp):
    try:
        with open(LAST_ENTRY_FILE, "w") as f:
            f.write(str(timestamp))
    except Exception as e:
        logger.error(f"Error saving last publication date: {e}")

def format_message(entry):
    return f"<b>{entry.title}</b>\n\n{entry.description}\n\n<a href='{entry.link}'>{entry.link}</a>"

async def process_feed(bot, channel_id):
    try:
        logger.info(f"Starting daily feed processing at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if not os.path.exists(RSS_FILE):
            logger.error(f"RSS file not found: {RSS_FILE}")
            return False

        with open(RSS_FILE, 'r') as f:
            feed_content = f.read()
            feed = feedparser.parse(feed_content)
        
        entries = feed.entries
        if not entries:
            logger.info("No entries found in RSS feed")
            return True

        last_pub_timestamp = get_last_publication_date()
        new_entries_with_ts = []

        for entry in entries:
            pub_date_str = entry.get('published')
            if not pub_date_str:
                logger.warning("Entry missing 'published', skipping")
                continue
            try:
                pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
                entry_timestamp = int(pub_date.timestamp())
            except Exception as e:
                logger.error(f"Error parsing date '{pub_date_str}': {e}")
                continue

            if last_pub_timestamp is None:
                new_entries_with_ts.append((entry, entry_timestamp))
                continue

            if entry_timestamp > last_pub_timestamp:
                new_entries_with_ts.append((entry, entry_timestamp))
            else:
                break

        new_entries = [entry for entry, _ in new_entries_with_ts]

        if new_entries:
            logger.info(f"Found {len(new_entries)} new entries")
            new_entries.reverse()

            for entry in new_entries:
                try:
                    message = format_message(entry)
                    await bot.send_message(
                        chat_id=channel_id,
                        text=message,
                        parse_mode='HTML'
                    )
                    logger.info(f"Posted: {entry.title}")
                    await asyncio.sleep(MESSAGE_DELAY)
                except TelegramError as e:
                    logger.error(f"Failed to send message: {e}")
                    await asyncio.sleep(10)

            if new_entries_with_ts:
                max_timestamp = max(ts for _, ts in new_entries_with_ts)
                save_last_publication_date(max_timestamp)
            else:
                logger.error("No timestamps available to save")
        else:
            logger.info("No new entries found")

        return True

    except Exception as e:
        logger.error(f"Error processing feed: {e}")
        return False

async def main():
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHANNEL_ID = os.getenv("CHANNEL_ID")

    if not BOT_TOKEN or not CHANNEL_ID:
        logger.error("Please set BOT_TOKEN and CHANNEL_ID environment variables")
        return

    bot = Bot(token=BOT_TOKEN)
    success = await process_feed(bot, CHANNEL_ID)
    if success:
        logger.info("Daily processing completed successfully")
    else:
        logger.warning("Daily processing completed with errors")

if __name__ == "__main__":
    asyncio.run(main())
