from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.inline import kb_start


async def admin_start(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Привет мой господин 👑\n"
                         "Чем я могу помочь ❓", reply_markup=kb_start)


async def admin_help(message: Message):
    await message.answer("👑👑👑")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(admin_help, commands=["help"], state="*", is_admin=True)
