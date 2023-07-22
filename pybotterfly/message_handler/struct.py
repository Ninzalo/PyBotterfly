import inspect
from dataclasses import dataclass
from typing import Coroutine


@dataclass()
class Func:
    getter: Coroutine
    setter: Coroutine

    def __post_init__(self) -> None:
        self._checks()

    def _checks(self) -> None:
        main_args = [
            "user_messenger_id",
            "user_messenger",
        ]
        for arg in main_args:
            self.args_check(arg, self.getter)
            self.args_check(arg, self.setter)

    def args_check(self, arg: str, func: Coroutine) -> None:
        if arg not in inspect.getfullargspec(func)[0]:
            error_str = f"Coroutine '{func}' must have argument '{arg}'"
            raise AttributeError(error_str)
