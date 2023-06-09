import json
import asyncio
from datetime import datetime
from pybotterfly.base_config import BaseConfig
from pybotterfly.bot.struct import MessageStruct
from pybotterfly.server.server_func import send_to_server

# Vk async library
from vkbottle import GroupEventType
from vkbottle.bot import Message, MessageEvent, Bot


class VkClient:
    def __init__(
        self,
        handler: Bot,
        local_ip: str,
        local_port: int,
        base_config: BaseConfig = BaseConfig,
    ) -> None:
        self._bot = handler
        self._local_ip = local_ip
        self._local_port = local_port
        self._config = base_config
        self._testing = False
        self._bot.on.raw_event(
            GroupEventType.MESSAGE_EVENT, dataclass=MessageEvent
        )(self.handle_callback_event)
        self._bot.on.message()(self.handle_message_event)

    async def handle_callback_event(self, event: MessageEvent):
        user_id = int(event.object.user_id)
        payload = event.object.payload
        message = MessageStruct(
            user_id=user_id, messenger="vk", payload=payload
        )
        await send_to_server(
            message=message,
            local_ip=self._local_ip,
            local_port=self._local_port,
        )

    async def handle_message_event(self, event: Message):
        if event.payload:
            payload = json.loads(event.payload)
        else:
            payload = None
        message = MessageStruct(
            user_id=int(event.from_id),
            messenger="vk",
            text=event.text,
            payload=payload,
        )
        await send_to_server(
            message=message,
            local_ip=self._local_ip,
            local_port=self._local_port,
        )

    def start_vk_bot(self):
        if self._testing:
            print(f"[ERROR] Ensure not to run test")
            return
        print(
            f"VK listening started"
            f"{' in Debug mode' if self._config.DEBUG_STATE else ''}"
        )
        self._bot.run_forever()

    async def test_messages(self, test_id: int, messages_amount: int):
        test_start_time = datetime.now()
        if not self._config.DEBUG_STATE:
            print(f"Failed to run test (running not in Debug mode)")
            return
        print(f"Rate test started at {test_start_time}")
        for num in range(1, messages_amount + 1):
            message_struct = MessageStruct(
                user_id=test_id, messenger="vk", text=f"{num}"
            )
            await send_to_server(
                message=message_struct,
                local_ip=self._local_ip,
                local_port=self._local_port,
            )
        print(
            f"Rate test to {test_id} with {messages_amount} messages finished "
            f"in {(datetime.now() - test_start_time).total_seconds()} seconds"
        )

    def run_test(self, test_id: int, messages_amount: int) -> None:
        self._testing = True
        asyncio.run(
            self.test_messages(
                test_id=test_id, messages_amount=messages_amount
            )
        )


def start_vk_client(
    handler: Bot,
    handler_ip: str,
    handler_port: int,
    base_config: BaseConfig = BaseConfig,
) -> None:
    """
    Initialize and start a VK client bot.

    :param handler: Bot object that will be used to handle incoming messages
    :type handler: Bot

    :param handler_ip: The local IP address of the handler that will
        receive incoming messages
    :type handler_ip: str

    :param handler_port: The local port number of the handler that will
        receive incoming messages
    :type handler_port: int

    :param base_config: BaseConfig object containing VK API settings
    :type base_config: BaseConfig, optional

    :return: None
    :rtype: NoneType
    """

    vk_client = _get_vk_client(
        handler=handler,
        handler_ip=handler_ip,
        handler_port=handler_port,
        base_config=base_config,
    )
    vk_client.start_vk_bot()


def run_test(
    test_id: int,
    messages_amount: int,
    handler: Bot,
    handler_ip: str,
    handler_port: int,
    base_config: BaseConfig = BaseConfig,
) -> None:
    """
    Runs a load test on the specified `handler` using the specified
    VK client. Sends `messages_amount` messages to the handler and waits
    for them to be processed.

    :param test_id: The ID of the test being run.
    :type test_id: int

    :param messages_amount: The number of messages to send to the
        handler.
    :type messages_amount: int

    :param handler: The bot handler to test.
    :type handler: Bot

    :param handler_ip: The IP address on which to run the handler.
    :type handler_ip: str

    :param handler_port: The port on which to run the handler.
    :type handler_port: int

    :param base_config: The base configuration to use for the VK client,
        defaults to `BaseConfig`.
    :type base_config: BaseConfig, optional

    :return: None
    :rtype: NoneType
    """

    vk_client = _get_vk_client(
        handler=handler,
        handler_ip=handler_ip,
        handler_port=handler_port,
        base_config=base_config,
    )
    vk_client.run_test(test_id=test_id, messages_amount=messages_amount)


def _get_vk_client(
    handler: Bot,
    handler_ip: str,
    handler_port: int,
    base_config: BaseConfig = BaseConfig,
):
    return VkClient(
        handler=handler,
        local_ip=handler_ip,
        local_port=handler_port,
        base_config=base_config,
    )
