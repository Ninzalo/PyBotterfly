import sys
from loguru import logger
from vkbottle import API
from vkbottle.bot import Bot
from configs.config import token_vk

bot = Bot(token=token_vk)
api = API(token=token_vk)
logger.remove()
logger.add(sys.stderr, level="INFO")
