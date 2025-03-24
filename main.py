import telebot
import subprocess

BOT_TOKEN = "7717097105:AAH5JxYXCPVlCxNyQOY4ZfkgX-gFIdfFWdU"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['scan'])
def handle_scan(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Usage: /scan <target>\nExample: /scan example.com")
        return

    target = parts[1]
    bot.reply_to(message, f"🔍 Running Nmap scan on {target}... Please wait.")

    try:
        process = subprocess.run(["nmap", "--unprivileged", "-p 1-100", target], 
                                 capture_output=True, text=True, check=False)
        output = process.stdout + "\n" + process.stderr
        bot.reply_to(message, f"✅ Nmap Scan Results for {target}:\n```\n{output}\n```", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Error running Nmap scan: {str(e)}")

if __name__ == "__main__":
    bot.infinity_polling()
