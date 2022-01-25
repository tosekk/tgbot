#Standard Modules
from time import sleep

#Third-party Modules
from telebot import TeleBot
from telebot import types

#Local Modules
import bot_token
from commands_handler import CommandsHandler


bot = TeleBot(bot_token.token)
commands = CommandsHandler()


@bot.message_handler(commands=['start'])
def welcome_message(message):
    reply = commands.reply_handler(message.text)
    animation = open("static/greeting.gif", "rb")

    bot.send_animation(message.chat.id, animation)
    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=['help'])
def help_message(message):
    reply = commands.reply_handler(message.text)

    bot.send_message(message.chat.id, reply, parse_mode='html')


@bot.message_handler(commands=['setwelcomesticker'])
def set_welcome_sticker(message):
    bot.send_message(message.chat.id, "Done!")

bot.polling(none_stop=True, interval=0)