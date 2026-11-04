import os
import threading
from flask import Flask
import telebot

TOKEN = '9016031285:AAHf6-B6rbIvWcnK280auGe89vpKnxOYvRY'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! বট সচল আছে।")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    bot.polling(none_stop=True)
