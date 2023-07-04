from pybotterfly.message_handler.message_handler import MessageHandler
from configs.config import BASE_CONFIG
from configs.transitions.transitions_config import transitions
from lib.users import (
    get_user_stage,
    change_user_stage,
    get_user_access_level,
    change_user_access_level,
)


message_handler = MessageHandler(
    transitions=transitions,  # Transitions of Transitions class
    user_stage_getter=get_user_stage,  # :Coroutine. Function to get user’s stage. Should contain ‘user_messenger_id’ and ‘user_messenger’ args.
    user_stage_changer=change_user_stage,  # :Coroutine. Function to change user’s stage. Should contain 'to_stage_id', ‘user_messenger_id’ and ‘user_messenger’ args.
    user_access_level_getter=get_user_access_level,  # :Coroutine. [Optional] Function to get user’s access level. Should contain ‘user_messenger_id’ and ‘user_messenger’ args.
    user_access_level_changer=change_user_access_level,  # :Coroutine. [Optional] Function to change user’s access level. Should contain 'tu_access_level', ‘user_messenger_id’ and ‘user_messenger’ args.
    base_config=BASE_CONFIG,  # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)
