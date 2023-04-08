from configs.config import BASE_CONFIG, LOCAL_IP, LOCAL_PORT, TEST_ID_TG
from configs.messengers_configs.tg_config import dp
from pybotterfly.runners.tg_client import start_tg_client, run_test

start_tg_client(
    dispatcher=dp,  # Your preconfigured TG Dispatcher
    handler_ip=LOCAL_IP,  # :str. Your local ip
    handler_port=LOCAL_PORT,  # :int. Your local port
    base_config=BASE_CONFIG,  # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
)

# run_test(
#     test_id=TEST_ID_TG,  # :int. You TG id for testing
#     messages_amount=30,  # :int. Amount of test messages
#     dispatcher=dp,  # Your preconfigured TG Dispatcher
#     handler_ip=LOCAL_IP,  # :str. Your local ip
#     handler_port=LOCAL_PORT,  # :int. Your local port
#     base_config=BASE_CONFIG,  # [Optional] specify your base config of BaseConfig class if there are any changes. Defaults to BaseConfig
# )
