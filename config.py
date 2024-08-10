from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Telegram Bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Chat ID of the Telegram group
CHAT_ID = int(os.getenv("CHAT_ID"))

# Topic IDs for News and Announcements
NEWS_TOPIC_ID = int(os.getenv("NEWS_TOPIC_ID"))
ANNOUNCES_TOPIC_ID = int(os.getenv("ANNOUNCES_TOPIC_ID"))

# Maximum number of topics managed by the bot
MAX_MANAGED_TOPICS = int(os.getenv("MAX_MANAGED_TOPICS"))

# SQLite database file
DATABASE_FILE = os.getenv("DATABASE_FILE")
