#Standard Modules
from time import sleep

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

#Global Flags
bot.isSticker = False
bot.isAnimation = True
bot.isPhoto = False
bot.isTextOnly = False

@bot.message_handler(commands=['start'])
def welcome_message(message: Message):
    reply = cmd_handler.reply_handler(message.text)    
    
    if bot.isSticker:
        with open("static/g_sticker.webp", 'rb') as sticker:
            bot.send_sticker(message.chat.id, sticker)
            bot.send_message(message.chat.id, reply)
    elif bot.isAnimation:
        with open("static/g_animation.gif", 'rb') as anim:
            bot.send_animation(message.chat.id, anim)
            bot.send_message(message.chat.id, reply)
    elif bot.isPhoto:
        with open("static/g_photo.png", 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
            bot.send_message(message.chat.id, reply)
    elif bot.isTextOnly:
        bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=['help'])
def help_message(message: Message):
    reply = cmd_handler.reply_handler(message.text)

    bot.send_message(message.chat.id, reply, parse_mode='html')


@bot.message_handler(commands=['welcomeconfig'])
def init_welcome_sticker(message: Message) -> None:
    bot.send_message(message.chat.id, "Выберите тип приветствия", 
        reply_markup=__init_greeting_keyboard())

def set_welcome_animation(message: Message):
    cmd_handler.file_handler(bot, message, bot_token.token)

def set_welcome_sticker(message: Message) -> None:
    cmd_handler.file_handler(bot, message, bot_token.token)

def set_welcome_photo(message: Message) -> None:
    cmd_handler.file_handler(bot, message, bot_token.token)

def set_welcome_text(message: Message) -> None:
    cmd_handler.change_greeting(bot, message.text)
    bot.send_message(message.chat.id, "Приветствие изменено!")

def __init_greeting_keyboard():
    """Initialize greeting control keyboard

    Returns:
        InlineKeyboardMarkup: Keyboard for the message sent by the command
    """
    greeting_keyboard = types.InlineKeyboardMarkup()

    anim_key = types.InlineKeyboardButton(text="Анимация + Текст", 
                                          callback_data="animation")
    sticker_key = types.InlineKeyboardButton(text="Стикер + Текст", 
                                             callback_data="sticker")
    photo_key = types.InlineKeyboardButton(text="Фото + Текст", 
                                           callback_data="photo")
    text_key = types.InlineKeyboardButton(text="Только текст", 
                                          callback_data="text_only")
    
    greeting_keyboard.add(anim_key, sticker_key, photo_key, 
                          text_key, row_width=2)

    return greeting_keyboard


@bot.message_handler(["animetop"])
def check_ratings(message: Message) -> str:
    animetop_keyboard = __init_animetop_keyboard()

    bot.send_message(message.chat.id, "Hi!", reply_markup=animetop_keyboard)

def __init_animetop_keyboard():
    """Creates the keyboard for animetop command

    Returns:
        InlineKeyboardMarkup: Keyboard for the message sent by the command
    """
    animetop_keyboard = types.InlineKeyboardMarkup()

    alltime = types.InlineKeyboardButton(text="За все время", 
                                         callback_data="alltime")
    cur_year = types.InlineKeyboardButton(text="",
                                         callback_data="cur_year")
    cur_season = types.InlineKeyboardButton(text="",
                                                callback_data="cur_season")
    awaited = types.InlineKeyboardButton(text="",
                                         callback_data="awaited")
    by_decade = types.InlineKeyboardButton(text="",
                                           callback_data="by_decade")
    
    animetop_keyboard.add(alltime, cur_year, cur_season,
                          awaited, by_decade, row_width=2)
    
    return animetop_keyboard  


@bot.message_handler(commands=['animesearch'])
def search_anime(message):
    print("Placeholder!")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id)
    
    #Сигналы из клавиатуры настройки приветствия
    if (call.data == "animation"):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 
                        "Отправьте мне анимацию в .gif формате :3")
        bot.register_next_step_handler(call.message, set_welcome_animation)
    if (call.data == "sticker"):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Отправьте мне стикер :3")
        bot.register_next_step_handler(call.message, set_welcome_sticker)
    if (call.data == "photo"):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 
                        "Отправьте мне фото в .png формате :3")
        bot.register_next_step_handler(call.message, set_welcome_photo)
    if (call.data == "text_only"):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, 
                        "Отправьте мне текст сообщением :3")
        bot.register_next_step_handler(call.message, set_welcome_text)
    
    #Сигналы из клавиатуры рейтинга аниме
    if (call.data == "alltime"):
        bot.send_message(call.message.chat.id, "Ожидайте :3")
        sleep(3)
        # Add function call
    if (call.data == "cur_year"):
        bot.send_message(call.message.chat.id, "Ожидайте :3")
        sleep(3)
        # Add function call
    if (call.data == "cur_season"):
        bot.send_message(call.message.chat.id, "Ожидайте :3")
        sleep(3)
        # Add function call
    if (call.data == "awaited"):
        bot.send_message(call.message.chat.id, "Ожидайте :3")
        sleep(3)
        # Add function call
    if (call.data == "by_decade"):
        bot.send_message(call.message.chat.id, "Ожидайте :3")
        sleep(3)
        # Add function call


bot.polling(none_stop=True, interval=0)