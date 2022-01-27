#Third Party Modules
from bs4 import BeautifulSoup
from requests import get

file_path = "tgbot-project/static/anime_rating.txt"

def get_rating():
    table = get("http://www.world-art.ru/animation/rating_top.php")
    soup = BeautifulSoup(table.text, "lxml")

    anime_rating = soup.select(".review")
    anime_titles = __get_anime_title(anime_rating)
    #anime_scores = __get_anime_score(anime_rating)

    with open(file_path, "w", encoding="utf-8") as file:
        for index, value in enumerate(anime_titles):
            file.write(f"{index + 1}. {value}\n")

    return file_path
        

def __get_anime_title(anime_rating) -> list:
    titles = []

    for item in anime_rating:
        if item.select("a"):
            anime_title = item.select("a")[0].text
            titles.append(anime_title)
    
    return titles
            
def __get_anime_score(anime_rating) -> list:
    scores = []

    for item in anime_rating:
        if item.select("td .review"):
            anime_score = item.select("td .review")[1].text
            scores.append(anime_score)
    
    return scores

get_rating()