import os
import telebot
import yfinance as yf
from flask import Flask
import threading
import time

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8966694832:AAHGPoRrGZBs6zCHm8FXRmeFsbHnwlKifDU"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live!"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "✅ Bot Active!\n\nUse:\n/signal EUR/USD\n/signal USD/JPY\n/signal USD/BRL")

@bot.message_handler(commands=['signal'])
def signal(m):
    try:
        # /signal USD/BRL - OTC হলে 2 টা ভাগ হয়, তাই ঠিক করলাম
        text = m.text.replace("/signal", "").strip().upper()
        if not text:
            bot.reply_to(m, "❌ Use: /signal EUR/USD")
            return

        pair = text.replace("-OTC","").replace(" OTC","").replace("OTC","").strip()
        symbol = pair.replace("/", "") + "=X"

        df = yf.download(symbol, period="2d", interval="1m", progress=False, auto_adjust=True)

        if df.empty:
            bot.reply_to(m, f"❌ Data not found for {pair}")
            return

        # Fix for yfinance bug
