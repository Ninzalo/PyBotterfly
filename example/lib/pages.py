from pybotterfly.bot.returns.message import Returns
from lib import keyboards
from lib import texts
from lib import stages
from lib.users import change_user_stage


async def first_page(
    user_messenger_id: int, user_messenger: str, message: str
) -> Returns:
    await change_user_stage(
        new_stage=stages.General.first,
        user_messenger_id=user_messenger_id,
        user_messenger=user_messenger,
    )
    text = await texts.first_str()
    keyboard = await keyboards.first_kb()
    return_cls = Returns()
    await return_cls.add_return(
        user_messenger_id=user_messenger_id,
        user_messenger=user_messenger,
        text=text,
        keyboard=keyboard,
    )
    return return_cls


async def second_page(
    user_messenger_id: int, user_messenger: str, message: str
) -> Returns:
    await change_user_stage(
        new_stage=stages.General.second,
        user_messenger_id=user_messenger_id,
        user_messenger=user_messenger,
    )
    text = await texts.second_str()
    inline_keyboard = await keyboards.second_kb()
    return_cls = Returns()
    await return_cls.add_return(
        user_messenger_id=user_messenger_id,
        user_messenger=user_messenger,
        text=text,
        inline_keyboard=inline_keyboard,
    )
    return return_cls


async def third_page(
    user_messenger_id: int, user_messenger: str, message: str
) -> Returns:
    await change_user_stage(
        new_stage=stages.General.third,
        user_messenger_id=user_messenger_id,
        user_messenger=user_messenger,
    )
    text = await texts.third_str()
    keyboard = await keyboards.third_kb()
    return_cls = Returns()
    await return_cls.add_return(
        user_messenger_id=user_messenger_id,
        user_messenger=user_messenger,
        text=text,
        keyboard=keyboard,
    )
    return return_cls


async def error_page(
    user_messenger_id: int, user_messenger: str, message: str
) -> Returns:
    text = await texts.error_return(message=message)
    return_cls = Returns()
    await return_cls.add_return(
        user_messenger_id=user_messenger_id,
        user_messenger=user_messenger,
        text=text,
    )
    return return_cls
