import asyncpg
from configs.config import DB_NAME, PG_PORT, PG_USERNAME, LOCAL_IP


async def execute(sql, *args):
    connection = await _get_db()
    values = await connection.execute(sql, *args)
    await connection.close()
    return values


async def fetch(sql, *args):
    connection = await _get_db()
    values = await connection.fetch(sql, *args)
    await connection.close()
    return values


async def fetchval(sql, *args):
    connection = await _get_db()
    values = await connection.fetchval(sql, *args)
    await connection.close()
    return values


async def fetchrow(sql, *args):
    connection = await _get_db()
    values = await connection.fetchrow(sql, *args)
    await connection.close()
    return values


async def _get_db():
    conn = await asyncpg.connect(
        user=PG_USERNAME,
        host=LOCAL_IP,
        database=DB_NAME,
        port=PG_PORT,
    )
    return conn
