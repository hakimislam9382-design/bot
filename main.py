import telebot
import yfinance as yf
from flask import Flask
import threading
import os

BOT_TOKEN = "8966694832:AAHGPoRrGZBs6zCHm8FXm8oRz"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Bot Active ✅")

@bot.message_handler(func=lambda m: True)
def sig(m):
    if "usd" in m.text.lower():
        d = yf.download("USDBRL=X", period="1d", interval="1m")
        p = d['Close'].iloc[-1]
        bot.reply_to(m, f"USD/BRL: {p}")
    else:
        bot.reply_to(m, "Lekho: usd brl")

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Running!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

threading.Thread(target=run_flask).start()
bot.infinity_polling()
