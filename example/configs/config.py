import os
from typing import Literal, TypeAlias
from dotenv import load_dotenv
from pybotterfly.base_config import BaseConfig

load_dotenv()

# VK data
token_vk = str(os.getenv("GROUP_API_VK"))  # :str. Your VK GROUP API KEY
group_id = str(os.getenv("GROUP_ID_VK"))  # :str. Your group id
TEST_ID_VK = int(os.getenv("TEST_ID_VK"))  # :int. Your VK id for running tests

# TG data
token_tg = str(os.getenv("BOT_API_TG"))  # :str. Your TG bot's API KEY
TEST_ID_TG = int(os.getenv("TEST_ID_TG"))  # :int. Your TG id for running tests

LOCAL_IP = "127.0.0.1"  # :str. default local ip
LOCAL_PORT = 8888  # :int. default local port

# Replies per second
MESSAGE_REPLY_RATE = 4

# Database data
PG_USERNAME = "postgres"  # :str. Your PostgreSQL username
DB_NAME = "YOUR_DB_NAME"  # :str. Your PostgreSQL database name
PG_PORT = 5433  # :int. Your PostgreSQL port

# Edit Base bots config
BASE_CONFIG = BaseConfig()
BASE_CONFIG.ADDED_MESSENGERS: TypeAlias = Literal[
    "vk", "tg"
]  # Messengers added to the bot
BASE_CONFIG.BUTTONS_COLORS: TypeAlias = Literal[
    "primary",
    "secondary",
    "positive",
    "negative",  # Default colors for VK keyboard
]
BASE_CONFIG.DEBUG_STATE: bool = (
    True  # =True is recommended while setting up the bot logic
)
