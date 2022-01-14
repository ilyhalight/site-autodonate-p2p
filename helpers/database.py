import os
import traceback
import mysql.connector
from mysql.connector import errorcode

from logger import logger
from helpers.env import get_env


get_env()

_csgo_config = {
    'user': os.environ.get('DB_CSGO_USER'),
    'password': os.environ.get('DB_CSGO_PASSWORD'),
    'host': os.environ.get('DB_CSGO_HOST'),
    'database': os.environ.get('DB_CSGO_NAME'),
    'auth_plugin': 'mysql_native_password'
}

if mysql.connector.__version_info__ > (2, 1) and mysql.connector.HAVE_CEXT:
    _csgo_config['use_pure'] = False

def open_csgo_db_connection():
    try:
        db = mysql.connector.connect(**_csgo_config)
        return db
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger.error('Неверное имя пользователя или пароль от БД')
            logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger.error('База данных не существует')
            logger.debug(f'Причина ошибки:\n{traceback.format_exc()}')
        else:
            print(err)