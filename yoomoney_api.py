import os
import requests
from helpers.privillege_cost import privillege_cost
from logger import logger
from helpers.env import get_env


def operation_history_details(api_secret_token):
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + api_secret_token
    s.headers['content-type'] = 'application/x-www-form-urlencoded'

    data = {
        "records": 30,
        "details": 'true',
        "type": "deposition",
        "label": "fame_donate"
    }

    h = s.post('https://yoomoney.ru/api/operation-history', data = data)
    return h.json()

def operation_details(api_secret_token, operation_id):
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + api_secret_token
    s.headers['content-type'] = 'application/x-www-form-urlencoded'

    data = {
        "operation_id": operation_id,
    }

    h = s.post('https://yoomoney.ru/api/operation-details', data = data)
    return h.json()

def generate_payment_form(payment_type: str, uuid: str, sum: int):
    """Создание формы оплаты

    Args:
        api_secret_token (str): Секретный токен YooMoney
        payment_type (str): Выберите один из вариантов - PC (Из кошелька), AC (С банковской карты), MC (С баланса мобильного)
        uuid (str): Сгенерированный uuid4
        sum (int): Цена

    Returns:
        h.url: Ссылка на оплату
    """
    s = requests.Session()
    s.headers['content-type'] = 'application/x-www-form-urlencoded'

    payment_sum = 0
    amount_due = 0
    privillege_cost_array = []

    for item in privillege_cost['30days']:
        privillege_cost_array.append(item)
    for item in privillege_cost['permanent']:
        privillege_cost_array.append(item)

    while True:
        if str(f'{round(payment_sum - amount_due, 2)}0') not in privillege_cost_array:
            if payment_type == 'PC':
                a = 0.005
                final_coefficient = round(a / (1 + a), 6) # 0.004975
                amount_due = round(sum * final_coefficient, 2)

            else:
                a = 0.02
                amount_due = round(sum - sum * (1 - a), 2)

            payment_sum = round(sum + amount_due, 2)
            logger.info(str(f'{round(payment_sum - amount_due, 2)}0'))
        else:
            break

    parameters = {
        "receiver": "410018063704641",
        "quickpay-form": "shop",
        "targets": "Поддержка Fame",
        "paymentType": payment_type,
        "sum": payment_sum,
        "formcomment": "Поддержка Fame",
        "short-dest": "Поддержка Fame",
        "comment": uuid,
        "label": "fame_donate"
    }

    h = s.post('https://yoomoney.ru/quickpay/confirm.xml', params = parameters)
    return h.url

def create_payment(payment_type: str, uuid: str, amount: int):
    # Создаёт форму платежа
    # payment_type
    # uuid
    # amount
    generate_result = generate_payment_form(payment_type, uuid, amount)
    if generate_result is not None:
        logger.info(f'Сгенерированная ссылка: {generate_result}')
        return True, generate_result
    else:
        return False, generate_result

def find_donate(uuid: str):
    history_result = operation_history_details(os.environ.get('YOOMONEY_ACCESS_TOKEN'))
    for operations in history_result['operations']:
        if operations['details'] == uuid or operations['details'] == f'Поддержка Fame;\n{uuid}' or operations['details'].startswith(uuid) or operations['details'].split(' ')[5][:-9].replace('№', '') == uuid:
            logger.info('Операция найдена!')
            return True, operations['status'], operations['details'], operations['amount']
        else:
            logger.debug(operations['details'])
            logger.debug(operations['details'].split(' '))
            logger.debug(operations['details'].split(' ')[5][:-9].replace('№', ''))

if __name__ == '__main__':
    get_env()
    history_result = operation_history_details(os.environ.get('YOOMONEY_ACCESS_TOKEN'))
    print(history_result)