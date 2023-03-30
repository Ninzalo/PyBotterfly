from dataclasses import dataclass
from typing import Optional
from pybotterfly.bot.returns.message import Return
from pybotterfly.base_config import BaseConfig

# Vk async library
from vkbottle import API
from vkbottle import Keyboard as VkKeyboard
from vkbottle import KeyboardButtonColor as VkKeyboardColor
from vkbottle import Text as VkText

# Tg async library
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup as TgInlineKeyboard
from aiogram.types import InlineKeyboardButton as TgInlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup as TgKeyboard
from aiogram.types import KeyboardButton as TgKeyboardButton


@dataclass()
class DefaultVkReplier:
    """
    A default implementation of a VK replier.

    :param vk_api: An instance of the VK API to use for sending messages.
    :type vk_api: vk_api.vk_api.VkApiMethod
    :param config: An instance of the configuration for the replier. Optional.
        Defaults to BaseConfig.
    :type config: BaseConfig, optional

    """

    vk_api: API
    config: BaseConfig = BaseConfig

    async def vk_answer(self, return_message: Return) -> None:
        """
        Asynchronously sends a response message to a user via the VK API
        with an optional keyboard.

        :param return_message: The message to send.
        :type return_message: Return
        """
        keyboard = await self._get_vk_keyboard(
            return_message.keyboard, return_message.inline_keyboard
        )
        await self.vk_api.messages.send(
            peer_id=return_message.user_messenger_id,
            message=return_message.text,
            random_id=0,
            keyboard=keyboard.get_json() if keyboard is not None else None,
        )

    async def _get_vk_keyboard(
        self,
        keyboard: Optional[Return.keyboard],
        inline_keyboard: Optional[Return.inline_keyboard],
    ) -> Optional[VkKeyboard]:
        """
        Converts a `Return` object's `keyboard` or `inline_keyboard` attribute
        to a `vk_api.keyboard.VkKeyboard` object.

        If both `keyboard` and `inline_keyboard` are `None`, returns `None`.

        :param keyboard: The keyboard to convert.
        :type keyboard: Optional[Return.keyboard]
        :param inline_keyboard: The inline keyboard to convert.
        :type inline_keyboard: Optional[Return.inline_keyboard]
        :return: A `vk_api.keyboard.VkKeyboard` object.
        :rtype: Optional[vk_api.keyboard.VkKeyboard]
        """
        if keyboard is None and inline_keyboard is None:
            return None
        buttons = inline_keyboard or keyboard or []
        keyboard_cls = VkKeyboard(one_time=False, inline=bool(inline_keyboard))
        for button in buttons:
            kwargs = {"label": button.label}
            if inline_keyboard:
                kwargs["payload"] = button.payload
            keyboard_cls.add(
                VkText(**kwargs),
                await self._vk_color_picker(button.color),
            )
            if button.new_line_after:
                keyboard_cls.row()
        return keyboard_cls

    async def _vk_color_picker(
        self, color: config.BUTTONS_COLORS
    ) -> VkKeyboardColor:
        """
        Converts a button color to a VK Keyboard color.

        :param color: A string specifying the color of the button. Must
            be one of:
                - "primary"
                - "secondary"
                - "positive"
                - "negative"
        :type color: config.BUTTONS_COLORS
        :return: The VK Keyboard color. A VK button color enum value
            corresponding to the input color string.
        :rtype: vk_api.keyboard.VkKeyboardColor
        """
        color_map = {
            "primary": VkKeyboardColor.PRIMARY,
            "secondary": VkKeyboardColor.SECONDARY,
            "positive": VkKeyboardColor.POSITIVE,
            "negative": VkKeyboardColor.NEGATIVE,
        }
        return color_map.get(color, VkKeyboardColor.PRIMARY)


@dataclass()
class DefaultTgReplier:
    """
    A dataclass that contains information about a Telegram bot and a
    configuration object.

    :param tg_bot: The Telegram bot instance.
    :type tg_bot: telegram.Bot
    :param config: The configuration object to use. Default is BaseConfig.
    :type config: BaseConfig, optional
    """

    tg_bot: Bot
    config: BaseConfig = BaseConfig

    async def tg_answer(self, return_message: Return) -> None:
        """
        Sends a Telegram message with an optional inline keyboard or reply
        keyboard.
        The method first gets the appropriate keyboard format for the
        message using the _get_tg_keyboard method. It then sends the
        message to the Telegram user using the tg_bot.send_message method,
        specifying the user's messenger ID and the message text. If the
        message includes keyboard data, it is included in the message
        using the reply_markup parameter.

        :param return_message: The message to send.
        :type return_message: Return
        """
        keyboard = await self._get_tg_keyboard(
            return_message.keyboard, return_message.inline_keyboard
        )
        await self.tg_bot.send_message(
            chat_id=return_message.user_messenger_id,
            text=return_message.text,
            reply_markup=keyboard if keyboard is not None else None,
        )

    async def _get_tg_keyboard(
        self,
        keyboard: Optional[Return.keyboard],
        inline_keyboard: Optional[Return.inline_keyboard],
    ) -> TgInlineKeyboard | TgKeyboard | None:
        """
        Generates a Telegram keyboard object from the provided keyboard
        and inline_keyboard parameters.

        :param keyboard: Optional. A list of buttons to include in the keyboard.
        :type keyboard: Optional[Return.keyboard]
        :param inline_keyboard: Optional. A list of inline buttons to include
            in the keyboard.
        :type inline_keyboard: Optional[Return.inline_keyboard]
        :return: A Telegram keyboard with the provided buttons or None if no
            buttons are given.
        :rtype: tg_inline_kb | tg_kb | None
        """
        if keyboard is None and inline_keyboard is None:
            return None
        buttons = inline_keyboard or keyboard or []
        keyboard_cls = (
            TgInlineKeyboard()
            if inline_keyboard is not None
            else TgKeyboard(resize_keyboard=True)
        )
        for button in buttons:
            button_text = (
                f"{await self._tg_color_picker(color=button.color)}"
                f"{button.label}"
            )
            if inline_keyboard is not None:
                keyboard_cls.add(
                    TgInlineKeyboardButton(
                        button_text, callback_data=str(button.payload)
                    )
                )
            else:
                keyboard_cls.add(TgKeyboardButton(button_text))
            if button.new_line_after:
                keyboard_cls.row()
        return keyboard_cls

    async def _tg_color_picker(self, color: config.BUTTONS_COLORS) -> str:
        """
        Converts a button color to a corresponding emoji representing the color.

        :param color: A string specifying the color of the button. Must
            be one of:
                - "primary"
                - "secondary"
                - "positive"
                - "negative"
        :type color: config.BUTTONS_COLORS
        :return: A string representing the color as a Telegram emoji.
        :rtype: str
        """
        color_map = {
            "primary": "⚪️",
            "secondary": "⚫️",
            "positive": "🟢",
            "negative": "🔴",
        }
        return color_map.get(color, "⚪️")
