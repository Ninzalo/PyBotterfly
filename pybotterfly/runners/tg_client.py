import asyncio
from datetime import datetime
from pybotterfly.base_config import BaseConfig
from pybotterfly.bot.struct import MessageStruct
from pybotterfly.bot.converters import str_to_dict
from pybotterfly.server.server_func import send_to_server

# Tg async library
from aiogram import types, executor, Dispatcher


class TgClient:
    def __init__(
        self,
        dispatcher: Dispatcher,
        local_ip: str,
        local_port: int,
        base_config: BaseConfig,
    ) -> None:
        self._dp = dispatcher
        self._local_ip = local_ip
        self._local_port = local_port
        self._config = base_config
        self._dp.callback_query_handler()(self.callback_message_handler)
        self._dp.message_handler()(self.message_handler)
        self._started = False

    async def callback_message_handler(
        self,
        query: types.CallbackQuery,
    ) -> None:
        message_struct = MessageStruct(
            user_id=query.from_user.id,
            messenger="tg",
            payload=str_to_dict(string=query.data),
        )
        await send_to_server(
            message=message_struct,
            local_ip=self._local_ip,
            local_port=self._local_port,
        )

    async def message_handler(self, message: types.Message) -> None:
        message_struct = MessageStruct(
            user_id=message.from_id, messenger="tg", text=message.text
        )
        await send_to_server(
            message=message_struct,
            local_ip=self._local_ip,
            local_port=self._local_port,
        )

    async def test_messages_rate(self, test_id: int, messages_amount: int):
        self._started = True
        test_start_time = datetime.now()
        if not self._config.DEBUG_STATE:
            print(f"Failed to run test (running not in Debug mode)")
            return
        print(f"Rate test started at {test_start_time}")
        for num in range(1, messages_amount + 1):
            message_struct = MessageStruct(
                user_id=test_id, messenger="tg", text=f"{num}"
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

    def start_tg_client(self) -> None:
        if self._started:
            print(f"[ERROR] Ensure not to run test")
            return
        print(
            f"TG listening started"
            f"{' in Debug mode' if self._config.DEBUG_STATE else ''}"
        )
        executor.start_polling(self._dp, skip_updates=True)

    def run_test(self, test_id: int, messages_amount: int) -> None:
        asyncio.run(
            self.test_messages_rate(
                test_id=test_id, messages_amount=messages_amount
            )
        )


def start_tg_client(
    dispatcher: Dispatcher,
    handler_ip: str,
    handler_port: int,
    base_config: BaseConfig = BaseConfig,
) -> None:
    """
    Starts a Telegram client that listens for incoming messages and forwards
    them to the given `dispatcher` for handling. The client connects to the
    Telegram server using the provided `handler_ip` and `handler_port` and
    uses the given `base_config`.

    :param dispatcher: The `Dispatcher` instance that will handle incoming
        messages.
    :type dispatcher: Dispatcher
    :param handler_ip: The IP address to use to connect to the Telegram server.
    :type handler_ip: str
    :param handler_port: The port number to use to connect to the Telegram
        server.
    :type handler_port: int
    :param base_config: The configuration options to use for the Telegram
        client. Defaults to `BaseConfig`.
    :type base_config: BaseConfig
    :return: None
    :rtype: NoneType
    """

    tg_client = _get_tg_client(
        dispatcher=dispatcher,
        handler_ip=handler_ip,
        handler_port=handler_port,
        base_config=base_config,
    )
    tg_client.start_tg_client()


def run_test(
    test_id: int,
    messages_amount: int,
    dispatcher: Dispatcher,
    handler_ip: str,
    handler_port: int,
    base_config: BaseConfig = BaseConfig,
) -> None:
    """
    Runs a test for the Telegram client by sending `messages_amount` messages
    to the specified `dispatcher` and checking for the expected response. The
    test is identified by `test_id`. The client connects to the Telegram server
    using the provided `handler_ip` and `handler_port` and uses the given
    `base_config`.

    :param test_id: The ID of the test to be run.
    :type test_id: int
    :param messages_amount: The number of messages to send to the `dispatcher`.
    :type messages_amount: int
    :param dispatcher: The `Dispatcher` instance to send messages to.
    :type dispatcher: Dispatcher
    :param handler_ip: The IP address to use to connect to the Telegram server.
    :type handler_ip: str
    :param handler_port: The port number to use to connect to the Telegram
        server.
    :type handler_port: int
    :param base_config: The configuration options to use for the Telegram
        client. Defaults to `BaseConfig`.
    :type base_config: BaseConfig
    :return: None
    :rtype: NoneType
    """

    tg_client = _get_tg_client(
        dispatcher=dispatcher,
        handler_ip=handler_ip,
        handler_port=handler_port,
        base_config=base_config,
    )
    tg_client.run_test(test_id=test_id, messages_amount=messages_amount)


def _get_tg_client(
    dispatcher: Dispatcher,
    handler_ip: str,
    handler_port: int,
    base_config: BaseConfig,
) -> TgClient:
    """
    Returns a new Tg_client instance with the specified configuration options.

    :param dispatcher: An instance of the Dispatcher class that represents the
        bot's event dispatcher.
    :type dispatcher: Dispatcher

    :param handler_ip: A string that represents the IP address of the bot's
        message handler.
    :type handler_ip: str

    :param handler_port: An integer that represents the port number of the bot's
        message handler.
    :type handler_port: int

    :param base_config: An instance of the BaseConfig class that represents the
        base configuration options for the bot.
    :type base_config: BaseConfig

    :returns: A new Tg_client instance with the specified configuration options.
    :rtype: Tg_client
    """
    return TgClient(
        dispatcher=dispatcher,
        local_ip=handler_ip,
        local_port=handler_port,
        base_config=base_config,
    )
