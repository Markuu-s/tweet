from twitter import ParseTwitterAccount
import time
import telebot
import threading

def inf_parse(USER):
    ps = ParseTwitterAccount(USER)
    bot = telebot.TeleBot('1599410074:AAG4hA_djCJZQoH3UAggn4dHokzv0vu9C38')
    while 1:
        ls = ps.parse()
        for l in ls:
            bot.send_message('752078021', l)
        #print('\n' + '*-'*10 + '\n')
        time.sleep(60)

users = [
    'https://twitter.com/itvnews',
    'https://twitter.com/cnnbrk',
    'https://twitter.com/CNN',
    'https://twitter.com/rtenews',
    'https://twitter.com/SkyNews',
    'https://twitter.com/ABC'
]
#users = ['https://twitter.com/MultiFeed2']
for user in users:
    threading.Thread(target=inf_parse, args=(user, )).start()
    time.sleep(30)