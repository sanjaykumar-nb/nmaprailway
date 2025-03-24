import os
import telebot
import subprocess
import requests
import time

# Hardcode your Telegram Bot Token here
BOT_TOKEN = "7924802116:AAHhn6UBw_fZSYX39ZSUSCZKcFKjSxLAIDw"  # e.g., "1234567890:ABCdefGHIJKLMnoPQRstuVWXYZ"

# Delete any existing webhook to avoid conflicts
delete_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
response = requests.get(delete_webhook_url)
print("Webhook delete response:", response.json())

# Initialize the TeleBot instance
bot = telebot.TeleBot(BOT_TOKEN)

# Function to run Nmap scan and capture output even if error occurs
def run_nmap_scan(target):
    try:
        # Run nmap with -F (fast scan) option; do not raise exception on non-zero exit status
        process = subprocess.run(
            ["nmap", "-F", target],
            capture_output=True,
            text=True,
            check=False  # Do not raise exception on error
        )
        # Combine stdout and stderr for full output
        output = process.stdout + "\n" + process.stderr
        return output.strip()
    except Exception as e:
        return f"Exception occurred: {str(e)}"

# Command handler for /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to the Nmap Scanner Bot!\nUse /scan <target> to perform an Nmap scan.")

# Command handler for /scan
@bot.message_handler(commands=['scan'])
def handle_scan(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Usage: /scan <target>\nExample: /scan example.com")
        return
    
    target = parts[1]
    bot.reply_to(message, f"🔍 Scanning {target}... Please wait.")
    
    scan_result = run_nmap_scan(target)
    bot.reply_to(message, f"✅ Scan Results for {target}:\n```\n{scan_result}\n```", parse_mode="Markdown")

if __name__ == "__main__":
    print("🚀 Starting Telegram bot using polling...")
    # Adding a short delay to ensure webhook deletion propagates
    time.sleep(2)
    bot.infinity_polling()
