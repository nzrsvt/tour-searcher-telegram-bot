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
    cur.execute('INSERT INTO telegram_user_selections VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (telegramId, userName, "none", "none", -1, 999, -1, 9999999, "none"))
    base.commit()

def sqlCheckTelegramId(id):
    if cur.execute('SELECT selected_country FROM telegram_user_selections WHERE telegram_id = ?', (id,)).fetchone() != None:
        return cur.execute('SELECT selected_country FROM telegram_user_selections WHERE telegram_id = ?', (id,)).fetchone()[0]
    else:
        return "no_id"
    
def sqlSelectAllTours():
    return cur.execute('SELECT * FROM Trip_Info').fetchall()

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