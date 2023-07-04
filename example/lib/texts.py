async def first_str() -> str:
    text = f"This is the first page!\nTap 'Start' to continue..."
    return text


async def second_str() -> str:
    text = f"This is the second page!\nNow let's tap the inline button"
    return text


async def third_str(message: dict | None = None) -> str:
    text = (
        f"This is the third page!\n"
        f"You can go back by tapping the 'Go to previous' button\n"
        f"Or you can go to the beginning by tapping the 'Go to beginning' button"
    )
    if isinstance(message, dict):
        text += (
            f"\n\nYour data from payload: "
            f"{message.get('data'), message.get('plus')}"
        )
    else:
        text += f"\n\nNo data passed in as a dict"
    return text


async def fourth_str() -> str:
    text = (
        f"This is the fourth page.\n"
        f"You will not be able to go to the secret page until you become "
        f"an Admin.\n"
        f"You can became an admin by tapping the 'Admin' button."
    )
    return text


async def fourth_admin_str() -> str:
    text = f"Now you are an admin!\n"
    return text


async def fifth_str() -> str:
    text = (
        f"Congrats! You've reached the secret page!\n"
        f"You can switch back to a normal user by tapping the 'User' button.\n"
        f"Or you can just go to the beginning by tapping the 'Go to beginning'"
        f"button"
    )
    return text


async def secret_page() -> str:
    text = f"Wow! You are on the secret page!\nGood job c:"
    return text


async def error_return(message: str | None = None) -> str:
    text = f"Input error :c"
    if message != None:
        text += f"\nUnsopported message: {message}"
    return text
