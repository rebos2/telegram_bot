from datetime import datetime

import requests
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, BotCommandScopeChat, CallbackQuery
from aiogram.utils.markdown import quote_html

from tgbot.keyboards.inline import kb_start
from tgbot.misc.states import Weather


async def user_start(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Привет 🍪\n"
                         "Чем я могу помочь ❓", reply_markup=kb_start)


async def user_help(message: Message):
    await message.answer("🍪🍪🍪")


async def show_base(callback: CallbackQuery):
    await callback.answer(cache_time=5)
    await callback.message.answer("В разработке ⏳")


async def show_weather(callback: CallbackQuery):
    await callback.answer(cache_time=5)
    await callback.message.answer("Введите название города 🔍\n⬇⬇⬇")
    await Weather.input_city.set()


async def weather_info(message: Message, state: FSMContext):
    token = message.bot.get("config").misc.weather_token
    code_to_smile = {
        "Thunderstorm": "Гроза 🌩",
        "Drizzle": "Небольшой дождь ☔",
        "Rain": "Дождь 🌧",
        "Snow": "Снег ❄",
        "Clear": "Ясно ☀",
        "Clouds": "Облачно ☁",
    }

    try:
        req = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={message.text}&appid={token}")
        lat = req.json()[0]["lat"]
        lon = req.json()[0]["lon"]
        req = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={token}&units=metric")
        name = req.json()["name"]
        temp = req.json()["main"]["temp"]
        humidity = req.json()["main"]["humidity"]
        pressure = req.json()["main"]["pressure"]
        wind_speed = req.json()["wind"]["speed"]
        sunrise = datetime.fromtimestamp(req.json()['sys']['sunrise'])
        sunset = datetime.fromtimestamp(req.json()['sys']['sunset'])

        if req.json()["weather"][0]["main"] in code_to_smile:
            weather_smile = code_to_smile[f'{req.json()["weather"][0]["main"]}']
        else:
            weather_smile = "Выгляни в окно, не пойму что там за погода 🙄"

        await message.answer(f"*** {datetime.now().strftime('%Y-%m-%d %H:%M')} ***\n"
                             f"Город: {name}\n"
                             f"Температура: {temp} C° {weather_smile}\n"
                             f"Влажность: {humidity} %\n"
                             f"Давление: {pressure} мм. рт. ст.\n"
                             f"Скорость ветра: {wind_speed} м/c\n"
                             f"Рассвет: {sunrise.strftime('%H:%M')}\n"
                             f"Закат: {sunset.strftime('%H:%M')}\n"
                             f"Продолжительность светового дня: {sunset - sunrise}"
                             )
    except Exception:
        await message.answer("Что-то пошло не так🤨\nПроверь название города")

    await state.finish()


async def btc_price(callback: CallbackQuery):
    await callback.answer(cache_time=5)
    try:
        req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
        sell_price = req.json()["btc_usd"]["sell"]
        await callback.message.answer(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price: {sell_price}💵")
    except Exception as ex:
        print(ex)
        await callback.message.answer("Не получилось🥺\nпопробуйте в другой раз ")


async def delete_commands(message: Message):
    # await message.bot.delete_my_commands(scope=BotCommandScopeChat(message.from_user.id), language_code="ru")
    no_args = await message.bot.get_my_commands()
    no_lang = await message.bot.get_my_commands(scope=BotCommandScopeChat(message.from_user.id))
    ru_lang = await message.bot.get_my_commands(scope=BotCommandScopeChat(message.from_user.id),
                                                language_code="ru")

    await message.reply("\n\n".join(
        f'<pre>{quote_html(arg)}</>' for arg in (no_args, no_lang, ru_lang)
    ))


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(user_help, commands=["help"], state="*")
    dp.register_callback_query_handler(show_base, text="show_base")
    dp.register_callback_query_handler(show_weather, text="show_weather")
    dp.register_message_handler(weather_info, state=Weather.input_city)
    dp.register_callback_query_handler(btc_price, text="btc_price")
    dp.register_message_handler(delete_commands, commands=["delete_commands"])
