from flask import Flask, request, jsonify
import nmap
import threading
import time
import telebot
import os

# Initialize Flask App
app = Flask(__name__)

# Telegram Bot Token (Replace with your own)
BOT_TOKEN = "7924802116:AAHhn6UBw_fZSYX39ZSUSCZKcFKjSxLAIDw"
bot = telebot.TeleBot(BOT_TOKEN)

# Keep-Alive Function to Prevent Railway from Sleeping
def keep_alive():
    while True:
        try:
            print("Keeping API alive...")
            time.sleep(300)  # Every 5 minutes
        except Exception as e:
            print(f"Error in Keep-Alive: {e}")

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
        nm.scan(target, arguments='-T4 --top-ports 10')  # Optimized for fast scanning
        scan_results = nm.csv()  # Get results in CSV format
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"target": target, "scan_result": scan_results})

# Telegram Command to Trigger Nmap Scan
@bot.message_handler(commands=['scan'])
def handle_scan(message):
    try:
        target = message.text.split(" ")[1]  # Extract target from message
        api_url = f"https://your-nmap-api.up.railway.app/scan?target={target}"
        response = requests.get(api_url).json()

        if "error" in response:
            bot.reply_to(message, f"Error: {response['error']}")
        else:
            bot.reply_to(message, f"Nmap Scan Results for {target}:\n{response['scan_result']}")
    except IndexError:
        bot.reply_to(message, "Usage: /scan <target>\nExample: /scan example.com")

# Background Thread to Run Telegram Bot
def start_telegram_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # Start Keep-Alive Thread
    threading.Thread(target=keep_alive, daemon=True).start()

    # Start Telegram Polling in a Separate Thread
    threading.Thread(target=start_telegram_bot, daemon=True).start()

    # Run Flask App
    app.run(host='0.0.0.0', port=5000)
