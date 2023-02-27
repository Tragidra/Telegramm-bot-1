import time
import telebot
from deeppavlov import build_model
from deeppavlov.core.common.file import read_json

bot = telebot.TeleBot('5678654199:AAGqvTEHAdXE3mPdkDbc-x6kMkN5Pvqop4w')

model_config = read_json('squad_ru_bert_infer.json')
model = build_model(model_config, download=True)

file_name = "C:\\Users\\amir1\\PycharmProjects\\ChatBot\\pyshkin.txt"
access_mode = "r"
text = open(file_name, access_mode, encoding="utf8")
print(model(['DeepPavlov is library for NLP and dialog systems.'], ['What is DeepPavlov?']))



# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(message.chat.id, "Добро пожаловать!")
#
#
# @bot.message_handler(commands=["raz"])
# def raz(message):
#     bot.send_message(message.chat.id, text="Раз Два Три")





@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # print(message.text)
    # for xer in message.items():
    #     if xer['text'] == 'asdasdasd':
    #         print(xer)
    #         break
    bot.send_message(message.from_user.id, model(text, message.text))
    # if message.text == "Привет":
    #    bot.send_message(message.from_user.id, "Здравствуй")
    # elif message.text == '/help':
    #     bot.send_message(message.from_user.id, "Напиши 'Привет'")
    # else:
    #     bot.send_message(message.from_user.id, "Я Вас не понял, напишите /help.")


# bot.polling(none_stop=True)
#
# print("Bot listening")
#

print("Bot listening")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
