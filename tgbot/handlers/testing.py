from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.misc.states import Test


async def test(message: Message):
    await message.answer("Тестовых работ не проводится 💤")

    # await message.answer("Вход в Тест\n\n"
    #                      "Напишите что-то")
    # await Test.Q1.set()


async def state_q1(message: Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data["1"] = answer
    await message.answer("Напишите еще что-то")
    await Test.Q2.set()


async def state_q2(message: Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("1")
    answer2 = message.text
    await message.answer(f"Первая запись: {answer1}\n"
                         f"Вторая запись: {answer2}")
    await state.finish()


def register_testing(dp: Dispatcher):
    dp.register_message_handler(test, commands=["test"], state="*", is_admin=True)
    dp.register_message_handler(state_q1, state=Test.Q1, is_admin=True)
    dp.register_message_handler(state_q2, state=Test.Q2, is_admin=True)
