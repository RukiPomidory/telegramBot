
import telebot
import config

bot = telebot.TeleBot(config.token)


@bot.message_handler(func=lambda x:x=='Нет',content_types='text')
def send_no(message):
    bot.reply_to(message, 'Нет')


if __name__ == '__main__':
    bot.polling()
