from configs.config import BASE_CONFIG, LOCAL_IP, LOCAL_PORT, TEST_ID_VK
from configs.messengers_configs.vk_config import bot
from pybotterfly.runners.vk_client import start_vk_client, run_test

start_vk_client(
    handler=bot,
    handler_ip=LOCAL_IP,
    handler_port=LOCAL_PORT,
    base_config=BASE_CONFIG,
)

# run_test(
#     test_id=TEST_ID_VK,
#     messages_amount=30,
#     handler=bot,
#     handler_ip=LOCAL_IP,
#     handler_port=LOCAL_PORT,
#     base_config=BASE_CONFIG,
# )
