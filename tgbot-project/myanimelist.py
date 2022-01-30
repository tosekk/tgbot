#Third Party Modules
from email.message import Message
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from requests import get


#URL
ranking_url = "https://myanimelist.net/topanime.php?{}limit={}"
search_url = "https://myanimelist.net/anime.php?q={}&cat=anime"

#File Format Variables
site_name = "myanimelist"


class MALRatings:
    
    def show_ratings(self, rating_type: str) -> str:
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
        rankings = []
        
        for element in ranking_table:
            if element.select("span[class*=top-anime-rank-text]"):
                anime_rank = element.select("span[class*=top-anime-rank-text]")[0].text
                rankings.append(anime_rank)
        
        return rankings     
    
    def __get_anime_title(self, ranking_table: ResultSet) -> list:
        titles = []
        
        for element in ranking_table:
            if element.select("h3 a"):
                anime_title = element.select("h3 a")[0].text
                titles.append(anime_title)
                
        return titles
    
    def __get_anime_scores(self, ranking_table: ResultSet) -> list:
        scores = []
        
        for element in ranking_table:
            if element.select("span[class*=score-label]"):
                anime_scores = element.select("span[class*=score-label]")[0].text
                scores.append(anime_scores)
                
        return scores
    
    def __write_rankings(self, rating_type: str, file_mode: str, 
                         anime_rankings: list, anime_titles: list, 
                         anime_scores: list) -> str:
        file_path = f"static/myanimelist_{rating_type}.txt"
        
        with open(file_path, 
                  file_mode, encoding="utf-8") as file:
            for line in range(len(anime_rankings)):
                file.write(f"{anime_rankings[line]}. {anime_titles[line]}\nРейтинг: {anime_scores[line]}\n")
        
        return file_path
    
class MALSearch:
    
    def search(self, anime_title: str) -> list:
        anime_title = [word for word in anime_title.split()]
        words = anime_title[:]
        title_in_url = "%20".join(anime_title)
                
        website = get(search_url.format(title_in_url))
        soup = BeautifulSoup(website.text, "lxml")
        
        results = self.__get_results(words, soup)
        
        return results

    def __get_results(self, words: list, soup: BeautifulSoup) -> list:
        site_results = soup.select(".title")
        results = []
        
        for result in site_results:
            result_text = result.select("a")[0].text
            match = 0
            
            if result.select("a"):
                for word in words:
                    if word.lower() in result_text.lower():
                        match += 1
                if match >= len(words):
                    results.append(result_text)
        return results