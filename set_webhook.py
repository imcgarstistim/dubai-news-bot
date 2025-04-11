import requests

BOT_TOKEN = '7554657413:AAEGxaBjPAflLfdT5FfdKpuSRAtQOvpxxfE'
WEBHOOK_URL = f'https://dubai-news-bot-7.onrender.com/{BOT_TOKEN}'

response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}')
print(response.text)

