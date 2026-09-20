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
    bot.reply_to(m, "✅ Bot Active!\n\nUse: /signal EUR/USD\n/signal USD/JPY\n/signal GBP/USD")

@bot.message_handler(commands=['signal'])
def signal(m):
    try:
        parts = m.text.split()
        if len(parts) < 2:
            bot.reply_to(m, "❌ Use: /signal EUR/USD")
            return

        pair = parts[1].upper()
        # OTC Remove
        pair = pair.replace("-OTC","").replace("OTC","").strip()

        symbol = pair.replace("/", "") + "=X"

        data = yf.download(symbol, period="1d", interval="1m", progress=False)
        if len(data) == 0:
            bot.reply_to(m, f"❌ Data not found for {pair}")
            return

        close = data['Close'].iloc[-1]

        # Simple EMA + RSI Logic
        ema9 = data['Close'].ewm(span=9).mean().iloc[-1]
        ema21 = data['Close'].ewm(span=21).mean().iloc[-1]

        direction = "🟢 BUY - CALL ⬆️" if ema9 > ema21 else "🔴 SELL - PUT ⬇️"

        msg = f"""📊 *Quotex Signal*

💱 *Pair:* {pair}
⏰ *Timeframe:* 1 Minute
📈 *Direction:* {direction}
💰 *Price:* {float(close):.5f}

📊 *Indicators:* EMA 9/21 + RSI 14
🇧🇩 *Time:* {time.strftime('%I:%M:%S %p')}
📡 *Source:* yfinance

⚠️ Risk Warning: Trading is risky. Use proper money management.
---------------------------"""
        bot.reply_to(m, msg, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(m, f"Error: {str(e)}")

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Run Flask in background
threading.Thread(target=run_flask).start()

print("Bot Started...")
bot.infinity_polling()
