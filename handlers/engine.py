from aiogram import types, Dispatcher
import asyncio
from create_bot import bot
from keyboards import keyboard

async def startCommand(message: types.Message):
    user_name = message.from_user.full_name
    await message.answer(f'{user_name}, Вас вітає бот у якому Ви можете зручно шукати тури!', reply_markup=keyboard.startKb)

async def mainMenuCall(callback : types.CallbackQuery):
    await callback.message.answer(f'Оберіть наступну дію: ', reply_markup=keyboard.mainMenuKb)
    await callback.answer()

async def searchMenuCall(callback : types.CallbackQuery):
    await callback.message.answer(f'Знайдені тури: ', reply_markup=keyboard.searchMenuKb)
    await callback.answer()

async def sortMenuCall(callback : types.CallbackQuery):
    await callback.message.answer(f'Оберіть варіант сортування: ', reply_markup=keyboard.sortMenuKb)
    await callback.answer()

async def filterMenuCall(callback : types.CallbackQuery):
    await callback.message.answer(f'Оберіть фільтри: ', reply_markup=keyboard.filterMenuKb)
    await callback.answer()

def register_handlers(dp : Dispatcher):
    dp.register_message_handler(startCommand, commands=['start', 'help'])
    dp.register_callback_query_handler(mainMenuCall, text=['startCb', 'returnToMainMenuCb'])
    dp.register_callback_query_handler(searchMenuCall, text=['searchCb', 'returnToSearchMenuCb'])
    dp.register_callback_query_handler(sortMenuCall, text=['sortCb'])
    dp.register_callback_query_handler(filterMenuCall, text=['filterCb'])