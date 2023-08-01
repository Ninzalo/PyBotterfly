from typing import List
from dataclasses import dataclass
from pybotterfly.base_config import BaseConfig
from pybotterfly.bot.logger import BaseLogger, Log, DefaultLogger


@dataclass()
class _Button:
    def __init__(
        self,
        label: str,
        color: BaseConfig.BUTTONS_COLORS,
        new_line_after: bool = False,
        base_config: BaseConfig = BaseConfig,
    ):
        self.label = label
        self.color: base_config.BUTTONS_COLORS = color
        self.new_line_after = new_line_after

    def __str__(self) -> str:
        return f"Button(label='{self.label}', color='{self.color}')"

    def __repr__(self) -> str:
        return self.__str__()


@dataclass()
class _InlineButton:
    def __init__(
        self,
        label: str,
        color: BaseConfig.BUTTONS_COLORS,
        payload: dict,
        new_line_after: bool = False,
        base_config: BaseConfig = BaseConfig,
    ):
        self.label = label
        self.color: base_config.BUTTONS_COLORS = color
        self.payload = payload
        self.new_line_after = new_line_after

    def __str__(self) -> str:
        return_str = (
            f"Button(label='{self.label}', color='{self.color}', "
            f"payload={self.payload})"
        )
        return return_str

    def __repr__(self) -> str:
        return self.__str__()


@dataclass()
class Buttons:
    """
    Class representing a list of buttons for messaging interfaces.

    :param buttons: A list of _Button objects representing the buttons to
        be added.
    :type buttons: List[_Button], optional

    :param config: An instance of BaseConfig class to configure the buttons.
    :type config: BaseConfig, optional

    :param logger: An instance of the BaseLogger class that represents the
        base logger for the bot.
    :type logger:  BaseLogger

    :param _since_new_line: An integer representing the amount of buttons
        added since the last line break.
    :type _since_new_line: int, default 0

    :param _rows: An integer representing the number of rows created for
        the buttons.
    :type _rows: int, default 0

    :param _buttons_amount: An integer representing the number of buttons
        added to the list.
    :type _buttons_amount: int, default 0
    """

    def __init__(
        self,
        buttons: List[_Button] | None = None,
        config: BaseConfig = BaseConfig,
        logger: BaseLogger | None = None,
    ):
        self.buttons = buttons if buttons != None else []
        self.config = config
        self._logger = (
            logger if logger != None else DefaultLogger(config=config)
        )
        self._since_new_line = 0
        self._rows = 0
        self._buttons_amount = 0

    def add_button(self, label: str, color: str) -> None:
        """
        Adds a button to the button list.

        :param label: A string representing the button label.
        :type label: str

        :param color: A string representing the button color.
        :type color: self.config.BUTTONS_COLORS

        :raises AssertionError: If the maximum number of buttons in a row is exceeded.
        :return: None
        """
        if self._since_new_line >= self.config.MAX_BUTTONS_IN_ROW:
            self.add_line()
        self._since_new_line += 1
        self._buttons_amount += 1
        self.buttons.append(_Button(label=label, color=color))
        self._logger.log(
            log=Log(
                level="INFO", text=f"Added button: {str(self.buttons[-1])}"
            )
        )

    def add_line(self) -> None:
        """
        Adds new line after the last created button

        :raises ValueError: If there are no buttons in the list.
        :return: None
        """
        if self._buttons_amount > 0:
            self.buttons[-1].new_line_after = True
            self._since_new_line = 0
            self._rows += 1
            self._logger.log(
                log=Log(
                    level="INFO",
                    text=f"Added line after: {self.buttons[-1]}",
                )
            )
        else:
            raise ValueError(f"[ERROR] Can't add new line, no buttons in list")

    def remove_last_button(self) -> None:
        """
        Removes the last button from the button list.

        :raises ValueError: If there are no buttons in the list.
        :return: None
        """
        if self._buttons_amount > 0:
            self._logger.log(
                log=Log(
                    level="INFO",
                    text=f"Last button: {self.buttons[-1]} removed",
                )
            )
            self.buttons.pop(-1)
            if self._since_new_line > 0:
                self._since_new_line -= 1
        else:
            raise ValueError(
                f"[ERROR] Can't remove last button, no buttons in list"
            )

    def confirm(self) -> List[_Button]:
        """
        Confirm the buttons and return the list of buttons.
        Fixing the wrong lining

        :raises ValueError: If there are too many buttons or too many rows.

        :return: List of buttons.
        :rtype: List[_Button]
        """
        if self._buttons_amount > self.config.MAX_BUTTONS_AMOUNT:
            raise ValueError(
                f"[ERROR] Too much buttons: {self._buttons_amount}"
            )
        if self._rows > self.config.MAX_BUTTON_ROWS:
            raise ValueError(f"[ERROR] Too much rows: {self._rows}")
        if self._buttons_amount > 0:
            if self.buttons[-1].new_line_after:
                self.buttons[-1].new_line_after = False
        return self.buttons


@dataclass()
class InlineButtons:
    """
    A class to represent a list of inline buttons.

    :param buttons: A list of _Inline_button objects.
    :type buttons: List[_Inline_button]

    :param config: An object of type BaseConfig that specifies the
        configuration of the buttons.
    :type config: BaseConfig, optional

    :param _since_new_line: An integer representing the number of buttons
        since the last new line.
    :type _since_new_line: int, default 0

    :param _rows: An integer representing the number of rows of buttons.
    :type _rows: int, default 0

    :param _buttons_amount: An integer representing the total number of buttons.
    :type _buttons_amount: int, default 0

    :param _logger: An instance of the BaseLogger class that represents the
        base logger for the bot.
    :type logger: BaseLogger
    """

    def __init__(
        self,
        buttons: List[_InlineButton] | None = None,
        config: BaseConfig = BaseConfig,
        logger: BaseLogger | None = None,
    ):
        self.buttons = buttons if buttons != None else []
        self.config = config
        self._logger = (
            logger if logger != None else DefaultLogger(config=config)
        )
        self._since_new_line = 0
        self._rows = 0
        self._buttons_amount = 0

    def add_button(self, label: str, color: str, payload: dict) -> None:
        """
        Adds a new button to the inline keyboard.

        :param label: The label to display on the button.
        :type label: str

        :param color: The color of the button.
        :type color: self.config.BUTTONS_COLORS

        :param payload: The data to send when the button is pressed.
        :type payload: dict

        :raises AssertionError: If the maximum number of buttons in a row is exceeded.
        :return: None
        """
        if self._since_new_line >= self.config.MAX_BUTTONS_IN_ROW:
            self.add_line()
        self._since_new_line += 1
        self._buttons_amount += 1
        self.buttons.append(
            _InlineButton(label=label, color=color, payload=payload)
        )
        self._logger.log(
            log=Log(
                level="INFO", text=f"Added button: {str(self.buttons[-1])}"
            )
        )

    def add_line(self) -> None:
        """
        Adds a new line after the last button in the list, if there are any.
        Raises a ValueError if there are no buttons in the list.

        :raises ValueError: If there are no buttons in the list.
        :return: None
        """
        if self._buttons_amount > 0:
            self.buttons[-1].new_line_after = True
            self._since_new_line = 0
            self._rows += 1
            self._logger.log(
                log=Log(
                    level="INFO",
                    text=f"Added line after: {self.buttons[-1]}",
                )
            )
        else:
            raise ValueError(f"[ERROR] Can't add new line, no buttons in list")

    def remove_last_button(self) -> None:
        """
        Removes the last button added to the keyboard.

        If the last button added is on a new line, the new line will be
        removed as well.

        :raises ValueError: If there are no buttons to remove.
        :return: None
        """
        if self._buttons_amount > 0:
            self._logger.log(
                log=Log(
                    level="INFO",
                    text=f"Last button: {self.buttons[-1]} removed",
                )
            )
            self.buttons.pop(-1)
            if self._since_new_line > 0:
                self._since_new_line -= 1
        else:
            raise ValueError(
                f"[ERROR] Can't remove last button, no buttons in list"
            )

    def confirm(self) -> List[_InlineButton]:
        """
        Confirm the buttons and return a list of inline buttons.
        Fixing the wrong lining

        :raises ValueError: If there are too many buttons or too many rows.
        :return: List of inline buttons.
        :rtype: List[_Inline_button]
        """
        if self._buttons_amount > self.config.MAX_BUTTONS_AMOUNT:
            raise ValueError(
                f"[ERROR] Too much buttons: {self._buttons_amount}"
            )
        if self._rows > self.config.MAX_BUTTON_ROWS:
            raise ValueError(f"[ERROR] Too much rows: {self._rows}")
        if self._buttons_amount > 0:
            if self.buttons[-1].new_line_after:
                self.buttons[-1].new_line_after = False
        return self.buttons
