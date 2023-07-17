import inspect
from typing import Coroutine
from pybotterfly.base_config import BaseConfig
from pybotterfly.bot.returns.message import Returns
from pybotterfly.bot.struct import MessageStruct
from pybotterfly.bot.transitions.transitions import Transitions


class MessageHandler:
    def __init__(
        self,
        transitions: Transitions,
        user_stage_getter: Coroutine,
        user_stage_changer: Coroutine,
        user_access_level_getter: Coroutine | None = None,
        user_access_level_changer: Coroutine | None = None,
        base_config: BaseConfig = BaseConfig,
    ) -> None:
        """
        Initialises a Message_handler instance.

        :param transitions: An instance of the Transitions class.
        :type transitions: Transitions

        :param user_stage_getter: A coroutine that receives 'user_messenger_id'
            and 'user_messenger'.
        :type user_stage_getter: Coroutine

        :param user_stage_changer: A coroutine that changes the 'user_stage'
        :type user_stage_changer: Coroutine

        :user_access_level_getter: A coroutine that receives 'user_type'
        :type user_access_level_getter: Coroutine | None

        :user_access_level_changer: A coroutine that changes the 'user_type'
        :type user_access_level_changer: Coroutine | None

        :param base_config: An instance of the BaseConfig class.
        :type base_config: BaseConfig

        :returns: None
        :rtype: NoneType
        """
        self._transitions = transitions
        self._user_stage_getter = user_stage_getter
        self._user_stage_changer = user_stage_changer
        self._user_access_level_getter = user_access_level_getter
        self._user_access_level_changer = user_access_level_changer
        self._base_config = base_config
        self._config = base_config
        if self._config.DEBUG_STATE:
            print(f"Added user stage getter: {user_stage_getter}")
            if self._user_access_level_getter:
                print(
                    f"Added user access level getter: "
                    f"{user_access_level_getter}"
                )
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
        user_access_level = "any"
        if self._user_access_level_getter != None:
            user_access_level = await self._user_access_level_getter(
                message_class.user_id, message_class.messenger
            )
        return_cls = await self._transitions.run(
            message=message_class,
            user_messenger_id=message_class.user_id,
            user_messenger=message_class.messenger,
            user_stage=user_stage,
            user_stage_changer=self._user_stage_changer,
            user_access_level=user_access_level,
            user_access_level_changer=self._user_access_level_changer,
        )
        return_cls = await self._shorten_inline_buttons(return_func=return_cls)
        return return_cls

    async def _shorten_inline_buttons(self, return_func: Returns) -> None:
        if self._transitions.payloads == None:
            return return_func
        if return_func == None:
            return return_func
        for return_message in return_func.returns:
            if return_message.inline_keyboard != None:
                for inline_button in return_message.inline_keyboard.buttons:
                    inline_button.payload = (
                        self._transitions.payloads.shortener(
                            inline_button.payload
                        )
                    )
        return return_func

    def _checks(self) -> None:
        """
        Performs checks to ensure that the Message_handler instance has
        been correctly initialised.

        :returns: None
        :rtype: NoneType

        :raises:
            RuntimeError: if the Transitions instance hasn't been compiled
            RuntimeError: if the user stage getter coroutine doesn't receive
                'user_messenger_id' and 'user_messenger'.
            RuntimeError: if the user access level getter coroutine is not set
                while user access level changer is set
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
        if inspect.getfullargspec(self._user_stage_changer)[0] != [
            "to_stage_id",
            "user_messenger_id",
            "user_messenger",
        ]:
            error_str = (
                "User stage changer don't receive 'to_stage_id', "
                "'user_messenger_id' and 'user_messenger'"
            )
            raise RuntimeError(error_str)
        if (
            self._user_access_level_changer != None
            and self._user_access_level_getter == None
        ):
            error_str = (
                "user_access_level_getter must be set if "
                "user_access_level_changer is set"
            )
            raise RuntimeError(error_str)
        if self._user_access_level_getter != None and inspect.getfullargspec(
            self._user_access_level_getter
        )[0] != [
            "user_messenger_id",
            "user_messenger",
        ]:
            raise RuntimeError(
                "User access level getter don't receive 'user_messenger_id' "
                "and 'user_messenger'"
            )
        if self._user_access_level_changer != None and inspect.getfullargspec(
            self._user_access_level_changer
        )[0] != ["to_access_level", "user_messenger_id", "user_messenger"]:
            error_str = (
                "User access level changer don't receive "
                "'to_access_level', 'user_messenger_id' and "
                "'user_messenger'"
            )
            raise RuntimeError(error_str)
        if self._config.DEBUG_STATE:
            print(f"\n[SUCCESS] Message handler's checks passed\n")
