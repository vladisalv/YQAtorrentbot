#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import os
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Привет! Я маленький войковский бот, который позволяет тебе удобно смотреть пиратский контент!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Просто вышли мне торрент файл, и я все сделаю!')


def torrent_file(update, context):
    file_name = update.message.document.file_name
    if (file_name.endswith('.torrent')):
        update.message.reply_text(f'Я получил файл {file_name}. Начинаю загрузку.\
            Можешь проверить статус загрузки по ссылке http://192.168.88.88:9091')
        torrent_file = update.message.document.get_file(time_out=5)
        torrent_file.download(custom_path=os.path.join('/mnt/transmission/torrents', file_name))
    else:
        update.message.reply_text('Непонятный файл. Мне нужен файл с расширением .torrent')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    TOKEN=os.environ['TG_TOKEN']
    REQUEST_KWARGS={
        'proxy_url': 'socks5://167.172.185.196:1080/',
    }
    updater = Updater(TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.document, torrent_file))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
