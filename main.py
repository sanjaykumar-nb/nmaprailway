import requests

BOT_TOKEN = "7924802116:AAHhn6UBw_fZSYX39ZSUSCZKcFKjSxLAIDw"
requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook")
