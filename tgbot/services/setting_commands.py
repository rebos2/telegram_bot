from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat


async def set_default_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand("start", "Начать заново"),
            BotCommand("help", "Помощь"),
            BotCommand("test", "Тестирование"),
            # BotCommand("delete_commands", "Удалить команды")
        ],
        scope=BotCommandScopeDefault()
    )


async def set_starting_commands(bot: Bot, chat_id: int):
    STARTING_COMMANDS = {
        "ru": [
            BotCommand("start", "Начать заново"),
            BotCommand("get_commands", "Получить список команд"),
            BotCommand("reset_comands", "Сбросить команды"),
        ],
        "en": [
            BotCommand("start", "Restart bot"),
            BotCommand("get_commands", "Retrive command list"),
            BotCommand("reset_comands", "Reset commands"),
        ]
    }
    for language_code, commands in STARTING_COMMANDS.items():
        await bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeChat(chat_id),
            language_code=language_code
        )
