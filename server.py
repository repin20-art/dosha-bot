import os
import telebot
from flask import Flask, request

# Можно вписать токен прямо здесь (быстро, но небезопасно)
# TOKEN = "8363642763:AAH05iIxIAsbpGLhtOLIyV9id0C73Zfyelg"
# Или через переменные окружения (правильнее):
TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/' + TOKEN, methods=['POST'])
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '', 200
    return "Bot is running!", 200

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message, "Бот онлайн и готов работать ✅")

@bot.message_handler(func=lambda message: True)
def echo_handler(message):
    bot.reply_to(message, f"Эхо: {message.text}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))