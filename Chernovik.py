import time

import telebot
from deeppavlov import build_model
from deeppavlov.core.common.file import read_json
import requests
from urllib.parse import urlencode
import yadisk
y = yadisk.YaDisk(token="y0_AgAAAABO8QQLAAiIyAAAAADSbK1TU1Bm_WWWRWun3sA3LYx57g_PtKM")

bot = telebot.TeleBot('5701370182:AAHYcFUmp6c0MfnfynlzMzuFrxw9gUCVthU')
model_config = read_json('squad_ru_bert_infer.json')
model = build_model(model_config, download=True)
access_mode = "r"
base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
file = open('text.txt', 'r', encoding="utf-8")
text = file.read()

def download_statu(public_key):
    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']
    download_response = requests.get(download_url)
    with open('text.txt', 'wb') as f:
        f.write(download_response.content)

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.send_message(message.from_user.id,'Пожалуйста, введите название статьи')
    if message.text == "Дифференциальные уравнения и их роль на уроках физики":
        # public_key = 'https://disk.yandex.ru/i/HvUtBj7NRO14SA'
        # download_statu(public_key)
        y.download("/test/Дифференциальные уравнения и их роль на уроках физики.txt", "text.txt")
        bot.send_message(message.from_user.id, 'Соединение установлено, файл найден.')
    elif message.text == "Новые взгляды на квантовые скачки бросают вызов основным принципам физики":
        # public_key = 'https://disk.yandex.ru/i/JgXm2Pry02_r3g'
        # download_statu(public_key)
        y.download("/test/Новые взгляды на квантовые скачки бросают вызов основным принципам физики.txt", "text.txt")
        bot.send_message(message.from_user.id, 'Соединение установлено, файл найден.')
    elif message.text == "Сюри-Дзё и его значение в истории королевства Рюкю":
        # public_key = 'https://disk.yandex.ru/i/4PtY6HNcfHL-Rg'
        # download_statu(public_key)
        y.download("/test/Сюри-Дзё и его значение в истории королевства Рюкю.txt", "text.txt")
        bot.send_message(message.from_user.id,'Соединение установлено, файл найден.')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, model([text], [message.text])[0][0])


print("Bot listening")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
