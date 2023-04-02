from lib.db_funcs import fetch, execute, fetchval
from lib import stages


async def user_exists(user_messenger_id: int, user_messenger: str):
    sql = """SELECT user_id FROM users 
    WHERE user_messenger_id = $1 AND user_messenger = $2"""
    params = (user_messenger_id, user_messenger)
    users = await fetch(sql, *params)
    return bool(len(users))


async def add_user(user_messenger_id: int, user_messenger: str):
    if await user_exists(
        user_messenger_id=user_messenger_id, user_messenger=user_messenger
    ):
        return
    sql = """INSERT INTO users (user_messenger_id, user_messenger, user_stage) 
    VALUES ($1, $2, $3)"""
    params = (user_messenger_id, user_messenger, stages.General.start)
    await execute(sql, *params)


async def get_user_stage(user_messenger_id: int, user_messenger: str):
    await add_user(
        user_messenger_id=user_messenger_id, user_messenger=user_messenger
    )
    sql = """SELECT user_stage FROM users 
    WHERE user_messenger_id = $1 AND user_messenger = $2"""
    params = (user_messenger_id, user_messenger)
    result = await fetchval(sql, *params)
    return result


async def change_user_stage(
    new_stage: str, user_messenger_id: int, user_messenger: str
):
    sql = """UPDATE users SET user_stage = $1 
    WHERE user_messenger_id = $2 AND user_messenger = $3"""
    params = (new_stage, user_messenger_id, user_messenger)
    await execute(sql, *params)
