#Standard Modules
from time import sleep

#Third-party Modules
from telebot import TeleBot
from telebot.types import (CallbackQuery, InlineKeyboardMarkup, 
                           InlineKeyboardButton, Message)

#Local Modules
import bot_token
from commands_handler import CommandsHandler
from myanimelist import MALRatings, MALSearch


#Bot Setup
bot = TeleBot(bot_token.token)
files_path = f'https://api.telegram.org/file/bot{bot_token.token}/'

#Commands Handler Class
anime_ratings = MALRatings()
anime_search = MALSearch()
cmd_handler = CommandsHandler()

#Global Flags
bot.isSticker = False
bot.isAnimation = True
bot.isPhoto = False
bot.isTextOnly = False
bot.page_num = 0


@bot.message_handler(commands=['start'])
def welcome_message(message: Message) -> None:
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
def help_message(message: Message) -> None:
    reply = cmd_handler.reply_handler(message.text)

    bot.send_message(message.chat.id, reply, parse_mode='html')


@bot.message_handler(commands=['welcomeconfig'])
def show_greeting_keyboard(message: Message) -> None:
    bot.send_message(message.chat.id, "Выберите тип приветствия", 
                     reply_markup=__init_greeting_keyboard())


def set_welcome_animation(message: Message) -> None:
    cmd_handler.file_handler(bot, message, bot_token.token)
    
    text_keyboard = __init_text_keyboard()
    bot.send_message(message.chat.id, "Хотите ли вы изменить текст?",
                     reply_markup=text_keyboard)


def set_welcome_sticker(message: Message) -> None:
    cmd_handler.file_handler(bot, message, bot_token.token)
    
    text_keyboard = __init_text_keyboard()
    bot.send_message(message.chat.id, "Хотите ли вы изменить текст?",
                     reply_markup=text_keyboard)


def set_welcome_photo(message: Message) -> None:
    cmd_handler.file_handler(bot, message, bot_token.token)
    
    text_keyboard = __init_text_keyboard()
    bot.send_message(message.chat.id, "Хотите ли вы изменить текст?",
                     reply_markup=text_keyboard)


def set_welcome_text(message: Message) -> None:
    cmd_handler.change_greeting(bot, message.text)
    bot.send_message(message.chat.id, "Приветствие изменено!")


def __init_greeting_keyboard() -> InlineKeyboardMarkup:
    """Initialize greeting control keyboard

    Returns:
        InlineKeyboardMarkup: Keyboard for the message sent by the command
    """
    greeting_keyboard = InlineKeyboardMarkup()

    anim_key = InlineKeyboardButton(text="Анимация + Текст", 
                                          callback_data="animation")
    sticker_key = InlineKeyboardButton(text="Стикер + Текст", 
                                             callback_data="sticker")
    photo_key = InlineKeyboardButton(text="Фото + Текст", 
                                           callback_data="photo")
    text_key = InlineKeyboardButton(text="Только текст", 
                                          callback_data="text_only")
    
    greeting_keyboard.add(anim_key, sticker_key, photo_key, 
                          text_key, row_width=2)

    return greeting_keyboard


def __init_text_keyboard() -> InlineKeyboardMarkup:
    text_keyboard = InlineKeyboardMarkup()
    
    yes_key =  InlineKeyboardButton(text="", callback_data="yes")
    no_key = InlineKeyboardButton(text="", callback_data="no")
    
    text_keyboard.add(yes_key, no_key, row_width=2)
    
    return text_keyboard


@bot.message_handler(["animetop"])
def show_toptype_keyboard(message: Message) -> None:
    toptype_keyboard = __init_toptype_keyboard()

    bot.send_message(message.chat.id, "Выберите рейтинг", 
                     reply_markup=toptype_keyboard)

    
def show_anime_ratings(message: Message, call_data: str) -> None:
    rating_title = __toptype_message(call_data)
    bot.send_message(message.chat.id, rating_title, parse_mode="html")
    
    ratings_file = anime_ratings.show_ratings(call_data)
    
    with open(ratings_file, "r", encoding="utf-8") as file:
        bot.content = file.readlines()
        page_message(message, bot.content, 0)


def __init_toptype_keyboard() -> InlineKeyboardMarkup:
    """Creates the keyboard for animetop command

    Returns:
        InlineKeyboardMarkup: Keyboard for the message sent by the command
    """
    toptype_keyboard = InlineKeyboardMarkup()

    alltime = InlineKeyboardButton(text="За все время", 
                                   callback_data="alltime")
    popular = InlineKeyboardButton(text="Самые популярные",
                                   callback_data="popular")
    upcoming = InlineKeyboardButton(text="Самые ожидаемые",
                                   callback_data="upcoming")
    favourite = InlineKeyboardButton(text="Самые любимые",
                                     callback_data="favourite")
    airing = InlineKeyboardButton(text="Лучшие сезона",
                                  callback_data="airing")
    
    toptype_keyboard.add(alltime, popular, airing,
                          upcoming, favourite, row_width=2)
    
    return toptype_keyboard


def __toptype_message(call_data: str) -> str:
    if call_data == "alltime":
        return "<b>Лучшие За Все Время</b>"
    if call_data == "upcoming":
        return "<b>Самые Ожидаемые</b>"
    if call_data == "popular":
        return "<b>Самые Популярные</b>"
    if call_data == "favourite":
        return "<b>Самые Любимые</b>"
    if call_data == "airing":
        return "<b>Лучшие Сезона</b>"


#Страничные сообщения
def page_message(message: Message, text: list, increment: int) -> None:
    pages_keyboard = __init_pages_keyboard()
    
    page = __process_text(text, increment)
    
    bot.send_message(message.chat.id, page, reply_markup=pages_keyboard)


def __process_text(text: list, increment: int) -> str:
    page = []
    
    if increment == 0:
        bot.page_num = 0
    elif increment == -1 or increment == 1:
        bot.page_num += increment
        if bot.page_num == -1:
            bot.page_num = 0
        elif bot.page_num == 10:
            bot.page_num = 9
    elif increment == 2:
        bot.page_num = 9
    
    page_start = 0 + (20 * bot.page_num)
    page_stop = 20 + (20 * bot.page_num)
    
    for line in range(page_start, page_stop):
        if bot.page_num == 0 or len(page) < line:
            page.append(text[line])
        else:
            page[line - page_start] = text[line]
            
    page = ''.join(page)
    
    return page


def __init_pages_keyboard() -> InlineKeyboardMarkup:
    pages_keyboard = InlineKeyboardMarkup()
    
    first = InlineKeyboardButton(text="1", callback_data="first")
    prev = InlineKeyboardButton(text="<<", callback_data="previous")
    next = InlineKeyboardButton(text=">>", callback_data="next")
    last = InlineKeyboardButton(text="10", callback_data="last")
    
    pages_keyboard.add(first, prev, next, last, row_width=4)
    
    return pages_keyboard


@bot.message_handler(commands=['animesearch'])
def ask_anime_title(message: Message) -> None:
    bot.send_message(message.chat.id, 
                     "Напишите название аниме(на английском)")
    bot.register_next_step_handler(message, show_search_result)

   
def show_search_result(message: Message) -> None:
    results = anime_search.search(message.text)
        
    bot.send_message(message.chat.id, "<b>Результаты поиска</b>",
                     parse_mode="html")
    bot.send_message(message.chat.id, "\n".join(results))


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery) -> None:
    """Handles InlineKeyboardMarkup's calls

    Args:
        call (CallbackQuery): InlineKeyboardButton callback
    """
    bot.answer_callback_query(call.id)
    
    #Клавиатура приветствия
    __greeting_query(call)
    
    #Клавиатура видов рейтинга
    __rating_query(call)

    #Клавиатура страниц
    __page_query(call)
    
    #Клавиатура текста
    __greeting_text_query(call)


def __greeting_query(call: CallbackQuery) -> None:
    """Handles greeting keyboard's calls

    Args:
        call (CallbackQuery): InlineKeyboardButton callback
    """
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

      
def __page_query(call: CallbackQuery) -> None:
    """Handles page keyboard's calls

    Args:
        call (CallbackQuery): InlineKeyboardButton callback
    """
    if (call.data == "first"):
        bot.delete_message(call.message.chat.id, call.message.id)
        page_message(call.message, bot.content, 0)
    if (call.data == "previous"):
        bot.delete_message(call.message.chat.id, call.message.id)
        page_message(call.message, bot.content, -1)
    if (call.data == "next"):
        bot.delete_message(call.message.chat.id, call.message.id)
        page_message(call.message, bot.content, 1)
    if (call.data == "last"):
        bot.delete_message(call.message.chat.id, call.message.id)
        page_message(call.message, bot.content, 2)

       
def __rating_query(call: CallbackQuery) -> None:
    """Handles anime rating keyboard's calls

    Args:
        call (CallbackQuery): InlineKeyboardButton callback
    """
    if (call.data == "alltime"):
        bot.send_message(call.message.chat.id, "Собираю информацию...")
        show_anime_ratings(call.message, call.data)
        sleep(2)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
    if (call.data == "popular"):
        bot.send_message(call.message.chat.id, "Собираю информацию...")
        show_anime_ratings(call.message, call.data)
        sleep(2)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
    if (call.data == "airing"):
        bot.send_message(call.message.chat.id, "Собираю информацию...")
        show_anime_ratings(call.message, call.data)
        sleep(2)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
    if (call.data == "upcoming"):
        bot.send_message(call.message.chat.id, "Собираю информацию...")
        show_anime_ratings(call.message, call.data)
        sleep(2)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
    if (call.data == "favourite"):
        bot.send_message(call.message.chat.id, "Собираю информацию...")
        sleep(2)
        show_anime_ratings(call.message, call.data)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)


def __greeting_text_query(call: CallbackQuery) -> None:
    """Handles text keyboard's calls

    Args:
        call (CallbackQuery): InlineKeyboardButton callback
    """
    if (call.data == "yes"):
        bot.register_next_step_handler(call.message, set_welcome_text)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
    if (call.data == "no"):
        bot.register_next_step_handler(call.message, set_welcome_text)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)


bot.polling(none_stop=True, interval=0)