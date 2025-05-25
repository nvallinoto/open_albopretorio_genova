import os
import asyncio
import feedparser
from telegram import Bot
from telegram.error import TelegramError
import logging
from datetime import datetime
from dotenv import load_dotenv

# Configuration
PUB_DIR = "pub"
RSS_FILE = "{}/albogenova_rss.xml".format(PUB_DIR)
MESSAGE_DELAY = 3  # seconds
LAST_ENTRY_FILE = "{}/last_entry.txt".format(PUB_DIR)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_last_publication_date():
    try:
        with open(LAST_ENTRY_FILE, "r") as f:
            date_str = f.read().strip()
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except FileNotFoundError:
        return None
    except Exception as e:
        logger.error(f"Error reading last publication date: {e}")
        return None

def save_last_publication_date(pub_date):
    try:
        with open(LAST_ENTRY_FILE, "w") as f:
            f.write(pub_date.strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        logger.error(f"Error saving last publication date: {e}")

def format_message(entry):
    return f"<b>{entry.title}</b>\n\n{entry.description}\n\n<a href='{entry.link}'>{entry.link}</a>"

async def process_feed(bot, channel_id):
    try:
        logger.info(f"Starting daily feed processing at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check if RSS file exists
        if not os.path.exists(RSS_FILE):
            logger.error(f"RSS file not found: {RSS_FILE}")
            return False        

        # Fetch and parse RSS feed
        with open(RSS_FILE, 'r') as f:
            feed_content = f.read()
            feed = feedparser.parse(feed_content)
            # The Universal Feed Parser can parse feeds whether they are well-formed XML or not. 
            # Since some time the application warn users about non-well-formed feeds we commented the check
            # if feed.bozo:
            #    logger.warning("Feed parsing error detected")
            #    return False
        
        entries = feed.entries
        if not entries:
            logger.info("No entries found in RSS feed")
            return True
        
        last_pub_date = get_last_publication_date()
        new_entries = []

        # Collect new entries
        for entry in entries:
            if 'published_parsed' not in entry:
                logger.warning("Entry missing 'published_parsed', skipping")
                continue
            pub_struct = entry.published_parsed
            entry_pub_date = datetime.utcfromtimestamp(calendar.timegm(pub_struct))
            if last_pub_date is None:
                new_entries.append(entry)
                continue
            if entry_pub_date <= last_pub_date:
                break
                
            new_entries.append(entry)

        # Process new entries in chronological order
        if new_entries:
            logger.info(f"Found {len(new_entries)} new entries")
            new_entries.reverse()  # Oldest first

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
                    await asyncio.sleep(10)  # Wait longer on Telegram errors

           # Update last publication date to the most recent entry
            latest_entry = entries[0]
            latest_pub_struct = latest_entry.published_parsed
            latest_pub_date = datetime.utcfromtimestamp(calendar.timegm(latest_pub_struct))
            save_last_publication_date(latest_pub_date)
        else:
            logger.info("No new entries found")

        return True

    except Exception as e:
        logger.error(f"Error processing feed: {e}")
        return False

async def main():
    # Load environment variables
    load_dotenv()
    # Get environment variables
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHANNEL_ID = os.getenv("CHANNEL_ID")

    if not BOT_TOKEN or not CHANNEL_ID:
        logger.error("Please set BOT_TOKEN and CHANNEL_ID environment variables")
        return

    bot = Bot(token=BOT_TOKEN)
    
    # Single execution pattern
    success = await process_feed(bot, CHANNEL_ID)
    if success:
        logger.info("Daily processing completed successfully")
    else:
        logger.warning("Daily processing completed with errors")

if __name__ == "__main__":
    asyncio.run(main())
