# -*- coding: utf-8 -*-
import requests
import feedparser
from datetime import datetime
import time
import telegram
from googletrans import Translator

# ==== تنظیمات اصلی ====
BOT_TOKEN = "7554657413:AAFcXvPt8y4SCX8Q1u8R62aAX-GZmYpseZI"
CHAT_ID = "<emrooznews_bot>"  # در ادامه روش پیدا کردنش رو می‌گم

RSS_FEEDS = [
    # منابع فعلی
    "https://www.khaleejtimes.com/rss", 
    "https://gulfnews.com/rss?generatorName=top-stories",
    "https://www.bloomberg.com/feed/podcast/etf-report.xml",
    "https://www.zoomit.ir/feed/",

    # منابع جدید - اخبار امارات
    "https://www.thenationalnews.com/arc/outboundfeeds/rss/",  # The National
    "https://www.arabianbusiness.com/rss/en/news",  # Arabian Business
    "https://www.timeoutdubai.com/rss.xml",  # Time Out Dubai
    "https://lovindubai.com/feed",  # Lovin Dubai

    # منابع جدید - فناوری و جهانی
    "https://techcrunch.com/feed/",  # TechCrunch
    "https://www.theverge.com/rss/index.xml",  # The Verge
    "https://www.engadget.com/rss.xml",  # Engadget
    "https://interestingengineering.com/feed",  # Interesting Engineering

    # منابع تصویری و مسافرتی
    "https://edition.cnn.com/travel/section/middle-east/rss/index.xml",  # CNN Travel Middle East
    "https://www.nationalgeographic.com/content/natgeo/en_us/index.rss"  # National Geographic
]

translator = Translator()
bot = telegram.Bot(token=BOT_TOKEN)

sent_articles = set()  # ذخیره لینک خبرهایی که قبلاً ارسال شدند

def fetch_latest_articles():
    articles = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:2]:  # دو خبر اول هر سایت
            link = entry.link
            if link not in sent_articles:
                title = entry.title
                summary = entry.summary if 'summary' in entry else ''

                # ترجمه خبر
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
        print("خطا در ارسال پیام:", e)

# اجرای همیشگی: بررسی هر ۱۵ دقیقه یک بار
while True:
    now = datetime.now()
    if now.minute % 15 == 0:
        send_news()
        time.sleep(60)
    time.sleep(20)
