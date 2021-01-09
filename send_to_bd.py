import telebot


def send(tweets=None):
    if tweets is None:
        tweets = ['Check']

    bot = telebot.TeleBot('1599410074:AAG4hA_djCJZQoH3UAggn4dHokzv0vu9C38')
    for tweet in tweets:
        bot.send_message('752078021', tweet)
# 752078021

