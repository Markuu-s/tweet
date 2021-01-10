import telebot
from twitter import parse_twitter_account
import time

ID_USER = ''

def send(tweets, ID_USER):
    if tweets is None:
        tweets = ['Check']

    bot = telebot.TeleBot('1599410074:AAG4hA_djCJZQoH3UAggn4dHokzv0vu9C38')
    for tweet in tweets:
        bot.send_message(ID_USER, tweet)

bot = telebot.TeleBot('1599410074:AAG4hA_djCJZQoH3UAggn4dHokzv0vu9C38')

@bot.message_handler(commands=['add'])
def add_twitter(message):
    bot.send_message(message.chat.id, 'Add a link to twitter account')
    global ID_USER
    ID_USER = message.chat.id
    @bot.message_handler(content_types=['text'])
    def adding(message1):
        pta0 = parse_twitter_account(message1.text)
        while 1:
            send(pta0.parse(), message1.chat.id)
            time.sleep(60 * 1)

bot.polling()