class Watchlist:
    """Handles watchlist operations
    """
    def load_entry(self) -> str:
        """Handles watchlist loading

        Returns:
            str: Watchlist entries
        """
        
        entries = ''
        
        cmd_start = "[watchlist]\n"
        cmd_stop = "[/watchlist]\n"
        
        with open("static/text/texts.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            start = lines.index(cmd_start) + 1
            stop = lines.index(cmd_stop)
            
            for line in range(start, stop):
                entries += lines[line]
                
        return entries
    
    def add_entry(self, entry: str) -> None:
        """Handles adding entries to watchlist

        Args:
            entry (str): New entry
        """
        
        curr_entries = self.load_entry()
        curr_entries = curr_entries.split("/n")
        
        for index in range(len(curr_entries)):
            if index == len(curr_entries) - 1:
                curr_entries.append(f"{len(curr_entries) + 1}. {entry}\n")
            else:
                curr_entries[index] += "\n"
        
        cmd_start = "[watchlist]\n"
        cmd_stop = "[/watchlist]\n"
        
        with open("static/text/texts.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            start = lines.index(cmd_start)
            
            prev_section = lines[:start]
            
        file_data = prev_section
        file_data.append(cmd_start)
        file_data.extend(curr_entries)
        file_data.append(cmd_stop)
        
        with open("static/text/texts.txt", "w", encoding="utf-8") as file:
            file.writelines(file_data)