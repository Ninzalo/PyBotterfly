from dataclasses import dataclass, field
from typing import List, Any
from pybotterfly.bot.returns.message import Return
from pybotterfly.base_config import BaseConfig
from pybotterfly.bot.throttlers import ThrottledResource


@dataclass()
class _Messenger:
    """
    Represents a messaging platform that the bot can respond to.

    :param trigger: The messaging platform that triggers the reply.
    :type trigger: BaseConfig.ADDED_MESSENGERS
    :param reply_func: The function that sends the response.
    :type reply_func: Any
    :param messages_per_second: The maximum number of messages the bot can
        send per second.
    :type messages_per_second: int
    :param _throttler: A ThrottledResource object that throttles the rate at
        which messages can be sent. Defaults to None.
    :type _throttler: ThrottledResource or None
    """

    trigger: BaseConfig.ADDED_MESSENGERS
    reply_func: Any
    messages_per_second: int
    _throttler: ThrottledResource | None = None


@dataclass()
class Messengers_division:
    """
    A class that represents a division of messengers to answer. Contains a
    list of _Messenger objects that correspond to specific messaging
    platforms, and a boolean attribute that indicates whether the list
    has been compiled or not.

    :param _messengers_to_answer: The list of _Messenger objects that
        correspond to specific messaging platforms.
    :type _messengers_to_answer: List[_Messenger]
    :param _compiled: A boolean indicating whether the list of
        _Messenger objects has been compiled or not.
    :type _compiled: bool
    """

    config: BaseConfig = BaseConfig
    _messengers_to_answer: List[_Messenger] = field(default_factory=list)
    _compiled: bool = False

    def register_messenger(
        self,
        trigger: BaseConfig.ADDED_MESSENGERS,
        reply_func: Any,
        messages_per_second: int,
    ) -> None:
        """
        Registers a new messenger to reply with, along with its trigger, reply
        function, and messages per second limit. The messenger is added to the
        `_messengers_to_answer` list.

        Raises a `ValueError` if the `Bot` object has already been compiled, or
        if the new messenger to reply has the same `trigger` as an existing one
        or the same `reply_func` as an existing one.

        :param trigger: The messenger trigger to register.
        :type trigger: BaseConfig.ADDED_MESSENGERS
        :param reply_func: The reply function to associate with the messenger.
        :type reply_func: Any
        :param messages_per_second: The limit of messages that can be sent per
            second by the messenger.
        :type messages_per_second: int
        """

        if self._compiled:
            error_str = (
                f"Messengers already compiled"
                f"\nEnsure to add messengers before compiling"
            )
            raise ValueError(error_str)
        new_messenger_to_reply = _Messenger(
            trigger=trigger,
            reply_func=reply_func,
            messages_per_second=messages_per_second,
        )
        if new_messenger_to_reply in self._messengers_to_answer:
            error_str = f"Messenger already registered"
            raise ValueError(error_str)
        if reply_func in [
            func.reply_func for func in self._messengers_to_answer
        ]:
            error_str = f"Same reply func already used"
            raise ValueError(error_str)
        self._messengers_to_answer.append(new_messenger_to_reply)

    def compile(self) -> None:
        """
        Compiles the registered messengers by initializing a `ThrottledResource`
        for each messenger with the given messages per second rate and reply
        function. This method must be called after all messengers have been
        registered and before starting the client.

        :return: None
        :rtype: None
        :raises ValueError: If the messengers are already compiled.
        """

        if self._compiled:
            raise ValueError(f"Messengers already compiled")
        for messenger in self._messengers_to_answer:
            messenger._throttler = ThrottledResource(
                delay=1.0 / messenger.messages_per_second,
                func_to_throttle=messenger.reply_func,
            )
            if self.config.DEBUG_STATE:
                print(
                    f"Added throttler for Messenger '{messenger.trigger}' "
                    f"with rate of {messenger.messages_per_second} messages "
                    f"per second"
                )
        if self.config.DEBUG_STATE:
            print(f"\n[SUCCESS] Messengers compiled successfully\n")
        if not self._compiled:
            self._compiled = True

    async def get_func(
        self, messenger: BaseConfig.ADDED_MESSENGERS, return_cls: Return
    ) -> None:
        """
        If the list of `_Messenger` objects has been compiled, this method
        finds the existing `_Messenger` object that corresponds to the
        specified `messenger` and makes an asynchronous query to it using
        the specified `return_cls`. If no matching `_Messenger` object is
        found, an error message is printed.

        :param messenger: The messenger platform to query.
        :type messenger: BaseConfig.ADDED_MESSENGERS
        :param return_cls: The return type for the query.
        :type return_cls: Return
        """

        if self._compiled:
            for existing_messenger in self._messengers_to_answer:
                if existing_messenger.trigger == messenger:
                    await existing_messenger._throttler.query(return_cls)
                    return
            error_str = (
                f"[ERROR] Needed messenger '{messenger}' wasn't registered"
            )
            print(error_str)
