import asyncio
from uuid import uuid4
import os
from flask import Flask, render_template, request, redirect
from give_privillege import csgo_give_privillege
from qiwi_api import create_payment, check_payment
from helpers.env import get_env
from helpers.privillege_cost import privillege_cost
from logger import logger
from helpers.uuid_blacklist import uuid_blacklist, update_uuid_blacklist
import yoomoney_api
from crystalpay_api import create_payment as crystalpay_create_payment, check_payment as crystalpay_check_payment
from helpers.settings import settings


privillege_array_30d = privillege_cost['30days']
privillege_array_permanent = privillege_cost['permanent']
privillege_array_discord = privillege_cost['discord_privillege']

app = Flask(__name__)

def send_tg_alert(text: str):
    if settings['telegram_logs']:
        try:
            from tg.main import telegram_alert
            asyncio.run(telegram_alert(text))
        except:
            logger.warning('Не удалось отправить уведомление в телеграм!')

def autodonate_give_privillege(uuid, amount, steam):
    logger.info(f'Полученная сумма доната - {amount}')
    amount_2 = None
    if type(amount) is float or type(amount) is int:
        amount_2 = amount + 1
        amount_2 = str(amount_2)
        amount_2 = amount_2.split('.')
        amount_2 = amount_2[0]
        amount_2 = f'{amount_2}.00'
    amount = str(amount)
    amount = amount.split('.')
    amount = amount[0]
    amount = f'{amount}.00'
    logger.debug('Проверка статуса платежа | Оплачено')
    if uuid in uuid_blacklist:
        return redirect(f"/autodonate/result?redirect=110100011000011100011110101111001011110010", code = 302)
    else:
        uuid_blacklist.append(uuid)
        update_uuid_blacklist(uuid_blacklist)
        logger.debug(f'{uuid} был использован и добавлен в ЧС')
        try:
            if amount in list(privillege_array_30d):
                try:
                    status = csgo_give_privillege(steam, privillege_array_30d[amount], '30d')
                    if status is True:
                        try:
                            send_tg_alert(f'Новая привилегия выдана:\n👤Игрок: <a href="{steam}">Ссылка</a>\n💎Привилегия: {privillege_array_30d[amount]}\n⏳Срок: 30 Дней')
                        except:
                            pass
                        if privillege_array_30d[amount] in privillege_array_discord:
                            return redirect(f"/autodonate/result?steam={steam}&days=30&redirect=11000010110010001101101011010010110111000001010", code = 302)
                        return redirect(f"/autodonate/result?steam={steam}&days=30&redirect=1100111110111111011111100100", code = 302)
                    try:
                        send_tg_alert(f'Ошибка при выдачи привилегии:\n👤Игрок: <a href="{steam}">Ссылка</a>\n💎Привилегия: {privillege_array_30d[amount]}\n⏳Срок: 30 Дней\nОшибка: У игрока уже есть какая-то привилегия')
                    except:
                        pass
                    return redirect(f"/autodonate/result?steam={steam}&redirect=110111011011111110100110001011000011100100", code = 302) # notbad
                except:
                    try:
                        send_tg_alert(f'Ошибка при выдачи привилегии:\n👤Игрок: <a href="{steam}">Ссылка</a>\n💎Привилегия: {privillege_array_30d[amount]}\n⏳Срок: 30 Дней\nОшибка: Ошибка выдачи')
                    except:
                        pass
                    return redirect(f"/autodonate/result?steam={steam}&redirect=011001110110100101110110011001010110010101110010011100100110111101110010", code = 302) # giverror
            elif amount in list(privillege_array_permanent):
                try:
                    status = csgo_give_privillege(steam, privillege_array_permanent[amount], '9999d')
                    if status is True:
                        try:
                            send_tg_alert(f'Новая привилегия выдана:\n👤Игрок: <a href="{steam}">Ссылка</a>\n💎Привилегия: {privillege_array_permanent[amount]}\n⏳Срок: 9999 Дней')
                        except:
                            pass
                        if privillege_array_permanent[amount] in privillege_array_discord:
                            return redirect(f"/autodonate/result?steam={steam}&days=9999&redirect=11000010110010001101101011010010110111000001010", code = 302)
                        return redirect(f"/autodonate/result?steam={steam}&days=9999&redirect=1100111110111111011111100100", code = 302)
                    try:
                        send_tg_alert(f'Ошибка при выдачи привилегии:\n👤Игрок: <a href="{steam}">Ссылка</a>\n💎Привилегия: {privillege_array_permanent[amount]}\n⏳Срок: 9999 Дней\nОшибка: У игрока уже есть какая-то привилегия')
                    except:
                        pass
                    return redirect(f"/autodonate/result?steam={steam}&redirect=110111011011111110100110001011000011100100", code = 302) # notbad
                except:
                    try:
                        send_tg_alert(f'Ошибка при выдачи привилегии:\n👤Игрок: <a href="{steam}">Ссылка</a>\n💎Привилегия: {privillege_array_permanent[amount]}\n⏳Срок: 9999 Дней\nОшибка: Ошибка выдачи')
                    except:
                        pass
                    return redirect(f"/autodonate/result?steam={steam}&redirect=011001110110100101110110011001010110010101110010011100100110111101110010", code = 302) # giverror
            elif amount_2 is not None and amount_2 in list(privillege_array_30d):
                try:
                    status = csgo_give_privillege(steam, privillege_array_30d[amount_2], '30d')
                    if status is True:
                        try:
                            send_tg_alert(f'Новая привилегия выдана:\n👤Игрок: <a href="{steam}">Ссылка</a>\n💎Привилегия: {privillege_array_30d[amount_2]}\n⏳Срок: 30 Дней')
                        except:
                            pass
                        if privillege_array_30d[amount_2] in privillege_array_discord:
                            return redirect(f"/autodonate/result?steam={steam}&days=30&redirect=11000010110010001101101011010010110111000001010", code = 302)
                        return redirect(f"/autodonate/result?steam={steam}&days=30&redirect=1100111110111111011111100100", code = 302)
                    try:
                        send_tg_alert(f'Ошибка при выдачи привилегии:\n👤Игрок: <a href="{steam}">Ссылка</a>\n💎Привилегия: {privillege_array_30d[amount_2]}\n⏳Срок: 30 Дней\nОшибка: У игрока уже есть какая-то привилегия')
                    except:
                        pass
                    return redirect(f"/autodonate/result?steam={steam}&redirect=110111011011111110100110001011000011100100", code = 302) # notbad
                except:
                    try:
                        send_tg_alert(f'Ошибка при выдачи привилегии:\n👤Игрок: <a href="{steam}">Ссылка</a>\n💎Привилегия: {privillege_array_30d[amount_2]}\n⏳Срок: 30 Дней\nОшибка: Ошибка выдачи')
                    except:
                        pass
                    return redirect(f"/autodonate/result?steam={steam}&redirect=011001110110100101110110011001010110010101110010011100100110111101110010", code = 302) # giverror
            elif amount_2 is not None and amount_2 in list(privillege_array_permanent):
                try:
                    status = csgo_give_privillege(steam, privillege_array_permanent[amount_2], '9999d')
                    if status is True:
                        try:
                            send_tg_alert(f'Новая привилегия выдана:\n👤Игрок: <a href="{steam}">Ссылка</a>\n💎Привилегия: {privillege_array_permanent[amount_2]}\n⏳Срок: 9999 Дней')
                        except:
                            pass
                        if privillege_array_permanent[amount_2] in privillege_array_discord:
                            return redirect(f"/autodonate/result?steam={steam}&days=9999&redirect=11000010110010001101101011010010110111000001010", code = 302)
                        return redirect(f"/autodonate/result?steam={steam}&days=9999&redirect=1100111110111111011111100100", code = 302)
                    try:
                        send_tg_alert(f'Ошибка при выдачи привилегии:\n👤Игрок: <a href="{steam}">Ссылка</a>\n💎Привилегия: {privillege_array_permanent[amount_2]}\n⏳Срок: 9999 Дней\nОшибка: У игрока уже есть какая-то привилегия')
                    except:
                        pass
                    return redirect(f"/autodonate/result?steam={steam}&redirect=110111011011111110100110001011000011100100", code = 302) # notbad
                except:
                    try:
                        send_tg_alert(f'Ошибка при выдачи привилегии:\n👤Игрок: <a href="{steam}">Ссылка</a>\n💎Привилегия: {privillege_array_permanent[amount_2]}\n⏳Срок: 9999 Дней\nОшибка: Ошибка выдачи')
                    except:
                        pass
                    return redirect(f"/autodonate/result?steam={steam}&redirect=011001110110100101110110011001010110010101110010011100100110111101110010", code = 302) # giverror
            else:
                return redirect(f"/autodonate/result?steam={steam}&redirect=11011101101111111010011001101101111111010111011101100100", code = 302) # notfound
        except Exception as err:
            logger.error('Не удалось выдать привилегию из-за ошибки:')
            logger.error(err)
            return redirect(f"/autodonate/result?steam={steam}&redirect=11011101101111111010011001101101111111010111011101100100", code = 302) # giverror



# QIWI
@app.route('/autodonate/qiwi', methods = ['GET'])
def autodonate_qiwi():
    price = request.args.get('price', default = 500, type = int)
    html_response = render_template('autodonate.html', name = 'QIWI', price = price)
    return html_response

@app.route('/autodonate/qiwi/post', methods = ['POST'])
def autodonate_qiwi_post():
    if request.method == 'POST':
        price = request.args.get('price', default = 500, type = int)
        form_result = request.form
        steam = form_result.getlist('steam')
        result = 0
        pay_url = 0
        comment = 0
        if price > 24:
            result, pay_url, comment = create_payment(uuid4(), price)
            if result is True:
                return redirect(f"/autodonate/qiwi/check?uuid={comment}&steam={steam[0]}&pay_url={pay_url}", code=302)
            else:
                html_response = render_template('request.html', request_color = 'red', request_text = 'Не удалось сгенерировать форму оплаты :(')
                return html_response
        else:
            html_response = render_template('request.html', request_color = 'red', request_text = 'Жулик, минимальный платеж от 25 рублей!')
            return html_response
    else:
        html_response = render_template('request.html', request_color = 'red', request_text = 'Жулик, тебе сюда нельзя!')
        return html_response

@app.route('/autodonate/qiwi/check', methods = ['GET'])
def autodonate_qiwi_check():
    uuid = request.args.get('uuid')
    steam = request.args.get('steam', default = 'Не введён', type = str)
    pay_url = request.args.get('pay_url')
    html_response = render_template('autodonate_post_success.html', name = 'QIWI', pay_url = pay_url, comment = uuid, steam = steam)
    return html_response

@app.route('/autodonate/qiwi/check_payment', methods = ['POST'])
def autodonate_qiwi_check_payment():
    if request.method == 'POST':
        uuid = request.args.get('uuid')
        steam = request.args.get('steam', default = 'Не введён', type = str)
        if uuid is not None and uuid != '':
            try:
                result, status, comment, amount = check_payment(uuid)
            except:
                result = False
            if result is True and comment == uuid:
                if status == 'PAID':
                    return autodonate_give_privillege(uuid, amount, steam)
                else:
                    logger.debug('Проверка статуса платежа | Ещё не оплачено')
                    return redirect(request.referrer, code = 302)
            else:
                logger.info('Не удалось найти платёж с таким UUID')
                return redirect(request.referrer, code = 302)
        else:
            logger.info('Поле UUID не задано или является пустой строкой')
            return redirect(request.referrer, code = 302)
    else:
        html_response = '<html><body><h2>Жулик, тебе сюда нельзя!</h2></body></html>'
        return html_response



# AUTODONATE ALL
@app.route('/autodonate/result', methods = ['GET'])
def autodonate_check_result():
    steam = request.args.get('steam', default = 'Не введён', type = str)
    days = request.args.get('days', default = 'Неизвестно', type = str)
    redirect_result = request.args.get('redirect')
    if str(redirect_result) == '1100111110111111011111100100': # good redirect
        logger.debug(f'Игрок задонатил и получил привилегию на свой аккаунт {steam} сроком на {days}')
        html_response = render_template('request.html', request_color = 'green', request_text = f'На аккаунт "{steam}" была выдана привилегия сроком на "{days}" дней')
    elif str(redirect_result) == '11000010110010001101101011010010110111000001010': # admin redirect
        logger.debug(f'Игрок задонатил и получил модер/админ-привилегию на свой аккаунт {steam} сроком на {days}')
        html_response = render_template('request.html', request_color = 'green', request_text = f'На аккаунт "{steam}" была выдана модер/админ-привилегия сроком на "{days}" дней. Внимание! Зайдите на наш дискорд сервер и сообщите, что вы купили модер/админ привилегию, чтобы получить доступ к проверке')
    elif str(redirect_result) == '110111011011111110100110001011000011100100': # not bad redirect
        logger.debug(f'Игрок задонатил и не получил привилегию на свой аккаунт {steam} т.к. уже имеет какую-то привилегию')
        html_response = render_template('request.html', request_color = 'orange', request_text = f'На вашем аккаунте "{steam}", скорее всего, уже есть привилегия, свяжитесь с нами в ВК или в Дискорд для обновления текущей привилегии')
    elif str(redirect_result) == '110100011000011100011110101111001011110010': # hacker redirect
        logger.debug(f'Попытка с {steam} | Этот UUID уже был оплачен и использован кем-то другим')
        html_response = render_template('request.html', request_color = 'red', request_text = 'Этот UUID уже был оплачен и использован кем-то другим')
    elif str(redirect_result) == '11011101101111111010011001101101111111010111011101100100': # notfound redirect
        logger.debug(f'Попытка с {steam} | Не удалось найти подходящую привилегию')
        html_response = render_template('request.html', request_color = 'red', request_text = 'Не удалось найти подходящую привилегию. Если вы считаете, что произошла ошибка: отпишите в дс/тг/вк (https://fame-community.ru/contact)')
    elif str(redirect_result) == '011001110110100101110110011001010110010101110010011100100110111101110010': # giveerror redirect
        logger.debug(f'Попытка с {steam} | Не удалось выдать привилегию из-за ошибки на сервере')
        html_response = render_template('request.html', request_color = 'red', request_text = 'Не удалось выдать привилегию из-за ошибки на сервере. Если вы считаете, что произошла ошибка: отпишите в дс/тг/вк (https://fame-community.ru/contact)')
    else:
        logger.debug(f'Произошла ошибка и на аккаунт "{steam}" не была выдана привилегия')
        html_response = render_template('request.html', request_color = 'red', request_text = f'Произошла ошибка и на аккаунт "{steam}" не была выдана привилегия')
    return html_response



# YOOMONEY
@app.route('/autodonate/yoomoney', methods = ['GET'])
def autodonate_yoomoney():
    price = request.args.get('price', default = 500, type = int)
    html_response = render_template('autodonate.html', name = 'YooMoney', price = price)
    return html_response

@app.route('/autodonate/yoomoney/post', methods = ['POST'])
def autodonate_yoomoney_post():
    if request.method == 'POST':
        price = request.args.get('price', default = 500, type = int)
        form_result = request.form
        steam = form_result.getlist('steam')
        result = 0
        pay_url = 0
        comment = uuid4()
        payment_type = 'PC'
        if price > 25:
            result, pay_url = yoomoney_api.create_payment(payment_type, f'{comment}', price)
            if result is True:
                logger.info('redirecting...')
                return redirect(f"/autodonate/yoomoney/check?uuid={comment}&steam={steam[0]}&pay_url={pay_url}", code=302)
            else:
                logger.warning('Не удалось сгенерировать форму оплаты :(')
                html_response = render_template('request.html', request_color = 'red', request_text = 'Не удалось сгенерировать форму оплаты :(')
                return html_response
        else:
            logger.warning('минимальный платеж от 25 рублей!')
            html_response = render_template('request.html', request_color = 'red', request_text = 'Жулик, минимальный платеж от 25 рублей!')
            return html_response
    else:
        logger.warning('get запрос заместо post')
        html_response = render_template('request.html', request_color = 'red', request_text = 'Жулик, тебе сюда нельзя!')
        return html_response

@app.route('/autodonate/yoomoney/check', methods = ['GET'])
def autodonate_yoomoney_check():
    uuid = request.args.get('uuid')
    steam = request.args.get('steam', default = 'Не введён', type = str)
    pay_url = request.args.get('pay_url')
    html_response = render_template('autodonate_post_success.html', name = 'YooMoney', pay_url = pay_url, comment = uuid, steam = steam)
    logger.info('Страница содержащая оплату платежа и его проверку успешно загружена')
    return html_response

@app.route('/autodonate/yoomoney/check_payment', methods = ['POST'])
def autodonate_yoomoney_check_payment():
    if request.method == 'POST':
        uuid = request.args.get('uuid')
        steam = request.args.get('steam', default = 'Не введён', type = str)
        if uuid is not None and uuid != '':
            try:
                result, status, comment, amount = yoomoney_api.find_donate(uuid)
            except:
                result = False
            if result is True and comment == uuid or result is True and comment == f'Поддержка Fame;\n{uuid}':
                if status == 'success':
                    return autodonate_give_privillege(uuid, amount, steam)
                else:
                    logger.debug('Проверка статуса платежа | Ещё не оплачено')
                    return redirect(request.referrer, code = 302)
            else:
                logger.info('Не удалось найти платёж с таким UUID')
                return redirect(request.referrer, code = 302)
        else:
            logger.info('Поле UUID не задано или является пустой строкой')
            return redirect(request.referrer, code = 302)
    else:
        html_response = '<html><body><h2>Жулик, тебе сюда нельзя!</h2></body></html>'
        return html_response


# CrystalPay
@app.route('/autodonate/crystalpay', methods = ['GET'])
def autodonate_crystalpay():
    price = request.args.get('price', default = 500, type = int)
    html_response = render_template('autodonate.html', name = 'CrystalPAY', price = price)
    return html_response

@app.route('/autodonate/crystalpay/post', methods = ['POST'])
def autodonate_crystalpay_post():
    if request.method == 'POST':
        price = request.args.get('price', default = 500, type = int)
        form_result = request.form
        steam = form_result.getlist('steam')
        result = 0
        pay_url = 0
        comment = uuid4()
        if price > 25:
            result, pay_url, pay_id = crystalpay_create_payment(f'{comment}', price)
            if result is True:
                return redirect(f"/autodonate/crystalpay/check?uuid={comment}&steam={steam[0]}&pay_url={pay_url}&pid={pay_id}", code = 302)
            else:
                html_response = render_template('request.html', request_color = 'red', request_text = 'Не удалось сгенерировать форму оплаты :(')
                return html_response
        else:
            html_response = render_template('request.html', request_color = 'red', request_text = 'Жулик, минимальный платеж от 25 рублей!')
            return html_response
    else:
        html_response = render_template('request.html', request_color = 'red', request_text = 'Жулик, тебе сюда нельзя!')
        return html_response

@app.route('/autodonate/crystalpay/check', methods = ['GET'])
def autodonate_crystalpay_check():
    uuid = request.args.get('uuid')
    steam = request.args.get('steam', default = 'Не введён', type = str)
    pay_url = request.args.get('pay_url')
    pay_id = request.args.get('pid')
    html_response = render_template('autodonate_post_success.html', name = 'CrystalPAY', pay_url = pay_url, comment = uuid, steam = steam, pid = pay_id)
    return html_response

@app.route('/autodonate/crystalpay/check_payment', methods = ['POST'])
def autodonate_crystalpay_check_payment():
    if request.method == 'POST':
        uuid = request.args.get('uuid')
        steam = request.args.get('steam', default = 'Не введён', type = str)
        pid = request.args.get('pid')
        if all((uuid, pid)) is not None and all((uuid, pid)) != '':
            try:
                result, status, comment, amount = crystalpay_check_payment(uuid, pid)
            except:
                result = False
            if result is True and comment == uuid:
                if status == 'payed':
                    return autodonate_give_privillege(uuid, amount, steam)
                else:
                    logger.debug('Проверка статуса платежа | Ещё не оплачено')
                    return redirect(request.referrer, code = 302)
            else:
                logger.info('Не удалось найти платёж с таким UUID')
                return redirect(request.referrer, code = 302)
        else:
            logger.info('Поле UUID не задано или является пустой строкой')
            return redirect(request.referrer, code = 302)
    else:
        html_response = '<html><body><h2>Жулик, тебе сюда нельзя!</h2></body></html>'
        return html_response



if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer
    get_env()
    logger.debug(f'Server starting on port {os.environ.get("PORT")}')
    # app.run(host='127.0.0.1', port = os.environ.get("PORT"))
    http_server = WSGIServer(('127.0.0.1', int(os.environ.get("PORT"))), app)
    http_server.serve_forever()