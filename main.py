import os
import time
import telebot
import subprocess
import requests

# Set your Telegram Bot Token here (replace with your actual token)
BOT_TOKEN = "7924802116:AAHhn6UBw_fZSYX39ZSUSCZKcFKjSxLAIDw"  # e.g., "1234567890:ABCdefGHIJKLMnoPQRstuVWXYZ"

# Delete any existing webhook to avoid conflicts
delete_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
try:
    response = requests.get(delete_webhook_url)
    print("Webhook deletion response:", response.json())
except Exception as e:
    print("Error deleting webhook:", str(e))

# Wait a few seconds for Telegram to process the deletion
time.sleep(2)

# Initialize the TeleBot instance
bot = telebot.TeleBot(BOT_TOKEN)

# Handler for /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome! Use /scan <target> to perform an Nmap scan.")

# Handler for /scan command
@bot.message_handler(commands=['scan'])
def handle_scan(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Usage: /scan <target>\nExample: /scan example.com")
        return

    target = parts[1]
    bot.reply_to(message, f"🔍 Scanning {target}... Please wait.")

    try:
        # Run Nmap with the fast scan option; capturing stdout and stderr
        process = subprocess.run(
            ["nmap", "-F", target],
            capture_output=True,
            text=True,
            check=False
        )
        output = process.stdout + "\n" + process.stderr
        bot.reply_to(message, f"✅ Scan Results for {target}:\n```\n{output}\n```", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Error running Nmap scan: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting bot using polling...")
    bot.infinity_polling()
