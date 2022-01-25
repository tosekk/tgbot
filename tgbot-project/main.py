#Standard Modules
from time import sleep
from requests import get

#Third-party Modules
from telebot import TeleBot
from telebot import types

#Local Modules
import bot_token
from commands_handler import CommandsHandler


#Bot Setup
bot = TeleBot(bot_token.token)
files_path = f'https://api.telegram.org/file/bot{bot_token.token}/'

#Commands Handler Class
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
def init_welcome_sticker(message) -> None:
    #sticker_keyboard = types.InlineKeyboardMarkup()
    #anim_key = types.InlineKeyboardButton(text="Выбрать анимацию...", callback_data='animation')
    #sticker_key = types.InlineKeyboardButton(text="Выбрать стикер...", callback_data='sticker')
    #sticker_keyboard.add(anim_key, sticker_key, row_width=2)

    bot.send_message(message.chat.id, "Отправьте мне анимацию или стикер!")
    bot.register_next_step_handler(message, set_welcome_sticker)


def set_welcome_sticker(message):
    if message.photo:
        file_info = bot.get_file(message.photo[-1].file_id)
        file = get(files_path + file_info.file_path, allow_redirects=True)
        filename = file_info.file_path.rsplit('/', 1)[1]
        open('static/' + filename, 'wb').write(file.content)
        bot.send_message(message.chat.id, "Устанавливаем стикер...")
        sleep(5)
        bot.send_message(message.chat.id, "Стикер установлен!")
        
        new_sticker = open('static' + filename, 'rb')
        bot.send_photo(message.chat.id, new_sticker)


@bot.message_handler(commands=['animesearch'])
def search_anime(message):
    print("Placeholder!")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id)


bot.polling(none_stop=True, interval=0)