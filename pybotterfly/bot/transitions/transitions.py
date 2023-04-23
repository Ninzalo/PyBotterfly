import inspect
from emoji import replace_emoji
from dataclasses import dataclass, field
from typing import Coroutine, List
from pybotterfly.base_config import BaseConfig
from pybotterfly.bot.returns.message import Returns
from pybotterfly.bot.struct import MessageStruct
from pybotterfly.bot.transitions import payloads
from pybotterfly.bot.transitions.payloads import Payloads


@dataclass()
class Transition:
    """
    Describes a transition between two stages in a conversation.

    :param trigger: The event that triggers the transition, if any.
        Defaults to None.
    :type trigger: str or None

    :param from_stage: The name of the stage to transition from.
    :type from_stage: str

    :param to_stage: The coroutine representing the stage to transition to.
    :type to_stage: Coroutine
    """

    trigger: str | None
    from_stage: str
    to_stage: Coroutine


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
        self, trigger: str | None, src: str, dst: Coroutine
    ) -> None:
        """
        Adds a transition to the list of transitions.

        :param trigger: The trigger that causes the transition to occur.
            If None, the transition will act as a default transition.
        :type trigger: str | None
        :param src: The source state of the transition.
        :type src: str
        :param dst: The coroutine function that the transition goes to.
        :type dst: Coroutine
        :raises ValueError: If transitions are already compiled, or if the
            transition already exists or if another trigger has already
            realized the transition, or if multiple 'else' blocks
            aren't supported.
        """
        if isinstance(trigger, str):
            trigger = trigger.lower()
        new_transition = Transition(
            trigger=trigger, from_stage=src, to_stage=dst
        )
        if self._compiled:
            raise ValueError(
                "Transitions already compiled. "
                "Please, compile after adding all of the transitions"
            )
        if new_transition in self.transitions:
            error_str = f"Transition already exists: {new_transition}"
            raise ValueError(error_str)

        if self._counter_unique(trigger=trigger, src=src, dst=dst) > 0:
            raise ValueError("Transition already realized by other trigger")

        if new_transition.trigger is None:
            if self._counter_none(src=src) > 0:
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
        user_messenger_id: int,
        user_messenger: BaseConfig.ADDED_MESSENGERS,
        user_stage: str,
        message: MessageStruct,
    ) -> Returns:
        """
        Runs the state machine with the given input message, and returns the
        output.

        :param user_messenger_id: The ID of the user's messenger account.
        :type user_messenger_id: int

        :param user_messenger: The type of messenger account
            (e.g., VK Messenger, Telegram, etc.).
        :type user_messenger: BaseConfig.ADDED_MESSENGERS

        :param user_stage: The current stage of the state machine.
        :type user_stage: str

        :param message: The message to process. Should have .text/.payload
        :type message: Message_struct

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
        if message.text != None:
            message.text = replace_emoji(message.text, replace="")
            stage_transitions = await self._get_transitions_by_stage(
                stage=user_stage
            )
            for transition in stage_transitions:
                if transition.trigger == message.text.lower():
                    answer = await transition.to_stage(
                        user_messenger_id, user_messenger, message.text
                    )
                    return answer
            else_transition = await self._get_none_transition_by_stage(
                stage=user_stage
            )
            answer = await else_transition.to_stage(
                user_messenger_id, user_messenger, message.text
            )
            return answer
        elif message.payload != None:
            if self.payloads != None:
                output = await self.payloads.run(entry_dict=message.payload)
                if (
                    user_stage == output.get("src")
                    or output.get("src") == "any"
                ):
                    needed_func = await output.get("dst")(
                        user_messenger_id,
                        user_messenger,
                        output.get("full_dict"),
                    )
                    return needed_func
                needed_func = await self.error_return(
                    user_messenger_id, user_messenger, output.get("full_dict")
                )
                return needed_func

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
        list_of_transitions = list(
            set([transition.from_stage for transition in self.transitions])
        )
        if self.payloads is not None:
            list_of_transitions += self.payloads.get_all_source_stages()
            list_of_transitions = list(set(list_of_transitions))
        return list_of_transitions

    def _add_none_transition_to_all_stages(self) -> int:
        added_none_transitions = 0
        for stage in self._get_all_source_stages():
            if not self._check_none_transition_by_stage(stage=stage):
                self.add_transition(
                    trigger=None, src=stage, dst=self.error_return
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
            if transition.trigger is None and transition.from_stage == stage:
                return transition
