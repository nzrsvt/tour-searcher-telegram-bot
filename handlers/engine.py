from aiogram import types, Dispatcher
import asyncio
from create_bot import bot
from keyboards import keyboard
import db_operations as db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSM(StatesGroup):
    country = State()
    city = State()
    durationFrom = State()
    durationTo = State()
    priceFrom = State()
    priceTo = State()

async def startCommand(message: types.Message):
    if db.sqlCheckTelegramId(message.chat.id) == "no_id":
        await message.delete()
        await message.answer(f'{message.from_user.full_name}, Вас вітає бот у якому Ви можете зручно шукати тури!', reply_markup=keyboard.startKb)
        db.sqlAddNewUser(message.chat.id, message.from_user.full_name)
    else:
        await message.delete()
        await message.answer(f'{message.from_user.full_name}, Вас знову вітає бот у якому Ви можете зручно шукати тури!', reply_markup=keyboard.startKb)


async def mainMenuCall(callback : types.CallbackQuery):
    await callback.message.answer(f'Оберіть наступну дію: ', reply_markup=keyboard.mainMenuKb)
    await callback.answer()

async def searchMenuCall(callback : types.CallbackQuery):
    await callback.message.answer(f'Знайдені тури: ', reply_markup=keyboard.searchMenuKb)
    for tour in db.sqlSelectAllTours():
        await callback.message.answer(f'Країни: {tour[1]}\nМіста: {tour[2]}\nТривалість: {tour[3]}\nПосилання: {tour[4]}\nВартість: {tour[5]}\n')
    await callback.answer()

async def sortMenuCall(callback : types.CallbackQuery):
    await callback.message.answer(f'Оберіть варіант сортування: ', reply_markup=keyboard.sortMenuKb)
    await callback.answer()

async def filterMenuCall(callback : types.CallbackQuery):
    await callback.message.answer(f'Оберіть фільтри: ', reply_markup=keyboard.filterMenuKb)
    await callback.answer()

async def sortCall(callback : types.CallbackQuery):
    if callback.data == 'dontSortCb':
        db.sortTypeSet(callback.message.chat.id, 'none')
    else:
        db.sortTypeSet(callback.message.chat.id, callback.data)
    if callback.data == 'sortByPriceIncrCb':
        await callback.message.answer(f'Ви успішно обрали сортування турів за зростанням ціни.', reply_markup=keyboard.sortMenuKb)
    elif callback.data == 'sortByPriceDecrCb':
        await callback.message.answer(f'Ви успішно обрали сортування турів за спаданням ціни.', reply_markup=keyboard.sortMenuKb)
    elif callback.data == 'sortByDurationIncrCb':
        await callback.message.answer(f'Ви успішно обрали сортування турів за зростанням тривалості.', reply_markup=keyboard.sortMenuKb)
    elif callback.data == 'sortByDurationDecrCb':
        await callback.message.answer(f'Ви успішно обрали сортування турів за спаданням тривалості.', reply_markup=keyboard.sortMenuKb)
    elif callback.data == 'dontSortCb':
        await callback.message.answer(f'Ви успішно скасували сортування турів.', reply_markup=keyboard.sortMenuKb)
    await callback.answer()

async def countryFilterCall(callback : types.CallbackQuery):
    await FSM.country.set()
    await callback.message.answer(f'Введіть назву країни:')
    await callback.answer()

async def countryFilterLoad(message : types.message, state : FSMContext):
    async with state.proxy() as data:
        data['country'] = message.text
    db.selectedCountrySet(message.chat.id, message.text)
    await message.answer(f'Ви успішно обрали країну {message.text}.', reply_markup=keyboard.filterSelectionKb)
    await state.finish()

async def cityFilterCall(callback : types.CallbackQuery):
    await FSM.city.set()
    await callback.message.answer(f'Введіть назву міста:')
    await callback.answer()

async def cityFilterLoad(message : types.message, state : FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
    db.selectedCitySet(message.chat.id, message.text)
    await message.answer(f'Ви успішно обрали місто {message.text}.', reply_markup=keyboard.filterSelectionKb)
    await state.finish()

async def durationFilterCall(callback : types.CallbackQuery):
    await callback.message.answer(f'Оберіть мінімальну і/або максимальну тривалість туру:', reply_markup=keyboard.durationSelectionKb)
    await callback.answer()

async def durationFromFilterCall(callback : types.CallbackQuery):
    await FSM.durationFrom.set()
    await callback.message.answer(f'Введіть мінімальну тривалість туру:')
    await callback.answer()

async def durationFromFilterLoad(message : types.message, state : FSMContext):
    async with state.proxy() as data:
        data['durationFrom'] = message.text
    db.selectedDurationFromSet(message.chat.id, message.text)
    await message.answer(f'Ви успішно обрали мінімальну тривалість туру {message.text} діб.', reply_markup=keyboard.returnToDurationFilterMenuKb)
    await state.finish()

async def durationToFilterCall(callback : types.CallbackQuery):
    await FSM.durationTo.set()
    await callback.message.answer(f'Введіть максимальну тривалість туру:')
    await callback.answer()

async def durationToFilterLoad(message : types.message, state : FSMContext):
    async with state.proxy() as data:
        data['durationTo'] = message.text
    db.selectedDurationToSet(message.chat.id, message.text)
    await message.answer(f'Ви успішно обрали максимальну тривалість туру {message.text} діб.', reply_markup=keyboard.returnToDurationFilterMenuKb)
    await state.finish()

async def priceFilterCall(callback : types.CallbackQuery):
    await callback.message.answer(f'Оберіть мінімальну і/або максимальну вартість туру:', reply_markup=keyboard.priceSelectionKb)
    await callback.answer()

async def priceFromFilterCall(callback : types.CallbackQuery):
    await FSM.priceFrom.set()
    await callback.message.answer(f'Введіть мінімальну вартість туру:')
    await callback.answer()

async def priceFromFilterLoad(message : types.message, state : FSMContext):
    async with state.proxy() as data:
        data['priceFrom'] = message.text
    db.selectedPriceFromSet(message.chat.id, message.text)
    await message.answer(f'Ви успішно обрали мінімальну вартість туру {message.text} гривень.', reply_markup=keyboard.returnToPriceFilterMenuKb)
    await state.finish()

async def priceToFilterCall(callback : types.CallbackQuery):
    await FSM.priceTo.set()
    await callback.message.answer(f'Введіть максимальну вартість туру:')
    await callback.answer()

async def priceToFilterLoad(message : types.message, state : FSMContext):
    async with state.proxy() as data:
        data['priceTo'] = message.text
    db.selectedPriceToSet(message.chat.id, message.text)
    await message.answer(f'Ви успішно обрали максимальну вартість туру {message.text} гривень.', reply_markup=keyboard.returnToPriceFilterMenuKb)
    await state.finish()

async def clearCountryFilterCall(callback : types.CallbackQuery):
    db.selectedCountryClear(callback.message.chat.id)
    await callback.message.answer(f'Ви успішно скасували фільтрування турів за країною.', reply_markup=keyboard.filterMenuKb)
    await callback.answer()

async def clearCityFilterCall(callback : types.CallbackQuery):
    db.selectedCityClear(callback.message.chat.id)
    await callback.message.answer(f'Ви успішно скасували фільтрування турів за містом.', reply_markup=keyboard.filterMenuKb)
    await callback.answer()

async def clearDurationFilterCall(callback : types.CallbackQuery):
    db.selectedDurationClear(callback.message.chat.id)
    await callback.message.answer(f'Ви успішно скасували фільтрування турів за тривалістю.', reply_markup=keyboard.filterMenuKb)
    await callback.answer()

async def clearPriceFilterCall(callback : types.CallbackQuery):
    db.selectedPriceClear(callback.message.chat.id)
    await callback.message.answer(f'Ви успішно скасували фільтрування турів за вартістю.', reply_markup=keyboard.filterMenuKb)
    await callback.answer()

async def clearAllFiltersCall(callback : types.CallbackQuery):
    db.selectedAllClear(callback.message.chat.id)
    await callback.message.answer(f'Ви успішно скасували фільтрування турів.', reply_markup=keyboard.filterMenuKb)
    await callback.answer()

def registerHandlers(dp : Dispatcher):
    dp.register_message_handler(startCommand, commands=['start', 'help'])
    dp.register_callback_query_handler(mainMenuCall, text=['startCb', 'returnToMainMenuCb'])
    dp.register_callback_query_handler(searchMenuCall, text=['searchCb', 'returnToSearchMenuCb'])
    dp.register_callback_query_handler(sortMenuCall, text=['sortCb'])
    dp.register_callback_query_handler(filterMenuCall, text=['filterCb', 'returnToFilterMenuCb'])
    dp.register_callback_query_handler(sortCall, text=['sortByPriceIncrCb', 'sortByPriceDecrCb', 'sortByDurationIncrCb', 'sortByDurationDecrCb', 'dontSortCb'])
    dp.register_callback_query_handler(countryFilterCall, text=['selectCountryCb'])
    dp.register_message_handler(countryFilterLoad, state=FSM.country)
    dp.register_callback_query_handler(cityFilterCall, text=['selectCityCb'])
    dp.register_message_handler(cityFilterLoad, state=FSM.city)
    dp.register_callback_query_handler(durationFilterCall, text=['selectDurationCb', 'returnToDurationFilterMenuCb'])
    dp.register_callback_query_handler(durationFromFilterCall, text=['selectDurationFromCb'])
    dp.register_message_handler(durationFromFilterLoad, state=FSM.durationFrom)
    dp.register_callback_query_handler(durationToFilterCall, text=['selectDurationToCb'])
    dp.register_message_handler(durationToFilterLoad, state=FSM.durationTo)
    dp.register_callback_query_handler(priceFilterCall, text=['selectPriceCb', 'returnToPriceFilterMenuCb'])
    dp.register_callback_query_handler(priceFromFilterCall, text=['selectPriceFromCb'])
    dp.register_message_handler(priceFromFilterLoad, state=FSM.priceFrom)
    dp.register_callback_query_handler(priceToFilterCall, text=['selectPriceToCb'])
    dp.register_message_handler(priceToFilterLoad, state=FSM.priceTo)
    dp.register_callback_query_handler(clearCountryFilterCall, text=['clearCountryCb'])
    dp.register_callback_query_handler(clearCityFilterCall, text=['clearCityCb'])
    dp.register_callback_query_handler(clearDurationFilterCall, text=['clearDurationCb'])
    dp.register_callback_query_handler(clearPriceFilterCall, text=['clearPriceCb'])
    dp.register_callback_query_handler(clearAllFiltersCall, text=['clearAllCb'])