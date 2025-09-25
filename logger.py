from pyrogram import Client
from config import LOGGER_ID

async def bot_started_log(app: Client):
    """
    Sends a message to the logger channel that the bot has started.
    Safe for async usage and will not crash if Telegram time is out of sync.
    """
    try:
        await app.send_message(LOGGER_ID, "🤖 Bot has started successfully!")
    except Exception as e:
        # Just print the error, the bot will continue running
        print(f"Failed to send startup log: {e}")
