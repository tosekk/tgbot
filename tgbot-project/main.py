#Standard Modules
from random import choice, randint
from time import sleep


#Third-party Modules
from telebot import TeleBot
from telebot.types import (CallbackQuery, InlineKeyboardMarkup, 
                           InlineKeyboardButton, Message)


#Local Modules
import bot_token
from greeting_handler import GreetingsHandler
from myanimelist import (MALRatings, MALSearch, MALOst, 
                         MALCast, MALSummary, MALTrailer)
from watchlist import Watchlist


#Bot Setup
bot = TeleBot(bot_token.token)
files_path = f'https://api.telegram.org/file/bot{bot_token.token}/'

#Greetings Handler
g_handler = GreetingsHandler()

#Anime Commands Classes
anime_ratings = MALRatings()
anime_search = MALSearch()
anime_ost = MALOst()
anime_cast = MALCast()
anime_summary = MALSummary()
anime_trailer = MALTrailer()

#Watchlist Handler
watchlist = Watchlist()

#Global Flags
bot.g_type = "animation"
bot.page_num = 0


@bot.message_handler(['start'])
def welcome_message(message: Message) -> None:
    """Handles welcome message

    Args:
        message (Message): Message that contains the command
    """
    
    reply = g_handler.reply_handler(message.text)    
    
    if bot.g_type == "sticker":
        with open("static/g_sticker.webp", 'rb') as sticker:
            bot.send_sticker(message.chat.id, sticker)
            bot.send_message(message.chat.id, reply)
    elif bot.g_type == "animated sticker":
        with open("static/g_sticker_anim.tgs", 'rb') as anim:
            bot.send_animation(message.chat.id, anim)
            bot.send_message(message.chat.id, reply)
    elif bot.g_type == "animation":
        with open("static/g_animation.gif", 'rb') as anim:
            bot.send_animation(message.chat.id, anim)
            bot.send_message(message.chat.id, reply)
    elif bot.g_type == "photo":
        with open("static/g_photo.png", 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
            bot.send_message(message.chat.id, reply)
    elif bot.g_type == "text_only":
        bot.send_message(message.chat.id, reply)


@bot.message_handler(['help'])
def help_message(message: Message) -> None:
    """Handles help message

    Args:
        message (Message): Message that contains the command
    """
    
    reply = g_handler.reply_handler(message.text)

    bot.send_message(message.chat.id, reply, parse_mode='html')


@bot.message_handler(['welcomeconfig'])
def show_greeting_keyboard(message: Message) -> None:
    """Handles greeting configuration

    Args:
        message (Message): Message that contains the command
    """
    
    bot.send_message(message.chat.id, "???????????????? ?????? ??????????????????????", 
                     reply_markup=__init_greeting_keyboard())


def __set_welcome_animation(message: Message, call_data: str) -> None:
    """Private method that handles greetings with animation

    Args:
        message (Message): Message
        call_data (str): Keyboard button call data
    """
    
    g_handler.file_handler(bot, message, call_data, bot_token.token)
    
    text_keyboard = __init_text_keyboard()
    bot.send_message(message.chat.id, "???????????? ???? ???? ???????????????? ???????????",
                     reply_markup=text_keyboard)


def __set_welcome_sticker(message: Message, call_data: str) -> None:
    """Private method that handles greetings with sticker

    Args:
        message (Message): Message
        call_data (str): Keyboard button call data
    """
    
    g_handler.file_handler(bot, message, call_data, bot_token.token)
    
    text_keyboard = __init_text_keyboard()
    bot.send_message(message.chat.id, "???????????? ???? ???? ???????????????? ???????????",
                     reply_markup=text_keyboard)


def __set_welcome_photo(message: Message, call_data: str) -> None:
    """Private method that handles greetings with photo

    Args:
        message (Message): Message
        call_data (str): Keyboard button call data
    """
    
    g_handler.file_handler(bot, message, call_data, bot_token.token)
    
    text_keyboard = __init_text_keyboard()
    bot.send_message(message.chat.id, "???????????? ???? ???? ???????????????? ???????????",
                     reply_markup=text_keyboard)


def __set_welcome_text(message: Message, call_data: str="with_file") -> None:
    """Private method that handles greeting text

    Args:
        message (Message): Message
        call_data (str, optional): Keyboard button call data. 
        Defaults to "with_file".
    """
    
    g_handler.change_greeting(bot, message.text, call_data)
    bot.send_message(message.chat.id, "?????????????????????? ????????????????!")


def __init_greeting_keyboard() -> InlineKeyboardMarkup:
    """Initialize greeting control keyboard

    Returns:
        InlineKeyboardMarkup: Keyboard
    """
    
    greeting_keyboard = InlineKeyboardMarkup()

    anim_key = InlineKeyboardButton(text="???????????????? + ??????????", 
                                          callback_data="animation")
    sticker_key = InlineKeyboardButton(text="???????????? + ??????????", 
                                             callback_data="sticker")
    photo_key = InlineKeyboardButton(text="???????? + ??????????", 
                                           callback_data="photo")
    text_key = InlineKeyboardButton(text="???????????? ??????????", 
                                          callback_data="text_only")
    
    greeting_keyboard.add(anim_key, sticker_key, photo_key, 
                          text_key, row_width=2)

    return greeting_keyboard


def __init_text_keyboard() -> InlineKeyboardMarkup:
    """Handles greeting text config question keyboard

    Returns:
        InlineKeyboardMarkup: Keyboard
    """
    
    text_keyboard = InlineKeyboardMarkup()
    
    yes_key =  InlineKeyboardButton(text="????", callback_data="yes")
    no_key = InlineKeyboardButton(text="??????", callback_data="no")
    
    text_keyboard.add(yes_key, no_key, row_width=2)
    
    return text_keyboard


def __init_sticker_keyboard() -> InlineKeyboardMarkup:
    """Creates sticker type keyboard

    Returns:
        InlineKeyboardMarkup: Keyboard
    """
    
    sticker_keyboard = InlineKeyboardMarkup()
    
    ordinary = InlineKeyboardButton(text="??????????????", callback_data="ordinary")
    animated = InlineKeyboardButton(text="??????????????????????????", callback_data="animated")
    
    sticker_keyboard.add(ordinary, animated, row_width=2)
    
    return sticker_keyboard


@bot.message_handler(commands=['animesearch', 'animeost', 
                               'animecast', 'animesummary',
                               'animetrailer'])
def ask_anime_title(message: Message) -> None:
    """Handles anime search by title

    Args:
        message (Message): Message
    """
    
    bot.send_message(message.chat.id, 
                     "???????????? ???????????????? ??????????(???? ????????????????????)")
    
    if message.text == "/animesearch":
        bot.register_next_step_handler(message, __check_language,
                                       __show_search_result, message.text)
    else:
        bot.register_next_step_handler(message, __check_language,
                                       __select_anime, message.text)

   
def __show_search_result(message: Message) -> None:
    """Handles showing search results

    Args:
        message (Message): Message
    """
    
    results = anime_search.search(message.text)
    text = ""
    
    for i in range(len(results[0])):
        text += f"<a href=\"{results[1][i]}\">{results[0][i]}</a>\n"
    
    with open("static/command_stickers/c_found.webp", "rb") as sticker:
        bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, "??????????!")
    sleep(0.5)
    bot.send_message(message.chat.id, "????????????????????...")
    sleep(1)
    bot.send_message(message.chat.id, "<b>???????????????????? ????????????</b>",
                    parse_mode="html")
    bot.send_message(message.chat.id, text, parse_mode="html")


def __select_anime(message: Message, command: str) -> None:
    """Handles anime selection from a list of found anime titles

    Args:
        message (Message): Message
        command (str): Anime command
    """
    
    title_url = anime_search.search(message.text)
    
    text = ""
    
    for i in range(len(title_url[0])):
        text += f"{i + 1}. {title_url[0][i]}\n"
    text += f"???????????????? ???????? ???? ??????????????????(1-{len(title_url[0])})"
    
    
    bot.send_message(message.chat.id, "<b>???????????????????? ????????????</b>",
                    parse_mode="html")
    bot.send_message(message.chat.id, text)
    
    if command == "/animeost":
        __thinking(message)
        sleep(1.5)
        bot.register_next_step_handler(message, __search_ost, title_url)
    if command == "/animecast":
        __thinking(message)
        sleep(1.5)
        bot.register_next_step_handler(message, __search_cast, title_url)
    if command == "/animesummary":
        __thinking(message)
        sleep(1.5)
        bot.register_next_step_handler(message, __search_summary, title_url)
    if command == "/animetrailer":
        bot.register_next_step_handler(message, __search_trailer, title_url)

   
def __search_ost(message: Message, titles_urls: list) -> None:
    """Handles anime soundtrack search

    Args:
        message (Message): Message
        titles_urls (list): List of found anime titles and their urls
    """
    
    url = titles_urls[1][int(message.text) - 1]
    soundtracks = anime_ost.search(url)
    
    text = ''
    
    for i in range(len(soundtracks)):
        text += f"{i + 1}. {soundtracks[i]}\n"
    
    bot.send_message(message.chat.id, 
                     f"<b>???????????????????? {titles_urls[0][int(message.text) - 1]}</b>",
                     parse_mode="html")
    bot.send_message(message.chat.id, text)
    
    __send_tired(message)     


def __search_cast(message: Message, titles_urls: list) -> None:
    """Handles anime cast search

    Args:
        message (Message): Message
        titles_urls (list): List of found anime titles and their urls
    """
    
    url = titles_urls[1][int(message.text) - 1]
    cast = anime_cast.search(url)
    
    text = ""
    
    for i in range(len(cast[0])):
        ch_name = cast[0][i][1]
        ch_url = cast[0][i][0]
        a_name = cast[1][i][1]
        a_url = cast[1][i][0]
        ch_sentence = f"<a href=\"{ch_url}\">{ch_name}</a>"
        a_sentence = f" - <a href=\"{a_url}\"><b>{a_name}</b></a>\n"
        text += ch_sentence + a_sentence

    bot.send_message(message.chat.id,
                     f"<b>???????????? {titles_urls[0][int(message.text) - 1]}</b>",
                     parse_mode="html")
    bot.send_message(message.chat.id, text, parse_mode="html")
    
    __send_tired(message)   


def __search_summary(message: Message, titles_urls: list) -> None:
    """Handles anime summary seach

    Args:
        message (Message): Message
        titles_urls (list): List of found anime titles and their urls
    """
    
    url = titles_urls[1][int(message.text) - 1]
    summary = anime_summary.search(url)
    
    bot.send_message(message.chat.id, "<b>????????????????</b>", parse_mode="html")
    bot.send_message(message.chat.id, summary)
    
    __send_tired(message)    


def __search_trailer(message: Message, titles_urls: list) -> None:
    """Handles searching anime trailer

    Args:
        message (Message): Selected anime
        titles_urls (list): Anime titles and their urls
    """
    
    url = titles_urls[1][int(message.text) - 1]
    anime_title = titles_urls[0][int(message.text) - 1]
    
    with open("static/command_stickers/c_search.webp", "rb") as sticker:
        bot.send_sticker(message.chat.id, sticker)
        
    bot.send_message(message.chat.id, "?????????????? ?????????? :3")
    
    trailer_url = anime_trailer.search(url)
    trailer_url = f"<a href=\"{trailer_url}\">{anime_title}</a>"
    
    sleep(1.5)
    with open("static/command_stickers/c_found.webp", "rb") as sticker:
        bot.send_sticker(message.chat.id, sticker)
        
    bot.send_message(message.chat.id, "??????????!")
    bot.send_message(message.chat.id, trailer_url, parse_mode="html",
                     disable_web_page_preview=False)  


#Sticker Functions
def __thinking(message: Message) -> None:
    """Sends thinking sticker

    Args:
        message (Message): Message
    """
    
    th_stickers = ["static/command_stickers/c_think_1.webp", 
                   "static/command_stickers/c_think_2.webp",
                   "static/command_stickers/c_think_3.webp"]
    
    th_text = ["??????...", "??????-???? ?? ??????????????...",
               "????????????????????...", "?? ??????????...??????...???????"]
    
    sticker_index = randint(0, len(th_stickers) - 1)
    text_index = randint(0, len(th_text) - 1)
    
    with open(choice(th_stickers), "rb") as sticker:
        bot.send_sticker(message.chat.id, sticker)
        bot.send_message(message.chat.id, th_text[text_index])


def __send_tired(message: Message) -> None:
    """Sends tired sticker

    Args:
        message (Message): Message
    """
    
    with open("static/command_stickers/c_tired.webp", "rb") as sticker:
        bot.send_message(message.chat.id, "????????????...")
        sleep(1.5)
        bot.send_sticker(message.chat.id, sticker)   


def __check_language(message: Message, func, command: str) -> None:
    """Checks the message language

    Args:
        message (Message): Message
    """
    
    if not message.text.isascii():
        with open("static/command_stickers/c_dunno.webp", "rb") as sticker:
            bot.send_sticker(message.chat.id, sticker)
            
        bot.send_message(message.chat.id, 
                         "?? ???????????? ???? ??????????????, ???? ???? ???????? ?????????? ?????????? ???? ????????!")
        bot.send_message(message.chat.id,
                         "???????????? ???????????????? ?????????? ???? ????????????????????!")
        bot.register_next_step_handler(message, __check_language, 
                                       func, command)
    else:
        if command == "/animesearch":
            func(message)
        else:
            func(message, command)


# ?????????????? ???????????? ???????????????? ??????????
@bot.message_handler(["animetop"])
def show_toptype_keyboard(message: Message) -> None:
    """Handles rating type keyboard
    Args:
        message (Message): Command
    """
    
    toptype_keyboard = __init_toptype_keyboard()

    with open("static/command_stickers/c_rating.webp", "rb") as sticker:
        bot.send_sticker(message.chat.id, sticker)
    
    bot.send_message(message.chat.id, "???????????? ??????????????", 
                     reply_markup=toptype_keyboard)

    
def __show_anime_ratings(message: Message, call_data: str) -> None:
    """Handles showing user the ratings

    Args:
        message (Message): Rating type
        call_data (str): Keyboard call data
    """
    
    rating_title = __toptype_message(call_data)
    bot.send_message(message.chat.id, rating_title, parse_mode="html")
    
    ratings_file = anime_ratings.show_ratings(call_data)
    
    with open(ratings_file, "r", encoding="utf-8") as file:
        bot.content = file.readlines()
        __page_message(message, bot.content, 0)


def __init_toptype_keyboard() -> InlineKeyboardMarkup:
    """Creates the keyboard for animetop command

    Returns:
        InlineKeyboardMarkup: Keyboard
    """
    
    toptype_keyboard = InlineKeyboardMarkup()

    alltime = InlineKeyboardButton(text="???? ?????? ??????????", 
                                   callback_data="alltime")
    popular = InlineKeyboardButton(text="?????????? ????????????????????",
                                   callback_data="popular")
    upcoming = InlineKeyboardButton(text="?????????? ??????????????????",
                                   callback_data="upcoming")
    favourite = InlineKeyboardButton(text="?????????? ??????????????",
                                     callback_data="favourite")
    airing = InlineKeyboardButton(text="???????????? ????????????",
                                  callback_data="airing")
    
    toptype_keyboard.add(alltime, popular, airing,
                          upcoming, favourite, row_width=2)
    
    return toptype_keyboard


def __toptype_message(call_data: str) -> str:
    """Handles rating type responses

    Args:
        call_data (str): Keyboard call data

    Returns:
        str: Rating headline
    """
    
    if call_data == "alltime":
        return "<b>???????????? ???? ?????? ??????????</b>"
    if call_data == "upcoming":
        return "<b>?????????? ??????????????????</b>"
    if call_data == "popular":
        return "<b>?????????? ????????????????????</b>"
    if call_data == "favourite":
        return "<b>?????????? ??????????????</b>"
    if call_data == "airing":
        return "<b>???????????? ????????????</b>"


#???????????????????? ??????????????????
def __page_message(message: Message, text: list, increment: int) -> None:
    """Handles page function for the message

    Args:
        message (Message): Paged message
        text (list): Message text
        increment (int): Page increment value
    """
    
    pages_keyboard = __init_pages_keyboard()
    
    page = __process_text(text, increment)
    
    bot.send_message(message.chat.id, page, reply_markup=pages_keyboard)


def __process_text(text: list, increment: int) -> str:
    """Handles message text processing

    Args:
        text (list): Message text
        increment (int): Page increment value

    Returns:
        str: Message text
    """
    
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
    """Handles pages' buttons

    Returns:
        InlineKeyboardMarkup: Keyboard
    """
    
    pages_keyboard = InlineKeyboardMarkup()
    
    first = InlineKeyboardButton(text="1", callback_data="first")
    prev = InlineKeyboardButton(text="<<", callback_data="previous")
    next = InlineKeyboardButton(text=">>", callback_data="next")
    last = InlineKeyboardButton(text="10", callback_data="last")
    
    pages_keyboard.add(first, prev, next, last, row_width=4)
    
    return pages_keyboard


@bot.message_handler(["watchlater"])
def watchlater(message: Message) -> None:
    """Handles watchlater command response

    Args:
        message (Message): Command
    """
    
    bot.send_message(message.chat.id, 
                     "?????????? ?????????? ???????????? ???????????????? ?? ???????????????????")
    
    bot.register_next_step_handler(message, add_to_watchlist)
    

def add_to_watchlist(message: Message) -> None:
    """Handles adding an entry to watchlist

    Args:
        message (Message): Anime title
    """
    
    anime_title = message.text
    
    watchlist.add_entry(anime_title)
    
    good_stickers = ["static/command_stickers/c_good_1.webp",
                     "static/command_stickers/c_good_2.webp"]
    
    with open(choice(good_stickers), "rb") as sticker:
        bot.send_sticker(message.chat.id, sticker)
        
    bot.send_message(message.chat.id, 
                     f"\"{anime_title}\" ???????????????? ?? ??????????????????!")


@bot.message_handler(["watchlist"])
def load_watchlist(message: Message) -> None:
    """Handles watchlist loading

    Args:
        message (Message): Command
    """
    
    anime_titles = watchlist.load_entry()
    
    with open("static/command_stickers/c_watchlist.webp", "rb") as sticker:
        bot.send_sticker(message.chat.id, sticker)
        bot.send_message(message.chat.id, "<b>?????? ???????? ???????????? ??????????????????</b>",
                         parse_mode="html")
    
    bot.send_message(message.chat.id, anime_titles)
    

@bot.message_handler(["pat"])
def pat_me(message: Message) -> None:
    """Handles pat command response

    Args:
        message (Message): Command
    """
    
    with open("static/command_stickers/c_pat.webp", "rb") as sticker:
        bot.send_sticker(message.chat.id, sticker)
        bot.send_message(message.chat.id, "UwU")
    
    sleep(1.5)
    
    love_stickers = ["static/command_stickers/c_love_1.webp",
                     "static/command_stickers/c_love_2.webp",
                     "static/command_stickers/c_love_3.webp",
                     "static/command_stickers/c_love_4.webp"]
    
    with open(choice(love_stickers), "rb") as sticker:
        bot.send_sticker(message.chat.id, sticker)
        bot.send_message(message.chat.id, "Here you go <3")


@bot.message_handler(["cheeks"])
def pull_cheeks(message: Message) -> None:
    """Handles cheeks command response

    Args:
        message (Message): Command
    """
    
    with open("static/command_stickers/c_cheeks.webp", "rb") as sticker:
        bot.send_sticker(message.chat.id, sticker)
        sleep(0.5)
        bot.send_message(message.chat.id, "Shtawp ish pweez... ??????")


# ?????????????? ???????? ??????????????????
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery) -> None:
    """Handles InlineKeyboardMarkup's calls

    Args:
        call (CallbackQuery): InlineKeyboardButton callback
    """
    
    bot.answer_callback_query(call.id)
    
    #???????????????????? ??????????????????????
    __greeting_query(call)
    
    #???????????????????? ??????????????
    __sticker_query(call)
    
    #???????????????????? ?????????? ????????????????
    __rating_query(call)

    #???????????????????? ??????????????
    __page_query(call)
    
    #???????????????????? ????????????
    __greeting_text_query(call)


def __greeting_query(call: CallbackQuery) -> None:
    """Handles greeting keyboard's calls

    Args:
        call (CallbackQuery): InlineKeyboardButton callback
    """
    
    if (call.data == "animation"):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
        
        with open("static/command_stickers/c_file.webp", "rb") as sticker:
            bot.send_sticker(call.message.chat.id, sticker)
        
        bot.send_message(call.message.chat.id, 
                            "?????????????? ?????? ???????????????? ?? .gif ?????????????? :3")
        bot.register_next_step_handler(call.message, __set_welcome_animation,
                                       call.data)
    if (call.data == "sticker"):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
        
        sticker_keyboard = __init_sticker_keyboard()
        
        bot.send_message(call.message.chat.id, "?????? ??????????????",
                         reply_markup=sticker_keyboard)
    if (call.data == "photo"):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
        
        with open("static/command_stickers/c_file.webp", "rb") as sticker:
            bot.send_sticker(call.message.chat.id, sticker)
        
        bot.send_message(call.message.chat.id, 
                        "?????????????? ?????? ???????? ?? .png ?????????????? :3")
        bot.register_next_step_handler(call.message, __set_welcome_photo,
                                       call.data)
    if (call.data == "text_only"):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
        
        with open("static/command_stickers/c_file.webp", "rb") as sticker:
            bot.send_sticker(call.message.chat.id, sticker)
        
        bot.send_message(call.message.chat.id, 
                        "?????????????? ?????? ?????????? ???????????????????? :3")
        bot.register_next_step_handler(call.message, __set_welcome_text,
                                       call.data)


def __sticker_query(call: CallbackQuery) -> None:
    """Handles sticker keyboard

    Args:
        call (CallbackQuery): Keyboard call
    """
    if call.data == "ordinary" or call.data == "animated":
        with open("static/command_stickers/c_file.webp", "rb") as sticker:
                bot.send_sticker(call.message.chat.id, sticker)
            
        bot.send_message(call.message.chat.id, "?????????????? ?????? ???????????? :3")
        bot.register_next_step_handler(call.message, __set_welcome_sticker,
                                    call.data)

      
def __page_query(call: CallbackQuery) -> None:
    """Handles page keyboard's calls

    Args:
        call (CallbackQuery): InlineKeyboardButton callback
    """
    
    if (call.data == "first"):
        bot.delete_message(call.message.chat.id, call.message.id)
        __page_message(call.message, bot.content, 0)
    if (call.data == "previous"):
        bot.delete_message(call.message.chat.id, call.message.id)
        __page_message(call.message, bot.content, -1)
    if (call.data == "next"):
        bot.delete_message(call.message.chat.id, call.message.id)
        __page_message(call.message, bot.content, 1)
    if (call.data == "last"):
        bot.delete_message(call.message.chat.id, call.message.id)
        __page_message(call.message, bot.content, 2)

       
def __rating_query(call: CallbackQuery) -> None:
    """Handles anime rating keyboard's calls

    Args:
        call (CallbackQuery): InlineKeyboardButton callback
    """
    
    if (call.data == "alltime"):
        with open("static/command_stickers/c_search.webp", "rb") as sticker:
            bot.send_sticker(call.message.chat.id, sticker)
        
        bot.send_message(call.message.chat.id, "?????????????? ????????????????????...")
        __show_anime_ratings(call.message, call.data)
        sleep(2)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
    if (call.data == "popular"):
        with open("static/command_stickers/c_search.webp", "rb") as sticker:
            bot.send_sticker(call.message.chat.id, sticker)
        
        bot.send_message(call.message.chat.id, "?????????????? ????????????????????...")
        __show_anime_ratings(call.message, call.data)
        sleep(2)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
    if (call.data == "airing"):
        with open("static/command_stickers/c_search.webp", "rb") as sticker:
            bot.send_sticker(call.message.chat.id, sticker)
        
        bot.send_message(call.message.chat.id, "?????????????? ????????????????????...")
        __show_anime_ratings(call.message, call.data)
        sleep(2)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
    if (call.data == "upcoming"):
        with open("static/command_stickers/c_search.webp", "rb") as sticker:
            bot.send_sticker(call.message.chat.id, sticker)
        
        bot.send_message(call.message.chat.id, "?????????????? ????????????????????...")
        __show_anime_ratings(call.message, call.data)
        sleep(2)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
    if (call.data == "favourite"):
        with open("static/command_stickers/c_search.webp", "rb") as sticker:
            bot.send_sticker(call.message.chat.id, sticker)
        
        bot.send_message(call.message.chat.id, "?????????????? ????????????????????...")
        sleep(2)
        __show_anime_ratings(call.message, call.data)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)


def __greeting_text_query(call: CallbackQuery) -> None:
    """Handles text keyboard's calls

    Args:
        call (CallbackQuery): InlineKeyboardButton callback
    """
    
    good_1 = "static/command_stickers/c_good_1.webp"
    good_2 = "static/command_stickers/c_good_2.webp"
    
    good_list = [good_1, good_2]
    
    if (call.data == "yes"):
        with open("static/command_stickers/c_text.webp", "rb") as sticker:
            bot.send_sticker(call.message.chat.id, sticker)
        bot.send_message(call.message.chat.id, "???????????? ?????????? ??????????????????????!")
        
        bot.register_next_step_handler(call.message, __set_welcome_text)
        
        sleep(2)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)
    if (call.data == "no"):
        with open(choice(good_list), "rb") as sticker:
            bot.send_sticker(call.message.chat.id, sticker)
            bot.send_message(call.message.chat.id, "???????????? :3")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id)


bot.polling(none_stop=True, interval=0)