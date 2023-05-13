from aiogram.utils import executor
from handlers import engine
from create_bot import dp
import db_operations

async def onStartup(_):
    print('Bot has been launched successfully.')
    db_operations.sqlStart()

engine.registerHandlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=onStartup)