import asyncio
import pickle
from pybotterfly.bot.struct import Message_struct
from pybotterfly.bot.converters import dataclass_to_dict


async def send_to_server(
    message: Message_struct, local_ip: str, local_port: int
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

    message_dict = dataclass_to_dict(message)
    data = pickle.dumps(message_dict)
    writer.write(data)
    await writer.drain()
    writer.write_eof()
    writer.close()
