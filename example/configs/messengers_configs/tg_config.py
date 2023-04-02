import logging
from aiogram import Bot, Dispatcher
from configs.config import token_tg

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token_tg)
dp = Dispatcher(bot)
