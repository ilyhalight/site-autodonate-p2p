import time

from logger import logger
from helpers.steamid import parse_steamid
from helpers.database import open_csgo_db_connection

time_rotation = {
    's': '1',
    'm': '60',
    'h': '3600',
    'd': '86400',
    'w': '604800'
}


def get_data_from_db(steamid):
    """Получение данных из базы данных CS:GO

    Args:
        steamid: steamid3

    Returns:
        result: (848110702, 'Toil', 1639503546, 0, 'ADMIN', 0) - Success
        result: False - Fail
    """
    try:
        logger.debug('Пытаюсь подключиться к БД - Пользователь: SYSTEM.')
        db = open_csgo_db_connection() # Открываем соединение с БД
        logger.debug('Подключение к БД установлено - Пользователь: SYSTEM.')
        cursor = db.cursor() # Создаем курсор управления БД
        logger.debug('Курсор управления БД создан - Пользователь: SYSTEM.')

        logger.debug('Пытаюсь отправить SQL запрос на получение данных из БД - Пользователь: SYSTEM.')
        cursor.execute(f'SELECT * FROM vip_users WHERE account_id={steamid}') # Отправляем SQL запрос
        logger.debug('Данные из БД были получены - Пользователь: SYSTEM.')
        result = cursor.fetchone() # Получаем первую строку из полученного кортежа
        logger.debug('Получена первая строка из полученного кортежа - Пользователь: SYSTEM.')

        cursor.close()
        logger.debug('Доступ к курсору был закрыт - Пользователь: SYSTEM.')
        db.close()
        logger.debug('Подключение к БД было закрыто - Пользователь: SYSTEM.')
        return result
    except Exception as err:
        logger.error(err)
        return False

def transfer_data_to_db(steamid, username, lastvisit, privillege, expiries):
    """Передача данных в базу данных CS:GO

    Args:
        steamid (int): steamid3 без [], :
        username (str): Имя игрока
        lastvisit (int): Последний вход на сервер (можно указать любую дату, главное в unix формате)
        privillege (str): Название привилегии, как записано в groups.ini
        expiries (int): Дата истечения привилегии (unix формат)

    Returns:
        result: True - Успех
        result: None - Неудача
    """
    try:
        logger.debug('Пытаюсь подключиться к БД - Пользователь: SYSTEM.')
        db = open_csgo_db_connection() # Открываем соединение с БД
        logger.debug('Подключение к БД установлено - Пользователь: SYSTEM.')
        cursor = db.cursor() # Создаем курсор управления БД
        logger.debug('Курсор управления БД создан - Пользователь: SYSTEM.')

        logger.debug('Пытаюсь отправить SQL запрос на отправку данных в БД - Пользователь: SYSTEM.')
        sql = ('INSERT INTO `vip_users` (`account_id`, `name`, `lastvisit`, `sid`, `group`, `expires`) VALUES (%s, %s, %s, %s, %s, %s)') 
        data = (int(steamid), username, int(lastvisit), 0, privillege, int(expiries))
        cursor.execute(sql, data) # Отправляем SQL запрос
        logger.debug('Данные были получены БД - Пользователь: SYSTEM.')
        db.commit() # Сохраняем изменения в базе данных
        logger.debug('Изменения были сохранены в БД - Пользователь: SYSTEM.')

        cursor.close()
        logger.debug('Доступ к курсору был закрыт - Пользователь: SYSTEM.')
        db.close()
        logger.debug('Подключение к БД было закрыто - Пользователь: SYSTEM.')
        return True
    except Exception as err:
        logger.error(err)
        return None
    
def csgo_give_privillege(steam_link: str, privillege: str, expiries: str):
    """Выдача привилегии на сервере CS:GO

    Args:
        steamlink (str): Ссылка на профиль в стиме
        privillege (str): Название привилегии, как записано в groups.ini
        expiries (str): На какое время выдавать, не ставьте слишком огромное количество (желательно не более 9999 дней)

    Returns:
        True
    """
    try:
        parser = parse_steamid(steam_link) # Парсим steamID
    except Exception as err:
        parser = None
        logger.error('Произошла ошибка при парсинге. Возможно вы ввели несуществующий профиль')
        logger.error(err)
    logger.debug(f'Информация из парсера steamid: {parser}')
    if isinstance(parser, list):
        if parser[2].startswith('[U:1:'):
            steamid3_1 = parser[2].split('[U:1:')
            steamid3_2 = steamid3_1[1].split(']')
            steamid3 = steamid3_2[0]

        # Преобразуем время в unix
        alternative_time = ''

        for s in expiries:
            if s.lower() in time_rotation:
                intermediate_time = time_rotation[s.lower()]
            else:
                alternative_time += f'{s}'

        if int(alternative_time) <= 0:
            alternative_time = 1

        final_time = int(alternative_time) * int(intermediate_time)
        timestamp = int(time.time())
        result_timestamp = int(timestamp) + int(final_time)
        data_from_db = get_data_from_db(steamid3)

        if type(data_from_db) is not tuple and data_from_db is not False:
            transfer_result = transfer_data_to_db(steamid3, parser[-1], timestamp, privillege, result_timestamp)
            if transfer_result is True:
                logger.info(f'Выдана привилегия {privillege} (Срок: {expiries}) на сервере CS:GO игроку {parser[-1]} ("https://steamcommunity.com/id/{parser[0]}")')
                return True
            else:
                logger.error(f'Не удалось отправить/сохранить данные о новой привилегии игрока на сервере CS:GO в БД')

        elif type(data_from_db) is tuple and data_from_db[0] == int(steamid3):
            if int(data_from_db[5]) > int(timestamp):
                logger.info(f'У игрока {parser[-1]} ("https://steamcommunity.com/id/{parser[0]}") уже есть привилегия {data_from_db[4]} (Срок: {data_from_db[5]}) на сервере CS:GO')
            else:
                transfer_result = transfer_data_to_db(steamid3, parser[-1], timestamp, privillege, result_timestamp)
                if transfer_result is True:
                    logger.info(f'Выдана привилегия {privillege} (Срок: {expiries}) на сервере CS:GO игроку {parser[-1]} ("https://steamcommunity.com/id/{parser[0]}")')
                    return True
                else:
                    logger.error(f'Не удалось отправить/сохранить данные о новой привилегии игрока на сервере CS:GO в БД')

        elif data_from_db is False:
            logger.error(f'Не удалось получить данные из БД')

        else:
            logger.error(f'Произошла неизвестная ошибка')
    else:
        logger.error(f'Не удалось получить подлинные данные о стиме игрока')
