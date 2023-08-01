from pybotterfly.message_handler.message_handler import MessageHandler
from pybotterfly.message_handler.struct import Func

from configs.config import BASE_CONFIG
from configs.logger import logger
from configs.transitions.transitions_config import transitions
from lib.users import (
    get_user_stage,
    change_user_stage,
    get_user_access_level,
    change_user_access_level,
)


message_handler = MessageHandler(
    transitions=transitions,  # :Transitions. Transitions of Transitions class
    user_stage=Func(
        getter=get_user_stage,  # :Coroutine. A coroutine to get user’s stage. Should contain ‘user_messenger_id’ and ‘user_messenger’ args.
        setter=change_user_stage,  # :Coroutine. A coroutine to change user’s stage. Should contain 'to_stage_id', ‘user_messenger_id’ and ‘user_messenger’ args.
    ),
    # [Optional]
    user_access_level=Func(
        getter=get_user_access_level,  # :Coroutine. [Optional] A coroutine to get user’s access level. Should contain ‘user_messenger_id’ and ‘user_messenger’ args.
        setter=change_user_access_level,  # :Coroutine. [Optional] A coroutine to change user’s access level. Should contain 'to_access_level', ‘user_messenger_id’ and ‘user_messenger’ args.
    ),
    base_config=BASE_CONFIG,  # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    logger=logger,  # :BaseLogger. [Optional] specify your logger of BaseLogger class if there are any changes
)
