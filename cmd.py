import asyncio, quiz
from aiogram import Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

DisPatch = Dispatcher()

@DisPatch.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Начать квиз'))
    await message.answer("Добро пожаловать!", reply_markup=builder.as_markup(resize_keyboard=True))        

@DisPatch.message(F.text == 'Начать квиз')
async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнем квиз!", reply_markup=types.ReplyKeyboardRemove())
    await quiz.quiz_start(message)

@DisPatch.callback_query(lambda c: c.data.startswith('quiz_quest_button_'))
async def quest_true(data : types.CallbackQuery):
    otvet = data.data.split('_')[3]
    await data.bot.edit_message_text(
        text = data.message.text + f"\nВаш ответ:{otvet}",
        chat_id = data.from_user.id,
        message_id = data.message.message_id,
        reply_markup = None
    )
    data_quest = await quiz.get_data_quest(await quiz.get_quest_index(data.from_user.id))
    if data_quest['options'][data_quest['correct_option']] == otvet:
        new_index = await quiz.get_quest_index(data.from_user.id) + 1
        new_state = await quiz.get_quest_state(data.from_user.id) + 1
    else:
        new_index = await quiz.get_quest_index(data.from_user.id) + 1
        new_state = await quiz.get_quest_state(data.from_user.id)
    if new_index < len(quiz.Data):
        await quiz.set_quest_data(data.from_user.id, new_index, new_state)
        await quiz.quiz_question(data.message, data.from_user.id)
    else:
        await data.message.answer(f'Конец квиза. Ваш счет:{new_state}')
