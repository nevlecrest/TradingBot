import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import requests

TOKEN = '5780535542:AAEi6j8fu-83GpbElpgKPfrziIrpIR6_rPU'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\nЯ бот, который может показать текущий курс валюты.\n"
                        "Для этого используй команду /exchange RUB USD, где RUB - валюта, из которой мы конвертируем, "
                        "USD - валюта, в которую мы конвертируем.")

@dp.message_handler(commands=['exchange'])
async def exchange_rate(message: types.Message):
    try:
        command_args = message.get_args().split()
        if len(command_args) != 2:
            await message.reply("Неверное количество аргументов. Используйте формат /exchange RUB USD")
            return

        from_currency, to_currency = command_args
        response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{from_currency}')
        data = response.json()

        if 'error' in data:
            await message.reply(f"Ошибка: {data['error']}")
            return

        rate = data['rates'][to_currency]
        await message.reply(f"1 {from_currency} = {rate} {to_currency}")

    except Exception as e:
        await message.reply(f"Произошла ошибка: {str(e)}")

@dp.message_handler(commands=['currencies'])
async def list_currencies(message: types.Message):
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        data = response.json()

        if 'error' in data:
            await message.reply(f"Ошибка: {data['error']}")
            return

        currencies = list(data['rates'].keys())
        await message.reply("Доступные валюты:\n" + "\n".join(currencies))

    except Exception as e:
        await message.reply(f"Произошла ошибка: {str(e)}")

if __name__ == '__main__':
    executor.start_polling(dp)