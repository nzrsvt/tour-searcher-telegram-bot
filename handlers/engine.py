from aiogram import types, Dispatcher
import asyncio
from create_bot import bot
from keyboards import keyboard
import db_operations

async def startCommand(message: types.Message):
    userName = message.from_user.full_name
    telegramId = message.chat.id
    if db_operations.sqlCheckTelegramId(message.chat.id) == "no_id":
        await message.delete()
        await message.answer(f'{userName}, Вас вітає бот у якому Ви можете зручно шукати тури!', reply_markup=keyboard.startKb)
        db_operations.sqlAddNewUser(telegramId, userName)
    else:
        await message.delete()
        await message.answer(f'{userName}, Вас знову вітає бот у якому Ви можете зручно шукати тури!', reply_markup=keyboard.startKb)


async def mainMenuCall(callback : types.CallbackQuery):
    await callback.message.answer(f'Оберіть наступну дію: ', reply_markup=keyboard.mainMenuKb)
    await callback.answer()

async def searchMenuCall(callback : types.CallbackQuery):
    await callback.message.answer(f'Знайдені тури: ', reply_markup=keyboard.searchMenuKb)
    for tour in db_operations.sqlSelectAllTours():
        await callback.message.answer(f'Країни: {tour[1]}\nМіста: {tour[2]}\nТривалість: {tour[3]}\nПосилання: {tour[4]}\nВартість: {tour[5]}\n')
    await callback.answer()

async def sortMenuCall(callback : types.CallbackQuery):
    await callback.message.answer(f'Оберіть варіант сортування: ', reply_markup=keyboard.sortMenuKb)
    await callback.answer()

async def filterMenuCall(callback : types.CallbackQuery):
    await callback.message.answer(f'Оберіть фільтри: ', reply_markup=keyboard.filterMenuKb)
    await callback.answer()

def registerHandlers(dp : Dispatcher):
    dp.register_message_handler(startCommand, commands=['start', 'help'])
    dp.register_callback_query_handler(mainMenuCall, text=['startCb', 'returnToMainMenuCb'])
    dp.register_callback_query_handler(searchMenuCall, text=['searchCb', 'returnToSearchMenuCb'])
    dp.register_callback_query_handler(sortMenuCall, text=['sortCb'])
    dp.register_callback_query_handler(filterMenuCall, text=['filterCb'])