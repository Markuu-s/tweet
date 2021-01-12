from twitter import parse_twitter_account
import time
import telebot

USER = 'https://twitter.com/MultiFeed2'
ps = parse_twitter_account(USER)
bot = telebot.TeleBot('1599410074:AAG4hA_djCJZQoH3UAggn4dHokzv0vu9C38')
while 1:
    ls = ps.parse()
    for l in ls:
        bot.send_message('752078021', l)
    #print('\n' + '*-'*10 + '\n')
    time.sleep(60)
