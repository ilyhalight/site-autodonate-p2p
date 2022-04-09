import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

logging.basicConfig(level = logging.INFO)
dotenv_path = os.path.join(os.path.dirname(__file__), '../', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
bot = Bot(token = os.environ.get('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher(bot)

@dp.message_handler()
async def echo(message: types.Message):
    await message.reply('К сожалению, я не умею отвечать на команды. Я всего-лишь Алерт-Бот')

async def telegram_alert(text: str):
    await bot.send_message(587778212, text, parse_mode = 'html')

async def on_startup(dp):
    logging.info('Telegram bot started...')

def main():
    executor.start_polling(dp, skip_updates = True, on_startup = on_startup)

if __name__ == '__main__':
    main()