import os
import re
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler

import requests
from bs4 import BeautifulSoup


def 네이버_실검():
    res = requests.get("http://naver.com")
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    tag_list = soup.select('.PM_CL_realtimeKeyword_rolling .ah_k')

    keyword_list = []

    for tag in tag_list:
        label = tag.text
        keyword_list.append(label)

    return keyword_list



def start(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    bot.send_message(chat_id=chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    chat_id = update.message.chat_id  # 메세지를 받은 대화방의 ID (텍스트, 사진, 비디오, 오디오 등의 다양한 메세지)
    text = update.message.text  # 받은 텍스트 메세지

    try:
        if text == '네이버 실검':
            response = '\n'.join(네이버_실검())
        else:
            response = "니가 무슨 말 하는 지 모르겠어. :("
    except Exception as e:
        response = "오류 발생 : {}".format(e)

    bot.send_message(chat_id=chat_id, text=response)


def main(token):
    bot = Updater(token=TOKEN)

    handler = CommandHandler('start', start)
    bot.dispatcher.add_handler(handler)

    handler = MessageHandler(Filters.text, echo)
    bot.dispatcher.add_handler(handler)

    bot.start_polling()

    print('running telegram bot ...')
    bot.idle()


if __name__ == '__main__':
    TOKEN = ''  # FIXME: 각자의 Token을 적용해주세요.
    main(TOKEN)

