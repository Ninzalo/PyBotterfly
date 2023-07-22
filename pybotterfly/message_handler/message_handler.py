from pybotterfly.base_config import BaseConfig
from pybotterfly.bot.returns.message import Returns
from pybotterfly.bot.struct import MessageStruct
from pybotterfly.bot.transitions.transitions import Transitions
from pybotterfly.message_handler.struct import Func


class MessageHandler:
    def __init__(
        self,
        transitions: Transitions,
        user_stage: Func,
        user_access_level: Func | None = None,
        base_config: BaseConfig = BaseConfig,
    ) -> None:
        """
        Initialises a Message_handler instance.

        :param transitions: An instance of the Transitions class.
        :type transitions: Transitions

        :param user_stage: Dataclass that contains:
            - .getter - a coroutine to get user’s stage. Should contain
                ‘user_messenger_id’ and ‘user_messenger’ args.
            - .setter - a coroutine to change user’s stage. Should contain
                'to_stage_id', ‘user_messenger_id’ and ‘user_messenger’ args.
        :type user_stage: Func

        :param user_access_level: Dataclass that contains:
            - .getter - a coroutine to get user’s access level. Should contain
                ‘user_messenger_id’ and ‘user_messenger’ args.
            - .setter - a coroutine to change user’s access level. Should
                contain 'tu_access_level', ‘user_messenger_id’ and
                ‘user_messenger’ args.
        :type user_access_level: Func | None

        :param base_config: An instance of the BaseConfig class.
        :type base_config: BaseConfig

        :returns: None
        :rtype: NoneType
        """
        self._transitions = transitions
        self._user_stage = user_stage
        self._user_access_level = user_access_level
        self._base_config = base_config
        self._config = base_config
        if self._config.DEBUG_STATE:
            print(f"Added user stage getter: {user_stage.getter}")
            if self._user_access_level:
                print(
                    f"Added user access level getter: "
                    f"{user_access_level.getter}"
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
        user_stage = await self._user_stage.getter(
            message_class.user_id, message_class.messenger
        )
        user_access_level = "any"
        if self._user_access_level != None:
            user_access_level = await self._user_access_level.getter(
                message_class.user_id, message_class.messenger
            )
        return_cls = await self._transitions.run(
            message=message_class,
            user_messenger_id=message_class.user_id,
            user_messenger=message_class.messenger,
            user_stage=user_stage,
            user_stage_changer=self._user_stage.setter,
            user_access_level=user_access_level,
            user_access_level_changer=self._user_access_level.setter,
        )
        return_cls = await self._shorten_inline_buttons(return_func=return_cls)
        return return_cls

    async def _shorten_inline_buttons(self, return_func: Returns) -> None:
        if self._transitions.payloads == None or return_func == None:
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
            AttributeError: if the user stage getter coroutine doesn't receive
                'user_messenger_id' and 'user_messenger'.
            AttributeError: if the user access level getter coroutine is not set
                while user access level changer is set
        """
        if not self._transitions._compiled:
            raise RuntimeError(f"Transitions aren't compiled")
        self._user_stage.args_check(
            arg="to_stage_id", func=self._user_stage.setter
        )
        if self._user_access_level != None:
            self._user_access_level.args_check(
                arg="to_access_level", func=self._user_access_level.setter
            )
        if self._config.DEBUG_STATE:
            print(f"\n[SUCCESS] Message handler's checks passed\n")
