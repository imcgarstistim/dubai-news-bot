import requests

TOKEN = "7554657413:AAEGxaBjPAflLfdT5FfdKpuSRAtQOvpxxfE"
URL = "https://dubai-news-bot-7.onrender.com"  # آدرس اپت توی Render

set_webhook_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL}"
res = requests.get(set_webhook_url)
print("Set webhook response:", res.text)
