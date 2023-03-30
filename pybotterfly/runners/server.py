import asyncio
from datetime import datetime
import pickle
from pybotterfly.base_config import BaseConfig
from pybotterfly.bot.converters import dataclass_from_dict
from pybotterfly.bot.returns.message import Return
from pybotterfly.bot.struct import MessageStruct
from pybotterfly.bot.reply.reply_division import MessengersDivision
from pybotterfly.message_handler.message_handler import MessageHandler


class Server:
    def __init__(
        self,
        messengers: MessengersDivision,
        message_reply_rate: int | float,
        message_handler: MessageHandler,
        base_config: BaseConfig,
    ) -> None:
        self._messengers = messengers
        self._message_reply_rate = message_reply_rate
        self._message_handler = message_handler
        self._config = base_config
        self._check_errors()

    def _check_errors(self) -> None:
        if not self._messengers:
            raise RuntimeError(f"Messengers weren't added")
        if not self._message_handler:
            raise RuntimeError(f"Message handler wasn't added")
        if not self._messengers._compiled:
            raise RuntimeError(f"Messengers weren't compiled")

    async def handle_echo(
        self,
        reader: asyncio.streams.StreamReader,
        writer: asyncio.streams.StreamWriter,
    ) -> None:
        tasks = []
        while True:
            data = await reader.read()
            if not data:
                break
            message = pickle.loads(data)
            message_cls = dataclass_from_dict(
                struct=MessageStruct, dictionary=message
            )
            addr = writer.get_extra_info("peername")
            print(f"Received {message_cls!r} from {addr!r}")
            if self._config.DEBUG_STATE:
                print(f"Fetching {message_cls} started at {datetime.now()}")
            return_cls = await self._message_handler.get(
                message_class=message_cls
            )
            if self._config.DEBUG_STATE:
                print(f"Fetching {message_cls} finished at {datetime.now()}")
            if not return_cls:
                if self._config.DEBUG_STATE:
                    print(
                        f"An incorrect request resulted in an error. "
                        f"Request skipped. "
                        f"Return_cls: {return_cls}"
                    )
                break
            for answer in return_cls.returns:
                task = asyncio.create_task(self.replier(answer))
                tasks.append(task)
        await asyncio.gather(*tasks)
        writer.close()

    async def replier(self, return_cls: Return):
        await self._messengers.get_func(
            messenger=return_cls.user_messenger, return_cls=return_cls
        )
        if self._config.DEBUG_STATE:
            request = (
                f"{'='*10}"
                f"\nTime: {datetime.now()}"
                f"\nUser_id: {return_cls.user_messenger_id}"
                f"\nMessage: {return_cls}"
                f"\n{'='*10}"
            )
            print(request)

    async def main(self, local_ip: str, local_port: int) -> None:
        for messenger in self._messengers._messengers_to_answer:
            messenger._throttler.start()
        server = await asyncio.start_server(
            lambda reader, writer: self.handle_echo(
                reader=reader, writer=writer
            ),
            local_ip,
            local_port,
        )
        addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
        print(
            f"Serving on {addrs}"
            f"{' in Debug mode' if self._config.DEBUG_STATE else ''}"
        )
        async with server:
            await server.serve_forever()

    def start_server(self, local_ip: str, local_port: int) -> None:
        asyncio.run(self.main(local_ip=local_ip, local_port=local_port))


def run_server(
    messengers: MessengersDivision,
    message_reply_rate: int | float,
    message_handler: MessageHandler,
    local_ip: str,
    local_port: int,
    base_config: BaseConfig = BaseConfig,
) -> None:
    """
    Starts the server and begins listening for incoming messages.

    :param messengers: An instance of the Messengers_division class that
        represents the messengers to be used by the bot.
    :type messengers: Messengers_division

    :param message_reply_rate: The rate at which the bot should reply to
        incoming messages, measured in messages per second.
    :type message_reply_rate: int | float

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

    :returns: None
    :rtype: NoneType
    """
    server = Server(
        messengers=messengers,
        message_reply_rate=message_reply_rate,
        message_handler=message_handler,
        base_config=base_config,
    )
    server.start_server(local_ip=local_ip, local_port=local_port)
