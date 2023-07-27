import asyncio
import asyncpg
from configs.config import PG_PORT, LOCAL_IP, DB_NAME, PG_USERNAME


async def create_users_table():
    sql = """
    CREATE TABLE IF NOT EXISTS public.users
(
    user_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    user_messenger_id integer NOT NULL,
    user_messenger character varying(2) COLLATE pg_catalog."default" NOT NULL,
    connection_time timestamp without time zone NOT NULL DEFAULT (now() AT TIME ZONE 'utc-3'::text),
    user_stage character varying COLLATE pg_catalog."default" NOT NULL,
    user_type character varying COLLATE pg_catalog."default" NOT NULL DEFAULT 'user'::character varying,
    CONSTRAINT users_pkey PRIMARY KEY (user_id)
)
    """
    conn = await asyncpg.connect(
        user=PG_USERNAME,
        host=LOCAL_IP,
        database=DB_NAME,
        port=PG_PORT,
    )
    values = await conn.execute(sql)
    await conn.close()
    return values


async def main():
    await create_users_table()
    print(f"Users table created successfully")


if __name__ == "__main__":
    asyncio.run(main())
