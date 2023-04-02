from pybotterfly.bot.reply.reply_division import MessengersDivision
from pybotterfly.bot.reply.default_reply_types import (
    DefaultVkReplier,
    DefaultTgReplier,
)
from configs.messengers_configs.tg_config import bot
from configs.messengers_configs.vk_config import api
from configs.config import BASE_CONFIG

messengers = MessengersDivision(config=BASE_CONFIG)
messengers.register_messenger(
    trigger="tg",
    reply_func=DefaultTgReplier(tg_bot=bot, config=BASE_CONFIG).tg_answer,
    messages_per_second=4,
)
messengers.register_messenger(
    trigger="vk",
    reply_func=DefaultVkReplier(vk_api=api, config=BASE_CONFIG).vk_answer,
    messages_per_second=4,
)
messengers.compile()
