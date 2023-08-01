from typing import List
from dataclasses import dataclass

from pybotterfly.base_config import BaseConfig
from pybotterfly.bot.logger import BaseLogger, Log, DefaultLogger


@dataclass()
class ServerData:
    """
    A dataclass representing the IP address and port number of a server.

    :param server_ip: The IP address of the server.
    :type server_ip: str

    :param server_port: The port number of the server.
    :type server_port: int
    """

    server_ip: str
    server_port: int


class ServersList:
    """
    A container for `ServerData` objects representing a list of servers.

    :param servers: A list of `ServerData` objects representing servers.
    :type servers: List[ServerData]

    :param config: A configuration object to use with the server list,
        defaults to `BaseConfig`.
    :type config: BaseConfig

    :param logger: An instance of the BaseLogger class that represents the
        base logger for the bot.
    :type logger: BaseLogger

    :type config: BaseConfig, optional
    """

    def __init__(
        self,
        servers: List[ServerData],
        config: BaseConfig = BaseConfig,
        logger: BaseLogger | None = None,
    ) -> None:
        self.servers = servers
        self.config = config
        self._logger = (
            logger if logger != None else DefaultLogger(config=config)
        )

    def add_server(self, server: ServerData) -> None:
        """
        Adds a server to the list of servers.

        :param server: Server data to be added.
        :type server: ServerData

        :raises ValueError: If the server is already in the list.
        """

        if server in self.servers:
            raise RuntimeError("Server already exists.")
        self.servers.append(server)
        self._logger.log(
            log=Log(
                level="INFO",
                text=f"New server added to servers list: {server}",
            )
        )
