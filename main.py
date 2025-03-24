import os
import time
import telebot
import subprocess
import requests

# Hardcoded Bot Token (replace with your actual token)
BOT_TOKEN = "7717097105:AAH5JxYXCPVlCxNyQOY4ZfkgX-gFIdfFWdU"  # Format: "1234567890:ABCdefGHIJKLMnoPQRstuVWXYZ"

# Delete any existing webhook to avoid conflict with polling
delete_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
try:
    response = requests.get(delete_webhook_url)
    print("Webhook deletion response:", response.json())
except Exception as e:
    print("Error deleting webhook:", str(e))

# Wait a couple of seconds to let Telegram process the deletion
time.sleep(2)

# Initialize the TeleBot instance for polling
bot = telebot.TeleBot(BOT_TOKEN)

# Function to run Nmap scan using TCP connect scan (-sT) on ports 1-100
def run_nmap_scan(target):
    try:
        # Use TCP Connect Scan which doesn't require raw socket privileges
        process = subprocess.run(
            ["nmap", "-sT", "-p", "1-100", target],
            capture_output=True,
            text=True,
            check=False
        )
        # Combine stdout and stderr
        output = process.stdout + "\n" + process.stderr
        return output.strip()
    except Exception as e:
        return f"Error running Nmap: {str(e)}"

# Function to analyze the scan output in plain language
def analyze_scan(scan_output):
    if "80/tcp open" in scan_output and "filtered" in scan_output:
        return "Safe: Only the standard HTTP port (80) is open and other ports are filtered, which is typical for a secure web server."
    elif "open" in scan_output:
        return "Caution: Some ports are open. Please review the scan output for potential vulnerabilities."
    else:
        return "Further analysis required."

# Handler for /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to the Nmap Scanner Bot!\nUse /scan <target> to perform a scan.")

# Handler for /scan command
@bot.message_handler(commands=['scan'])
def handle_scan(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Usage: /scan <target>\nExample: /scan example.com")
        return
    
    target = parts[1]
    bot.reply_to(message, f"🔍 Scanning {target}... Please wait.")
    
    scan_output = run_nmap_scan(target)
    analysis = analyze_scan(scan_output)
    
    response_message = (
        f"✅ Scan Results for {target}:\n```\n{scan_output}\n```\n\n"
        f"Scan Analysis:\n{analysis}"
    )
    bot.reply_to(message, response_message, parse_mode="Markdown")

if __name__ == "__main__":
    print("🚀 Starting bot using polling...")
    bot.infinity_polling()
