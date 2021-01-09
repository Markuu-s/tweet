import telebot

def send(tweets):
    bot = telebot.TeleBot('1599410074:AAG4hA_djCJZQoH3UAggn4dHokzv0vu9C38')

    @bot.message_handler(content_types=['text'])
    def lol(message):
        for tweet in tweets:
            bot.send_message('752078021', tweet)

    bot.polling(none_stop=True)
#752078021

