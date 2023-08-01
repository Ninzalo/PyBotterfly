from pybotterfly.runners.vk_client import start_vk_client, run_test

from configs.config import BASE_CONFIG, LOCAL_IP, LOCAL_PORT, TEST_ID_VK
from configs.logger import logger
from configs.messengers_configs.vk_config import bot

start_vk_client(
    handler=bot,  # :Bot. Your preconfigured VK Bot
    handler_ip=LOCAL_IP,  # :str. Your local ip
    handler_port=LOCAL_PORT,  # :int. Your local port
    base_config=BASE_CONFIG,  # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
    logger=logger,  # :BaseLogger. [Optional] specify your logger of BaseLogger class if there are any changes.
)

# run_test(
#     test_id=TEST_ID_VK,  # :int. You VK id for testing
#     messages_amount=30,  # :int. Amount of test messages
#     handler=bot,  # :Bot. Your preconfigured VK Bot
#     handler_ip=LOCAL_IP,  # :str. Your local ip
#     handler_port=LOCAL_PORT,  # :int. Your local port
#     base_config=BASE_CONFIG,  # :BaseConfig. [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
#     logger=logger,  # :BaseLogger. [Optional] specify your logger of BaseLogger class if there are any changes.
# )
