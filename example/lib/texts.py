async def first_str() -> str:
    text = f"This is the first page!\nTap 'Start' to continue..."
    return text


async def second_str() -> str:
    text = (
        f"Try to tap on the “Deleted button” or on the 'Start'. You will "
        f"receive an error.\n"
        f"The only way to get to the next page is to click "
        f"'Go next' inline button."
    )
    return text


async def third_before_str(data: str, id: int) -> str:
    text = (
        f"You passed in 'data' and 'id' params with the previous payload.\n"
        f"Data: {data}\n"
        f"ID:  {id}\n"
        f"Now press the 'Tap it' button"
    )
    return text


async def third_after_str() -> str:
    text = (
        f"Your 'stage_id' field in the DB was not changed, but the "
        f"page was updated.\n"
        f"You can check it by clicking 'Tap it' button from the previous "
        f"message"
    )
    return text


async def fourth_str() -> str:
    text = (
        f"Only admins are allowed to go to next page.\n"
        f"You can check it by clicking 'Next' button. You will receive "
        f"an error until you press the 'Admin' button"
    )
    return text


async def fifth_str() -> str:
    text = (
        f"Here you can send me any photo (nothing will be saved, "
        f"promise you) to go to the next page.\n"
        f"Or you can just skip this :c"
    )
    return text


async def sixth_str() -> str:
    text = (
        f"Here you can send me any document with ‘.xls’ / ‘.xlsx’ "
        f"/ ’.docx’ / ’.pdf’ extension (again, nothing will be saved) to "
        f"complete the training"
    )
    return text


async def seventh_str() -> str:
    text = (
        f"Congrats!!!\n"
        "You’ve completed the training.\n"
        "Now you know how to create basic bot with the PyBotterfly library.\n"
        "Click the button below to restart your training"
    )
    return text


async def error_return() -> str:
    text = f"Input error :c"
    return text
