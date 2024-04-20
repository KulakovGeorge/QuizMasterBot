import asyncio, baze, quiz
from aiogram import Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

DisPatch = Dispatcher()

ButQuiz = ReplyKeyboardBuilder()
ButNone = types.ReplyKeyboardRemove()

ButQuiz.add(types.KeyboardButton(text='Начать квиз'))

@DisPatch.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать!", reply_markup=ButQuiz.as_markup(resize_keyboard=True))        

@DisPatch.message(F.text == 'Начать квиз')
@DisPatch.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    text = "Давайте начнем квиз!\n"
    state = await baze.quiz_get_final_state(message.from_user.id)
    if state is not None:
        text += "Ваш прошлый результат: " + str(state[0])
    await message.answer(text, reply_markup=ButNone)
    await quiz.quiz_start(message)
    
@DisPatch.message(F.text == 'Список лидеров')
@DisPatch.message(Command('list'))
async def cmd_list(message: types.Message):
    await message.answer("Список 10 лидеров прохождения квиза:")
    text = ""
    for item in await baze.quiz_list_state():
        user = await message.bot.get_chat(item[0])
        text += f"{user.first_name} {user.last_name}: {item[1]}\n"
    await message.answer(text)
     
@DisPatch.callback_query(lambda c: c.data.startswith('quiz_quest_button_'))
async def quest_true(data : types.CallbackQuery):
    otvet = data.data.split('_')[3]
    await data.bot.edit_message_text(
        text = data.message.text + f"\nВаш ответ:{otvet}",
        chat_id = data.from_user.id,
        message_id = data.message.message_id,
        reply_markup = None
    )
    data_quest = await quiz.get_data_quest(await baze.quiz_get_index(data.from_user.id))
    if data_quest['options'][data_quest['correct_option']] == otvet:
        new_index = await baze.quiz_get_index(data.from_user.id) + 1
        new_state = await baze.quiz_get_state(data.from_user.id) + 1
    else:
        new_index = await baze.quiz_get_index(data.from_user.id) + 1
        new_state = await baze.quiz_get_state(data.from_user.id)
    if new_index < len(quiz.Data):
        await baze.quiz_update(data.from_user.id, new_index, new_state)
        await quiz.quiz_question(data.message, data.from_user.id)
    else:
        await data.message.answer(f'Конец квиза. Ваш счет:{new_state}', reply_markup=ButQuiz.as_markup(resize_keyboard=True))
        await baze.quiz_set_final_state(data.from_user.id, new_state)
