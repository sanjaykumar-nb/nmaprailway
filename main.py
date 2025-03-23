from flask import Flask, request, jsonify
import nmap
import telebot
import threading
import requests
import time

# Flask App
app = Flask(__name__)

# Telegram Bot Token (Replace with your bot token)
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot = telebot.TeleBot(BOT_TOKEN)

# Keep-Alive Function to Prevent Railway from Sleeping
def keep_alive():
    while True:
        try:
            print("🔄 Keeping API alive...")
            time.sleep(300)  # Every 5 minutes
        except Exception as e:
            print(f"🔥 Keep-Alive Error: {e}")

@app.route('/')
def home():
    return jsonify({"message": "Nmap API is running!"})

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

# Telegram Command to Trigger Nmap Scan
@bot.message_handler(commands=['scan'])
def handle_scan(message):
    try:
        target = message.text.split(" ")[1]  # Extract target
        api_url = f"https://your-nmap-api.up.railway.app/scan?target={target}"

        bot.reply_to(message, f"🔍 Scanning {target}... Please wait.")
        print(f"📡 Sending request to {api_url}")

        response = requests.get(api_url)
        print(f"🔄 Response Status: {response.status_code}")

        if response.status_code != 200:
            bot.reply_to(message, f"⚠️ Error: {response.text}")
            return

        data = response.json()
        print(f"📊 Received Data: {data}")

        if "error" in data:
            bot.reply_to(message, f"⚠️ Error: {data['error']}")
        else:
            bot.reply_to(message, f"✅ Nmap Scan Results for {target}:\n{data['scan_result']}")
    except IndexError:
        bot.reply_to(message, "❌ Usage: /scan <target>\nExample: /scan example.com")
    except Exception as e:
        bot.reply_to(message, f"❌ Unexpected Error: {str(e)}")
        print(f"🔥 Exception: {str(e)}")

# Run Telegram Bot in Background
def start_telegram_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=keep_alive, daemon=True).start()  # Prevent Sleeping
    threading.Thread(target=start_telegram_bot, daemon=True).start()  # Start Telegram Bot
    app.run(host='0.0.0.0', port=5000)
