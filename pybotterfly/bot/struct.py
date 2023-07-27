from dataclasses import dataclass, field
from typing import List
from pybotterfly.base_config import BaseConfig


@dataclass()
class File:
    name: str
    ext: BaseConfig.ALLOWED_FILE_EXTENSIONS
    tag: BaseConfig.ALLOWED_FILE_TYPES
    file_bytes: bytes

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.name}, {self.tag}, {self.ext})"
        )

    def __dict__(self):
        return {
            "name": self.name,
            "ext": self.ext,
            "tag": self.tag,
            "file_bytes": self.file_bytes,
        }


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

    :param files: List of files attached to the message. Defaults to [].
    :type files: List[File], optional
    """

    user_id: int
    messenger: BaseConfig.ADDED_MESSENGERS
    text: str | None = None
    payload: dict | None = None
    files: List[File] = field(default_factory=list)
