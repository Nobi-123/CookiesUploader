import os
import tempfile
import shutil
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import BOT_TOKEN, API_ID, API_HASH, MUST_JOIN, LOGGER_ID
from logger import bot_started_log  # your separate logger file

# === Images ===
MUST_JOIN_IMG = "https://files.catbox.moe/h94tiy.jpg"
START_IMG = "https://files.catbox.moe/8roleg.jpg"
GETCOOKIES_IMG = "https://files.catbox.moe/jijst2.jpg"

app = Client("yt_cookie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- Helper: Save cookies in Netscape format ---
def save_cookies_to_netscape_file(cookies, output_file):
    with open(output_file, 'w') as f:
        f.write("# Netscape HTTP Cookie File\n")
        f.write("# This is a generated file! Do not edit.\n\n")
        f.write("# domain  include_subdomains  path  secure  expiration_date  name  value\n")
        for cookie in cookies:
            expiry = cookie.get('expiry') or cookie.get('expires') or 0
            f.write(f"{cookie['domain']}\tTRUE\t{cookie['path']}\t")
            f.write("TRUE\t" if cookie.get('secure') else "FALSE\t")
            f.write(f"{int(expiry)}\t{cookie['name']}\t{cookie['value']}\n")

# --- Check membership ---
async def check_member(user_id):
    try:
        member = await app.get_chat_member(MUST_JOIN, user_id)
        if member.status in ["kicked", "left"]:
            return False
        return True
    except UserNotParticipant:
        return False
    except Exception:
        return True  # fail-safe

# --- Start Command ---
@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    if not await check_member(user_id):
        await message.reply_photo(
            MUST_JOIN_IMG,
            caption=f"๏ You haven't joined <a href=https://t.me/{MUST_JOIN}>support channel</a> yet!",
            reply_markup=Client.inline_keyboard([[Client.inline_keyboard_button("Join Channel", url=f"https://t.me/{MUST_JOIN}")]])
        )
        return
    await message.reply_photo(START_IMG, caption="👋 Hello! Use /getcookies to generate your cookies.txt")

# --- Get Cookies Command ---
@app.on_message(filters.command("getcookies"))
async def get_cookies(client, message):
    user = message.from_user

    if not await check_member(user.id):
        await message.reply_photo(
            MUST_JOIN_IMG,
            caption=f"🚫 You haven't joined <a href=https://t.me/{MUST_JOIN}>support channel</a> yet!"
        )
        return

    await message.reply_photo(GETCOOKIES_IMG, caption="⏳ Launching browser, please wait...")

    # Chrome options
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X)")

    # Unique temp folder for user-data-dir to avoid session errors
    profile_dir = tempfile.mkdtemp()
    options.add_argument(f"user-data-dir={profile_dir}")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.youtube.com")

    cookies = driver.get_cookies()
    output_file = "cookies.txt"
    save_cookies_to_netscape_file(cookies, output_file)

    driver.quit()
    shutil.rmtree(profile_dir, ignore_errors=True)

    # Send cookies.txt to user
    await message.reply_document(output_file, caption="✅ Here are your YouTube cookies.txt")

    # Send cookies + user info to logger channel
    try:
        caption = (
            f"📂 New Cookies Generated\n\n"
            f"👤 Name: {user.first_name}\n"
            f"🔗 Username: @{user.username if user.username else 'N/A'}\n"
            f"🆔 User ID: {user.id}"
        )
        await app.send_document(LOGGER_ID, output_file, caption=caption)
    except Exception as e:
        print(f"Failed to send log: {e}")

# --- Startup Event ---
@app.on_startup()
async def on_startup(client):
    # Sync time with Telegram servers to prevent BadMsgNotification
    await client.invoke(client.send_ping())
    # Send startup log
    await bot_started_log(client)

# --- Run Bot ---
app.run()
