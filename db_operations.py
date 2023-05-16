import pypyodbc

server = 'NZRSVT\SQLEXPRESS' 
database = 'Travel_Site' 

def sqlStart():
    global base, cur
    base = pypyodbc.connect('Driver={SQL Server};'
                        'Server=' + server + ';'
                        'Database=' + database + ';'
                        'Trusted_Connection=yes;')
    cur = base.cursor()
    if base:
        print("Database connected successfully.")

def sqlAddNewUser(telegramId, userName):
    cur.execute('INSERT INTO telegram_user_selections VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (telegramId, userName, "none", "none", -1, 999999, -1, 999999, "none"))
    base.commit()

def sqlCheckTelegramId(id):
    if cur.execute('SELECT selected_country FROM telegram_user_selections WHERE telegram_id = ?', (id,)).fetchone() != None:
        return cur.execute('SELECT selected_country FROM telegram_user_selections WHERE telegram_id = ?', (id,)).fetchone()[0]
    else:
        return "no_id"
    
def sqlSelectTours(telegramId):
    result = cur.execute('SELECT * FROM Trip_Info').fetchall()
    if sqlSelectUserCountry(telegramId) != 'none':
        result = [tour for tour in result if sqlSelectUserCountry(telegramId) in tour[1]]
    if sqlSelectUserCity(telegramId) != 'none':
        result = [tour for tour in result if sqlSelectUserCity(telegramId) in tour[2]]
    if sqlSelectUserDurationFrom(telegramId) != -1:
        result = [tour for tour in result if sqlSelectUserDurationFrom(telegramId) <= tour[3]]
    if sqlSelectUserDurationTo(telegramId) != 999999:
        result = [tour for tour in result if sqlSelectUserDurationTo(telegramId) >= tour[3]]
    if sqlSelectUserPriceFrom(telegramId) != -1:
        result = [tour for tour in result if sqlSelectUserPriceFrom(telegramId) <= tour[5]]
    if sqlSelectUserPriceTo(telegramId) != 999999:
        result = [tour for tour in result if sqlSelectUserPriceTo(telegramId) >= tour[5]]
    tempSortType = sqlSelectUserSort(telegramId)
    if tempSortType == 'sortByDurationIncrCb':
        result = sorted(result, key=lambda x: x[3])
    elif tempSortType == 'sortByDurationDecrCb':
        result = sorted(result, key=lambda x: x[3], reverse=True)
    elif tempSortType == 'sortByPriceIncrCb':
        result = sorted(result, key=lambda x: x[5])
    elif tempSortType == 'sortByPriceDecrCb':
        result = sorted(result, key=lambda x: x[5], reverse=True)
    return result

def sortTypeSet(telegramId, sortType):
    cur.execute('UPDATE telegram_user_selections SET selected_sort = ? WHERE telegram_id = ?', (sortType, telegramId))
    base.commit()

def selectedCountrySet(telegramId, country):
    cur.execute('UPDATE telegram_user_selections SET selected_country = ? WHERE telegram_id = ?', (country, telegramId))
    base.commit()

def selectedCitySet(telegramId, city):
    cur.execute('UPDATE telegram_user_selections SET selected_city = ? WHERE telegram_id = ?', (city, telegramId))
    base.commit()

def selectedDurationFromSet(telegramId, durationFrom):
    cur.execute('UPDATE telegram_user_selections SET selected_duration_from = ? WHERE telegram_id = ?', (durationFrom, telegramId))
    base.commit()

def selectedDurationToSet(telegramId, durationTo):
    cur.execute('UPDATE telegram_user_selections SET selected_duration_to = ? WHERE telegram_id = ?', (durationTo, telegramId))
    base.commit()

def selectedPriceFromSet(telegramId, priceFrom):
    cur.execute('UPDATE telegram_user_selections SET selected_price_from = ? WHERE telegram_id = ?', (priceFrom, telegramId))
    base.commit()

def selectedPriceToSet(telegramId, priceTo):
    cur.execute('UPDATE telegram_user_selections SET selected_price_to = ? WHERE telegram_id = ?', (priceTo, telegramId))
    base.commit()

def selectedCountryClear(telegramId):
    cur.execute('UPDATE telegram_user_selections SET selected_country = ? WHERE telegram_id = ?', ("none", telegramId))
    base.commit()

def selectedCityClear(telegramId):
    cur.execute('UPDATE telegram_user_selections SET selected_city = ? WHERE telegram_id = ?', ("none", telegramId))
    base.commit()

def selectedDurationClear(telegramId):
    cur.execute('UPDATE telegram_user_selections SET selected_duration_from = ? WHERE telegram_id = ?', (-1, telegramId))
    base.commit()
    cur.execute('UPDATE telegram_user_selections SET selected_duration_to = ? WHERE telegram_id = ?', (999999, telegramId))
    base.commit()

def selectedPriceClear(telegramId):
    cur.execute('UPDATE telegram_user_selections SET selected_price_from = ? WHERE telegram_id = ?', (-1, telegramId))
    base.commit()
    cur.execute('UPDATE telegram_user_selections SET selected_price_to = ? WHERE telegram_id = ?', (999999, telegramId))
    base.commit()

def selectedAllClear(telegramId):
    selectedCountryClear(telegramId)
    selectedCityClear(telegramId)
    selectedDurationClear(telegramId)
    selectedPriceClear(telegramId)

def sqlSelectUserCountry(telegramId):
    return cur.execute('SELECT selected_country FROM telegram_user_selections WHERE telegram_id = ?', (telegramId, )).fetchone()[0]

def sqlSelectUserCity(telegramId):
    return cur.execute('SELECT selected_city FROM telegram_user_selections WHERE telegram_id = ?', (telegramId, )).fetchone()[0]

def sqlSelectUserDurationFrom(telegramId):
    return cur.execute('SELECT selected_duration_from FROM telegram_user_selections WHERE telegram_id = ?', (telegramId, )).fetchone()[0]

def sqlSelectUserDurationTo(telegramId):
    return cur.execute('SELECT selected_duration_to FROM telegram_user_selections WHERE telegram_id = ?', (telegramId, )).fetchone()[0]

def sqlSelectUserPriceFrom(telegramId):
    return cur.execute('SELECT selected_price_from FROM telegram_user_selections WHERE telegram_id = ?', (telegramId, )).fetchone()[0]

def sqlSelectUserPriceTo(telegramId):
    return cur.execute('SELECT selected_price_to FROM telegram_user_selections WHERE telegram_id = ?', (telegramId, )).fetchone()[0]

def sqlSelectUserSort(telegramId):
    return cur.execute('SELECT selected_sort FROM telegram_user_selections WHERE telegram_id = ?', (telegramId, )).fetchone()[0]

def checkFiltersSelected(telegramId):
    if sqlSelectUserCountry(telegramId) != 'none':
        return 'True'
    elif sqlSelectUserCity(telegramId) != 'none':
        return 'True'
    elif sqlSelectUserDurationFrom(telegramId) != -1:
        return 'True'
    elif sqlSelectUserDurationTo(telegramId) != 999999:
        return 'True'
    elif sqlSelectUserPriceFrom(telegramId) != -1:
        return 'True'
    elif sqlSelectUserPriceTo(telegramId) != 999999:
        return 'True'
    else:
        return 'False'

def returnSelectedFilters(telegramId):   
    result = "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n"
    tempSelection = sqlSelectUserCountry(telegramId)
    if tempSelection != 'none':
        result += "🌍Обрана країна: " + tempSelection + ";\n"
    tempSelection = sqlSelectUserCity(telegramId)
    if tempSelection != 'none':
        result += "🚩Обране місто: " + tempSelection + ";\n"
    tempSelection = sqlSelectUserDurationFrom(telegramId)
    tempSelection2 = sqlSelectUserDurationTo(telegramId)
    if (tempSelection != -1) and (tempSelection2 != 999999):
        result += "📆Обрана тривалість: від " + str(tempSelection) + " до " + str(tempSelection2) + " діб;\n"
    elif tempSelection != -1:
        result += "📆Обрана мінімальна тривалість:  " + str(tempSelection) + " діб;\n"
    elif tempSelection2 != 999999:
        result += "📆Обрана максимальна тривалість:  " + str(tempSelection2) + " діб;\n"
    tempSelection = sqlSelectUserPriceFrom(telegramId)
    tempSelection2 = sqlSelectUserPriceTo(telegramId)
    if (tempSelection != -1) and (tempSelection2 != 999999):
        result += "💵Обрана вартість: від " + str(tempSelection) + " до " + str(tempSelection2) + " грн.\n"
    elif tempSelection != -1:
        result += "💵Обрана мінімальна вартість:  " + str(tempSelection) + " грн.\n"
    elif tempSelection2 != 999999:
        result += "💵Обрана максимальна вартість:  " + str(tempSelection2) + " грн.\n"
    result += "〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️"
    return result

def returnSelectedSortName(telegramId):
    sort = sqlSelectUserSort(telegramId)
    if sort == 'sortByPriceIncrCb':
        return "зростанням вартості"
    elif sort == 'sortByPriceDecrCb':
        return "спаданням вартості"
    elif sort == 'sortByDurationIncrCb':
        return "зростанням тривалості"
    elif sort == 'sortByDurationDecrCb':
        return "спаданням тривалості"