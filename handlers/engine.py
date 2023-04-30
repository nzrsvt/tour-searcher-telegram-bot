from aiogram import types, Dispatcher
import asyncio
from create_bot import bot

async def start_command(message: types.Message):
    user_name = message.from_user.full_name
    await message.answer(f'{user_name}, Вас вітає бот у якому Ви можете зручно шукати тури!')

def register_handlers(dp : Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])