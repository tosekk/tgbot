#Standard Modules
from time import sleep
from requests import get

#Third-party Modules
from telebot import TeleBot
from telebot import types
from telebot.types import Message

#Local Modules
import bot_token
from commands_handler import CommandsHandler


#Bot Setup
bot = TeleBot(bot_token.token)
files_path = f'https://api.telegram.org/file/bot{bot_token.token}/'

#Commands Handler Class
cmd_handler = CommandsHandler()

#Files Paths
g_animation = open("static/g_animation.gif", "rb")
g_sticker = open("static/g_sticker.webp", "rb")
g_photo = open("static/g_photo.png", "rb")

#Global Flags
bot.isSticker = False
bot.isAnimation = True
bot.isPhoto = False
bot.isTextOnly = False

@bot.message_handler(commands=['start'])
def welcome_message(message):
    reply = cmd_handler.reply_handler(message.text)    
    
    if bot.isSticker:
        bot.send_sticker(message.chat.id, g_sticker)
        bot.send_message(message.chat.id, reply)
    elif bot.isAnimation:
        bot.send_animation(message.chat.id, g_animation)
        bot.send_message(message.chat.id, reply)
    elif bot.isPhoto:
        bot.send_photo(message.chat.id, g_photo)
        bot.send_message(message.chat.id, reply)
    elif bot.isTextOnly:
        bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=['help'])
def help_message(message):
    reply = cmd_handler.reply_handler(message.text)

    bot.send_message(message.chat.id, reply, parse_mode='html')


@bot.message_handler(commands=['welcomeconfig'])
def init_welcome_sticker(message) -> None:
    #sticker_keyboard = types.InlineKeyboardMarkup()
    #anim_key = types.InlineKeyboardButton(text="Выбрать анимацию...", callback_data='animation')
    #sticker_key = types.InlineKeyboardButton(text="Выбрать стикер...", callback_data='sticker')
    #sticker_keyboard.add(anim_key, sticker_key, row_width=2)

    bot.send_message(message.chat.id, "Выберите тип приветствия", reply_markup=__init_greeting_keyboard())

def set_welcome_animation(message):
    g_animation = cmd_handler.file_handler(bot, message, bot_token.token)

    _file_prep(message, g_animation, 0)

def set_welcome_sticker(message) -> None:
    g_sticker = cmd_handler.file_handler(bot, message, bot_token.token)

    _file_prep(message, g_sticker, 1)

def set_welcome_photo(message) -> None:
    g_sticker = cmd_handler.file_handler(bot, message, bot_token.token)

    _file_prep(message, g_sticker, 2)

def set_welcome_text(message) -> None:
    print("Hi")

def _file_prep(message: Message, g_file: str, f_type: int) -> None:
    """Handles greeting files sent by the user

    Args:
        message (Message): File sent by the user
        g_file (str): File path
        f_type (int): 0 - animation, 1 - sticker, 2 - photo
    """
    files = ['Анимация', 'Стикер', 'Фото']
    ending = ['а', '', 'о']

    bot.send_message(message.chat.id, f"{files[f_type]} загружается...")
    sleep(3)
    bot.send_message(message.chat.id, f"{files[f_type]} установлен{ending[f_type]}!")
    
    with open(g_file, 'rb') as file:
        bot.isAnimation = True
        bot.send_animation(message.chat.id, file)

def __init_greeting_keyboard():
    """Initialize greeting control keyboard

    Returns:
        InlineKeyboardMarkup: return a keyboard 2 rows wide with set keys
    """
    greeting_keyboard = types.InlineKeyboardMarkup()

    anim_key = types.InlineKeyboardButton(text="Анимация + Текст", callback_data="animation")
    sticker_key = types.InlineKeyboardButton(text="Стикер + Текст", callback_data="sticker")
    photo_key = types.InlineKeyboardButton(text="Фото + Текст", callback_data="photo")
    text_key = types.InlineKeyboardButton(text="Толкьо текст", callback_data="text_only")
    
    greeting_keyboard.add(anim_key, sticker_key, photo_key, text_key, row_width=2)

    return greeting_keyboard


@bot.message_handler(commands=['animesearch'])
def search_anime(message):
    print("Placeholder!")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id)
    if (call.data == "animation"):
        bot.send_message(call.message.chat.id, "Отправьте мне анимацию в .gif формате :3")
        bot.register_next_step_handler(call.message, set_welcome_animation)
    if (call.data == "sticker"):
        bot.send_message(call.message.chat.id, "Отправьте мне стикер :3")
        bot.register_next_step_handler(call.message, set_welcome_sticker)
    if (call.data == "photo"):
        bot.send_message(call.message.chat.id, "Отправьте мне фото в .png формате :3")
        bot.register_next_step_handler(call.message, set_welcome_photo)
    if (call.data == "text_only"):
        bot.send_message(call.message.chat.id, "Отправьте мне текст сообщением :3")
        bot.register_next_step_handler(call.message, set_welcome_text)


bot.polling(none_stop=True, interval=0)