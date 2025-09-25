from pyrogram import Client
from config import LOGGER_ID

async def bot_started_log(app: Client):
    """
    Sends an asynchronous message to the logger channel that the bot has started.
    """
    try:
        await app.send_message(LOGGER_ID, "🤖 Bot has started successfully!")
    except Exception as e:
        print(f"Failed to send startup log: {e}")
