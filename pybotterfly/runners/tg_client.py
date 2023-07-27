import asyncio
from datetime import datetime
from io import BytesIO
from pybotterfly.base_config import BaseConfig
from pybotterfly.bot.struct import File, MessageStruct
from pybotterfly.bot.converters import str_to_dict, file_to_string
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
        self._dp.message_handler(content_types=types.ContentTypes.DOCUMENT)(
            self.file_handler
        )
        self._dp.message_handler(content_types=types.ContentTypes.PHOTO)(
            self.photo_handler
        )
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
        await self.server_sender(message_struct=message_struct)

    async def photo_handler(self, message: types.Message) -> None:
        message_struct = MessageStruct(
            user_id=message.from_id, messenger="tg", text=message.text
        )
        if message.photo != []:
            file_in_io = BytesIO()
            await message.photo[-1].download(destination_file=file_in_io)
            message_struct.files.append(
                File(
                    name=message.photo[-1].file_unique_id,
                    tag="photo",
                    ext=".png",
                    file_bytes=file_to_string(file_in_io.getvalue()),
                )
            )
        await self.server_sender(message_struct=message_struct)

    async def file_handler(self, message: types.Message) -> None:
        message_struct = MessageStruct(
            user_id=message.from_id, messenger="tg", text=message.text
        )
        if message.document != None:
            file_in_io = BytesIO()
            await message.document.download(destination_file=file_in_io)
            message_struct.files.append(
                File(
                    name=f"{message.document.file_name}",
                    tag="document",
                    ext=f".{str(message.document.file_name).split('.')[-1]}",
                    file_bytes=file_to_string(file_in_io.getvalue()),
                )
            )
        await self.server_sender(message_struct=message_struct)

    async def message_handler(self, message: types.Message) -> None:
        message_struct = MessageStruct(
            user_id=message.from_id, messenger="tg", text=message.text
        )
        await self.server_sender(message_struct=message_struct)

    async def server_sender(self, message_struct: MessageStruct) -> None:
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
                user_id=test_id, messenger="tg", text=f"TEST_MESSAGE_n{num}"
            )
            await self.server_sender(message_struct=message_struct)
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

    if messages_amount <= 0:
        raise ValueError("Messages amount must be greater than 0")
    if messages_amount > 50:
        raise ValueError("Messages amount must be less than 50")

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
