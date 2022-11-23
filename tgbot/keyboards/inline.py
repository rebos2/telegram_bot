from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_start = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text="Показать базу 📚", callback_data="show_base")
).row(
    InlineKeyboardButton(text="Узнать погоду ☂", callback_data="show_weather"),
    InlineKeyboardButton(text="Узнать BTC price 💲", callback_data="btc_price")
)
