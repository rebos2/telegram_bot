import logging

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: Update, data: dict):
        logging.info("[------------------Новый апдейт!------------------]")
        logging.info("1. Pre Process Update")
        logging.info("Следующая точка: Process Update")
        data["middleware_data"] = "Это пройдет до on_process_update"

        banned_users = [1234567]