async def first_str() -> str:
    text = f"This is the first page!\nTap 'Start' to continue..."
    return text


async def second_str() -> str:
    text = f"This is the second page!\nNow let's tap the inline button"
    return text


async def third_str() -> str:
    text = (
        f"This is the third page!\n"
        f"You can go back by tapping the 'Go to previous' button\n"
        f"Or you can go to the beginning by tapping the 'Go to beginning' button"
    )
    return text


async def error_return() -> str:
    text = f"Input error :c"
    return text
