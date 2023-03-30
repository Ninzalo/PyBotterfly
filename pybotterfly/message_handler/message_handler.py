import inspect
from typing import Coroutine
from pybotterfly.base_config import BaseConfig
from pybotterfly.bot.returns.message import Returns
from pybotterfly.bot.struct import MessageStruct
from pybotterfly.bot.transitions.transitions import Transitions


class MessageHandler:
    def __init__(
        self,
        user_stage_getter: Coroutine,
        transitions: Transitions,
        base_config: BaseConfig = BaseConfig,
    ) -> None:
        """
        Initialises a Message_handler instance.

        :param user_stage_getter: A coroutine that receives 'user_messenger_id'
            and 'user_messenger'.
        :type user_stage_getter: Coroutine

        :param transitions: An instance of the Transitions class.
        :type transitions: Transitions

        :param base_config: An instance of the BaseConfig class.
        :type base_config: BaseConfig

        :returns: None
        :rtype: NoneType
        """
        self._transitions = transitions
        self._user_stage_getter = user_stage_getter
        self._config = base_config
        if self._config.DEBUG_STATE:
            print(f"Added user stage getter: {user_stage_getter}")
        self._checks()

    async def get(self, message_class: MessageStruct) -> Returns:
        """
        Retrieves a Returns instance by running the Transitions instance
        according to the provided message data and user stage data.

        :param message_class: An instance of the Message_struct class.
        :type message_class: Message_struct

        :returns: An instance of the Returns class.
        :rtype: Returns
        """
        user_stage = await self._user_stage_getter(
            message_class.user_id, message_class.messenger
        )
        return_cls = await self._transitions.run(
            user_messenger_id=message_class.user_id,
            user_messenger=message_class.messenger,
            user_stage=user_stage,
            message=message_class,
        )
        return return_cls

    def _checks(self) -> None:
        """
        Performs checks to ensure that the Message_handler instance has
        been correctly initialised.

        :returns: None
        :rtype: NoneType

        :raises: RuntimeError if the Transitions instance hasn't been compiled
            or if the user stage getter coroutine doesn't receive
            'user_messenger_id' and 'user_messenger'.
        """
        if not self._transitions._compiled:
            raise RuntimeError(f"Transitions aren't compiled")
        if inspect.getfullargspec(self._user_stage_getter)[0] != [
            "user_messenger_id",
            "user_messenger",
        ]:
            raise RuntimeError(
                "User stage getter don't receive 'user_messenger_id' "
                "and 'user_messenger'"
            )
        if self._config.DEBUG_STATE:
            print(f"\n[SUCCESS] Message handler's checks passed\n")
