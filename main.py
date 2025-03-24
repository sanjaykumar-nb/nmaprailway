import os
import time
import telebot
import subprocess
import requests

# Replace with your actual Telegram Bot Token
BOT_TOKEN = "7717097105:AAH5JxYXCPVlCxNyQOY4ZfkgX-gFIdfFWdU"  # e.g. "1234567890:ABCdefGHIJKLMnoPQRstuVWXYZ"

# Delete any existing webhook to ensure we use polling
delete_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
try:
    response = requests.get(delete_webhook_url)
    print("Webhook deletion response:", response.json())
except Exception as e:
    print("Error deleting webhook:", str(e))

# Wait 2 seconds to ensure Telegram processes the webhook deletion
time.sleep(2)

# Initialize the Telegram bot instance
bot = telebot.TeleBot(BOT_TOKEN)

# Function to run Nmap scan and capture both stdout and stderr
def run_nmap_scan(target):
    try:
        process = subprocess.run(
            ["nmap", "-F", target],
            capture_output=True,
            text=True,
            check=False
        )
        # Combine standard output and error for complete results
        output = process.stdout + "\n" + process.stderr
        return output.strip()
    except Exception as e:
        return f"Error running Nmap: {str(e)}"

# Function to analyze the scan output in plain language
def analyze_scan(scan_output):
    # Basic analysis: if port 80 is open and others are filtered, assume "safe" for a typical web server
    if "80/tcp open" in scan_output and "filtered" in scan_output:
        return "Safe: Only the standard HTTP port (80) is open and the remaining ports are filtered, which is expected for a secure web server."
    elif "open" in scan_output:
        return "Caution: Some ports are open; please review the scan output for potential vulnerabilities."
    else:
        return "Further analysis required."

# Handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to the Nmap Scanner Bot!\nUse /scan <target> to perform an Nmap scan.")

# Handler for the /scan command
@bot.message_handler(commands=['scan'])
def handle_scan(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Usage: /scan <target>\nExample: /scan example.com")
        return
    
    target = parts[1]
    bot.reply_to(message, f"🔍 Scanning {target}... Please wait.")
    
    # Run the Nmap scan
    scan_output = run_nmap_scan(target)
    # Analyze the scan results for a plain-language summary
    analysis = analyze_scan(scan_output)
    
    # Prepare the final response message (using Markdown formatting for code blocks)
    response_message = (
        f"✅ Scan Results for {target}:\n```\n{scan_output}\n```\n\n"
        f"Scan Analysis:\n{analysis}"
    )
    bot.reply_to(message, response_message, parse_mode="Markdown")

# Start polling for updates
if __name__ == "__main__":
    print("🚀 Starting bot using polling...")
    bot.infinity_polling()
