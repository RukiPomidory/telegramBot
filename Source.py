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
    first_button = types.InlineKeyboardButton(text="это", callback_data="first")
    second_button = types.InlineKeyboardButton(text="одно из двух", callback_data="second")
    markup.add(first_button, second_button)
    bot.send_message(message.chat.id, 'Либо это, либо одно из двух', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    bot.send_message(call.message.chat.id, call.data)

if __name__ == '__main__':
    bot.polling()
