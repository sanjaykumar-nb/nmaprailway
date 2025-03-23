import os
import threading
import requests
import telebot
import nmap
from flask import Flask, request, jsonify

# Load Telegram Bot Token from Railway environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Validate the Bot Token
if not BOT_TOKEN or ":" not in BOT_TOKEN:
    raise ValueError("❌ Invalid Telegram Bot Token! Check your Railway Variables.")

# Initialize Flask App & Telebot
app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)

# Home Route
@app.route('/')
def home():
    return jsonify({"message": "Nmap API is running!"})

# Nmap Scan API Route
@app.route('/scan', methods=['GET'])
def scan():
    target = request.args.get('target')
    if not target:
        return jsonify({"error": "No target provided!"}), 400
    
    nm = nmap.PortScanner()
    try:
        nm.scan(target, arguments='-T4 --top-ports 10')
        scan_results = nm.csv()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"target": target, "scan_result": scan_results})

# Telegram Bot Command: /scan
@bot.message_handler(commands=['scan'])
def handle_scan(message):
    try:
        # Extract target from message
        target = message.text.split(" ")[1]
        api_url = f"https://your-nmap-api.up.railway.app/scan?target={target}"

        # Notify user that scan is starting
        bot.reply_to(message, f"🔍 Scanning {target}... Please wait.")

        # Call Railway API
        response = requests.get(api_url)
        if response.status_code != 200:
            bot.reply_to(message, f"⚠️ Error: {response.text}")
            return

        data = response.json()
        if "error" in data:
            bot.reply_to(message, f"⚠️ Error: {data['error']}")
        else:
            bot.reply_to(message, f"✅ Scan Results for {target}:\n{data['scan_result']}")
    except IndexError:
        bot.reply_to(message, "❌ Usage: /scan <target>\nExample: /scan google.com")
    except Exception as e:
        bot.reply_to(message, f"❌ Unexpected Error: {str(e)}")

# Start Telegram Bot in a Thread
def start_telegram_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=start_telegram_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)

