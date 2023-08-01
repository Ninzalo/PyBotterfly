import asyncio
from datetime import datetime
from pybotterfly.base_config import BaseConfig
from pybotterfly.bot.converters import (
    bytes_to_dataclass,
    string_to_file,
)
from pybotterfly.bot.returns.message import Return
from pybotterfly.bot.reply.reply_division import MessengersDivision
from pybotterfly.message_handler.message_handler import MessageHandler
from pybotterfly.bot.logger import Log, DefaultLogger, BaseLogger


class Server:
    def __init__(
        self,
        messengers: MessengersDivision,
        message_handler: MessageHandler,
        base_config: BaseConfig,
        logger: BaseLogger,
    ) -> None:
        self._messengers = messengers
        self._message_handler = message_handler
        self._config = base_config
        self._logger = logger
        self._check_errors()

    def _check_errors(self) -> None:
        if not self._messengers:
            raise RuntimeError(f"Messengers weren't added")
        if not self._message_handler:
            raise RuntimeError(f"Message handler wasn't added")
        if not self._messengers._compiled:
            raise RuntimeError(f"Messengers weren't compiled")

    async def handle_request(
        self,
        reader: asyncio.streams.StreamReader,
        writer: asyncio.streams.StreamWriter,
    ) -> None:
        tasks = []
        byte_array = bytearray()
        while True:
            data = await reader.read()
            if not data:
                break
            byte_array.extend(data)
        if byte_array == bytearray():
            self._logger.log(
                log=Log(level="ERROR", text=(f"Received empty byte array"))
            )
            return
        message_cls = bytes_to_dataclass(byte_array)
        if message_cls.files != []:
            for encoded_file in message_cls.files:
                encoded_file.file_bytes = string_to_file(
                    encoded_file.file_bytes
                )
        addr = writer.get_extra_info("peername")
        receive_time = datetime.now()
        self._logger.log(
            log=Log(
                level="INFO",
                time=receive_time,
                text=(f"Received {message_cls!r} from {addr!r}"),
            )
        )
        self._logger.log(
            log=Log(
                level="INFO",
                time=receive_time,
                text=(f"Fetching {message_cls} started"),
            )
        )
        return_cls = await self._message_handler.get(message_class=message_cls)
        self._logger.log(
            log=Log(level="INFO", text=(f"Fetching {message_cls} finished"))
        )
        if not return_cls:
            self._logger.log(
                log=Log(
                    level="ERROR",
                    text=(
                        f"An incorrect request resulted in an error. "
                        f"Request skipped. Return_cls: {return_cls}"
                    ),
                )
            )
            return
        for return_message in return_cls.returns:
            task = asyncio.create_task(
                self.replier(return_message=return_message)
            )
            tasks.append(task)
        await asyncio.gather(*tasks)
        writer.close()

    async def replier(self, return_message: Return):
        await self._messengers.get_func(return_message=return_message)
        if self._config.DEBUG_STATE:
            self._logger.log(
                log=Log(
                    level="INFO",
                    text=(
                        f"Result message\n{' Output ':=^20}"
                        f"\nUser_id: {return_message.user_messenger_id}"
                        f"\nMessage: {return_message}"
                        f"\n{'='*20}"
                    ),
                )
            )

    async def main(self, local_ip: str, local_port: int) -> None:
        for messenger in self._messengers._messengers_to_answer:
            messenger._throttler.start()
        server = await asyncio.start_server(
            lambda reader, writer: self.handle_request(
                reader=reader, writer=writer
            ),
            local_ip,
            local_port,
        )
        addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
        self._logger.log(
            log=Log(
                level="INFO",
                text=(
                    f"Serving on {addrs}"
                    f"{' in Debug mode' if self._config.DEBUG_STATE else ''}"
                ),
            )
        )
        async with server:
            await server.serve_forever()

    def start_server(self, local_ip: str, local_port: int) -> None:
        asyncio.run(self.main(local_ip=local_ip, local_port=local_port))


def run_server(
    messengers: MessengersDivision,
    message_handler: MessageHandler,
    local_ip: str,
    local_port: int,
    base_config: BaseConfig = BaseConfig,
    logger: BaseLogger | None = None,
) -> None:
    """
    Starts the server and begins listening for incoming messages.

    :param messengers: An instance of the Messengers_division class that
        represents the messengers to be used by the bot.
    :type messengers: Messengers_division

    :param message_handler: An instance of the Message_handler class that
        represents the bot's message handler.
    :type message_handler: Message_handler

    :param local_ip: A string that represents the IP address on which the
        server should listen for incoming messages.
    :type local_ip: str

    :param local_port: An integer that represents the port number on which
        the server should listen for incoming messages.
    :type local_port: int

    :param base_config: An optional instance of the BaseConfig class that
        represents the base configuration options for the bot. Defaults to
        the BaseConfig class with its default values.
    :type base_config: BaseConfig, optional

    :param logger: An instance of the BaseLogger class that represents the
        base logger for the bot.
    :type logger: BaseLogger, optional

    :returns: None
    :rtype: NoneType
    """
    if logger == None:
        logger = DefaultLogger(config=base_config)
    server = Server(
        messengers=messengers,
        message_handler=message_handler,
        base_config=base_config,
        logger=logger,
    )
    server.start_server(local_ip=local_ip, local_port=local_port)
