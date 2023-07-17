import asyncio
from pybotterfly.bot.struct import MessageStruct
from pybotterfly.bot.converters import dataclass_to_bytes


async def send_to_server(
    message: MessageStruct, local_ip: str, local_port: int
) -> None:
    """
    Sends a message to a server at a specified IP address and port.

    :param message: An instance of the Message_struct class that represents
        the message to be sent to the server.
    :type message: Message_struct

    :param local_ip: A string that represents the IP address of the server.
    :type local_ip: str

    :param local_port: An integer that represents the port number of the server.
    :type local_port: int

    :returns: None
    :rtype: NoneType
    """
    _, writer = await asyncio.open_connection(local_ip, local_port)
    writer.write(dataclass_to_bytes(message))
    await writer.drain()
    writer.write_eof()
    writer.close()
