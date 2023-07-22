import re
import random

import requests
from lxml import html
from telegram.ext import Updater, CommandHandler

DEBUG = 1

def __debug(msg):
    if DEBUG:
        print("\033[94m[DEBUG]\033[0m", msg)

# Command handler for /start command
def start(bot, update):
    __debug("CALL start")

    update.message.reply_text(
        "Hello Abhishek! I am here to assist you. You can type /help to learn how I can be of help to you.")

# Command handler for /help command
def help(bot, update):
    __debug("CALL help")

    update.message.reply_text(
        "/video_at - I will send you one of the currently trending videos on YouTube.\n"
		"/haber_at - I will share one of the most read news articles from BBC.\n\n"
        "/help - Show this help message.")

# Command handler for /video_at command
def video_at(bot, update):
    __debug("CALL video_at")

    __debug(
        "video_at: Sending request to https://www.youtube.com/feed/trending")

    pg = requests.get("https://www.youtube.com/feed/trending")

    __debug("video_at: Got response: %d" % pg.status_code)

    if pg.status_code != 200:
        update.message.reply_text("Oops! Something went wrong :(")
        return

    video_list = re.findall('href="/watch\?v=\w{11}"', pg.text)

    if len(video_list) == 0:
        update.message.reply_text("Oops! Something went wrong! Couldn't find any videos :(")
        return

    update.message.reply_text("https://youtube.com" + random.choice(video_list)[6:-1])

# Command handler for /haber_at command
def haber_at(bot, update):
    __debug("CALL haber_at")

    __debug("haber_at: Sending request to https://www.bbc.com/news")

    pg = requests.get("https://www.bbc.com/news")

    __debug("haber_at: Got response: %d" % pg.status_code)

    if pg.status_code != 200:
        update.message.reply_text("Oops! Something went wrong :(")
        return

    tree = html.fromstring(pg.text)

    news_list = list()
    for i in range(1, 11):
        elem = tree.xpath("//li[@data-entityid='most-popular-read-{}']//a".format(i))

        if elem != []:
            news_list.append(elem[0])

    if len(news_list) == 0:
        update.message.reply_text("Oops! Something went wrong! Couldn't find any news articles :(")
        return

    update.message.reply_text("https://www.bbc.com" + random.choice(news_list).attrib["href"])

def main():
    __debug("CALL main")

    __debug("main: Initializing updater")
    updater = Updater("BOT TOKEN")  # Replace "BOT TOKEN" with the actual token of your Telegram bot
    dp = updater.dispatcher

    __debug("main: Configuring handlers")
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("video_at", video_at))
    dp.add_handler(CommandHandler("haber_at", haber_at))

    __debug("main: Starting idle process")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
