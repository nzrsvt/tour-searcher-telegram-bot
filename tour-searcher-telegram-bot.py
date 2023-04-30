from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


async def on_startup(_):
    print('Bot has been launched successfully.')



with open('telegram-bot-token.txt', 'r') as token_txt:
    TOKEN = token_txt.read()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)