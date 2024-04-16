import asyncio
import logging

import baze, cmd
from aiogram import Bot

API_TOKEN = '7188611203:AAGEVispLx22rLLBCmJ0bYGE4O7ZxlIPBts'
bot = Bot(token = API_TOKEN)

async def main():
    logging.basicConfig(level=logging.INFO)
    
    await baze.init_table()
    await cmd.DisPatch.start_polling(bot)

asyncio.run(main())
