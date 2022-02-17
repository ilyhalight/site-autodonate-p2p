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

privillege_array_30d = privillege_cost['30days']
privillege_array_permanent = privillege_cost['permanent']

app = Flask(__name__)

def autodonate_give_privillege(uuid, amount, steam):
    amount = str(f'{amount}0')
    logger.info(privillege_array_permanent[amount])
    logger.debug('Проверка статуса платежа | Оплачено')
    if uuid in uuid_blacklist:
        return redirect(f"/autodonate/result?redirect=110100011000011100011110101111001011110010", code=302)
    else:
        uuid_blacklist.append(uuid)
        update_uuid_blacklist(uuid_blacklist)
        logger.debug(f'{uuid} был использован и добавлен в ЧС')
        try:
            if amount in list(privillege_array_30d):
                csgo_give_privillege(steam, privillege_array_30d[amount], '30d')
                return redirect(f"/autodonate/result?steam={steam}&days=30&redirect=1100111110111111011111100100", code=302)
            elif amount in list(privillege_array_permanent):
                csgo_give_privillege(steam, privillege_array_permanent[amount], '9999d')
                return redirect(f"/autodonate/result?steam={steam}&days=9999&redirect=1100111110111111011111100100", code=302)
            else:
                return redirect(f"/autodonate/result?steam={steam}&redirect=110111011011111110100110001011000011100100", code=302)
        except Exception as err:
            logger.error('Не удалось выдать привилегию из-за ошибки:')
            logger.error(err)
            return redirect(f"/autodonate/result?steam={steam}&redirect=110001011000011100100", code=302)



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
def autodonate_check():
    uuid = request.args.get('uuid')
    steam = request.args.get('steam', default = 'Не введён', type = str)
    pay_url = request.args.get('pay_url')
    html_response = render_template('autodonate_post_success.html', name = 'QIWI', pay_url = pay_url, comment = uuid, steam = steam)
    return html_response

@app.route('/autodonate/qiwi/check_payment', methods = ['POST'])
def autodonate_check_payment():
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
                    autodonate_give_privillege(uuid, amount, steam)
                else:
                    logger.debug('Проверка статуса платежа | Ещё не оплачено')
                    return redirect(request.referrer, code=302)
            else:
                return redirect(request.referrer, code=302)
        else:
            return redirect(request.referrer, code=302)
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
        logger.debug(f'Кто-то задонатил и получил привилегию на свой аккаунт {steam} сроком на {days}')
        html_response = render_template('request.html', request_color = 'green', request_text = f'На аккаунт "{steam}" была выдана привилегия сроком на "{days}" дней')
    elif str(redirect_result) == '110111011011111110100110001011000011100100': # not bad redirect
        logger.debug(f'Кто-то задонатил и не получил привилегию на свой аккаунт {steam} т.к. уже имеет какую-то привилегию')
        html_response = render_template('request.html', request_color = 'orange', request_text = f'На вашем аккаунте "{steam}", скорее всего, уже есть привилегия, свяжитесь с нами в ВК или в Дискорд для обновления текущей привилегии')
    elif str(redirect_result) == '110100011000011100011110101111001011110010': # hacker redirect
        logger.debug(f'Попытка с {steam} | Этот UUID уже был оплачен и использован кем-то другим')
        html_response = render_template('request.html', request_color = 'red', request_text = 'Этот UUID уже был оплачен и использован кем-то другим')
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
                return redirect(f"/autodonate/yoomoney/check?uuid={comment}&steam={steam[0]}&pay_url={pay_url}", code=302)
            else:
                html_response = render_template('request.html', request_color = 'red', request_text = 'Не удалось сгенерировать форму оплаты :(')
                return html_response
        else:
            html_response = render_template('request.html', request_color = 'red', request_text = 'Жулик, минимальный платеж от 25 рублей!')
            return html_response
    else:
        html_response = render_template('request.html', request_color = 'red', request_text = 'Жулик, тебе сюда нельзя!')
        return html_response

@app.route('/autodonate/yoomoney/check', methods = ['GET'])
def autodonate_yoomoney_check():
    uuid = request.args.get('uuid')
    steam = request.args.get('steam', default = 'Не введён', type = str)
    pay_url = request.args.get('pay_url')
    html_response = render_template('autodonate_post_success.html', name = 'YooMoney', pay_url = pay_url, comment = uuid, steam = steam)
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
            if result is True and comment == uuid:
                if status == 'success':
                    return autodonate_give_privillege(uuid, amount, steam)
                else:
                    logger.debug('Проверка статуса платежа | Ещё не оплачено')
                    return redirect(request.referrer, code=302)
            else:
                return redirect(request.referrer, code=302)
        else:
            return redirect(request.referrer, code=302)
    else:
        html_response = '<html><body><h2>Жулик, тебе сюда нельзя!</h2></body></html>'
        return html_response



# YOOMONEY CARD
@app.route('/autodonate/yoomoney_card', methods = ['GET'])
def autodonate_yoomoney_card():
    price = request.args.get('price', default = 500, type = int)
    html_response = render_template('autodonate.html', name = 'YooMoney_Card', price = price)
    return html_response

@app.route('/autodonate/yoomoney_card/post', methods = ['POST'])
def autodonate_yoomoney_card_post():
    if request.method == 'POST':
        price = request.args.get('price', default = 500, type = int)
        form_result = request.form
        steam = form_result.getlist('steam')
        result = 0
        pay_url = 0
        comment = uuid4()
        payment_type = 'AC'
        if price > 25:
            result, pay_url = yoomoney_api.create_payment(payment_type, f'{comment}', price)
            if result is True:
                return redirect(f"/autodonate/yoomoney_card/check?uuid={comment}&steam={steam[0]}&pay_url={pay_url}", code=302)
            else:
                html_response = render_template('request.html', request_color = 'red', request_text = 'Не удалось сгенерировать форму оплаты :(')
                return html_response
        else:
            html_response = render_template('request.html', request_color = 'red', request_text = 'Жулик, минимальный платеж от 25 рублей!')
            return html_response
    else:
        html_response = render_template('request.html', request_color = 'red', request_text = 'Жулик, тебе сюда нельзя!')
        return html_response

@app.route('/autodonate/yoomoney_card/check', methods = ['GET'])
def autodonate_yoomoney_card_check():
    uuid = request.args.get('uuid')
    steam = request.args.get('steam', default = 'Не введён', type = str)
    pay_url = request.args.get('pay_url')
    html_response = render_template('autodonate_post_success.html', name = 'YooMoney_Card', pay_url = pay_url, comment = uuid, steam = steam)
    return html_response

@app.route('/autodonate/yoomoney_card/check_payment', methods = ['POST'])
def autodonate_yoomoney_card_check_payment():
    if request.method == 'POST':
        uuid = request.args.get('uuid')
        steam = request.args.get('steam', default = 'Не введён', type = str)
        if uuid is not None and uuid != '':
            try:
                result, status, comment, amount = yoomoney_api.find_donate(uuid)
            except:
                result = False
            if result is True and comment == uuid:
                if status == 'success':
                    return autodonate_give_privillege(uuid, amount, steam)
                else:
                    logger.debug('Проверка статуса платежа | Ещё не оплачено')
                    return redirect(request.referrer, code=302)
            else:
                return redirect(request.referrer, code=302)
        else:
            return redirect(request.referrer, code=302)
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