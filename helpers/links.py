import json
import traceback
from logger import logger


try:
    with open('./data/links.json', 'r') as links:
        links = json.load(links)

except FileNotFoundError:
    logger.error(f'Не удалось загрузить links.json')
    logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')

