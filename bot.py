from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
from telegram.ext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from translate import Translator 
from telegram import Update


def select_lang(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Russian",callback_data="Russian"),
            InlineKeyboardButton("Chinese",callback_data="Chinese"),
            InlineKeyboardButton("German",callback_data="German"),
            InlineKeyboardButton("Spanish",callback_data="Spanish"),
            InlineKeyboardButton("Arabic",callback_data="Arabic"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome! Choose A language to translate from English", reply_markup=reply_markup)

lang = ""

def button(update: Update, context: CallbackContext) -> None:
    global lang
    lang = update.callback_query.data.lower()
    query = update.callback_query
    query.answer
    query.edit_message_text(text=f"{query.data } has been selected for Translation! Type a text to translate:")


def lang_translator(user_input):
    translator = Translator(from_lang ="english", to_lang = lang)
    translation = translator.translate(user_input)
    return translation

def reply(update, context):
    user_input = update.message.text
    update.message.reply_text(lang_translator(user_input))


def main():
    api = open("api.txt", "r")
    updater = Updater(api.read(), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',select_lang))
    dp.add_handler(CommandHandler('select_lang',select_lang))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text, reply))
    updater.start_polling()
    updater.idle()


main()