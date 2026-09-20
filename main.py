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
    bot.reply_to(m, "✅ Bot Active!\n\nUse:\n/signal EUR/USD\n/signal USD/BRL")

@bot.message_handler(commands=['signal'])
def signal(m):
    try:
        text = m.text.replace("/signal", "").strip().upper()
        if not text:
            bot.reply_to(m, "❌ Use: /signal EUR/USD")
            return
        pair = text.replace("-OTC","").replace(" OTC","").replace("OTC","").strip()
        symbol = pair.replace("/", "") + "=X"
        df = yf.download(symbol, period="2d", interval="1m", progress=False, auto_adjust=True)
        if df.empty:
            bot.reply_to(m, f"❌ Data not found {pair}")
            return
        close = df['Close']
        if hasattr(close, 'columns'):
            close = close.iloc[:, 0]
        last = float(close.iloc[-1])
        e9 = float(close.ewm(span=9).mean().iloc[-1])
        e21 = float(close.ewm(span=21).mean().iloc[-1])
        direction = "🟢 BUY - CALL ⬆️" if e9 > e21 else "🔴 SELL - PUT ⬇️"
        msg = f"📊 Quotex Signal\n\n💱 Pair: {pair}\n📈 Signal: {direction}\n💰 Price: {last:.5f}\n\nEMA 9/21\n🇧🇩 {time.strftime('%I:%M %p')}"
        bot.reply_to(m, msg)
    except Exception as e:
        bot.reply_to(m, f"Error: {e}")

def run_flask():
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_flask, daemon=True).start()
bot.infinity_polling()
