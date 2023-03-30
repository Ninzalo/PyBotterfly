from dataclasses import dataclass
from pybotterfly.base_config import BaseConfig


@dataclass()
class MessageStruct:
    """
    A data class representing a message sent by a user.

    :param user_id: The ID of the user who sent the message.
    :type user_id: int

    :param messenger: The messenger platform the message was sent from
        (e.g. "vk" or "tg").
        Defaults to "vk".
    :type messenger: str, optional

    :param text: The text content of the message. Defaults to None.
    :type text: str, optional

    :param payload: Additional data sent with the message. Defaults to None.
    :type payload: dict, optional
    """

    user_id: int
    messenger: BaseConfig.ADDED_MESSENGERS = BaseConfig.ADDED_MESSENGERS
    text: str | None = None
    payload: dict | None = None
