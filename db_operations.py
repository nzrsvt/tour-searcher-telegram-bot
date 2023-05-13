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

