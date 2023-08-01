from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from abc import ABC, abstractmethod

from pybotterfly.base_config import BaseConfig


@dataclass()
class Log:
    level: Literal["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
    text: str
    time: datetime | None = None
    starts_with: str = ""


class BaseLogger(ABC):
    @abstractmethod
    def log(self, log: Log):
        pass


class DefaultLogger(BaseLogger):
    def __init__(self, config: BaseConfig = BaseConfig) -> None:
        self.config = config

    def log(self, log: Log):
        if self.config.DEBUG_STATE:
            log_str = (
                f"{log.starts_with}[{log.level}] "
                f"[{log.time if log.time != None else datetime.now()}]: "
                f"{log.text}"
            )
            print(log_str)
