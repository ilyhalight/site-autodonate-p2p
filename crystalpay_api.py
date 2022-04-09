import os
import requests
from helpers.env import get_env
from logger import logger
import uuid

def generate_payment(secret: str, uuid: str, sum: int):
    """Создание платежа с указанием секретного кода

    Args:
        secret (str): Секретный код 1
        uuid (str): Уникальный uuid
        sum (int): Сумма платежа

    Returns:
        (
            True,
            {
                'id': '715294321_JEjPXPKdJX',
                'url': 'https://pay.crystalpay.ru/?i=715294321_JEjPXPKdJX',
                'error': False,
                'auth': 'ok'
            }
        )
    """

    s = requests.Session()
    s.headers['content-type'] = 'application/json'
    parameters = {
        'o': 'receipt-create',
        'n': 'toil',
        's': secret,
        'amount': sum,
        'lifetime': 1440,
        'extra': uuid
    }

    h = s.get('https://api.crystalpay.ru/v1/', params = parameters)
    print(type(h.json()))
    if h.json()['auth'] == 'ok':
        logger.success('Авторизация пройдена')
        if h.json()['error'] is False:
            logger.success('Платёж был создан')
            return h.json()
        else:
            logger.warning(h.json()['error'])
            return 'Не удалось создать платёж'
    else:
        return 'Не авторизован'

def create_payment(uuid: str, amount: int):
    # Создаёт форму платежа
    # uuid
    # amount
    generate_result = generate_payment(os.environ.get('CRYSTALPAY_SECRET_1'), uuid, amount)
    if generate_result is not None or type(generate_result) is not str:
        logger.info(f'Сгенерированная ссылка: {generate_result}')
        return True, generate_result['url'], generate_result['id']
    else:
        return False, generate_result


def check_status_payment(secret: str, pid: str):
    """Проверка платежа по айди с указанием секретного кода

    Args:
        secret (str): Секретный код 1
        pid (str): Уникальный id оплаты

    Returns:
    """
    s = requests.Session()
    s.headers['content-type'] = 'application/json'
    parameters = {
        'o': 'receipt-check',
        'n': 'toil',
        's': secret,
        'i': pid
    }

    h = s.get('https://api.crystalpay.ru/v1/', params = parameters)
    if h.json()['auth'] == 'ok':
        logger.success('Авторизация пройдена')
        if h.json()['error'] is False:
            logger.success('Платёж был найден')
            logger.info('')
            return h.json()
        else:
            logger.warning(h.json()['error'])
            return 'Не удалось найти платёж'
    else:
        return 'Не авторизован'

def check_payment(uuid: str, pid: str):
    # Создаёт форму платежа
    # uuid
    # pid (payment id)

    # (True, 'notpayed', '421e65eb-4c69-49d8-91fc-1f89200cd53d', 350)
    # (True, 'processing', '421e65eb-4c69-49d8-91fc-1f89200cd53d', 350)
    # (True, 'payed', '421e65eb-4c69-49d8-91fc-1f89200cd53d', 350)
    check_result = check_status_payment(os.environ.get('CRYSTALPAY_SECRET_1'), pid)
    if type(check_result) is dict:
        if check_result['extra'] == uuid:
            logger.info('Операция найдена!')
            return True, check_result['state'], check_result['extra'], check_result['payamount']
        return False
    else:
        return False


if __name__ == '__main__':
    get_env()
    uuidp = str(uuid.uuid4())
    payment = create_payment(uuidp, 350)
    print(payment)
    result = check_payment(uuidp, payment[1]['id'])
    print(result)