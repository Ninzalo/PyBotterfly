from dataclasses import dataclass
from typing import Literal, TypeAlias, List, get_args


@dataclass()
class BaseConfig:
    """
    The BaseConfig class contains the base configuration options for the bot.

    :ivar ADDED_MESSENGERS: A Literal that represents the available messengers
        that can be used with the bot. The options are "vk" and "tg".
    :vartype ADDED_MESSENGERS: Literal["vk", "tg"]

    :ivar BUTTONS_COLORS: A Literal that represents the available button colors
        that can be used with the bot. The options are "primary", "secondary",
        "positive", and "negative".
    :vartype BUTTONS_COLORS: Literal["primary", "secondary", "positive", "negative"]

    :ivar DEBUG_STATE: A boolean that indicates whether the bot is in debug mode.
        Defaults to True.
    :vartype DEBUG_STATE: bool

    :ivar MAX_BUTTONS_IN_ROW: An integer that represents the maximum number of
        buttons that can be in a single row in a message sent by the bot.
        Defaults to 4.
    :vartype MAX_BUTTONS_IN_ROW: int

    :ivar MAX_BUTTON_ROWS: An integer that represents the maximum number of
        rows that can be in a message sent by the bot.
        Defaults to 9.
    :vartype MAX_BUTTON_ROWS: int

    :ivar MAX_BUTTONS_AMOUNT: An integer that represents the maximum number of
        buttons that can be in a message sent by the bot.
        Defaults to 10.
    :vartype MAX_BUTTONS_AMOUNT: int

    :ivar ALLOWED_FILE_EXTENSIONS: A list of allowed extensions for a file.
    :vartype ALLOWED_FILE_EXTENSIONS: Literal[".png", ".jpg", ".jpeg", ".xls",
        ".xlsx", ".doc", ".docx", ".pdf"]
    """

    ADDED_MESSENGERS: TypeAlias = Literal["vk", "tg"]
    BUTTONS_COLORS: TypeAlias = Literal[
        "primary", "secondary", "positive", "negative"
    ]
    DEBUG_STATE: bool = True
    MAX_BUTTONS_IN_ROW = 4
    MAX_BUTTON_ROWS = 9
    MAX_BUTTONS_AMOUNT = 10
    ALLOWED_FILE_TYPES: TypeAlias = Literal["photo", "document"]
    ALLOWED_FILE_EXTENSIONS: TypeAlias = Literal[
        # [PHOTO]
        ".png",
        ".jpg",
        ".jpeg",
        # [DOCUMENT]
        ".xls",
        ".xlsx",
        ".doc",
        ".docx",
        ".pdf",
    ]
    ALLOWED_FILE_EXTENSIONS_LIST: List[str] = get_args(ALLOWED_FILE_EXTENSIONS)
