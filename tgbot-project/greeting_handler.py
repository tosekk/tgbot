#Standard Modules
from datetime import datetime as dt
from requests import get
from time import sleep

#Third-Party Modules
from telebot import TeleBot
from telebot.types import Message


#Flag Variable
tf = [True, False]


class GreetingsHandler:
    """
        Handles command messages and operations that are performed
        on them.
    """

    #File Methods
    def file_handler(self, bot: TeleBot, message: Message, 
                     call_data: str, token: str) -> None:
        """Handles files sent by the user. Changes welcome images and text.

        Args:
            bot (TeleBot): Current running Telegram Bot
            message (Message): Message sent by the user
            token (str): Telegram Bot token string

        Returns:
            None
        """
        
        photos_path = f'https://api.telegram.org/file/bot{token}/'

        if call_data == "animation":
            file_info = bot.get_file(message.animation.file_id)
            file = get(photos_path + file_info.file_path, allow_redirects=True)
            with open("static/g_animation.gif", 'wb') as f:
                f.write(file.content)
            self.__g_file_prep(bot, message, "static/g_animation.gif", 0)

        if call_data == "ordinary":
            file_info = bot.get_file(message.sticker.file_id)
            file = get(photos_path + file_info.file_path, allow_redirects=True)
            with open("static/g_sticker.webp", 'wb') as f:
                f.write(file.content)
            self.__g_file_prep(bot, message, "static/g_sticker.webp", 1)
        
        if call_data == "animated":
            file_info = bot.get_file(message.sticker.file_id)
            file = get(photos_path + file_info.file_path, allow_redirects=True)
            with open("static/g_sticker_anim.tgs", 'wb') as f:
                f.write(file.content)
            self.__g_file_prep(bot, message, "static/g_sticker_anim.tgs", 2)
            
        if call_data == "photo":
            file_info = bot.get_file(message.photo.file_id)
            file = get(photos_path + file_info.file_path, allow_redirects=True)
            with open("static/g_photo.png", 'wb') as f:
                f.write(file.content)
            self.__g_file_prep(bot, message, "static/g_photo.png", 3)

    def __g_file_prep(self, bot: TeleBot, message: Message, 
                    g_file: str, f_type: int) -> None:
        """Handles greeting files sent by the user

        Args:
            message (Message): File sent by the user
            g_file (str): File path
            f_type (int): 0 - animation, 1 - sticker, 2 - photo
        """
        
        files = ['????????????????', '????????????', '?????????????????????????? ????????????', '????????']
        ending = ['??', '', '', '??']

        bot.send_message(message.chat.id, f"{files[f_type]} ??????????????????????...")
        sleep(3)
        bot.send_message(message.chat.id, 
                        f"{files[f_type]} ????????????????????{ending[f_type]}!")
        
        if f_type == 0:
            with open(g_file, 'rb') as file:
                bot.g_type = "animation"
                bot.send_animation(message.chat.id, file)
        if f_type == 1:
            with open(g_file, 'rb') as file:
                bot.g_type = "sticker"
                bot.send_sticker(message.chat.id, file)
        if f_type == 2:
            with open(g_file, 'rb') as file:
                bot.g_type = "animated sticker"
                bot.send_sticker(message.chat.id, file)
        if f_type == 3:
            with open(g_file, 'rb') as file:
                bot.g_type = "photo"
                bot.send_photo(message.chat.id, file)

    #Greeting Text Methods
    def reply_handler(self, command: str) -> str:
        """A command messages handler.

        Args:
            command (str): a command message text

        Returns:
            str: message composed from the lines of texts.txt
        """
        
        text = ''
        start = f"[{command[1:]}]\n"
        stop = f"[{command}]\n"

        with open("static/text/texts.txt", "r", encoding="utf-8") as replies:
            lines = replies.readlines()
            starting_line = lines.index(start) + 1
            stoping_line = lines.index(stop)
            for line in range(starting_line, stoping_line):
                if line == 1:
                    text += self.select_greeting(lines[line])
                else:
                    text += lines[line]

        return text

    def select_greeting(self, line: str) -> str:
        """Selects a greeting according to the current time.

        Args:
            line (str): line from the file

        Returns:
            str: Selected greeting
        """
        
        text = ''
        greet_number = self.__greeting_time()

        greetings = line.split("!")[:-1]
        text += greetings[greet_number] + '!\n'

        return text
   
    def change_greeting(self, bot: TeleBot, message_text: str,
                        call_data: str) -> None:
        """Handles changing greeting text

        Args:
            bot (TeleBot): TeleBot instance
            message_text (str): Message text
            call_data (str): Keyboard call data
        """
        
        text = message_text.split("\n")

        with open("static/text/texts.txt", "r", encoding="utf-8") as f:
            file_data = f.readlines()
            if call_data == "text_only":
                bot.g_type == call_data

        file_data = self.__greeting_prep(text, file_data)

        with open("static/text/texts.txt", "w", encoding="utf-8") as f:
            f.writelines(file_data)

    def __greeting_time(self) -> int:
        """Handles current time and hour calculations.

        Returns:
            int: Returns time index
        """
        
        current_time = dt.now()
        current_hour = current_time.hour

        if 6 <= current_hour < 12:
            selected = 0
        elif 12 <= current_hour < 21:
            selected = 1
        elif 21 <= current_hour or current_hour < 6:
            selected = 2
        
        return selected
    
    def __greeting_prep(self, text: str, file_data: list) -> list:
        """Handles greeting text file and message text preparation.

        Args:
            text (str): Message text sent by the user
            file_data (list): Text file that contains the response to /start command

        Returns:
            list: Lines to be written into the file
        """
        
        start = "[start]\n??????????!??????????????????!????????????????!\n"
        stop = "[/start]\n"

        stop_line = file_data.index(stop) + 1
        help_section = file_data[stop_line:]
        file_data = []

        if len(text) == 1:
            to_add = [start, text[0] +"\n", stop]
            file_data.extend(to_add)
        else:
            for index in range(len(text)):
                file_data.append(text[index] + "\n")

                if index == 0:
                    file_data.insert(0, start)
                elif index == len(text) - 1:
                    file_data.append(stop)

        file_data.extend(help_section)

        return file_data