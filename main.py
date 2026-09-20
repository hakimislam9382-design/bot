
import os
import telebot
import yfinance as yf
from flask import Flask
import threading
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
    bot.reply_to(m, "✅ Bot Active!\nUse /signal EUR/USD")

@bot.message_handler(commands=['signal'])
def signal(m):
    try:
        text = m.text.replace("/signal","").strip().upper()
        pair = text.replace("-OTC","").replace("OTC","").strip()
        if not pair: pair="EUR/USD"
        symbol = pair.replace("/","")+"=X"
        df = yf.download(symbol, period="2d", interval="1m", progress=False, auto_adjust=True)
        close = df['Close']
        if hasattr(close,'columns'): close=close.iloc[:,0]
        last = float(close.iloc[-1])
        e9 = float(close.ewm(span=9).mean().iloc[-1])
        e21 = float(close.ewm(span=21).mean().iloc[-1])
        d = "🟢 BUY ⬆️" if e9>e21 else "🔴 SELL ⬇️"
        dhaka = pytz.timezone('Asia/Dhaka')
        now = datetime.now(dhaka).strftime('%I:%M %p')
        bot.reply_to(m, f"📊 {pair}\nSignal: {d}\nPrice: {last:.5f}\nTime: {now} 🇧🇩")
    except Exception as e:
        bot.reply_to(m, f"Error: {e}")

def run_flask():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_flask, daemon=True).start()
bot.infinity_polling()
