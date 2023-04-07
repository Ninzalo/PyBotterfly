from pybotterfly.message_handler.message_handler import MessageHandler
from configs.config import BASE_CONFIG
from configs.transitions.transitions_config import transitions
from lib.users import get_user_stage


message_handler = MessageHandler(
    user_stage_getter=get_user_stage, # :Coroutine. Function to get user’s stage. Should contain ‘user_messenger_id’ and ‘user_messenger’ args.
    transitions=transitions, # Transitions of Transitions class
    base_config=BASE_CONFIG, # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)
