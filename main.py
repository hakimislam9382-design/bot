import os
import telebot
import yfinance as yf
from flask import Flask
import threading
import time
from datetime import datetime
import pytz

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8966694832:AAHGPoRrGZBs6zCHm8FXRmeFsbHnwlKifDU"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live!"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "✅ Bot Active!")

@bot.message_handler(commands=['signal'])
def signal(m):
    try:
        text = m.text.replace("/signal", "").strip().upper()
        pair = text.replace("-OTC","").replace(" OTC","").replace("OTC","").strip()
        if not pair:
            pair = "EUR/USD"
        symbol = pair.replace("/", "") + "=X"
        df = yf.download(symbol, period="2d", interval="1m", progress=False, auto_adjust=True)
        close = df['Close']
        if hasattr(close, 'columns'):
           
