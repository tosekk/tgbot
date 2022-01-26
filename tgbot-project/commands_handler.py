#Standard Modules
from datetime import datetime as dt
from requests import get
from time import sleep

#Third-Party Modules
from telebot import TeleBot
from telebot.types import Message


class CommandsHandler():
    """
        Handles command messages and operations that are performed
        on them.
    """
    def select_greeting(self, line: str) -> str:
        """Selects a greeting according to the time by UTC.

        Args:
            line (str): line from the file

        Returns:
            str: message composed from the lines
        """
        text = ''
        greet_number = self.__greeting_time()

        greetings = line.split("!")[:-1]
        text += greetings[greet_number] + '!\n'

        return text

    def reply_handler(self, command: str) -> str:
        """A command messages handler

        Args:
            command (str): a command message text

        Returns:
            str: message composed from the lines of texts.txt
        """
        text = ''
        start = f"[{command[1:]}]"
        stop = f"[{command}]"
        to_return = False

        with open('texts.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith('['):
                    if start in line:
                        to_return = True
                        continue
                    elif stop in line:
                        to_return = False
                        break
                else:
                    if "Охайо" in line and to_return:
                        text += self.select_greeting(line)
                    elif to_return:
                        text += line
        return text

    def file_handler(self, bot: TeleBot, message: Message, token: str) -> str:
        photos_path = f'https://api.telegram.org/file/bot{token}/'

        if message.animation:
            file_info = bot.get_file(message.sticker.file_id)
            file = get(photos_path + file_info.file_path, allow_redirects=True)
            with open(bot.g_animation, 'wb') as f:
                f.write(file.content)
            self.__file_prep(bot, message, bot.g_animation, 0)

        if message.sticker:
            file_info = bot.get_file(message.sticker.file_id)
            file = get(photos_path + file_info.file_path, allow_redirects=True)
            with open(bot.g_sticker, 'wb') as f:
                f.write(file.content)
            self.__file_prep(bot, message, bot.g_sticker, 1)
            
        if message.photo:
            file_info = bot.get_file(message.sticker.file_id)
            file = get(photos_path + file_info.file_path, allow_redirects=True)
            with open(bot.g_photo, 'wb') as f:
                f.write(file.content)
            self.__file_prep(bot, message, bot.g_photo, 2)

    #Private Methods
    def __greeting_time(self):
        current_time = dt.now()
        current_hour = current_time.hour

        if 6 < current_hour < 12:
            selected = 0
        elif 12 < current_hour < 21:
            selected = 1
        elif 21 < current_hour or current_hour < 6:
            selected = 2
        
        return selected
    
    def __file_prep(self, bot: TeleBot, message: Message, g_file: str, f_type: int) -> None:
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
        
        if f_type == 0:
            with open(g_file, 'rb') as file:
                bot.isAnimation = True
                bot.isSticker = False
                bot.isPhoto = False
                bot.isTextOnly = False
                bot.send_animation(message.chat.id, file)
        if f_type == 1:
            with open(g_file, 'rb') as file:
                bot.isSticker = True
                bot.isAnimation = False
                bot.isPhoto = False
                bot.isTextOnly = False
                bot.send_sticker(message.chat.id, file)
        if f_type == 1:
            with open(g_file, 'rb') as file:
                bot.isPhoto = True
                bot.isSticker = False
                bot.isAnimation = False
                bot.isTextOnly = False
                bot.send_photo(message.chat.id, file)