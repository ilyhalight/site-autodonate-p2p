import requests
import os
from logger import logger
from datetime import datetime, timedelta

def check_status_payment(api_secret_token, uuid):
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + api_secret_token
    s.headers['accept'] = 'application/json'
    h = s.get('https://api.qiwi.com/partner/bill/v1/bills/' + uuid)
    return h.json()

def generate_payment(api_secret_token, uuid, sum):
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + api_secret_token
    s.headers['content-type'] = 'application/json'
    s.headers['accept'] = 'application/json'
    current_datetime = datetime.now() + timedelta(days=1)
    parameters = {
        "amount": {
            "currency": "RUB",
            "value": float(f'{sum}.00')
        },
        'comment': uuid,
        'expirationDateTime': current_datetime.strftime('%Y-%m-%dT%H:%M:%S.201+03:00')
    }
    h = s.put('https://api.qiwi.com/partner/bill/v1/bills/' + uuid, json = parameters)
    return h.json()

def create_payment(uuid, amount):
    # Создаёт форму платежа
    # uuid
    # amount
    generate_result = generate_payment(os.environ.get('SECRET_KEY'), f'{uuid}', amount)
    if type(generate_result) is dict:
        logger.info(f'Сгенерированная ссылка: {generate_result["payUrl"]}')
        return True, generate_result['payUrl'], generate_result['comment']
    else:
        return False

def check_payment(uuid):
    # Проверяет форму платежа
    # uuid
    check_result = check_status_payment(os.environ.get('SECRET_KEY'), f'{uuid}')
    if type(check_result) is dict:
        try:
            logger.info(f'Проверяем зачисление с uid: {check_result["comment"]} | Статус: {check_result["status"]["value"]}')
            return True, check_result['status']['value'], check_result['comment'], check_result['amount']['value']
        except:
            return False
    else:
        return False