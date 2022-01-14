import requests
from bs4 import BeautifulSoup

from logger import logger
from helpers.links import links

WINDOWS_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4400.8 Safari/537.36'}


def parse_steamid(link):
    """Парсинг SteamID, steamID3, steamID64, name с STEAMID I/O (www.steamdid.io)

    Args:
        link

    Returns:
        result: ['76561198808376430', 'STEAM_0:0:424055351', '[U:1:848110702]', 'Toil']
    """
    if link:
        steamid = links['steamid']
        links_array = []
        value_array = []
        response = requests.get(steamid['url'] + link, headers = WINDOWS_AGENT)
        logger.debug(f'Выполняю парсинг страницы {steamid["url"]}{link} - Пользователь: SYSTEM.')
        soup = BeautifulSoup(response.content, 'lxml')

        all_links = soup.find('dl', {'class': steamid['find_links']}).findAll('a')
        all_value = soup.find('dl', {'class': steamid['find_links']}).findAll('dd', {'class': steamid['find_value']})

        steamid64_url_result = all_links[2].get('href')

        if steamid64_url_result.startswith('https://steamid.io/lookup/'):
            steamid64 = steamid64_url_result.split('/')
            steamid64 = steamid64[-1]
            links_array.append(steamid64)

        all_links.pop(2)

        for item in all_links:
            links_array.append(item.text)

        for item in all_value:
            value_array.append(item.text)

        links_array.append(value_array[6])
        result = [links_array[0], links_array[1], links_array[2], links_array[-1]]
        return result
    else:
        return None