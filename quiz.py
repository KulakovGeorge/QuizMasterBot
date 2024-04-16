import baze, json
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

Data = []

with open('quiz.json', 'r') as file:
    Data = json.load(file)

async def quiz_start(message):
    user = message.from_user.id
    await baze.quiz_update(user)
    await quiz_question(message, user)

async def quiz_question(message, user):
    index = await baze.quiz_get_index(user)
    data = await get_data_quest(index)
    buts = InlineKeyboardBuilder()
    for opt in data['options']:
        buts.add(types.InlineKeyboardButton(
            text = opt,
            callback_data="quiz_quest_button_" + opt
            ))
    buts.adjust(2)
    await message.answer(data['question'], reply_markup=buts.as_markup())

async def get_data_quest(index):
    return Data[index]

    


