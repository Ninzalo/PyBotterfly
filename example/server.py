from configs.config import (
    BASE_CONFIG,
    LOCAL_IP,
    LOCAL_PORT,
)
from configs.reply.reply_config import messengers
from configs.message_handler.message_handler_config import message_handler
from pybotterfly.server.server import run_server

run_server(
    messengers=messengers,  # :MessengersDivision. An instance of preconfigured MessengersDivision class
    message_handler=message_handler,  # :MessageHandler. An instance of preconfigured MessageHandler class
    local_ip=LOCAL_IP,  # :str. Your local ip
    local_port=LOCAL_PORT,  # :int. Your local port
    base_config=BASE_CONFIG,  # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)
