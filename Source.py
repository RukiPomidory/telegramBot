import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.token)
is_question = False
is_answers = False
is_id = False
answers = []
question = ""
vote_results = {}


@bot.message_handler(commands=['show_id'])
def show_id(message):
    bot.send_message(message.chat.id, message.chat.id)


@bot.message_handler(commands=['show_results'])
def show_results(message):
    res = ''
    for i in vote_results:
        res += answers[vote_results[i]] + '\n'
    bot.send_message(message.chat.id, res)


@bot.message_handler(commands=['vote'])
def start_vote(message):
    global is_answers, is_question, is_id
    is_answers = False
    is_question = True
    is_id = False
    bot.send_message(message.chat.id, 'Начало голосования\nВведите вопрос:')


@bot.message_handler(commands=['stop'])
def stop_vote(message):
    global is_id
    if not is_answers or len(answers) == 0:
        bot.send_message(message.chat.id, 'Голосование остановлено')
        return
    bot.send_message(message.chat.id, 'Голосование сформировано!\nКуда отправить?')
    clear_flags()
    is_id = True


@bot.message_handler(func=lambda x: is_id, content_types='text')
def read_id(message):
    result = 'Голосование опубликовано'
    try:
        create_vote(message.text, question, answers)
    except:
        result = 'Произошла ошибка :/'
    bot.send_message(message.chat.id, result)
    clear_flags()


@bot.message_handler(func=lambda x: is_answers, content_types='text')
def read_answer(message):
    global answers
    answers.append(message.text)


@bot.message_handler(func=lambda x: is_question, content_types='text')
def read_question(message):
    global question, is_answers, is_question, is_id
    question = message.text
    bot.send_message(message.chat.id, 'Вопрос записан!\nНачните вводить ответы, по окончании - /stop')
    is_answers = True
    is_question = False
    is_id = False


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    vote_results[call.message.from_user.id] = call.data
    bot.send_message(call.message.chat.id, call.data)
    bot.send_message(call.message.chat.id, answers[call.data])


def create_vote(chat_id, question, answers):
    markup = types.InlineKeyboardMarkup()
    i = 0
    for answer in answers:
        markup.add(types.InlineKeyboardButton(text=answer, callback_data=i))
        i += 1
    bot.send_message(chat_id, question, reply_markup=markup)


def clear_flags():
    global is_question, is_answers, is_id
    is_question = False
    is_answers = False
    is_id = False


if __name__ == '__main__':
    bot.polling()
