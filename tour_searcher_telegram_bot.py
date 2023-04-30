from aiogram.utils import executor
from handlers import engine
from create_bot import dp

async def on_startup(_):
    print('Bot has been launched successfully.')

engine.register_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)