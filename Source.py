import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.token)


@bot.message_handler(func=lambda x: x.text == 'Нет', content_types='text')
def send_no(message):
    bot.reply_to(message, 'Нет')


@bot.message_handler(commands=['button'])
def test(message):
    markup = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейти на Яндекс", url="https://ya.ru")
    markup.add(url_button)
    bot.send_message(message.chat.id, 'TEST', reply_markup=markup)


if __name__ == '__main__':
    bot.polling()
