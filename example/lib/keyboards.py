from pybotterfly.bot.returns.buttons import Buttons, InlineButtons

from configs.config import BASE_CONFIG
from configs.logger import logger


async def first_kb() -> Buttons:
    keyboard = Buttons(config=BASE_CONFIG, logger=logger)
    keyboard.add_button(label="Start", color="positive")
    keyboard.confirm()  # Compiles the keyboard. You can't use keyboard without using this method
    return keyboard


async def second_ikb() -> InlineButtons:
    keyboard = InlineButtons(config=BASE_CONFIG, logger=logger)
    keyboard.add_button(
        label="Go next",
        color="positive",
        payload={
            "type": "data",
            "action": "go_to_third_page",
            "data": "hidden data",
            "id": 111,
        },  # payload argument is required for Inline_buttons
    )
    keyboard.add_line()
    # adding button that we will remove in configuration
    keyboard.add_button(
        label="Deleted button",
        color="negative",
        payload={
            "type": "fake",
            "id": "integer",
        },  # payload argument is required for Inline_buttons
    )
    keyboard.confirm()
    return keyboard


async def third_before_ikb() -> InlineButtons:
    keyboard = InlineButtons(config=BASE_CONFIG, logger=logger)
    keyboard.add_button(
        label="Tap it",
        color="primary",
        payload={
            "type": "transition",
            "action": "go_to_third_after_page",
        },
    )
    keyboard.confirm()
    return keyboard


async def third_after_ikb() -> InlineButtons:
    keyboard = InlineButtons(config=BASE_CONFIG, logger=logger)
    keyboard.add_button(
        label="Go next",
        color="positive",
        payload={"type": "transition", "action": "go_to_fourth_page"},
    )
    keyboard.confirm()
    return keyboard


async def fourth_kb() -> Buttons:
    keyboard = Buttons(config=BASE_CONFIG, logger=logger)
    keyboard.add_button(label="Admin", color="secondary")
    keyboard.add_button(label="Next", color="positive")
    keyboard.add_line()
    keyboard.add_button(label="Back", color="negative")
    keyboard.confirm()
    return keyboard


async def fifth_kb() -> Buttons:
    keyboard = Buttons(config=BASE_CONFIG, logger=logger)
    keyboard.add_button(label="Skip", color="secondary")
    keyboard.add_line()
    keyboard.add_button(label="Back", color="negative")
    keyboard.confirm()
    return keyboard


async def seventh_kb() -> Buttons:
    keyboard = Buttons(config=BASE_CONFIG, logger=logger)
    keyboard.add_button(label="Restart", color="positive")
    keyboard.add_line()
    keyboard.add_button(label="Back", color="negative")
    keyboard.confirm()
    return keyboard
