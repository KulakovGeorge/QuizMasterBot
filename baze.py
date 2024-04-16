import asyncio
import aiosqlite

NAME_BD = 'quiz_bot.db'

async def init_table(): # Инициализация Базы Данных
    async with aiosqlite.connect(NAME_BD) as bd:
        query = 'CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, quest INTEGER, state INTEGER)'
        await bd.execute(query)
        await bd.commit()
        query = 'CREATE TABLE IF NOT EXISTS quiz_final_state (user_id INTEGER PRIMARY KEY, state INTEGER)'
        await bd.execute(query)
        await bd.commit()

async def quiz_update(user, quest = 0, state = 0): # Добавление/Обновление записи в таблице с информация о стадии квиза
    async with aiosqlite.connect(NAME_BD) as bd:
        query = 'INSERT OR REPLACE INTO quiz_state (user_id, quest, state) VALUES (?, ?, ?)'
        await bd.execute(query, (user, quest, state))
        await bd.commit()
async def quiz_get_index(user): # Получение индекса вопроса квиза
    async with aiosqlite.connect(NAME_BD) as bd:
        query = 'SELECT * FROM quiz_state WHERE user_id = (?)'
        async with bd.execute(query, (user, )) as cursor:
            result = await cursor.fetchone()
            if result is not None:
                return result[1]
            return 0
async def quiz_get_state(user): # Получение счета квиза
    async with aiosqlite.connect(NAME_BD) as bd:
        query = 'SELECT * FROM quiz_state WHERE user_id = (?)'
        async with bd.execute(query, (user, )) as cursor:
            result = await cursor.fetchone()
            if result is not None:
                return result[2]
            return 0
        
async def quiz_set_final_state(user, state): # Установка нового результата квиза
    async with aiosqlite.connect(NAME_BD) as bd:
        query = 'INSERT OR REPLACE INTO quiz_final_state (user_id, state) VALUES (?, ?)'
        await bd.execute(query, (user, state))
        await bd.commit()        
async def quiz_get_final_state(user): # Получение последнего результата квиза
    async with aiosqlite.connect(NAME_BD) as bd:
        query = 'SELECT state FROM quiz_final_state WHERE user_id = (?)'
        async with bd.execute(query, (user, )) as cursor:
            result = await cursor.fetchone()
            return result
async def quiz_list_state(): # Получение списка игроков со счетам прохождения
    async with aiosqlite.connect(NAME_BD) as bd:
        query = 'SELECT * FROM quiz_final_state ORDER BY state DESC LIMIT 10'
        async with bd.execute(query) as cursor:
            result = await cursor.fetchall()
            return result
