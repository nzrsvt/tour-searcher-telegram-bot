from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()

with open('token.txt', 'r') as token_txt:
    TOKEN = token_txt.read()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)