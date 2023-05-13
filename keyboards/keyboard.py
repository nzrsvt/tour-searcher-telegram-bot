from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

startBtn = InlineKeyboardButton('Почати пошук турів', callback_data='startCb')
startKb = InlineKeyboardMarkup()
startKb.add(startBtn)

searchBtn = InlineKeyboardButton('Здійснити пошук', callback_data='searchCb')
filterBtn = InlineKeyboardButton('Налаштувати фільтри пошуку', callback_data='filterCb')
mainMenuKb = InlineKeyboardMarkup()
mainMenuKb.add(searchBtn).add(filterBtn)

returnToMainMenuBtn = InlineKeyboardButton('Повернутися на головне меню', callback_data='returnToMainMenuCb')

sortBtn = InlineKeyboardButton('Сортувати тури', callback_data='sortCb')
searchMenuKb = InlineKeyboardMarkup()
searchMenuKb.add(sortBtn).add(returnToMainMenuBtn)

addCountryBtn = InlineKeyboardButton('Додати країну', callback_data='addCountryCb')
clearCountryBtn = InlineKeyboardButton('Очистити вибір країни', callback_data='clearCountryCb')
addCityBtn = InlineKeyboardButton('Додати місто', callback_data='addCityCb')
clearCityBtn = InlineKeyboardButton('Очистити вибір міста', callback_data='clearCityCb')
chooseDurationBtn = InlineKeyboardButton('Обрати тривалість', callback_data='chooseDurationCb')
clearDurationBtn = InlineKeyboardButton('Очистити вибір тривалості', callback_data='clearDurationCb')
choosePriceBtn = InlineKeyboardButton('Обрати вартість', callback_data='choosePriceCb')
clearPriceBtn = InlineKeyboardButton('Очистити вибір вартості', callback_data='clearPriceCb')
clearAllBtn = InlineKeyboardButton('Очистити весь вибір', callback_data='clearPriceCb')
filterMenuKb = InlineKeyboardMarkup()
filterMenuKb.row(addCountryBtn, clearCountryBtn).row(addCityBtn, clearCityBtn).row(chooseDurationBtn, clearDurationBtn).row(choosePriceBtn, clearPriceBtn).add(clearAllBtn).add(returnToMainMenuBtn)

sortByPriceIncrBtn = InlineKeyboardButton('За зростанням ціни', callback_data='sortByPriceIncrCb')
sortByPriceDecrBtn = InlineKeyboardButton('За спаданням ціни', callback_data='sortByPriceDecrCb')
sortByDurationIncrBtn = InlineKeyboardButton('За зростанням тривалості', callback_data='sortByDurationIncrCb')
sortByDurationDecrBtn = InlineKeyboardButton('За зростанням тривалості', callback_data='sortByDurationDecrCb')
dontSortBtn = InlineKeyboardButton('Не сортувати', callback_data='dontSortCb')
returnToSearchMenuBtn = InlineKeyboardButton('Повернутися до перегляду турів', callback_data='returnToSearchMenuCb')
sortMenuKb = InlineKeyboardMarkup()
sortMenuKb.row(sortByPriceIncrBtn, sortByPriceDecrBtn).row(sortByDurationIncrBtn, sortByDurationDecrBtn).add(dontSortBtn).add(returnToSearchMenuBtn)