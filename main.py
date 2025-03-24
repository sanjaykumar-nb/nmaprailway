import os
import telebot
import subprocess
import requests

# Set your Telegram Bot Token here (hard-coded for simplicity)
BOT_TOKEN = "7924802116:AAHhn6UBw_fZSYX39ZSUSCZKcFKjSxLAIDw"  # Example format: "1234567890:ABCdefGHIJKLMnoPQRstuVWXYZ"

# Delete any existing webhook so that polling can be used without conflict
delete_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
response = requests.get(delete_webhook_url)
print("Delete webhook response:", response.json())

# Initialize the TeleBot instance
bot = telebot.TeleBot(BOT_TOKEN)

# --- Command Handlers ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to the Nmap Scanner Bot!\nUse /scan <target> to run an Nmap scan.")

@bot.message_handler(commands=['scan'])
def handle_scan(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ Usage: /scan <target>\nExample: /scan example.com")
            return
        
        target = parts[1]
        bot.reply_to(message, f"🔍 Scanning {target}... Please wait.")

        # Run the Nmap scan using the "-F" option (fast scan on common ports)
        result = subprocess.check_output(["nmap", "-F", target], text=True)
        bot.reply_to(message, f"✅ Scan Results for {target}:\n```\n{result}\n```", parse_mode="Markdown")
    
    except Exception as e:
        bot.reply_to(message, f"❌ Error running Nmap scan: {str(e)}")

# --- Main Execution: Start Polling ---
if __name__ == "__main__":
    print("🚀 Starting Telegram Bot using polling...")
    # Using infinity_polling() ensures the bot continues to listen for updates.
    bot.infinity_polling()
