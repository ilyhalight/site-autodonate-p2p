## 1.0.4 (Non-Tested)
- Добавлен выбор групп, при покупке которых будет отображаться уведомление о рекомендации зайти на наш дискорд сервер
- Добавлены логи с информацией о покупке привилегии в телеграм (вы должны создать бота, написать ему /start, а посел вставить его токен в .env)
- Добавлена оплата через ПС CrystalPay


## 1.0.3
- Исправлена ошибка, из-за которой серверу не удавалось найти платёж сделанный через кошелёк YooMoney
- Добавлена ссылка на дискорд на страницу ответа сервера
- Добавлена коррекция суммы полученного платежа YooMoney
- Теперь, на странице проверки автодоната пишется, если серверу не удалось определить, что за привилегию он должен выдать. (Ранее показывало, что у игрока уже есть привилегия)

## 1.0.2
- Пофиксил ошибку с мелким интерфейсом страницы на мобилках
- Увеличил длину дива в кастомной странице оставета/запроса

## 1.0.1
- Теперь, по умолчанию, запускается WSGI-сервер

## 1.0.0
- Добавлена функция добавления привилегии игроку (если уже есть привилегия, то просто выводится страница исключения)
- Добавлены страницы для запросов и ответов
- Добавлен чс для использованных uuid
- Создание и просмотр счетов оплаты QIWI P2P
- Включение/Отключение дебаг логов