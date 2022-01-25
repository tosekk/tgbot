#Standard Modules
from time import sleep

#Third-party Modules
from telebot import TeleBot
from telebot import types

#Local Modules
import bot_token

bot = TeleBot(bot_token.token)

def text_handler(command: str):
        text = ''
        start = f"[{command[1:]}]"
        stop = f"[{command}]"

        with open('texts.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if start in line:
                    continue
                elif stop in line:
                    break
                else:
                    text += line
        return text

@bot.message_handler(commands=['start'])
def welcome(message):
    reply = text_handler(message.text)

    bot.send_message(message.chat.id, reply)
    sleep(3)
    #bot.send_message(message.chat.id, "Какое аниме ты ищешь?")

bot.polling(none_stop=True, interval=0)