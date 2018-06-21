#-*- coding:utf-8 -*-

from telegram import Bot
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import time
import os
import requests
import re



TOKEN = 'xxxx'
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)


def login():
    global S
    username = 'xxxx'
    password = 'xxxx'
    login_url =  "http://kingss.vip:80/index/login/"
    S = requests.Session()
    login_data = {"swapname": username, "swappass": password}
    S.post(login_url,data=login_data)

def Inquire():
    global S
    url = 'http://kingss.vip/index.php/control/detail/63472/'
    rqs = S.get(url = url)
    #rqs.encoding='utf-8'
    data = rqs.text
    #data = unicode(data)
    find = re.findall('(\d+.\d+) GB',data)
    used_data = str(find[0])
    remain_data = str(find[1])
    return used_data,remain_data


def command(handler,cmd=None,**kw):
    def decorater(func):
        def wrapper(*args,**kw):
            return func(*args,**kw)
        if cmd==None:
            func_hander=handler(func,**kw)
        else:
            func_hander=handler(cmd,func,**kw)
        dispatcher.add_handler(func_hander)
        return wrapper
    return decorater

@command(CommandHandler,'start')
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="i'm a bot to inquire the residual data in kingss.Use /help to get help.")

@command(CommandHandler,'help')
def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="use /data to inquire the Residual data.")

@command(CommandHandler,'data')
def data(bot, update):
    login()
    used_data,remain_data = Inquire()
    text = '已用流量:' + used_data + ' GB | 剩余流量:' + remain_data + ' GB'
    bot.send_message(chat_id=update.message.chat_id, text=text)

@command(MessageHandler,Filters.text)
def echo(bot, update):
    file=open('/root/1.txt','a')
    file.write(update.message.text+'\n')
    file.close()
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

@command(CommandHandler,'caps',pass_args=True)
def caps(bot,update,args):
    text_caps=' '.join(args).upper()
    bot.sendMessage(chat_id=update.message.chat_id,text=text_caps)

updater.start_polling()






