from configs.config import (
    BASE_CONFIG,
    LOCAL_IP,
    LOCAL_PORT,
)
from configs.reply.reply_config import messengers
from configs.message_handler.message_handler_config import message_handler
from pybotterfly.runners.server import run_server

run_server(
    messengers=messengers,
    message_handler=message_handler,
    local_ip=LOCAL_IP,
    local_port=LOCAL_PORT,
    base_config=BASE_CONFIG,
)
