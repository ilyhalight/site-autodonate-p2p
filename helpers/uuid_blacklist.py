import json
import traceback
from logger import logger


try:
    with open('./data/uuid_blacklist.json', 'r') as uuid_blacklist:
        uuid_blacklist = json.load(uuid_blacklist)

except FileNotFoundError:
    logger.error(f'Не удалось загрузить uuid_blacklist.json')
    logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')

def update_uuid_blacklist(data):
    with open('./data/uuid_blacklist.json', 'w') as uuid_blacklist:
        uuid_blacklist.write(json.dumps(data, indent=4))


