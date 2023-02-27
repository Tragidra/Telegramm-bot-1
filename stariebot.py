from deeppavlov import build_model
from deeppavlov.core.common.file import read_json
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

updater = Updater("5701370182:AAHYcFUmp6c0MfnfynlzMzuFrxw9gUCVthU",
                  use_context=True)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Бла-бла-бла. Бла?")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /бла - бла
    /бла-бла - бла-бла
    /бла! - Бла!
    /бла? - Бла-бла-бла. Бла?""")


def bla2(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Бла-бла-бла.")


def bla3(update: Update, context: CallbackContext):
    update.message.reply_text("Бла-бла.")


def bla4(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Бла-бла-бла-бла")


def bla5(update: Update, context: CallbackContext):
    update.message.reply_text(
        "бла, бла, бла!")


def unknownbla(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Бла не бла-бла" % update.message.text)


def unknown_text_bla(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Ваш текст не бла" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('bla', bla4))
updater.dispatcher.add_handler(CommandHandler('бла-бла', help))
updater.dispatcher.add_handler(CommandHandler('bla3', bla3))
updater.dispatcher.add_handler(CommandHandler('bla7', bla2))
updater.dispatcher.add_handler(CommandHandler('bla5', bla5))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknownbla))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknownbla))  # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text_bla))

updater.start_polling()