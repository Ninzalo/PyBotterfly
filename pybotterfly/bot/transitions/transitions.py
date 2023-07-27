import inspect
from emoji import replace_emoji
from dataclasses import dataclass, field, is_dataclass
from typing import Coroutine, List
from pybotterfly.base_config import BaseConfig
from pybotterfly.bot.returns.message import Returns
from pybotterfly.bot.struct import MessageStruct
from pybotterfly.bot.transitions.payloads import Payloads


@dataclass(init=False)
class FileTrigger:
    def __init__(
        self,
        extensions: List[BaseConfig.ALLOWED_FILE_TYPES]
        | BaseConfig.ALLOWED_FILE_TYPES,
        temporary: bool = True,
    ) -> None:
        self.extensions = (
            extensions if isinstance(extensions, list) else [extensions]
        )
        self.temporary = temporary

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(extensions={self.extensions}, "
            f"temporary={self.temporary})"
        )


@dataclass()
class Transition:
    """
    Describes a transition between two stages in a conversation.

    :param trigger: The event that triggers the transition, if any.
        Defaults to None.
    :type trigger: str | FileTrigger | None

    :param from_stage: The name of the stage to transition from.
    :type from_stage: str

    :param to_stage: The coroutine representing the stage to transition to.
    :type to_stage: Coroutine

    :param to_stage_id: The ID of the stage to transition to. Defaults to None.
    :type to_stage_id: str | None

    :param access_level: The user's access level. Defaults to ['any'].
    :type access_level: List[str]

    :param to_access_level: The user's access level to transition to.
        Defaults to None
    :type to_access_level: str | None
    """

    trigger: str | FileTrigger | None
    from_stage: str
    to_stage: Coroutine
    to_stage_id: str | None = None
    access_level: List[str] = field(default_factory=["any"])
    to_access_level: str | None = None


@dataclass()
class Transitions:
    """
    FSM (finite state machine). Add transitions and compile before using

    param transitions: Added transitions
    param error_return: Coroutine with 'user_messenger_id'
    and 'user_messenger' args
    param payloads: Should be Payloads class
    """

    transitions: List[Transition] = field(default_factory=list)
    error_return: Coroutine | None = None
    payloads: Payloads | None = None
    config: BaseConfig = BaseConfig
    _compiled: bool = False

    def __post_init__(self):
        if self.config.DEBUG_STATE:
            if self.payloads is None:
                print(f"Payloads aren't added")

    def add_transition(
        self,
        trigger: str | None,
        from_stage: str,
        to_stage: Coroutine,
        to_stage_id: str | None = None,
        access_level: str | List[str] = "any",
        to_access_level: str | None = None,
    ) -> None:
        """
        Adds a transition to the list of transitions.

        :param trigger: The trigger that causes the transition to occur.
            If None, the transition will act as a default transition.
        :type trigger: str | None

        :param from_stage: The source state of the transition.
        :type from_stage: str

        :param to_stage: The coroutine function that the transition goes to.
        :type to_stage: Coroutine

        :param to_stage_id: The ID of the stage the transition goes to.
            Defaults to None
        :type to_stage_id: str | None

        :param access_level: The access level of the transition. Defaults
            to 'any'
        :type access_level: str | List[str]

        :raises ValueError: If transitions are already compiled, or if the
            transition already exists or if another trigger has already
            realized the transition, or if multiple 'else' blocks
            aren't supported.
        """
        if isinstance(trigger, str):
            trigger = trigger.lower()
        validated_access_level = (
            [access_level] if isinstance(access_level, str) else access_level
        )
        new_transition = Transition(
            trigger=trigger,
            from_stage=from_stage,
            to_stage=to_stage,
            to_stage_id=to_stage_id,
            access_level=validated_access_level,
            to_access_level=to_access_level,
        )
        if self._compiled:
            raise ValueError(
                "Transitions already compiled. "
                "Please, compile after adding all of the transitions"
            )
        if new_transition in self.transitions:
            error_str = f"Transition already exists: {new_transition}"
            raise ValueError(error_str)

        if (
            self._counter_unique(trigger=trigger, src=from_stage, dst=to_stage)
            > 0
        ):
            raise ValueError("Transition already realized by other trigger")

        if new_transition.trigger is None:
            if self._counter_none(src=from_stage) > 0:
                raise ValueError("Multiple 'else' blocks aren't supported")
            self.transitions.append(new_transition)
        else:
            self.transitions.append(new_transition)
        if self.config.DEBUG_STATE:
            print(f"Added transition: {new_transition}")

    def add_error_return(self, error_func: Coroutine) -> None:
        """
        Sets the error return function for the state machine.

        :param error_func: The coroutine function to call in the event of
            an error.
        :type error_func: Coroutine

        :returns: None
        """
        self.error_return = error_func
        if self.config.DEBUG_STATE:
            print(f"Added error transition return: {error_func}")

    def compile(self) -> None:
        """
        Compiles the transitions and performs various checks to ensure the
        validity of the transitions. This method should be called only after
        adding all the transitions.

        :raises ValueError: If the transitions have already been compiled.

        :return: None
        """
        self._add_none_transition_to_all_stages()
        self._checks()
        self.transitions.sort(key=lambda src: src.from_stage)
        self._compiled = True
        if self.config.DEBUG_STATE:
            print(f"\n[SUCCESS] Transitions compiled successfully\n")

    async def run(
        self,
        message: MessageStruct,
        user_messenger_id: int,
        user_messenger: config.ADDED_MESSENGERS,
        user_stage: str,
        user_access_level: str | None,
        user_stage_changer: Coroutine | None,
        user_access_level_changer: Coroutine | None,
        user_file_saver: Coroutine | None = None,
    ) -> Returns:
        """
        Runs the state machine with the given input message, and returns the
        output.

        :param message: The message to process. Should have .text/.payload
        :type message: Message_struct

        :param user_messenger_id: The ID of the user's messenger account.
        :type user_messenger_id: int

        :param user_messenger: The type of messenger account
            (e.g., VK Messenger, Telegram, etc.).
        :type user_messenger: BaseConfig.ADDED_MESSENGERS

        :param user_stage: The current stage of the state machine.
        :type user_stage: str

        :param user_access_level: The user's access level.
        :type user_access_level: str | None

        :param user_stage_changer: The stage changer function.
        :type user_stage_changer: Coroutine | None

        :param user_access_level_changer: The access level changer function.
        :type user_access_level_changer: Coroutine | None

        :param user_file_saver: A coroutine that saves user’s file to
            the database.
        :type user_file_saver: Coroutine | None

        :return: The output of the state machine.
        :rtype: Returns
        """

        if not self._compiled:
            raise ValueError(
                "Transitions not compiled. "
                f"\nEnsure to compile transitions to run"
            )
        if message.text != None and message.payload != None:
            message.text = None
        if message.text == None and message.payload == None:
            message.text = ""
        if message.text != None:
            return_func = await self._fetch_transition(
                message=message,
                user_messenger_id=user_messenger_id,
                user_messenger=user_messenger,
                user_stage=user_stage,
                user_access_level=user_access_level,
                user_stage_changer=user_stage_changer,
                user_access_level_changer=user_access_level_changer,
                user_file_saver=user_file_saver,
            )
            return return_func
        elif message.payload != None:
            return_func = await self._fetch_payload_transition(
                message=message,
                user_messenger_id=user_messenger_id,
                user_messenger=user_messenger,
                user_stage=user_stage,
                user_access_level=user_access_level,
                user_stage_changer=user_stage_changer,
                user_access_level_changer=user_access_level_changer,
            )
            return return_func

    async def _fetch_transition(
        self,
        message: MessageStruct,
        user_messenger_id: int,
        user_messenger: config.ADDED_MESSENGERS,
        user_stage: str,
        user_access_level: str,
        user_stage_changer: Coroutine,
        user_access_level_changer: Coroutine | None,
        user_file_saver: Coroutine | None = None,
    ):
        message.text = replace_emoji(message.text, replace="")
        stage_transitions = await self._get_transitions_by_stage(
            stage=user_stage
        )
        needed_transition = None
        for transition in stage_transitions:
            if not (
                user_access_level in transition.access_level
                or transition.access_level == ["any"]
            ):
                continue
            if not (
                (transition.trigger == message.text.lower())
                or (
                    is_dataclass(transition.trigger)
                    and bool(len(message.files))
                    and bool(
                        sum(
                            [
                                int(True)
                                for message_file in message.files
                                if message_file.ext
                                in transition.trigger.extensions
                            ]
                        )
                        == len(message.files)
                    )
                )
            ):
                continue
            needed_transition = transition
            break
        if needed_transition == None:
            needed_transition = await self._get_none_transition_by_stage(
                stage=user_stage
            )
        await self._change_user_stage(
            to_stage_id=needed_transition.to_stage_id,
            user_stage_changer=user_stage_changer,
            user_messenger_id=user_messenger_id,
            user_messenger=user_messenger,
        )
        await self._change_user_access_level(
            to_access_level=needed_transition.to_access_level,
            user_access_level_changer=user_access_level_changer,
            user_messenger_id=user_messenger_id,
            user_messenger=user_messenger,
        )
        await self._save_user_file(
            message=message,
            transition=needed_transition,
            user_messenger_id=user_messenger_id,
            user_messenger=user_messenger,
            user_file_saver=user_file_saver,
        )
        message.text = await self._convert_message_file_to_dict(
            message=message, transition=needed_transition
        )
        answer = await needed_transition.to_stage(
            user_messenger_id, user_messenger, message.text
        )
        return answer

    async def _fetch_payload_transition(
        self,
        message: MessageStruct,
        user_messenger_id: int,
        user_messenger: config.ADDED_MESSENGERS,
        user_stage: str,
        user_access_level: str,
        user_stage_changer: Coroutine,
        user_access_level_changer: Coroutine | None,
    ) -> None | Coroutine:
        if self.payloads == None:
            return
        output_dict = await self.payloads.run(
            entry_dict=message.payload,
            user_access_level=user_access_level,
            user_stage=user_stage,
        )
        needed_func = await output_dict.get("dst")(
            user_messenger_id,
            user_messenger,
            output_dict.get("full_dict"),
        )
        await self._change_user_stage(
            to_stage_id=output_dict.get("to_stage_id"),
            user_stage_changer=user_stage_changer,
            user_messenger_id=user_messenger_id,
            user_messenger=user_messenger,
        )
        await self._change_user_access_level(
            to_access_level=output_dict.get("to_access_level"),
            user_access_level_changer=user_access_level_changer,
            user_messenger_id=user_messenger_id,
            user_messenger=user_messenger,
        )
        return needed_func

    async def _change_user_access_level(
        self,
        to_access_level: str | None,
        user_access_level_changer: Coroutine | None,
        user_messenger_id: str | int,
        user_messenger: config.ADDED_MESSENGERS,
    ) -> None:
        if to_access_level != None and user_access_level_changer != None:
            await user_access_level_changer(
                to_access_level=to_access_level,
                user_messenger_id=user_messenger_id,
                user_messenger=user_messenger,
            )

    async def _change_user_stage(
        self,
        to_stage_id: str | None,
        user_stage_changer: Coroutine | None,
        user_messenger_id: str | int,
        user_messenger: config.ADDED_MESSENGERS,
    ) -> None:
        if to_stage_id != None and user_stage_changer != None:
            await user_stage_changer(
                to_stage_id=to_stage_id,
                user_messenger_id=user_messenger_id,
                user_messenger=user_messenger,
            )

    async def _save_user_file(
        self,
        message: MessageStruct,
        transition: Transition,
        user_messenger_id: int,
        user_messenger: config.ADDED_MESSENGERS,
        user_file_saver: Coroutine | None,
    ) -> None:
        if (
            user_file_saver != None
            and is_dataclass(transition.trigger)
            and bool(len(message.files))
            and not transition.trigger.temporary
        ):
            for message_file in message.files:
                await user_file_saver(
                    file_name=message_file.name,
                    file_extension=message_file.ext,
                    file_tag=message_file.tag,
                    file_bytes=message_file.file_bytes,
                    user_messenger_id=user_messenger_id,
                    user_messenger=user_messenger,
                )

    async def _convert_message_file_to_dict(
        self, message: MessageStruct, transition: Transition
    ) -> dict | str:
        if (
            message.text == ""
            and is_dataclass(transition.trigger)
            and bool(len(message.files))
        ):
            files_dict = {"files": message.files}
            return files_dict
        return message.text

    def _counter_none(self, src: str) -> int:
        amount = 0
        for transition in self.transitions:
            if transition.trigger is None and transition.from_stage == src:
                amount += 1
        return amount

    def _counter_unique(
        self, trigger: str | dict | None, src: str, dst: Coroutine
    ) -> int:
        amount = 0
        for transition in self.transitions:
            if transition.from_stage == src and transition.to_stage == dst:
                if trigger is not None:
                    if transition.trigger is None:
                        amount += 1
                else:
                    if transition.trigger is not None:
                        amount += 1
        return amount

    def _get_all_source_stages(self) -> List[str]:
        list_of_transitions = []
        for transition in self.transitions:
            if transition.from_stage != "any":
                list_of_transitions.append(transition.from_stage)
            if transition.to_stage_id != None:
                list_of_transitions.append(transition.to_stage_id)
        if self.payloads is not None:
            list_of_transitions += self.payloads.get_all_source_stages()
        list_of_transitions = list(set(list_of_transitions))
        return list_of_transitions

    def _add_none_transition_to_all_stages(self) -> int:
        added_none_transitions = 0
        for stage in self._get_all_source_stages():
            if not self._check_none_transition_by_stage(stage=stage):
                self.add_transition(
                    trigger=None, from_stage=stage, to_stage=self.error_return
                )
                added_none_transitions += 1
        return added_none_transitions

    def _check_none_transition_by_stage(self, stage: str) -> bool:
        for transition in self.transitions:
            if transition.trigger is None and transition.from_stage == stage:
                return True
        return False

    def _checks(self) -> None:
        if self.error_return is None:
            raise RuntimeError("Error return wasn't added")
        if len(self.transitions) == 0:
            raise RuntimeError(f"Can't compile while no transitions added")
        for transition in self.transitions:
            self._transition_args_check(func=transition.to_stage)
        self._transition_args_check(func=self.error_return)
        if self.payloads is not None:
            if not self.payloads._compiled:
                raise RuntimeError(f"Payloads aren't compiled")

    def _transition_args_check(self, func: Coroutine) -> None:
        list_of_args = [
            "user_messenger_id",
            "user_messenger",
            "message",
        ]
        func_args = inspect.getfullargspec(func)[0]
        for arg in list_of_args:
            if arg not in func_args:
                error_str = (
                    f"Transition to_stage should have '{arg}' arg:\n{func}"
                )
                raise ValueError(error_str)

    async def _get_transitions_by_stage(self, stage: str) -> List[Transition]:
        return [
            transition
            for transition in self.transitions
            if transition.from_stage == stage
        ]

    async def _get_none_transition_by_stage(self, stage: str) -> Transition:
        for transition in self.transitions:
            if transition.trigger == None and transition.from_stage == stage:
                return transition
