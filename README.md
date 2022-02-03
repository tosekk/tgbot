# Anime Super Bot
Not that simple telegram bot written in Python that gathers info about anime rankings and requested anime info.

## Table of Contents
[Project info](#project-info)__
[Technologies](#technologies)__
[Features](#features)__
[Available commands](#available-commands)__

## Project info
This project is built using Python 3.9.7. The main framework used was [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) as well as [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for some web scraping functions. This project's purpose is to teach my students(at the academy that I work at) Python and how to create a Telegram bot using it. All information related to anime is gathered from [MyAnimeList](https://myanimelist.net/)

## Technologies
1. Python 3.9.7__
2. [pyTelegramBotAPI 4.3.1](https://github.com/eternnoir/pyTelegramBotAPI)__
3. [BeautifulSoup4 4.10.0](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)__

## Features
- .PNG, .GIF, .WEBP, .TGS support__
- Welcome message customization__
- Top 100 Anime by categories__
- Anime OST, Synopsis, Trailer, Cast info__

#### Available commands
**COMMANDS**                **DESCRIPTION**__
**/start**                  Starts the bot. Sends the welcome message__
**/help**                   Shows the list of commands and their description__
**/welcomeconfig**          Lets user change welcome message type and text message: Photo + text, Sticker + text, Animiation + text, Only text__
**/animetop**               Top 100 Anime by categories: Alltime, Airing, Upcoming, Popular, Favourite__
**/animesearch**            Searches by anime title and sends a message with links__
**/animeost**               Searches by anime title and presents a list of anime OSTs__
**/animecast**              Searches by anime title and presents a list of anime cast with links to anime characters and voice actors__
**/animesummary**           Searches by anime title and presents the anime synopsis__
**/animetrailer**           Searches by anime title and presents a link to the video__
