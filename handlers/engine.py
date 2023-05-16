from aiogram import types, Dispatcher
import asyncio
from create_bot import bot
from keyboards import keyboard
import db_operations as db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from time import sleep
from aiogram.dispatcher.filters import Text
import additional_functions as af

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
        await message.answer(f'👋{message.from_user.full_name}, Вас вітає бот у якому Ви можете зручно шукати тури!\n🔹Для початку роботи з ботом натисніть на кнопку нижче.👇', reply_markup=keyboard.startKb)
        db.sqlAddNewUser(message.chat.id, message.from_user.full_name)
    else:
        await message.delete()
        await message.answer(f'👋{message.from_user.full_name}, Вас знову вітає бот у якому Ви можете зручно шукати тури!\n🔹Для початку роботи з ботом натисніть на кнопку нижче.👇', reply_markup=keyboard.startKb)

async def mainMenuCall(callback : types.CallbackQuery):
    await callback.message.answer(f'🔸Оберіть наступну дію:', reply_markup=keyboard.mainMenuKb)
    await callback.answer()

async def searchMenuCall(callback : types.CallbackQuery):
    tours = db.sqlSelectTours(callback.message.chat.id)
    if tours:
        filtersSelected = db.checkFiltersSelected(callback.message.chat.id)
        if filtersSelected == 'True':
            await callback.message.answer(f'🔹Тури знайдені відповідно до обраних фільтрів: ')
        else:
            await callback.message.answer(f'🔹Для зручності рекомендується обрати фільтри пошуку.\nУсі наявні на даний момент тури: ')
        await callback.answer()
        for tour in tours:
            await callback.message.answer(f'\
〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n\
🌍 Країни: {af.addSpacesAfterComma(tour[1])};\n\
🚩 Міста: {af.addSpacesAfterComma(tour[2])};\n\
📆 Тривалість: {tour[3]} діб;\n\
💵 Вартість: {tour[5]} грн.\n\
↗️ <a href="{tour[4]}">Переглянути тур</a>\n\
〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️'
                                          , parse_mode="HTML")
            sleep(0.4)
        if filtersSelected == 'True':
            await callback.message.answer(f'📍Це всі тури які вдалося знайти відповідно до обраних фільтрів.', reply_markup=keyboard.searchMenuKb)
        else:
            await callback.message.answer(f'📍Це всі наявні на даний момент тури.', reply_markup=keyboard.searchMenuKb)
    else:
        await callback.message.answer(f'❌На жаль, турів за обраними фільтрами не знайдено.', reply_markup=keyboard.searchMenuKb)
        await callback.answer()

async def sortMenuCall(callback : types.CallbackQuery):
    if db.sqlSelectUserSort(callback.message.chat.id) == 'none':
        await callback.message.answer(f'🔖Оберіть варіант сортування турів: ', reply_markup=keyboard.sortMenuKb)
    else:
        await callback.message.answer(f'🔖Оберіть варіант сортування турів.\n\n🔹На даний момент обрано сортування за {db.returnSelectedSortName(callback.message.chat.id)} турів.', reply_markup=keyboard.sortMenuKb)
    await callback.answer()

async def filterMenuCall(callback : types.CallbackQuery):
    if db.checkFiltersSelected(callback.message.chat.id) == "False":
        await callback.message.answer(f'🔖Оберіть фільтри пошуку турів: ', reply_markup=keyboard.filterMenuKb)
    else:
        await callback.message.answer(f'🔖Оберіть фільтри пошуку турів.\n\n🔹ℹ️Обрані на даний момент фільтри:\n{db.returnSelectedFilters(callback.message.chat.id)}', reply_markup=keyboard.filterMenuKb)
    await callback.answer()

async def sortCall(callback : types.CallbackQuery):
    if callback.data == 'dontSortCb':
        db.sortTypeSet(callback.message.chat.id, 'none')
    else:
        db.sortTypeSet(callback.message.chat.id, callback.data)
    if callback.data == 'sortByPriceIncrCb':
        await callback.message.answer(f'✅Ви успішно обрали сортування турів за зростанням вартості.', reply_markup=keyboard.sortSelectionKb)
    elif callback.data == 'sortByPriceDecrCb':
        await callback.message.answer(f'✅Ви успішно обрали сортування турів за спаданням вартості.', reply_markup=keyboard.sortSelectionKb)
    elif callback.data == 'sortByDurationIncrCb':
        await callback.message.answer(f'✅Ви успішно обрали сортування турів за зростанням тривалості.', reply_markup=keyboard.sortSelectionKb)
    elif callback.data == 'sortByDurationDecrCb':
        await callback.message.answer(f'✅Ви успішно обрали сортування турів за спаданням тривалості.', reply_markup=keyboard.sortSelectionKb)
    elif callback.data == 'dontSortCb':
        await callback.message.answer(f'✅Ви успішно скасували сортування турів.', reply_markup=keyboard.sortMenuKb)
    await callback.answer()

async def cancelFilterSelection(message: types.Message, state: FSMContext):
    currentState = await state.get_state()
    if currentState is None:
        return
    await state.finish()
    await message.answer("ℹ️Вибір успішно скасовано, оберіть наступну дію.", reply_markup=keyboard.filterMenuKb)

async def countryFilterCall(callback : types.CallbackQuery):
    await FSM.country.set()
    await callback.message.answer(f'🔹Введіть назву країни:\n❗️для скасування вибору напишіть "скасувати"')
    await callback.answer()

async def countryFilterLoad(message : types.message, state : FSMContext):
    async with state.proxy() as data:
        data['country'] = message.text.title()
    db.selectedCountrySet(message.chat.id, message.text.title())
    await message.answer(f'✅Ви успішно обрали країну {message.text.title()}.', reply_markup=keyboard.filterSelectionKb)
    await state.finish()

async def cityFilterCall(callback : types.CallbackQuery):
    await FSM.city.set()
    await callback.message.answer(f'🔸Введіть назву міста:\n❗️для скасування вибору напишіть "скасувати"')
    await callback.answer()

async def cityFilterLoad(message : types.message, state : FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text.title()
    db.selectedCitySet(message.chat.id, message.text)
    await message.answer(f'✅Ви успішно обрали місто {message.text.title()}.', reply_markup=keyboard.filterSelectionKb)
    await state.finish()

async def durationFilterCall(callback : types.CallbackQuery):
    await callback.message.answer(f'🔷Оберіть мінімальну або максимальну тривалість туру:', reply_markup=keyboard.durationSelectionKb)
    await callback.answer()

async def durationFromFilterCall(callback : types.CallbackQuery):
    await FSM.durationFrom.set()
    await callback.message.answer(f'🔹Введіть мінімальну тривалість туру:\n❗️для скасування вибору напишіть "скасувати"')
    await callback.answer()

async def durationFromFilterLoad(message : types.message, state : FSMContext):
    async with state.proxy() as data:
        data['durationFrom'] = message.text
    db.selectedDurationFromSet(message.chat.id, message.text)
    await message.answer(f'✅Ви успішно обрали мінімальну тривалість туру {message.text} діб.', reply_markup=keyboard.returnToDurationFilterMenuKb)
    await state.finish()

async def durationToFilterCall(callback : types.CallbackQuery):
    await FSM.durationTo.set()
    await callback.message.answer(f'🔸Введіть максимальну тривалість туру:\n❗️для скасування вибору напишіть "скасувати"')
    await callback.answer()

async def durationToFilterLoad(message : types.message, state : FSMContext):
    async with state.proxy() as data:
        data['durationTo'] = message.text
    db.selectedDurationToSet(message.chat.id, message.text)
    await message.answer(f'✅Ви успішно обрали максимальну тривалість туру {message.text} діб.', reply_markup=keyboard.returnToDurationFilterMenuKb)
    await state.finish()

async def priceFilterCall(callback : types.CallbackQuery):
    await callback.message.answer(f'Оберіть мінімальну і/або максимальну вартість туру:', reply_markup=keyboard.priceSelectionKb)
    await callback.answer()

async def priceFromFilterCall(callback : types.CallbackQuery):
    await FSM.priceFrom.set()
    await callback.message.answer(f'🔹Введіть мінімальну вартість туру:\n❗️для скасування вибору напишіть "скасувати"')
    await callback.answer()

async def priceFromFilterLoad(message : types.message, state : FSMContext):
    async with state.proxy() as data:
        data['priceFrom'] = message.text
    db.selectedPriceFromSet(message.chat.id, message.text)
    await message.answer(f'✅Ви успішно обрали мінімальну вартість туру {message.text} гривень.', reply_markup=keyboard.returnToPriceFilterMenuKb)
    await state.finish()

async def priceToFilterCall(callback : types.CallbackQuery):
    await FSM.priceTo.set()
    await callback.message.answer(f'🔸Введіть максимальну вартість туру:\n❗️для скасування вибору напишіть "скасувати"')
    await callback.answer()

async def priceToFilterLoad(message : types.message, state : FSMContext):
    async with state.proxy() as data:
        data['priceTo'] = message.text
    db.selectedPriceToSet(message.chat.id, message.text)
    await message.answer(f'✅Ви успішно обрали максимальну вартість туру {message.text} гривень.', reply_markup=keyboard.returnToPriceFilterMenuKb)
    await state.finish()

async def clearCountryFilterCall(callback : types.CallbackQuery):
    db.selectedCountryClear(callback.message.chat.id)
    await callback.message.answer(f'✅Ви успішно скасували фільтрування турів за країною.', reply_markup=keyboard.filterSelectionKb)
    await callback.answer()

async def clearCityFilterCall(callback : types.CallbackQuery):
    db.selectedCityClear(callback.message.chat.id)
    await callback.message.answer(f'✅Ви успішно скасували фільтрування турів за містом.', reply_markup=keyboard.filterSelectionKb)
    await callback.answer()

async def clearDurationFilterCall(callback : types.CallbackQuery):
    db.selectedDurationClear(callback.message.chat.id)
    await callback.message.answer(f'✅Ви успішно скасували фільтрування турів за тривалістю.', reply_markup=keyboard.filterSelectionKb)
    await callback.answer()

async def clearPriceFilterCall(callback : types.CallbackQuery):
    db.selectedPriceClear(callback.message.chat.id)
    await callback.message.answer(f'✅Ви успішно скасували фільтрування турів за вартістю.', reply_markup=keyboard.filterSelectionKb)
    await callback.answer()

async def clearAllFiltersCall(callback : types.CallbackQuery):
    db.selectedAllClear(callback.message.chat.id)
    await callback.message.answer(f'✅Ви успішно скасували фільтрування турів.', reply_markup=keyboard.filterSelectionKb)
    await callback.answer()

def registerHandlers(dp : Dispatcher):
    dp.register_message_handler(startCommand, commands=['start', 'help'])
    dp.register_callback_query_handler(mainMenuCall, text=['startCb', 'returnToMainMenuCb'])
    dp.register_callback_query_handler(searchMenuCall, text=['searchCb', 'returnToSearchMenuCb'])
    dp.register_callback_query_handler(sortMenuCall, text=['sortCb', 'returnToSortMenuCb'])
    dp.register_callback_query_handler(filterMenuCall, text=['filterCb', 'returnToFilterMenuCb'])
    dp.register_callback_query_handler(sortCall, text=['sortByPriceIncrCb', 'sortByPriceDecrCb', 'sortByDurationIncrCb', 'sortByDurationDecrCb', 'dontSortCb'])
    dp.register_message_handler(cancelFilterSelection, state="*", commands=["відмінити", "скасувати", "відміна"])
    dp.register_message_handler(cancelFilterSelection, Text(equals=["відмінити", "скасувати", "відміна"], ignore_case=True), state="*")
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