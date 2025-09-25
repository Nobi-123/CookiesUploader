import os
from pyrogram import Client, filters
from config import BOT_TOKEN, API_ID, API_HASH
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Bot setup
app = Client("yt_cookie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def save_cookies_to_netscape_file(cookies, output_file):
    with open(output_file, 'w') as f:
        f.write("# Netscape HTTP Cookie File\n")
        f.write("# This is a generated file! Do not edit.\n\n")
        f.write("# domain  include_subdomains  path  secure  expiration_date  name  value\n")

        for cookie in cookies:
            expiry = cookie.get('expiry') or cookie.get('expires') or 0
            f.write(f"{cookie['domain']}\t")
            f.write("TRUE\t")
            f.write(f"{cookie['path']}\t")
            f.write("TRUE\t" if cookie.get('secure') else "FALSE\t")
            f.write(f"{int(expiry)}\t")
            f.write(f"{cookie['name']}\t{cookie['value']}\n")

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("👋 Hello! Use /getcookies to generate your cookies.txt")

@app.on_message(filters.command("getcookies"))
async def get_cookies(client, message):
    await message.reply("⏳ Launching browser, please wait...")

    # Chrome options
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X)")

    driver = webdriver.Chrome(options=options)

    # Open YouTube (user must already be logged in on this instance)
    driver.get("https://www.youtube.com")

    # Save cookies
    cookies = driver.get_cookies()
    output_file = "cookies.txt"
    save_cookies_to_netscape_file(cookies, output_file)
    driver.quit()

    # Send file
    await message.reply_document(output_file, caption="✅ Here are your YouTube cookies.txt")

app.run()
