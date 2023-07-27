from dataclasses import dataclass, field
from typing import List, Self
from pybotterfly.bot.returns.buttons import Buttons, InlineButtons
from pybotterfly.base_config import BaseConfig
from pybotterfly.bot.struct import File


@dataclass()
class Return:
    """
    Represents a response that can be returned to a user on a specific messenger.

    :param user_messenger_id: The ID of the user on the messenger.
    :type user_messenger_id: int

    :param user_messenger: The messenger to which the response should be sent.
    :type user_messenger: BaseConfig.ADDED_MESSENGERS

    :param text: The text of the response.
    :type text: str

    :param keyboard: Optional buttons to include with the response.
    :type keyboard: Buttons | None

    :param inline_keyboard: Optional inline buttons to include with the response.
    :type inline_keyboard: InlineButtons | None

    :param attachments: Optional files to include with the response.
    :type attachments: List[File] | None
    """

    user_messenger_id: int
    user_messenger: BaseConfig.ADDED_MESSENGERS
    text: str
    keyboard: Buttons | None = None
    inline_keyboard: InlineButtons | None = None
    attachments: List[File] = field(default_factory=list)


@dataclass()
class Returns:
    """
    A class representing a list of message returns.

    :param returns: A list of Return objects representing the messages to return.
    :type returns: List[Return]
    """

    returns: List[Return] = field(default_factory=list)

    async def add_return(
        self,
        user_messenger_id: int,
        user_messenger: BaseConfig.ADDED_MESSENGERS,
        text: str,
        keyboard: Buttons | None = None,
        inline_keyboard: InlineButtons | None = None,
        attachments: List[File] | None = None,
    ) -> Self:
        """
        Add a new return message to the list of returns.

        :param user_messenger_id: The ID of the user on the messaging platform.
        :type user_messenger_id: int

        :param user_messenger: The messaging platform where the user is located.
        :type user_messenger: BaseConfig.ADDED_MESSENGERS

        :param text: The text message to be sent to the user.
        :type text: str

        :param keyboard: An optional keyboard to be displayed to the user.
        :type keyboard: Buttons | None

        :param inline_keyboard: An optional inline keyboard to be displayed
            to the user.
        :type inline_keyboard: InlineButtons | NoneType

        :param attachments: Optional files to include with the response.
        :type attachments: List[File] | None
        """
        new_return = Return(
            user_messenger_id=user_messenger_id,
            user_messenger=user_messenger,
            text=text,
            keyboard=keyboard,
            inline_keyboard=inline_keyboard,
            attachments=[] if attachments == None else attachments,
        )
        if new_return not in self.returns:
            self.returns.append(new_return)
        return self
