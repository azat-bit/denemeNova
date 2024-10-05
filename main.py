import apiText as keys
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import response as r

print("I am ALIVE...")

def startCommand(update: Update, context: CallbackContext):
    update.message.reply_text('Type something random to get us started')

def helpCommand(update: Update, context: CallbackContext):
    update.message.reply_text('If you need some help ... just check the internet it is so easy these days')

def handleMessage(update: Update, context: CallbackContext):
    text = str(update.message.text).lower()
    response = r.sampleResponse(text)
    update.message.reply_text(response)

def error(update: Update, context: CallbackContext):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(keys.API_Token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", startCommand))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handleMessage))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
