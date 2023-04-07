from pybotterfly.bot.reply.reply_division import MessengersDivision
from pybotterfly.bot.reply.default_reply_types import (
    DefaultVkReplier,
    DefaultTgReplier,
)
from configs.messengers_configs.tg_config import bot
from configs.messengers_configs.vk_config import api
from configs.config import BASE_CONFIG

messengers = MessengersDivision(
        config=BASE_CONFIG # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)
messengers.register_messenger(
    trigger="tg", # :str. The variable by which the separation occurs
    reply_func=DefaultTgReplier(
        tg_bot=bot, # An instance of preconfigured TG bot 
        config=BASE_CONFIG # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    ).tg_answer, # : Coroutine. A function that sends message to the user
    messages_per_second=4, # :int. Message reply rate in messages per second
)
messengers.register_messenger(
    trigger="vk",
    reply_func=DefaultVkReplier(vk_api=api, config=BASE_CONFIG).vk_answer,
    messages_per_second=4,
)
messengers.compile()
