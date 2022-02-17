import requests

def get_auth_uri(client_id):
    s = requests.Session()
    s.headers['content-type'] = 'application/x-www-form-urlencoded'
    parameters = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": "https://fame-community.ru",
        "scope": "account-info operation-history operation-details incoming-transfers payment-p2p payment-shop"
    }

    h = s.post(f'https://yoomoney.ru/oauth/authorize', data = parameters)
    if h.status_code == 200:
        print(h.url)


def get_access_token(temp_code, client_id, client_secret):
    s = requests.Session()
    s.headers['content-type'] = 'application/x-www-form-urlencoded'
    parameters = {
        "code": temp_code,
        "client_id": client_id,
        "grant_type": "authorization_code",
        "redirect_uri": "https://fame-community.ru",
        "client_secret": client_secret
    }

    h = s.post(f'https://yoomoney.ru/oauth/token', data = parameters)
    print(h.content)

get_auth_uri("ВАШ КЛИЕНТ ID")
temp_code = str(input('Code с полученного url (необходимо авторизоваться по ссылке): '))
get_access_token(temp_code, "ВАШ КЛИЕНТ ID", "ВАШ КЛИЕНТ СЕКРЕТ, ЕСЛИ ОН ЕСТЬ,ЕСЛИ НЕТУ УБЕРИТЕ ЕГО ОТСЮДА И ИЗ ЗАПРОСА")