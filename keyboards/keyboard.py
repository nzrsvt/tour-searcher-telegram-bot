from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

startBtn = InlineKeyboardButton('Почати пошук турів', callback_data='startCb')
startKb = InlineKeyboardMarkup()
startKb.add(startBtn)

searchBtn = InlineKeyboardButton('Здійснити пошук', callback_data='searchCb')
filterBtn = InlineKeyboardButton('Налаштувати фільтри пошуку', callback_data='filterCb')
sortBtn = InlineKeyboardButton('Налаштувати сортування турів', callback_data='sortCb')
mainMenuKb = InlineKeyboardMarkup()
mainMenuKb.add(searchBtn).add(filterBtn).add(sortBtn)

returnToMainMenuBtn = InlineKeyboardButton('Повернутися на головне меню↩️', callback_data='returnToMainMenuCb')

searchMenuKb = InlineKeyboardMarkup()
searchMenuKb.add(returnToMainMenuBtn)

selectCountryBtn = InlineKeyboardButton('Обрати країну', callback_data='selectCountryCb')
clearCountryBtn = InlineKeyboardButton('Очистити вибір країни', callback_data='clearCountryCb')
selectCityBtn = InlineKeyboardButton('Обрати місто', callback_data='selectCityCb')
clearCityBtn = InlineKeyboardButton('Очистити вибір міста', callback_data='clearCityCb')
selectDurationBtn = InlineKeyboardButton('Обрати тривалість', callback_data='selectDurationCb')
clearDurationBtn = InlineKeyboardButton('Очистити вибір тривалості', callback_data='clearDurationCb')
selectPriceBtn = InlineKeyboardButton('Обрати вартість', callback_data='selectPriceCb')
clearPriceBtn = InlineKeyboardButton('Очистити вибір вартості', callback_data='clearPriceCb')
clearAllBtn = InlineKeyboardButton('Очистити весь вибір', callback_data='clearAllCb')
filterMenuKb = InlineKeyboardMarkup()
filterMenuKb.row(selectCountryBtn, clearCountryBtn).row(selectCityBtn, clearCityBtn).row(selectDurationBtn, clearDurationBtn).row(selectPriceBtn, clearPriceBtn).add(clearAllBtn).add(returnToMainMenuBtn)

sortByPriceIncrBtn = InlineKeyboardButton('За зростанням вартості⬆️', callback_data='sortByPriceIncrCb')
sortByPriceDecrBtn = InlineKeyboardButton('За спаданням вартості⬇️', callback_data='sortByPriceDecrCb')
sortByDurationIncrBtn = InlineKeyboardButton('За зростанням тривалості⬆️', callback_data='sortByDurationIncrCb')
sortByDurationDecrBtn = InlineKeyboardButton('За спаданням тривалості⬇️', callback_data='sortByDurationDecrCb')
dontSortBtn = InlineKeyboardButton('Не сортувати🔀', callback_data='dontSortCb')
sortMenuKb = InlineKeyboardMarkup()
sortMenuKb.row(sortByPriceIncrBtn, sortByPriceDecrBtn).row(sortByDurationIncrBtn, sortByDurationDecrBtn).add(dontSortBtn).add(returnToMainMenuBtn)

returnToFiltersMenuBtn = InlineKeyboardButton('Повернутися на меню вибору фільтрів', callback_data='returnToFilterMenuCb')
filterSelectionKb = InlineKeyboardMarkup()
filterSelectionKb.add(returnToFiltersMenuBtn)

selectDurationFromBtn = InlineKeyboardButton('Обрати мінімальну тривалість', callback_data='selectDurationFromCb')
selectDurationToBtn = InlineKeyboardButton('Обрати максимальну тривалість', callback_data='selectDurationToCb')
durationSelectionKb = InlineKeyboardMarkup()
durationSelectionKb.add(selectDurationFromBtn).add(selectDurationToBtn).add(returnToFiltersMenuBtn)

selectPriceFromBtn = InlineKeyboardButton('Обрати мінімальну вартість', callback_data='selectPriceFromCb')
selectPriceToBtn = InlineKeyboardButton('Обрати максимальну вартість', callback_data='selectPriceToCb')
priceSelectionKb = InlineKeyboardMarkup()
priceSelectionKb.add(selectPriceFromBtn).add(selectPriceToBtn).add(returnToFiltersMenuBtn)

returnToDurationFilterMenuBtn = InlineKeyboardButton('Повернутися на меню вибору тривалості туру', callback_data='returnToDurationFilterMenuCb')
returnToDurationFilterMenuKb = InlineKeyboardMarkup()
returnToDurationFilterMenuKb.add(returnToDurationFilterMenuBtn)

returnToPriceFilterMenuBtn = InlineKeyboardButton('Повернутися на меню вибору вартості туру', callback_data='returnToPriceFilterMenuCb')
returnToPriceFilterMenuKb = InlineKeyboardMarkup()
returnToPriceFilterMenuKb.add(returnToPriceFilterMenuBtn)

returnToFiltersMenuKb = InlineKeyboardMarkup()
returnToFiltersMenuKb.add(returnToFiltersMenuBtn)

returnToSortMenuBtn = InlineKeyboardButton('Повернутися на меню вибору сортування', callback_data='returnToSortMenuCb')
sortSelectionKb = InlineKeyboardMarkup()
sortSelectionKb.add(returnToSortMenuBtn)