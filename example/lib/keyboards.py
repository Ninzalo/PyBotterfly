from pybotterfly.bot.returns.buttons import Buttons, InlineButtons

from configs.config import BASE_CONFIG


async def first_kb() -> Buttons:
    keyboard = Buttons(config=BASE_CONFIG)
    keyboard.add_button(label="Start", color="positive")
    keyboard.confirm()
    return keyboard


async def second_kb() -> InlineButtons:
    keyboard = InlineButtons(config=BASE_CONFIG)
    # payload param is required for Inline_buttons
    keyboard.add_button(
        label="Go to next",
        color="primary",
        payload={
            "t": "d",
            "a": "g_t_t_p",
        },  # words 'go', 'to', 'third', 'page' are in the 'words to shorten' list
    )
    keyboard.confirm()
    return keyboard


async def third_kb() -> Buttons:
    keyboard = Buttons(config=BASE_CONFIG)
    keyboard.add_button(label="Go to previous", color="secondary")
    keyboard.add_button(label="Go to beginning", color="negative")
    keyboard.confirm()
    return keyboard
