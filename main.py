import os
import time
import telebot
import subprocess
import requests

# Set your Telegram Bot Token here
BOT_TOKEN = "7924802116:AAHhn6UBw_fZSYX39ZSUSCZKcFKjSxLAIDw"  # e.g., "1234567890:ABCdefGHIJKLMnoPQRstuVWXYZ"

# Delete any existing webhook to ensure polling works
def delete_webhook():
    delete_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
    try:
        response = requests.get(delete_url)
        result = response.json()
        print("Webhook delete response:", result)
    except Exception as e:
        print("Error deleting webhook:", str(e))

# Call the deletion function and wait a few seconds to ensure the change propagates
delete_webhook()
time.sleep(2)

# Initialize the bot with polling mode
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message, "👋 Bot started using polling. Use /scan <target> to perform an Nmap scan.")

@bot.message_handler(commands=['scan'])
def scan_handler(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Usage: /scan <target>\nExample: /scan example.com")
        return
    target = parts[1]
    bot.reply_to(message, f"🔍 Scanning {target}... Please wait.")
    try:
        # Run Nmap using the "-F" (fast scan) option
        result = subprocess.check_output(["nmap", "-F", target], text=True)
        bot.reply_to(message, f"✅ Scan Results for {target}:\n```\n{result}\n```", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Error running Nmap scan: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting bot polling...")
    bot.infinity_polling()
