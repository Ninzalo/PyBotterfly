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
    keyboard.confirm()
    return keyboard


async def third_kb() -> Buttons:
    keyboard = Buttons(config=BASE_CONFIG)
    keyboard.add_button(label="Go to previous", color="secondary")
    keyboard.add_button(label="Go to beginning", color="negative")
    keyboard.add_line()  # Your next button will be on a new row
    keyboard.add_button(
        label="This button will not work", color="primary"
    )  # Really, this will not work. Just try to tap it c:
    keyboard.confirm()
    return keyboard
