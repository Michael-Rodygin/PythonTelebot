from pytube import YouTube
from telegram import *
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from random import randint

import os

PORT = int(os.environ.get('PORT', 5000))

TOKEN = "5392406783:AAE6FBf5aJ1_4J3aEZGGhMWQ-_SvwQJQ5wc"

cat_links = ['https://i.pinimg.com/originals/37/a7/6b/37a76b94646423e8a7cc5d7be4080c4e.jpg',
             'http://www.alleycat.org/wp-content/uploads/2019/03/FELV-cat.jpg',
             'https://www.scotsman.com/webimg/b25lY21zOjY0N2NiYTc5LTFhMmMtNGIwZC04NjZiLWE5MTVlODQ4OGJjYjpmOTlmMTQ1Ni1hYmU0LTQxNjctYTg2NC0xOGYzZmZhNTg5OTU=.jpg?width=1200&enable=upscale',
             'https://th-thumbnailer.cdn-si-edu.com/OP25AnQRquXRPHBQOUT92UK93M4=/1000x750/filters:no_upscale():focal(554x699:555x700)/https://tf-cmsv2-smithsonianmag-media.s3.amazonaws.com/filer/a4/04/a404c799-7118-459a-8de4-89e4a44b124f/img_1317.jpg',
             'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/220px-Cat03.jpg'
             ]

dog_links = ['https://cdn.arstechnica.net/wp-content/uploads/2022/04/GettyImages-997016774.jpg',
             'https://media-cldnry.s-nbcnews.com/image/upload/t_fit-760w,f_auto,q_auto:best/rockcms/2022-04/220428-dog-breeds-mb-1019-95b354.jpg',
             'https://kb.rspca.org.au/wp-content/uploads/2021/07/collie-beach-bokeh.jpg',
             'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/golden-retriever-royalty-free-image-506756303-1560962726.jpg?crop=0.672xw:1.00xh;0.166xw,0&resize=640:*',
             'https://www.thesprucepets.com/thmb/zY3HlLW8_ttejrOx2MlsNGcfLRo=/1414x1414/smart/filters:no_upscale()/EricVanderVeken500pxGettyImages-1068094978-9df2fa51da8749488b7d0b653fec8030.jpg'
             ]


def start(update: Update, context: CallbackContext):
    update.message.reply_text("PythonBot welcomes you!\nWrite /help to view available functions")


def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Available commands:\n/choice - choose whether to display a random cat or dog\nYou can also download a video by inserting it's url")


def choice(update: Update, context: CallbackContext):
    update.message.reply_text("Choose one of two commands:\n/Cats\n/Dogs")


def cats(update: Update, context: CallbackContext):
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=cat_links[randint(0, len(cat_links) - 1)])


def dogs(update: Update, context: CallbackContext):
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=dog_links[randint(0, len(dog_links) - 1)])


def text_handler(update: Update, context: CallbackContext):
    user_message = str(update.message.text)

    if update.message.parse_entities(types=MessageEntity.URL):
        update.message.reply_text(YouTube(user_message).streams.first().download())

    else:
        update.message.reply_text("Sorry I don't understand '%s'" % user_message)


def command_handler(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry '%s' is not a valid command" % update.message.text)


def main():
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('choice', choice))
    updater.dispatcher.add_handler(CommandHandler('cats', cats))
    updater.dispatcher.add_handler(CommandHandler('dogs', dogs))

    updater.dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, text_handler, run_async=True))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, command_handler))

    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook('https://yourherokuappname.herokuapp.com/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
