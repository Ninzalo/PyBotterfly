from configs.config import BASE_CONFIG, LOCAL_IP, LOCAL_PORT, TEST_ID_TG
from configs.messengers_configs.tg_config import dp
from pybotterfly.runners.tg_client import start_tg_client, run_test

start_tg_client(
    dispatcher=dp,
    handler_ip=LOCAL_IP,
    handler_port=LOCAL_PORT,
    base_config=BASE_CONFIG,
)

# run_test(
#     test_id=TEST_ID_TG,
#     dispatcher=dp,
#     handler_ip=LOCAL_IP,
#     handler_port=LOCAL_PORT,
#     messages_amount=30,
#     base_config=BASE_CONFIG,
# )
