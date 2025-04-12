# -*- coding: utf-8 -*-
import requests
import feedparser
from datetime import datetime
import time
import telegram
from googletrans import Translator
from flask import Flask, request
import threading
import os

# ==== تنظیمات اصلی ====
BOT_TOKEN = "7554657413:AAEGxaBjPAflLfdT5FfdKpuSRAtQOvpxxfE"
CHAT_ID = 263130171  # عددی که از getUpdates گرفتی

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

# === دریافت و ترجمه خبرها ===
def fetch_latest_articles():
    articles = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:2]:
            link = entry.link
            if link not in sent_articles:
                title = entry.title
                summary = entry.summary if 'summary' in entry else ''
                try:
                    translated_title = translator.translate(title, src='en', dest='fa').text
                    translated_summary = translator.translate(summary, src='en', dest='fa').text
                except:
                    translated_title = title
                    translated_summary = summary
                message = f"✉️ <b>{translated_title}</b>\n\n{translated_summary}\n\n<b>منبع:</b> {link}"
                articles.append((link, message))
    return articles

# === ارسال پیام به تلگرام ===
def send_news():
    try:
        new_articles = fetch_latest_articles()
        for link, msg in new_articles:
            bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=telegram.ParseMode.HTML)
            sent_articles.add(link)
            time.sleep(3)
    except Exception as e:
        print("🔴 خطا در ارسال پیام به تلگرام:", e)

# === اجرای دائم ربات ===
def run_bot():
    while True:
        now = datetime.now()
        print("⏰ بررسی خبرها در:", now)
        if now.minute % 15 == 0:
            send_news()
            time.sleep(60)
        time.sleep(20)

# === Flask app برای Webhook ===
app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Bot is running!"

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        print("📥 داده دریافتی:", data)

        update = telegram.Update.de_json(data, bot)

        if update.message:
            chat_id = update.message.chat_id
            text = update.message.text
            print(f"✅ پیام از کاربر دریافت شد: {text}")
            bot.send_message(chat_id=chat_id, text=f"✅ پیام دریافت شد: {text}")
        else:
            print("⚠️ پیام نداشت یا قابل پردازش نبود.")
    except Exception as e:
        print("❌ خطا در پردازش پیام:", e)

    return 'ok'

# === اجرای اپلیکیشن ===
if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
