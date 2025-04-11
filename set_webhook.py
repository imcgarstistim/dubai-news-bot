import requests

TOKEN = "7554657413:AAFcXvPt8y4SCX8Q1u8R62aAX-GZmYpseZI"
URL = f"https://dubai-news-bot-7.onrender.com"

set_webhook_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL}"

response = requests.get(set_webhook_url)
print(response.text)
