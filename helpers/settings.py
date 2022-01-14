import json
import sys
import traceback
from loguru import logger


try:
    with open('./data/settings.json', 'r') as settings:
        settings = json.load(settings)
except FileNotFoundError:
    logger.error(f'Не удалось загрузить settings.json - Пользователь: SYSTEM.')
    logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')
    sys.exit(3)

