import os
from typing import Literal
from dotenv import load_dotenv
from pybotterfly.base_config import BaseConfig

load_dotenv()

# VK data
token_vk = str(os.getenv("GROUP_API_VK"))  # specify your VK GROUP API KEY
group_id = str(os.getenv("GROUP_ID_VK"))  # specify your group id
TEST_ID_VK = int(
    os.getenv("TEST_ID_VK")
)  # specify your VK id for running tests

# TG data
token_tg = str(os.getenv("GROUP_API_TG"))  # specify your TG API KEY
TEST_ID_TG = int(
    os.getenv("TEST_ID_TG")
)  # specify your TG id for running tests

LOCAL_IP = "127.0.0.1"  # default local ip
LOCAL_PORT = 8888  # default local port

# Replies per second
MESSAGE_REPLY_RATE = 4

# PostgreSQL data
PG_USERNAME = "postgres"  # specify your PostgreSQL username
PG_DBNAME = "YOUR_DB_NAME"  # specify your PostgreSQL database name
PG_PORT = 5433  # specify your PostgreSQL port

# Edit Base bots config
BASE_CONFIG = BaseConfig()
BASE_CONFIG.ADDED_MESSENGERS = Literal["vk", "tg"]
BASE_CONFIG.BUTTONS_COLORS = Literal[
    "primary", "secondary", "positive", "negative"
]
BASE_CONFIG.DEBUG_STATE: bool = (
    True  # =True is recommended while setting up the bot logic
)
