import telebot
import yfinance as yf

BOT_TOKEN = "8966694832:AAHGPoRrGZBs6zCHm8FXRmeFsbHnwlKifDU"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Bot Active ✅\nLekho: usd brl signal")

@bot.message_handler(func=lambda m: True)
def sig(m):
    t = m.text.lower()
    if "usd" in t and "brl" in t:
        d = yf.download("USDBRL=X", period="1d", interval="1m")
        p = d['Close'].iloc[-1]
        bot.reply_to(m, f"USD/BRL: {p}\nSignal: BUY 1min")
    else:
        bot.reply_to(m, "Lekho: usd brl signal")

bot.infinity_polling()
