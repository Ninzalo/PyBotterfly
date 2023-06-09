from pybotterfly.bot.returns.buttons import Buttons, InlineButtons
from configs.config import BASE_CONFIG


async def first_kb() -> Buttons:
    keyboard = Buttons(config=BASE_CONFIG)
    keyboard.add_button(label="Start", color="positive")
    keyboard.confirm()  # Compiles the keyboard. You can't use keyboard without using this method
    return keyboard


async def second_kb() -> InlineButtons:
    keyboard = InlineButtons(config=BASE_CONFIG)
    keyboard.add_button(
        label="Go to next",
        color="primary",
        payload={
            "type": "default",
            "action": "go_to_third_page",
            "data": 123,
            "plus": 111,
        },  # payload argument is required for Inline_buttons
    )
    # adding button that we removed in configuration
    keyboard.add_button(
        label="Deleted button",
        color="negative",
        payload={
            "type": "fake",
            "id": "integer",
        },  # payload argument is required for Inline_buttons
    )
    keyboard.add_line()
    keyboard.add_button(
        label="Secret Page",
        color="negative",
        payload={
            "type": "secret",
            "action": "go_to_secret_page",
        },  # payload argument is required for Inline_buttons
    )
    keyboard.confirm()
    return keyboard


async def third_kb() -> Buttons:
    keyboard = Buttons(config=BASE_CONFIG)
    keyboard.add_button(label="Go to previous", color="secondary")
    keyboard.add_button(label="Go to beginning", color="negative")
    keyboard.add_line()  # Your next button will be on a new row
    keyboard.add_button(label="Go to next", color="positive")
    keyboard.add_line()
    keyboard.add_button(
        label="This button will not work", color="primary"
    )  # Really, this will not work. Just try to tap it c:
    keyboard.confirm()
    return keyboard


async def fourth_kb() -> Buttons:
    keyboard = Buttons(config=BASE_CONFIG)
    keyboard.add_button(label="Admin", color="positive")
    keyboard.add_button(label="Go back", color="negative")
    keyboard.confirm()
    return keyboard


async def fourth_admin_kb() -> Buttons:
    keyboard = Buttons(config=BASE_CONFIG)
    keyboard.add_button(label="Go back", color="negative")
    keyboard.confirm()
    return keyboard


async def fifth_kb() -> Buttons:
    keyboard = Buttons(config=BASE_CONFIG)
    keyboard.add_button(label="User", color="positive")
    keyboard.add_button(label="Go to beginning", color="negative")
    keyboard.confirm()
    return keyboard


async def secret_kb() -> Buttons:
    keyboard = Buttons(config=BASE_CONFIG)
    keyboard.add_button(label="Go to beginning", color="negative")
    keyboard.confirm()
    return keyboard
