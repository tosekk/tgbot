#Third Party Modules
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from requests import get


#URL
ranking_url = "https://myanimelist.net/topanime.php?{}limit={}"
search_url = "https://myanimelist.net/anime.php?q={}&cat=anime"

#File Format Variables
site_name = "myanimelist"


class MALRatings:
    """Handles rankings scraping from MyAnimeList
    """
    
    def show_ratings(self, rating_type: str) -> str:
        """Processes website and ranking table that is then sent to the bot

        Args:
            rating_type (str): Rating type: alltime, popular, etc.

        Returns:
            str: File path to the file with rankings listed
        """
        file_mode = "w"
        
        if rating_type == "alltime":
            _type = ""
        elif rating_type == "popular":
            _type = "type=bypopularity&"
        else:
            _type = f"type={rating_type}&"
        
        for page in [0, 50]:
            if page == 50:
                file_mode = "a"
            
            website = get(ranking_url.format(_type, page))
            soup = BeautifulSoup(website.text, "lxml")
            
            ranking_table = soup.select(".ranking-list")
            anime_rankings = self.__get_anime_ranking(ranking_table)
            anime_titles = self.__get_anime_title(ranking_table)
            anime_scores = self.__get_anime_scores(ranking_table)
            
            file_path = self.__write_rankings(rating_type, file_mode, 
                                              anime_rankings, anime_titles, 
                                              anime_scores)
        
        return file_path
    
    def __get_anime_ranking(self, ranking_table: ResultSet) -> list:
        """Handles gathering anime positions from ranking table

        Args:
            ranking_table (ResultSet): BeautifulSoup filtered tags

        Returns:
            list: Ranking index
        """
        rankings = []
        
        for element in ranking_table:
            if element.select("span[class*=top-anime-rank-text]"):
                anime_rank = element.select("span[class*=top-anime-rank-text]")[0].text
                rankings.append(anime_rank)
        
        return rankings     
    
    def __get_anime_title(self, ranking_table: ResultSet) -> list:
        """Handles gathering anime titles from ranking table

        Args:
            ranking_table (ResultSet): BeautifulSoup filtered tags

        Returns:
            list: Anime titles
        """
        titles = []
        
        for element in ranking_table:
            if element.select("h3 a"):
                anime_title = element.select("h3 a")[0].text
                titles.append(anime_title)
                
        return titles
    
    def __get_anime_scores(self, ranking_table: ResultSet) -> list:
        """Handles gathering anime scores from ranking table

        Args:
            ranking_table (ResultSet): BeautifulSoup filtered tags

        Returns:
            list: Anime scores
        """
        scores = []
        
        for element in ranking_table:
            if element.select("span[class*=score-label]"):
                anime_scores = element.select("span[class*=score-label]")[0].text
                scores.append(anime_scores)
                
        return scores
    
    def __write_rankings(self, rating_type: str, file_mode: str, 
                         anime_rankings: list, anime_titles: list, 
                         anime_scores: list) -> str:
        """Handles writing ranking table info to the file

        Args:
            rating_type (str): Rating type: alltime etc.
            file_mode (str): File mode "w" or "a"
            anime_rankings (list): Anime rankings
            anime_titles (list): Anime titles
            anime_scores (list): Anime scores

        Returns:
            str: Written file path
        """
        file_path = f"static/myanimelist_{rating_type}.txt"
        
        with open(file_path, 
                  file_mode, encoding="utf-8") as file:
            for line in range(len(anime_rankings)):
                file.write(
                    f"{anime_rankings[line]}. {anime_titles[line]}\nРейтинг: {anime_scores[line]}\n"
                    )
        
        return file_path
    
class MALSearch:
    """Handles anime search sequence on MyAnimeList
    """
    
    def search(self, anime_title: str) -> list:
        """Handles preprocessing search input and website tags

        Args:
            anime_title (str): Anime title

        Returns:
            list: Anime titles that satisfy the search input
        """
        anime_title = [word for word in anime_title.split()]
        title_in_url = "%20".join(anime_title)
                
        website = get(search_url.format(title_in_url))
        soup = BeautifulSoup(website.text, "lxml")
        
        results_text = self.__get_results_text(anime_title, soup)
        results_url = self.__get_results_url(anime_title, soup)
        
        return [results_text, results_url]

    def __get_results_text(self, words: list, soup: BeautifulSoup) -> list:
        """Handles filtering by title matching

        Args:
            words (list): Search input
            soup (BeautifulSoup): Website html

        Returns:
            list: Anime titles
        """
        site_results = soup.find_all("a", 
                                     class_="hoverinfo_trigger fw-b fl-l")
        results_text = []
        
        for result in site_results:
            result_text = result.text
            match = 0
            for word in words:
                if word.lower() in result_text.lower():
                    match += 1
            if match >= len(words):
                results_text.append(result_text)
        
        return results_text
    
    def __get_results_url(self, words: list, soup: BeautifulSoup) -> list:
        """Handles filtering by title matching

        Args:
            words (list): Search input
            soup (BeautifulSoup): Website html

        Returns:
            list: URLs
        """
        site_urls = soup.find_all(href=True)
        results_url = []
        
        for a in site_urls:
            match = 0
            for word in words:
                if word.lower() in a.text.lower():
                    match += 1
            if match >= len(words):
                results_url.append(a['href'])
        
        return results_url
    

class MALOst:
    
    def search(self, url: str) -> list:
        webpage = get(url)
        soup = BeautifulSoup(webpage.text, "lxml")
        
        st_title_tags = soup.find_all("span", class_="theme-song-title")
        st_artist_tags = soup.find_all("span", class_="theme-song-artist")
        
        soundtracks = []
        
        st_info = []
        
        st_info = self.__info_extraction(st_title_tags, st_artist_tags)
        
        
        for i in range(len(st_info[0])):
            soundtracks.append(st_info[0][i] + st_info[1][i])
        
        return soundtracks

    def __info_extraction(self, st_title_tags: ResultSet, 
                          st_artist_tags: ResultSet) -> list:
        st_titles = []
        st_artists = []
        
        for i in range(len(st_title_tags)):
            if (st_title_tags[i].text in st_titles)\
                or (st_artist_tags[i].text in st_artists):
                continue
            else:
                st_titles.append(st_title_tags[i].text)
                st_artists.append(st_artist_tags[i].text)
        
        return [st_titles, st_artists]
    

class MALCast:
    
    def search(self, url: str) -> list:
        webpage = get(url)
        soup = BeautifulSoup(webpage.text, "lxml")
        
        characters_tags = soup.find_all("h3", class_="h3_characters_voice_actors")
        actors_tags = soup.find_all("td", class_="va-t ar pl4 pr4")
        
        characters = []
        actors = []
        
        for i in range(len(characters_tags)):
            character = characters_tags[i].a.extract()
            actor = actors_tags[i].a.extract()
            characters.append([character['href'], character.text])
            actors.append([actor['href'], actor.text])
        
        return [characters, actors]
    

class MALSummary:
    
    def search(self, url: str) -> list:
        webpage = get(url)
        soup = BeautifulSoup(webpage.text, "lxml")
        
        summary_tags = soup.find_all("p", itemprop="description")
        
        return summary_tags[0].text