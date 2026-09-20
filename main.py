
import telebot
import yfinance as yf
from flask import Flask
import threading
import time

BOT_TOKEN = "8966694832:AAHGPoRrGZBs6zCHm8FXRmeFsbHnwlKifDU"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live!"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "✅ Bot Active!\n\nUse: /signal EUR/USD\n/signal USD/JPY")

@bot.message_handler(commands=['signal'])
def signal(m):
    try:
        parts = m.text.split()
        if len(parts) < 2:
            bot.reply_to(m, "❌ Use: /signal EUR/USD\nExample: /signal USD/JPY")
            return

        pair = parts[1].upper().replace("-OTC","").replace("OTC","").strip()
        symbol = pair.replace("/", "") + "=X"

        df = yf.download(symbol, period="2d", interval="1m", progress=False)

        if df.empty:
            bot.reply_to(m, f"❌ Data not found for {pair}")
            return

        # Fix for yfinance new version
        if 'Close' in df.columns:
            close_series = df['Close']
            if hasattr(close_series, 'iloc'):
                # if multi column
                try:
                    last_close = float(close_series.iloc[-1].iloc[-1] if hasattr(close_series.iloc[-1], 'iloc') else close_series.iloc[-1])
                except:
                    last_close = float(close_series.values[-1][-1] if len
