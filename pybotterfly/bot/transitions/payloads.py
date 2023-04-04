from dataclasses import dataclass, field
import inspect
from typing import Any, Coroutine, List
from pybotterfly.base_config import BaseConfig
from pybotterfly.bot.transitions.schedule import ScheduledJob


@dataclass()
class TypeData:
    key: str
    value: str


@dataclass()
class Payload:
    main_type_value: str
    src: str
    dst: Any
    space_for_data: int
    type_keys_and_values: List[TypeData] = field(default_factory=list)
    data_keys: List[str] = field(default_factory=list)


@dataclass()
class Payloads:
    main_type: str = "type"
    main_type_values: List[str] = field(default_factory=list)
    payloads: List[Payload] = field(default_factory=list)
    scheduled_jobs: List[ScheduledJob] = field(default_factory=list)
    error_return: Payload | None = None
    shorten: bool = True
    words_to_shorten: List[str] = field(default_factory=list)
    config: BaseConfig = BaseConfig
    use_for: config.ADDED_MESSENGERS | None = "tg" if shorten else None
    _compiled: bool = False

    def __post_init__(self):
        self.use_for = "tg" if self.shorten else None
        if self.config.DEBUG_STATE:
            print(f"Payloads are using for '{self.use_for}'")

    def add_reference(self, path: str, src: str, dst: Coroutine) -> None:
        """
        Adds a reference payload to the state machine.
        Allows you to add new payload based on existing references

        :param path: The path of the reference in the format like
            `main_type:main_type_value/type:type_value/id:/messenger:`, where
            `main_type` is a main type key, `main_type_value` is a main type
            value, `type` is a subtype key, `type_value` is a type value,
            `id` and `messenger` are data type (you will get its value in
            `run` func). You can rename them and add others.
        :type path: str

        :param src: The source stage of the reference.
        :type src: str

        :param dst: The coroutine to be called after the reference is resolved.
        :type dst: Coroutine

        :raises RuntimeError: If the state machine is already compiled.

        :returns: None
        """
        if self._compiled:
            error_str = (
                f"Payloads already compiled."
                f"\nEnsure to compile after all references added"
            )
            raise RuntimeError(error_str)
        self._value_type_check(value=[path, src], type_of_value=str)
        ref_dict = self._parse_path(path=path)
        self._auto_create_payload(ref_dict=ref_dict, src=src, dst=dst)
        if self.config.DEBUG_STATE:
            print(f"Added reference payload: {ref_dict}")

    def add_payload(self, path: str, src: str, dst: Coroutine) -> None:
        """
        Adds a new payload based on path to the state machine.

        :param path: The path to the payload, in dot notation.
        :type path: str
        :param src: The source stage of the payload.
        :type src: str
        :param dst: The destination stage of the payload.
        :type dst: Coroutine
        :raises RuntimeError: If the state machine has already been compiled.
        :raises TypeError: If either `path` or `src` are not strings.
        """
        if self._compiled:
            error_str = (
                f"Payloads already compiled."
                f"\nEnsure to compile after all payloads added"
            )
            raise RuntimeError(error_str)
        self._value_type_check(value=[path, src], type_of_value=str)
        new_payload_dict = self._parse_path(path=path)
        self._add_payload(new_dict=new_payload_dict, src=src, dst=dst)
        if self.config.DEBUG_STATE:
            print(f"Added payload: {new_payload_dict}")

    def add_error_return(self, error_return: Any) -> None:
        """
        Adds an error return payload to the state machine.

        :param error_return: The error return value.
        :type error_return: Any
        :raises RuntimeError: If an error return has already been added or
            if the state machine has already been compiled.
        """
        if self.error_return is not None:
            raise RuntimeError(f"Error return already added")
        if self._compiled:
            error_str = (
                f"Payloads already compiled."
                f"\nEnsure to compile after error return added"
            )
            raise RuntimeError(error_str)
        self.error_return = Payload(
            main_type_value="error",
            src="any",
            dst=error_return,
            space_for_data=0,
        )
        if self.config.DEBUG_STATE:
            print(f"Added error payload return: {self.error_return}")

    def add_scheduled_job(self, payload: str, dst: Coroutine):
        """
        Adds a new scheduled job to the state machine.

        :param payload: The payload of the job, as a dictionary.
        :type payload: dict
        :param dst: The coroutine that will be executed when the job is scheduled.
        :type dst: Coroutine
        :raises RuntimeError: If the state machine has already been compiled
            or the job already exists.
        """
        if self._compiled:
            raise RuntimeError(f"Payloads already compiled.")
        new_job = ScheduledJob(dst=dst, payload=payload)
        if new_job in self.scheduled_jobs:
            error_str = (
                f"Failed to add scheduled job:\n{new_job} already exists"
            )
            raise RuntimeError(error_str)
        if len(self.scheduled_jobs) == 0:
            self.add_reference(path=payload, src="any", dst=dst)
        else:
            self.add_payload(path=payload, src="any", dst=dst)
        self.scheduled_jobs.append(new_job)
        if self.config.DEBUG_STATE:
            print(f"Added scheduled job: {new_job}")

    def compile(self) -> None:
        """
        Compiles the payloads for the state machine.
        Prevents you from adding new payloads at runtime.

        :raises RuntimeError: If no payloads were added or if the error
            payload was not added.
        :raises RuntimeError: If the state machine has already been compiled.
        """
        if self.payloads == []:
            error_str = f"Failed to compile payloads \nNo payloads added"
            raise RuntimeError(error_str)
        if self.error_return is None:
            error_str = (
                f"Failed to compile payloads\nError payload wasn't added"
            )
            raise RuntimeError(error_str)
        if self._compiled:
            raise RuntimeError(f"Payloads already compiled.")
        for payload in self.payloads:
            self._payload_args_check(func=payload.dst)
        self._compiled = True
        if self.config.DEBUG_STATE:
            print(f"\n[SUCCESS] Payloads compiled successfully\n")

    def add_words_to_shorten(self, word: str | List[str]) -> None:
        """
        Adds one or more words to the list of words that can be shortened.

        :param word: A string or a list of strings representing the words to add.
        :type word: str or List[str]
        :raises TypeError: If `word` is neither a string nor a list of strings.
        :raises RuntimeError: If payloads were already created or if `word`
            is already in the list of words to shorten.
        :raises ValueError: If `word` is a single character or if `word`
            is already short.
        """
        if isinstance(word, list):
            for w in word:
                self.add_words_to_shorten(word=w)
            return
        self._value_type_check(value=word, type_of_value=str)
        if len(self.payloads) > 0:
            error_str = (
                "Payloads were already created"
                "\nEnsure to add words to shorten before "
                "adding payloads or references"
            )
            raise RuntimeError(error_str)
        if word in self.words_to_shorten:
            error_str = f"Word '{word}' already in list of words to shorten"
            raise ValueError(error_str)
        if len(word) < 2:
            error_str = f"Word '{word}' is already short"
            raise ValueError(error_str)
        self.words_to_shorten.append(word)
        if self.config.DEBUG_STATE:
            print(f"'Words to shorten' list appended by: '{word}'")

    async def run(self, entry_dict: dict) -> dict:
        """
        Runs the payload and returns a dictionary containing the payload data,
        the destination and source of the payload.
        Use-case: If you configured Payloads with 'shorten=True' param,
        you should ensure that 'entry_dict' is pre-shortened

        :param entry_dict: A dictionary containing the payload data.
        :type entry_dict: dict
        :raises RuntimeError: If payloads haven't been compiled.
        :raises TypeError: If entry_dict is not a dictionary.
        :return: A dictionary containing the payload data, the destination
            and source of the payload.
        :rtype: dict
        """
        if not self._compiled:
            raise RuntimeError(f"Payloads aren't compiled")
        self._value_type_check(entry_dict, dict)
        main_type = self._get_main_type_value(given_dict=entry_dict)
        reference = self._find_exact_reference(
            main_type_value=main_type, given_dict=entry_dict
        )
        data_output = dict(
            zip(
                reference.data_keys,
                [entry_dict.get(value) for value in reference.data_keys],
            )
        )
        output_keys_list = ["data", "dst", "src"]
        output_data_list = [data_output, reference.dst, reference.src]
        return dict(zip(output_keys_list, output_data_list))

    def _shortener(self, value: str) -> str:
        self._value_type_check(value=value, type_of_value=str)
        if len(value) == 0:
            error_str = f"Value '{value}' is too short already"
            raise ValueError(error_str)
        if self.shorten:
            return value[0]
        return value

    def _shorten_word_from_shorten_list(self, word: str) -> str:
        self._value_type_check(value=word, type_of_value=str)
        if self.shorten:
            for _ in range(len(self.words_to_shorten)):
                for word_to_shorten in self.words_to_shorten:
                    word = word.replace(word_to_shorten, word_to_shorten[0])
        return word

    def _value_type_check(self, value, type_of_value) -> None:
        if isinstance(value, list):
            for val in value:
                self._value_type_check(value=val, type_of_value=type_of_value)
            return
        if not isinstance(value, type_of_value):
            error_str = (
                f"Value '{value}' has type '{type(value)}' "
                f"instead of '{type_of_value}'"
            )
            raise TypeError(error_str)

    def _length(self, data: str | dict) -> int:
        data_length = len(str(data).encode())
        if self.use_for == "vk":
            max_length = 255
        elif self.use_for == "tg":
            max_length = 64
        else:
            max_length = 1000
        if data_length > max_length:
            error_str = (
                f"Dict is too big for {self.use_for} payloads: "
                f"{data_length}"
            )
            raise RuntimeError(error_str)
        return data_length

    def _parse_path(self, path: str) -> dict:
        self._value_type_check(value=path, type_of_value=str)
        return_dict = {}
        added_keys = []
        path = path.strip()
        for num, key_and_value in enumerate(path.split("/")):
            key, value = key_and_value.split(":")
            if num == 0:
                if key != self.main_type:
                    if self.payloads != []:
                        error_str = (
                            f"Main key '{key}' is wrong. "
                            f"It should be '{self.main_type}'"
                        )
                        raise KeyError(error_str)
                    else:
                        self.main_type = key
                value = self._shortener(value=value)
            elif len(value) > 0:
                value = self._shorten_word_from_shorten_list(word=value)
            elif len(value) == 0:
                value = 0
            key = self._shortener(value=key)
            if key in added_keys:
                error_str = f"Key '{key}' already added for that dict"
                raise ValueError(error_str)
            added_keys.append(key)
            return_dict[key] = value
        if self.shorten:
            self._length(return_dict)
        return return_dict

    def _get_type_data_from_dict(self, ref_dict: dict) -> List[TypeData]:
        self._value_type_check(ref_dict, dict)
        type_data = []
        for key, value in ref_dict.items():
            if key != self.main_type:
                if isinstance(value, str):
                    type_data.append(TypeData(key=key, value=value))
        return type_data

    def _get_data_keys_from_dict(self, ref_dict: dict) -> List[str]:
        self._value_type_check(ref_dict, dict)
        data_keys = []
        for key, value in ref_dict.items():
            if isinstance(value, int):
                data_keys.append(key)
        return data_keys

    def _get_space_for_data(self, ref_dict: dict):
        length = len(str(ref_dict).encode())
        max_length = 1000
        if self.use_for == "vk":
            max_length = 255
        elif self.use_for == "tg":
            max_length = 64
        return max_length - length

    def _auto_create_payload(self, ref_dict: dict, src: str, dst: Any) -> None:
        self._value_type_check(ref_dict, dict)
        self._value_type_check(src, str)
        type_data = self._get_type_data_from_dict(ref_dict=ref_dict)
        data_keys = self._get_data_keys_from_dict(ref_dict=ref_dict)
        space_for_data = self._get_space_for_data(ref_dict=ref_dict)
        for key, value in ref_dict.items():
            key = self._shortener(key)
            if key == self._shortener(self.main_type):
                if value in self.main_type_values:
                    error_str = f"Main type value '{value}' already exists"
                    raise ValueError(error_str)
                self.main_type_values.append(value)
                new_payload = Payload(
                    main_type_value=value,
                    src=src,
                    dst=dst,
                    space_for_data=space_for_data,
                    type_keys_and_values=type_data,
                    data_keys=data_keys,
                )
                if new_payload not in self.payloads:
                    self.payloads.append(new_payload)

    def _find_reference(self, main_type_value: str):
        self._value_type_check(main_type_value, str)
        for payload in self.payloads:
            if payload.main_type_value == main_type_value:
                return payload
        error_str = f"Can't find reference with main type {main_type_value}"
        raise ValueError(error_str)

    def _find_exact_reference(self, main_type_value: str, given_dict: dict):
        self._value_type_check(main_type_value, str)
        self._value_type_check(given_dict, dict)
        data_keys_and_values = self._get_type_data_from_dict(
            ref_dict=given_dict
        )
        data_keys_list = [key.key for key in data_keys_and_values]
        data_values_list = [key.value for key in data_keys_and_values]
        for payload in self.payloads:
            if payload.main_type_value == main_type_value:
                ref_data_keys_list = []
                ref_data_values_list = []
                for type_keys_and_value in payload.type_keys_and_values:
                    ref_data_keys_list.append(type_keys_and_value.key)
                    ref_data_values_list.append(type_keys_and_value.value)
                if (
                    ref_data_keys_list == data_keys_list
                    and ref_data_values_list == data_values_list
                ):
                    return payload

        if self.error_return is None:
            error_str = (
                f"Can't find reference with main type '{main_type_value}' "
                f"similar to {given_dict}"
            )
            raise ValueError(error_str)
        return self.error_return

    def _get_main_type_value(self, given_dict: dict):
        self._value_type_check(given_dict, dict)
        for num, key_and_value in enumerate(given_dict.items()):
            if num == 0:
                return key_and_value[1]
        raise ValueError(f"Can't find main type value")

    def _add_payload(self, new_dict: dict, src: str, dst: Any) -> None:
        self._value_type_check(new_dict, dict)
        self._value_type_check(src, str)
        main_type = self._get_main_type_value(given_dict=new_dict)
        reference = self._find_reference(main_type_value=main_type)
        ref_type_keys = [key.key for key in reference.type_keys_and_values]
        type_keys_and_values = self._get_type_data_from_dict(ref_dict=new_dict)
        type_keys = [key.key for key in type_keys_and_values]
        data_keys = self._get_data_keys_from_dict(ref_dict=new_dict)
        ref_data_keys = reference.data_keys
        space_for_data = self._get_space_for_data(ref_dict=new_dict)
        if ref_type_keys != type_keys:
            error_str = (
                f"Reference type keys aren't similar to the new dict: "
                f"{ref_type_keys} != {type_keys}"
            )
            raise RuntimeError(error_str)
        if len(data_keys) != len(ref_data_keys):
            error_str = (
                f"Taken not similar amount of data keys, as in the reference"
            )
            raise RuntimeError(error_str)
        new_payload = Payload(
            main_type_value=main_type,
            src=src,
            dst=dst,
            space_for_data=space_for_data,
            type_keys_and_values=type_keys_and_values,
            data_keys=data_keys,
        )
        if new_payload in self.payloads:
            raise RuntimeError(f"Payload already exists")
        self.payloads.append(new_payload)

    def _payload_args_check(self, func: Coroutine) -> None:
        list_of_args = [
            "user_messenger_id",
            "user_messenger",
            "message",
        ]
        func_args = inspect.getfullargspec(func)[0]
        for arg in list_of_args:
            if arg not in func_args:
                error_str = f"Payload dst should have '{arg}' arg:\n{func}"
                raise ValueError(error_str)
