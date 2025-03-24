import os
import time
import telebot
import subprocess
import requests

# Replace with your actual Telegram Bot Token
BOT_TOKEN = "7717097105:AAH5JxYXCPVlCxNyQOY4ZfkgX-gFIdfFWdU"  # e.g., "1234567890:ABCdefGHIJKLMnoPQRstuVWXYZ"

# Delete any existing webhook to avoid conflicts
delete_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
try:
    response = requests.get(delete_webhook_url)
    print("Webhook deletion response:", response.json())
except Exception as e:
    print("Error deleting webhook:", str(e))

# Wait a couple of seconds to ensure deletion is processed
time.sleep(2)

# Initialize the TeleBot instance
bot = telebot.TeleBot(BOT_TOKEN)

def run_nmap_scan(target):
    try:
        # Use TCP connect scan (-sT) with -Pn (skip host discovery) on ports 1-100.
        # This should avoid using raw sockets.
        process = subprocess.run(
            ["nmap", "-sT", "-Pn", "-p", "1-100", target],
            capture_output=True,
            text=True,
            check=False
        )
        output = process.stdout + "\n" + process.stderr
        return output.strip()
    except Exception as e:
        return f"Error running Nmap: {str(e)}"

def analyze_scan(scan_output):
    if "80/tcp open" in scan_output and "filtered" in scan_output:
        return ("Safe: Only the standard HTTP port (80) is open and the other ports are filtered, "
                "which is typical for a secure web server.")
    elif "open" in scan_output:
        return "Caution: Some ports are open. Please review the scan output for potential vulnerabilities."
    else:
        return "Caution: Some ports are open."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to the Nmap Scanner Bot!\nUse /scan <target> to perform a scan.")

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
