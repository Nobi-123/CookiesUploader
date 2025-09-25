from pyrogram import Client
from config import LOGGER_ID

def bot_started_log(app: Client):
    """
    Sends a message to the logger channel that the bot has started.
    """
    try:
        app.send_message(LOGGER_ID, "🤖 Bot has started successfully!")
    except Exception as e:
        print(f"Failed to send startup log: {e}")
