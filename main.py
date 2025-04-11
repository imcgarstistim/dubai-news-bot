# -*- coding: utf-8 -*-
import requests
import feedparser
from datetime import datetime
import telegram
from googletrans import Translator
from flask import Flask, request

# ==== تنظیمات اصلی ====
BOT_TOKEN = "7554657413:AAEGxaBjPAflLfdT5FfdKpuSRAtQOvpxxfE"
CHAT_ID = 263130171  # آی‌دی عددی

RSS_FEEDS = [
    "https://www.khaleejtimes.com/rss", 
    "https://gulfnews.com/rss?generatorName=top-stories",
    "https://www.bloomberg.com/feed/podcast/etf-report.xml",
    "https://www.zoomit.ir/feed/",
    "https://www.thenationalnews.com/arc/outboundfeeds/rss/",
    "https://www.arabianbusiness.com/rss/en/news",
    "https://www.timeoutdubai.com/rss.xml",
    "https://lovindubai.com/feed",
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.engadget.com/rss.xml",
    "https://interestingengineering.com/feed",
    "https://edition.cnn.com/travel/section/middle-east/rss/index.xml",
    "https://www.nationalgeographic.com/content/natgeo/en_us/index.rss"
]

translator = Translator()
bot = telegram.Bot(token=BOT_TOKEN)
sent_articles = set()

# === دریافت خبرها از فیدها و ترجمه ===
def fetch_latest_articles():
    articles = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:2]:  # فقط دو خبر اول
            link = entry.link
            if link not in sent_articles:
                title = entry.title
                summary = entry.summary if 'summary' in entry else ''
                translated_title = translator.translate(title, src='en', dest='fa').text
                translated_summary = translator.translate(summary, src='en', dest='fa').text
                message = f"\u2709\ufe0f <b>{translated_title}</b>\n\n{translated_summary}\n\n<b>\u0645نبع:</b> {link}"
                articles.append((link, message))
    return articles

# === ارسال پیام به تلگرام ===
def send_news():
    try:
        new_articles = fetch_latest_articles()
        for link, msg in new_articles:
            bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=telegram.ParseMode.HTML)
            sent_articles.add(link)
    except Exception as e:
        print("\ud83d\udd34 \u062e\u0637\u0627 \u062f\u0631 \u0627\u0631\u0633\u0627\u0644 \u067e\u06cc\u0627\u0645 \u0628\u0647 \u062a\u0644\u06af\u0631\u0627\u0645:", e)

# === وب اپلیکیشن Flask ===
app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Bot is running! Use /start command in Telegram."

@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat_id
    text = update.message.text

    if text == "/start":
        bot.send_message(chat_id=chat_id, text="✅ ربات خبررسان فعال است. لطفاً کمی صبر کنید تا خبرهای جدید ارسال شوند.")
        send_news()
    else:
        bot.send_message(chat_id=chat_id, text="🤖 دستور نامفهوم بود. لطفاً /start را ارسال کنید.")

    return 'ok'

# === اجرای اپلیکیشن ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
