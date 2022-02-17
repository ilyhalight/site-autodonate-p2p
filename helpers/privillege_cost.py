import json
import traceback
from logger import logger


try:
    with open('./data/privillege_cost.json', 'r') as privillege_cost:
        privillege_cost = json.load(privillege_cost)

except FileNotFoundError:
    logger.error(f'Не удалось загрузить privillege_cost.json')
    logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')

