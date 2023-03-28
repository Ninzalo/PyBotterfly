from dataclasses import dataclass, field
from typing import List

from pybotterfly.base_config import BaseConfig


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


@dataclass()
class ServersList:
    """
    A container for `ServerData` objects representing a list of servers.

    :param servers: A list of `ServerData` objects representing servers.
    :type servers: List[ServerData], optional
    :param config: A configuration object to use with the server list,
        defaults to `BaseConfig`.
    :type config: BaseConfig, optional
    """

    servers: List[ServerData] = field(default_factory=list)
    config: BaseConfig = BaseConfig

    def add_server(self, server: ServerData) -> None:
        """
        Adds a server to the list of servers.

        :param server: Server data to be added.
        :type server: ServerData
        :raises ValueError: If the server is already in the list.
        """

        if server in self.servers:
            raise ValueError("Server already exists.")
        self.servers.append(server)
        if self.config.DEBUG_STATE:
            print(f"New server added to servers list: {server}")
