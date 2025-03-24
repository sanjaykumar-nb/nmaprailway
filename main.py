import os
import json
import requests
import telebot
from flask import Flask, request
import subprocess

# Set your bot token
BOT_TOKEN = "7924802116:AAHhn6UBw_fZSYX39ZSUSCZKcFKjSxLAIDw"
WEBHOOK_URL = "https://nmaprailway.railway.app/webhook"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Set webhook for Telegram bot
@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]

        if text.startswith("/scan"):
            target = text.split(" ")[1] if len(text.split()) > 1 else None
            if target:
                scan_result = run_nmap_scan(target)
                bot.send_message(chat_id, f"Nmap Scan Results for {target}:\n{scan_result}")
            else:
                bot.send_message(chat_id, "⚠️ Please provide a target. Example: `/scan example.com`")
    
    return "OK", 200

# Function to run Nmap scan
def run_nmap_scan(target):
    try:
        result = subprocess.run(["nmap", "-F", target], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error running Nmap: {str(e)}"

# Set up webhook on bot startup
@app.route("/")
def index():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    return "Bot is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
