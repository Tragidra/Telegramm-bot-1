import multiprocessing
from multiprocessing import Process
import telebot
import time
import requests
import yadisk
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from deeppavlov import build_model, train_model
from deeppavlov.core.common.file import read_json


cqa_model_config = read_json('C:/Users/astra/PycharmProjects/DS1TG/09.12.2022/modeli_ot_bota/squad_ru_bert_infer.json')
cqa_model = build_model(cqa_model_config, download=True)

intent_catcher_model_config = read_json('C:/Users/astra/PycharmProjects/DS1TG/09.12.2022/modeli_ot_bota'
                                        '/intent_catcher.json')

bot = telebot.TeleBot('5701370182:AAHYcFUmp6c0MfnfynlzMzuFrxw9gUCVthU')
min_limit = 0
context = ''
y = yadisk.YaDisk(token="y0_AgAAAABO8QQLAAiIyAAAAADSbK1TU1Bm_WWWRWun3sA3LYx57g_PtKM")
access_mode = "r"
base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
file = open('text.txt', 'r', encoding="utf-8")
text = file.read()

def download_infi(public_key):
    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']
    download_response = requests.get(download_url)
    with open('text.txt', 'wb') as f:
        f.write(download_response.content)

def parser(url):
    html = requests.get(url=url).text
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ''.join(chunk for chunk in chunks if chunk)
    return text


def get_first_message(message):
    bot.reply_to(message, "Введите, что вы хотите узнать о дипломной работе 'Рабочее пространство и искусственный интеллект ЛаКрул':")
    bot.register_next_step_handler(message, get_url_message)

def actualnaja_infa_o_project(message):
    y.download("/RabLaKrulInfa/spisok.txt", "text.txt")
    bot.send_message(message.from_user.id,'Соединение установлено, о чём вы хотите узнать?(Веб-ассистент)') #Подгрузка с диска актуальных источников информации

def get_url_message(message):
    global context
    print("Информация о:", message.text)
    if message.text == 'Веб-ассистент' or message.text == 'веб-ассистент' or message.text == 'LaKrul':
        context = parser('https://docviewer.yandex.ru/view/1324418059/?*=O6eNOB7cFd0fYqYLttZsgyxe%2FHB7InVybCI6InlhLWRpc2stcHVibGljOi8vdWpIN0pqVm5RWTQwYkVpajRGVUZLclZJM0xTNnVrYnBBbWY2ZHU4YU1FTlRrM295cG1MeHhxUnZwZ0M4eFpZRnEvSjZicG1SeU9Kb25UM1ZvWG5EYWc9PSIsInRpdGxlIjoi0JLQtdCxLdCQ0YHRgdC40YHRgtC10L3Rgi50eHQiLCJub2lmcmFtZSI6ZmFsc2UsInVpZCI6IjEzMjQ0MTgwNTkiLCJ0cyI6MTY3MTczODQ5NzgyNiwieXUiOiI2Mzg1NTAxMzkxNjMwMzQ3NDMyIn0%3D')
        print('Сообщения идентичны')
        y.download("/RabLaKrulInfa/Веб-Ассистент.txt", "text.txt")
        file = open('text.txt', 'r', encoding="utf-8")
        context = file.read()
        print(context)
    elif message.text == 'Платформа' or message.text == 'Рабочее Пространство' or message.text == 'рабочее пространство' or message.text == 'веб-платформа':
        # context = html_to_text('https://web-standards.ru/articles/web-platform/')
        print('Сообщения идентичны')
        y.download("/RabLaKrulInfa/Платформа.txt", "text.txt")
        file = open('text.txt', 'r', encoding="utf-8")
        context = file.read()
        print(context)
    else:
        context = parser('http://127.0.0.1:8000/')
        print("Контекст" + context)
    bot.reply_to(message, 'Актуальная информация загружена, что именно вы хотите узнать?')


def get_answer_message(message):
    answer = cqa_model([context], [message.text])
    print("Метрики модели:", answer)
    if answer[2][0] < min_limit:
        bot.reply_to(message, "Простите, но запрашиваемая вами информация ещё не доступна")
    else:
        bot.reply_to(message, answer)

def get_review(message):
    y.download("/RabLaKrulInfa/Обзор.txt", "text.txt")
    file = open('file.txt', 'r', encoding="utf-8")
    context = file.read()
    answer = cqa_model([context], [message.text])
    print("Метрики модели:", answer)
    if answer[2][0] < min_limit:
        bot.reply_to(message, "Простите, но запрашиваемая вами информация ещё не доступна")
    else:
        bot.reply_to(message, answer)

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    print("Я пришёл к ожиданию сообщения")
    queue.put(message.text)
    intent_result = queue.get()
    print("Сообщение:", message.text)
    print("Интент:", intent_result[0])
    if intent_result[0] == 'nachalo':
        get_first_message(message)
    elif intent_result[0] == 'vopros':
        get_answer_message(message)
    elif intent_result[0] == 'review':
        bot.reply_to(message, "Получена вся актуальная информация о проекте\n")
        get_review(message)
    else: #не понял интент
        bot.reply_to(message, "В данный момент на проекте проводятся технические работы, запросите информацию позже (или вы запросили недоступную информацию).")


def model(q):
    intent_catcher_model = build_model(intent_catcher_model_config, download=False)
    # intent_catcher_model = train_model(intent_catcher_model_config)
    q.put(1)
    while True:
        q.put(intent_catcher_model([q.get()]))
        print("Я ушёл")


if __name__ == '__main__':
    print("Тону 1")
    queue = multiprocessing.Queue()
    print("Тону 2")
    child_process = Process(target=model, args=(queue,))
    child_process.start()
    print("Тону 3")
    queue.get()
    print('Тону 4')
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print("Утонул")
            print(e)
            time.sleep(2)
