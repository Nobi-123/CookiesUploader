from pyrogram import Client
from config import LOGGER_ID

async def bot_started_log(client: Client):
    """
    Sends a message to the logger channel after the bot has started.
    """
    try:
        await client.send_message(LOGGER_ID, "🤖 Bot has started successfully!")
    except Exception as e:
        print(f"Failed to send startup log: {e}")
