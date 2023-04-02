from pybotterfly.message_handler.message_handler import MessageHandler
from configs.config import BASE_CONFIG
from configs.transitions.transitions_config import transitions
from lib.users import get_user_stage


message_handler = MessageHandler(
    user_stage_getter=get_user_stage,
    transitions=transitions,
    base_config=BASE_CONFIG,
)
