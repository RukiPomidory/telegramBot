import requests
from time import sleep
import datetime

token = "399070662:AAG3Zo6kVptr8xi3dLMx8ELWGQPXAMArmAY"

class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)


    def get_updates(self, offset = None, timeout = 100):
        method = "getUpdates"
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(self.api_url + method, params)
        return response.json()['result']


    def send_message(self, chat_id, text):
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': text}
        return requests.post(self.api_url + method, params)


    def get_last_update(self):
        result = self.get_updates()
        if len(result) > 0:
            last_update = result[-1]
        else:
            last_update = None

        return last_update

greet_bot = BotHandler(token)
greetings = ('здравствуй', 'дарова', 'привет')
no = ('нет', 'Нет', 'нЕт', 'неТ', 'НеТ', 'НЕт', 'нЕТ', 'НЕТ', 'неь', 'Неь', 'НЕЬ', 'HET', 'net', 'NET', 'No', 'no', 'NO')
yes = []
now = datetime.datetime.now()


def main():
    new_offset = None
    today = now.day
    hour = now.hour
    append = False
    while True:
        greet_bot.get_updates(new_offset)
        last_update = greet_bot.get_last_update()
        if not last_update:
            continue
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        #last_chat_name = last_update['message']['chat']['first_name']
        if append:
            yes.append((last_chat_text))
            greet_bot.send_message(last_chat_id, 'Запомнил: "{}"'.format(last_chat_text))
            append = False
            new_offset = last_update_id + 1
            continue
        if last_chat_text == '/append':
            append = True
            greet_bot.send_message(last_chat_id, 'Жду...')
            new_offset = last_update_id + 1
            continue
        if last_chat_text in no:
            greet_bot.send_message(last_chat_id, 'Нет')
        if last_chat_text in yes:
            greet_bot.send_message(last_chat_id, 'Да')
        #    today += 1
        new_offset = last_update_id + 1



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
