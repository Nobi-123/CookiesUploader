import os
from pyrogram import Client, filters
from config import BOT_TOKEN, API_ID, API_HASH

app = Client("yt_cookie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("👋 Hello! Use /getcookies to start generating your cookies.")

@app.on_message(filters.command("getcookies"))
async def get_cookies(client, message):
    await message.reply("🔗 Open this link to log in: https://your-vnc-url.example.com
"
                        "After logging in, I’ll send your cookies.txt here.")

app.run()
