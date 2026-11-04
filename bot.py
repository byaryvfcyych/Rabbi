import os
import telebot

# আপনার টেলিগ্রাম বটের টোকেন
TOKEN = '9016031285:AAHf6-B6rbIvWcnK280auGe89vpKnxOYvRY'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! বট সচল আছে।")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)
