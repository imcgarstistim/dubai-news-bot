# main.py
# -*- coding: utf-8 -*-
import requests
import feedparser
from datetime import datetime
import time
import telegram
from googletrans import Translator
from flask import Flask, request
import threading

BOT_TOKEN = "توکن تو اینجاست"
CHAT_ID = 263130171  # آی‌دی عددی تلگرام

RSS_FEEDS = [
    "https://www.khaleejtimes.com/rss", 
    "https://gulfnews.com/rss?generatorName=top-stories",
    "https://www.zoomit.ir/feed/",
]

translator = Translator()
bot = telegram.Bot(token=BOT_TOKEN)
sent_articles = set()

def fetch_latest_articles():
    articles = []
    for feed_url in RSS_FEEDS:
        print(f"📡 در حال خواندن فید: {feed_url}")
        feed = feedparser.parse(feed_url)
        print(f"🔢 تعداد خبرها: {len(feed.entries)}")
        for entry in feed.entries[:2]:
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
            print("📤 در حال ارسال:", msg[:60])
            bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=telegram.ParseMode.HTML)
            sent_articles.add(link)
            time.sleep(3)
    except Exception as e:
        print("🔴 خطا در ارسال پیام:", e)

def run_bot():
    while True:
        print("⏰ بررسی در:", datetime.now())
        send_news()  # بدون شرط
        time.sleep(60)

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Bot is running!"

@app.route('/', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat_id
    text = update.message.text
    bot.send_message(chat_id=chat_id, text=f"پیام دریافت شد: {text}")
    return 'ok'

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
