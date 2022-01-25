#Standard Modules
from datetime import datetime as dt


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