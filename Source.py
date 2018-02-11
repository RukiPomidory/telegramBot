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
markup = types.InlineKeyboardMarkup()


@bot.message_handler(commands=['show_id'])
def show_id(message):
    bot.send_message(message.chat.id, message.chat.id)


@bot.message_handler(commands=['show_results'])
def show_results(message):
    table = {}
    for answer in answers:
        table[answer] = 0
    #-280095386
    for vr in vote_results:
        table[answers[int(vote_results[vr])]] += 1
    res = ''
    for item in table:
        res += '{} - \t({} штук)\n'.format(item, table[item])
    bot.send_message(message.chat.id, res)


@bot.message_handler(commands=['vote'])
def start_vote(message):
    global is_answers, is_question, is_id, answers, vote_results
    is_answers = False
    is_question = True
    is_id = False
    answers = []
    vote_results = {}
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
    global vote_results
    vote_results[call.from_user.id] = call.data

    table = {}
    for answer in answers:
        table[answer] = 0
    # -280095386
    for vr in vote_results:
        table[answers[int(vote_results[vr])]] += 1
    res = '{}\n'.format(question)
    for item in table:
        res += '{} - \t({} голосов)\n'.format(item, table[item])
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=res, reply_markup=markup)


def create_vote(chat_id, question, answers):
    global markup
    i = 0
    for answer in answers:
        markup.add(types.InlineKeyboardButton(text=answer, callback_data=str(i)))
        i += 1
    bot.send_message(chat_id, question, reply_markup=markup)


def clear_flags():
    global is_question, is_answers, is_id
    is_question = False
    is_answers = False
    is_id = False


def count(value, dict):
    i = 0
    for d in dict:
        if dict[d] == value:
            i += 1
    return i


if __name__ == '__main__':
    bot.polling()
