# -*- coding: utf-8 -*-
import requests
import feedparser
from datetime import datetime
import time
import telegram
from googletrans import Translator
from flask import Flask
import threading

# ==== تنظیمات اصلی ====
BOT_TOKEN = "7554657413:AAFcXvPt8y4SCX8Q1u8R62aAX-GZmYpseZI"
CHAT_ID = 263130171  # آی‌دی عددی که از getUpdates گرفتی رو اینجا بذار

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
bot = telegram.Bot(token=7554657413:AAFcXvPt8y4SCX8Q1u8R62aAX-GZmYpseZI)
sent_articles = set()

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
                message = f"✉️ <b>{translated_title}</b>\n\n{translated_summary}\n\n<b>منبع:</b> {link}"
                articles.append((link, message))
    return articles

def send_news():
    try:
        new_articles = fetch_latest_articles()
        for link, msg in new_articles:
            bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=telegram.ParseMode.HTML)
            sent_articles.add(link)
            time.sleep(3)
    except Exception as e:
        print("🔴 خطا در ارسال پیام به تلگرام:", e)

# === اجرای برنامه در بک‌گراند ===
def run_bot():
    while True:
        now = datetime.now()
        print("⏰ در حال بررسی خبرها در:", now)
        if now.minute % 15 == 0:
            send_news()
            time.sleep(60)
        time.sleep(20)

# === راه‌اندازی وب سرور برای Render ===
app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Bot is running!"

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
