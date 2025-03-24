import telebot
import requests
import os
import subprocess

# 🔹 Set Telegram Bot Token
BOT_TOKEN = "7924802116:AAHhn6UBw_fZSYX39ZSUSCZKcFKjSxLAIDw"
bot = telebot.TeleBot(BOT_TOKEN)

# 🔹 Ensure webhook is deleted to avoid conflicts
delete_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
requests.get(delete_webhook_url)

# 🔹 Nmap Scan Function
def run_nmap_scan(target):
    try:
        result = subprocess.check_output(["nmap", target], text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Error running Nmap: {e}"

# 🔹 Handle /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome! Use /scan <website> to run an Nmap scan.")

# 🔹 Handle /scan
@bot.message_handler(commands=['scan'])
def handle_scan(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "⚠ Please provide a website/IP. Example: /scan example.com")
            return
        
        target = parts[1]
        bot.reply_to(message, f"🔎 Scanning {target}... Please wait.")

        # Run Nmap
        scan_result = run_nmap_scan(target)

        # Send result to user
        bot.reply_to(message, f"🛡 Nmap Scan Results for {target}:\n```\n{scan_result}\n```", parse_mode="Markdown")
    
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# 🔹 Start Polling Mode (Ensures Only One Bot Instance Runs)
if __name__ == "__main__":
    print("🚀 Bot is running...")
    bot.infinity_polling()
