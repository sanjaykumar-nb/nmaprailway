import os
import time
import telebot
import subprocess
import requests

# Replace with your actual Telegram Bot Token
BOT_TOKEN = "7717097105:AAH5JxYXCPVlCxNyQOY4ZfkgX-gFIdfFWdU"

# Delete any existing webhook
delete_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
del_resp = requests.get(delete_webhook_url)
print("Webhook deletion response:", del_resp.json())

time.sleep(2)  # Wait for Telegram to process

# Check webhook status
get_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
info_resp = requests.get(get_webhook_url)
print("Webhook info after deletion:", info_resp.json())

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome! Use /scan <target> to perform an Nmap scan.")

@bot.message_handler(commands=['scan'])
def handle_scan(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Usage: /scan <target>\nExample: /scan example.com")
        return
    target = parts[1]
    bot.reply_to(message, f"🔍 Scanning {target}... Please wait.")

    try:
        # Use TCP Connect scan (-sT) instead of the default scan mode
        process = subprocess.run(["nmap", "-sT", "-p 1-100", target], 
                                 capture_output=True, text=True, check=False)
        output = process.stdout + "\n" + process.stderr
        bot.reply_to(message, f"✅ Scan Results for {target}:\n```\n{output}\n```", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Error running Nmap scan: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting bot using polling...")
    bot.infinity_polling()
