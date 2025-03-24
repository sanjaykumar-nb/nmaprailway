import os
import telebot
import subprocess

# Telegram Bot Token (Set this as an environment variable in Railway)
BOT_TOKEN = os.getenv("BOT_TOKEN", "7924802116:AAHhn6UBw_fZSYX39ZSUSCZKcFKjSxLAIDw")

bot = telebot.TeleBot(BOT_TOKEN)

# Function to run Nmap scan
def run_nmap_scan(target):
    try:
        result = subprocess.run(["nmap", "-F", target], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error running Nmap: {str(e)}"

# Handle /scan command
@bot.message_handler(commands=["scan"])
def handle_scan(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Please provide a target. Example: `/scan example.com`")
        return

    target = args[1]
    bot.reply_to(message, f"🛠 Scanning {target}... Please wait.")
    scan_result = run_nmap_scan(target)
    bot.reply_to(message, f"🔍 Nmap Scan Results for {target}:\n```\n{scan_result}\n```", parse_mode="Markdown")

# Start polling for updates
if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.polling(non_stop=True)
