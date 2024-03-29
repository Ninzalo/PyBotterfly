from pybotterfly.bot.returns.message import Returns, file_validator
from lib import keyboards
from lib import texts


# Every page coroutine should include 'user_messenger_id', 'user_messenger', 'message' arguments
async def first_page(
    user_messenger_id: int,  # :int. User id to send the message. 'user_messenger_id' is always required
    user_messenger: str,  # :str. Represents one of the added messengers to which the user belongs. 'user_messenger' is always required
    message: str
    | dict,  # :str|dict. Received message | payload from user. 'message' is always required
) -> Returns:
    text = await texts.first_str()
    keyboard = await keyboards.first_kb()
    return_cls = await Returns().add_return(
        user_messenger_id=user_messenger_id,  # :int. User id to send the message
        user_messenger=user_messenger,  # :str. Represents one of the added messengers to which the user belongs
        text=text,  #:str. Text of the message (page)
        keyboard=keyboard,  # :Buttons. [Optional] An instance of preconfigured Buttons class. You are not able to add this argument if your keyboard is the instance of InlineButtons class
        # inline_keyboard=keyboard,  # :InlineButtons. [Optional] An instance of preconfigured InlineButtons class. You are not able to add this argument if your keyboard is the instance of Buttons class
        # attachments=file_validator(
        #     message=message
        # ),  # :List[File]. [Optional] List of files to send with the message
    )
    return return_cls


async def second_page(
    user_messenger_id: int, user_messenger: str, message: str | dict
) -> Returns:
    text = await texts.second_str()
    inline_keyboard = await keyboards.second_ikb()
    return_cls = Returns()
    await return_cls.add_return(
        user_messenger_id=user_messenger_id,
        user_messenger=user_messenger,
        text=text,
        inline_keyboard=inline_keyboard,
    )
    return return_cls


async def third_before_page(
    user_messenger_id: int, user_messenger: str, message: str | dict
) -> Returns:
    text = await texts.third_before_str(
        data=message.get("data") if isinstance(message, dict) else None,
        id=message.get("id") if isinstance(message, dict) else None,
    )
    inline_keyboard = await keyboards.third_before_ikb()
    return_cls = Returns()
    await return_cls.add_return(
        user_messenger_id=user_messenger_id,
        user_messenger=user_messenger,
        text=text,
        inline_keyboard=inline_keyboard,
    )
    return return_cls


async def third_after_page(
    user_messenger_id: int, user_messenger: str, message: str | dict
) -> Returns:
    text = await texts.third_after_str()
    inline_keyboard = await keyboards.third_after_ikb()
    return_cls = Returns()
    await return_cls.add_return(
        user_messenger_id=user_messenger_id,
        user_messenger=user_messenger,
        text=text,
        inline_keyboard=inline_keyboard,
    )
    return return_cls


async def fourth_page(
    user_messenger_id: int, user_messenger: str, message: str | dict
) -> Returns:
    text = await texts.fourth_str()
    keyboard = await keyboards.fourth_kb()
    return_cls = Returns()
    await return_cls.add_return(
        user_messenger_id=user_messenger_id,
        user_messenger=user_messenger,
        text=text,
        keyboard=keyboard,
    )
    return return_cls


async def fifth_page(
    user_messenger_id: int, user_messenger: str, message: str | dict
) -> Returns:
    text = await texts.fifth_str()
    keyboard = await keyboards.fifth_kb()
    return_cls = Returns()
    await return_cls.add_return(
        user_messenger_id=user_messenger_id,
        user_messenger=user_messenger,
        text=text,
        keyboard=keyboard,
    )
    return return_cls


async def sixth_page(
    user_messenger_id: int, user_messenger: str, message: str | dict
) -> Returns:
    text = await texts.sixth_str()
    keyboard = await keyboards.fifth_kb()
    return_cls = Returns()
    await return_cls.add_return(
        user_messenger_id=user_messenger_id,
        user_messenger=user_messenger,
        text=text,
        keyboard=keyboard,
        attachments=file_validator(
            message=message
        ),  # :List[File]. [Optional] List of files to send with the message
    )
    return return_cls


async def seventh_page(
    user_messenger_id: int, user_messenger: str, message: str | dict
) -> Returns:
    text = await texts.seventh_str()
    keyboard = await keyboards.seventh_kb()
    return_cls = Returns()
    await return_cls.add_return(
        user_messenger_id=user_messenger_id,
        user_messenger=user_messenger,
        text=text,
        keyboard=keyboard,
        attachments=file_validator(
            message=message
        ),  # :List[File]. [Optional] List of files to send with the message
    )
    return return_cls


async def error_page(
    user_messenger_id: int, user_messenger: str, message: str | dict
) -> Returns:
    text = await texts.error_return()
    return_cls = Returns()
    await return_cls.add_return(
        user_messenger_id=user_messenger_id,
        user_messenger=user_messenger,
        text=text,
    )
    return return_cls
