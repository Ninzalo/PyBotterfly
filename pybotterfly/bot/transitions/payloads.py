import inspect
from dataclasses import dataclass, field
from collections import Counter
from typing import Coroutine, List, Tuple, Union, Dict, Any
from pybotterfly.base_config import BaseConfig

# from pybotterfly.bot.transitions.schedule import ScheduledJob


@dataclass()
class ShortenedItem:
    item: str

    def __post_init__(self) -> None:
        self.item = self.item.strip()
        if len(self.item) < 1:
            error_str = f"'{self.item}' is too short"
            raise ValueError(error_str)
        self.short_item = self.item[0]

    def __repr__(self) -> str:
        return_str = (
            f"{self.__class__.__name__}(item='{self.item}', "
            f"short_item='{self.short_item}')"
        )
        return return_str


@dataclass()
class ShortenedRuledItem(ShortenedItem):
    rules: List[ShortenedItem]

    def __post_init__(self) -> None:
        self.short_item = self.item
        split_item = self.item.split("_")
        new_short_item = ""
        for num, word in enumerate(split_item):
            adding_word = word
            for rule in self.rules:
                if word == rule.item:
                    adding_word = rule.short_item
            if num != len(split_item) - 1:
                new_short_item += "".join(f"{adding_word}_")
            else:
                new_short_item += "".join(f"{adding_word}")
        if new_short_item == "":
            new_short_item = self.item
        self.short_item = new_short_item

    def __repr__(self) -> str:
        return_str = (
            f"{self.__class__.__name__}(item='{self.item}', "
            f"short_item='{self.short_item}')"
        )
        return return_str


@dataclass()
class Trigger:
    rules: List[ShortenedItem]
    key: ShortenedItem
    value: ShortenedRuledItem

    def __repr__(self):
        return_str = (
            f"{self.__class__.__name__}(key={self.key}, value={self.value}"
        )
        return return_str


@dataclass()
class Payload:
    main_key: ShortenedItem
    main_value: ShortenedItem
    rules: List[ShortenedItem]
    triggers: List[Trigger]
    data: List[ShortenedItem]
    from_stage: str
    to_stage: Coroutine

    def __post_init__(self) -> None:
        self.space_for_data = self.get_space_for_data()

    def __repr__(self):
        return_str = (
            f"{self.__class__.__name__}(triggers={self.triggers}, "
            f"data={self.data}, from_stage={self.from_stage}, "
            f"to_stage={self.to_stage})"
        )
        return return_str

    def get_space_for_data(self) -> int:
        """
        This function returns the amount of space that can be used for
        data in the payload.
        """
        payload_dict = self.get_payload_dict()
        additional_data = len(self.data)
        length_of_payload = len(str(payload_dict).encode())
        length = length_of_payload - additional_data
        space_for_data = 64 - length
        if (
            len(self.rules) > 0
            and space_for_data < additional_data
            and additional_data > 0
        ):
            error_str = f"Not enough space for data in: {self.__repr__()}"
            raise ValueError(error_str)
        return space_for_data

    def get_payload_dict(self) -> dict:
        payload_dict = {self.main_key.short_item: self.main_value.short_item}
        for trigger in self.triggers:
            payload_dict[trigger.key.short_item] = trigger.value.short_item
        for data_key in self.data:
            payload_dict[data_key.short_item] = 0
        return payload_dict

    def _get_full_payload_dict(self) -> dict:
        payload_dict = {self.main_key.item: self.main_value.item}
        for trigger in self.triggers:
            payload_dict[trigger.key.item] = trigger.value.item
        for data_key in self.data:
            payload_dict[data_key.item] = 0
        return payload_dict

    def __dict__(self) -> dict:
        self_dict = {}
        short_dict = {
            "main": {
                "main_key": self.main_key.short_item,
                "main_value": self.main_value.short_item,
            },
            "payload": self.get_payload_dict(),
            "from_stage": self.from_stage,
            "to_stage": self.to_stage,
            "space_for_data": self.space_for_data,
        }
        full_dict = {
            "main": {
                "main_key": self.main_key.item,
                "main_value": self.main_value.item,
            },
            "payload": self._get_full_payload_dict(),
            "from_stage": self.from_stage,
            "to_stage": self.to_stage,
            "space_for_data": self.space_for_data,
        }
        self_dict["short_dict"] = short_dict
        self_dict["full_dict"] = full_dict
        return self_dict


@dataclass()
class Classification:
    rules: List[ShortenedItem]
    main_value: ShortenedItem
    payloads: List[Payload]

    def __dict__(self) -> dict:
        self_dict = {"payloads": [item.__dict__() for item in self.payloads]}
        return self_dict


class Rules:
    def __init__(self) -> None:
        self.rules: List[ShortenedItem] = []

    def _add_rule(self, word: str | List[str]) -> None:
        if isinstance(word, list):
            for w in word:
                self._add_rule(word=w)
            return
        new_rule = ShortenedItem(item=word)
        if new_rule in self.rules:
            error_str = f"'{new_rule}' already exists"
            raise ValueError(error_str)
        self.rules.append(new_rule)


class Payloads(Rules):
    def __init__(self, config: BaseConfig = BaseConfig) -> None:
        self.config = config
        self.main_key: ShortenedItem = ShortenedItem(item="type")
        self.classes: List[Classification] = []
        self._error_payload: Payload | None = None
        self._short_main_values: List[str] = []
        self._main_key_changed: int = 0
        self._compiled: bool = False
        self._added_trigger_values_before_autoruling: Union[
            Dict[Any, Any], List[Any]
        ] = []
        self._added_payloads_before_autoruling: Tuple[str, str, Coroutine] = []
        self._rules_applied: bool = False
        super().__init__()

    def apply_rules(self) -> None:
        if self._rules_applied:
            raise RuntimeError("Rules already applied")
        self._rules_applied = True
        self.classes = []
        self.main_key = ShortenedItem(item="type")
        self._short_main_values = []
        self._main_key_changed = 0
        self._set_trigger_values()
        self._split_trigger_values()
        self._count_items()
        self._auto_add_rules()
        for payload, src, dst in self._added_payloads_before_autoruling:
            self.add_payload(payload=payload, from_stage=src, to_stage=dst)
        self._added_trigger_values_before_autoruling = []
        self._added_payloads_before_autoruling = []

    def remove_payload(self, payload: str) -> None:
        if self._compiled:
            error_str = f"Payloads are already compiled"
            raise RuntimeError(error_str)
        main_value, list_of_triggers, list_of_data_items = self._parse_payload(
            payload=payload
        )
        if main_value not in [
            classification.main_value for classification in self.classes
        ]:
            error_str = f"Payload '{payload}' not found"
            raise ValueError(error_str)
        classification = self._get_classification(main_value=main_value)
        for num, existing_payload in enumerate(classification.payloads):
            if (
                main_value == existing_payload.main_value
                and list_of_triggers == existing_payload.triggers
                and list_of_data_items == existing_payload.data
            ):
                if self.config.DEBUG_STATE:
                    print(f"Removed payload: '{payload}'")
                classification.payloads.pop(num)
                return
        error_str = f"Payload '{payload}' not found"
        raise ValueError(error_str)

    def add_payload(
        self, payload: str, from_stage: str, to_stage: Coroutine
    ) -> Payload:
        self._payload_args_check(func=to_stage)
        if not self._rules_applied:
            self._added_payloads_before_autoruling.append(
                (payload, from_stage, to_stage)
            )
        main_value, list_of_triggers, list_of_data_items = self._parse_payload(
            payload=payload
        )
        new_payload = Payload(
            main_key=self.main_key,
            main_value=main_value,
            rules=self.rules,
            triggers=list_of_triggers,
            data=list_of_data_items,
            from_stage=from_stage,
            to_stage=to_stage,
        )
        if main_value not in [
            classification.main_value for classification in self.classes
        ]:
            self._add_new_classification(main_value=main_value)
            if main_value.short_item in self._short_main_values:
                error_str = (
                    f"Can't add payload: '{payload}'. Short main value "
                    f"'{main_value.short_item}' already exists"
                )
                raise ValueError(error_str)
        self._short_main_values.append(main_value.short_item)
        classification = self._get_classification(main_value=main_value)
        if new_payload in classification.payloads:
            error_str = (
                f"Payload already exists in classification"
                f"\nPayload: {new_payload}"
                f"\nClassification: {classification}"
            )
            raise ValueError(error_str)
        classification.payloads.append(new_payload)
        if len(new_payload.triggers) != len(
            classification.payloads[0].triggers
        ) or len(new_payload.data) != len(classification.payloads[0].data):
            error_str = (
                f"Length of new payload is not similar to existing "
                f"classification's payloads"
                f"\nError from: '{payload}'"
            )
            raise ValueError(error_str)
        if self.config.DEBUG_STATE and self._rules_applied:
            info_str = (
                f"Added payload: "
                f"{self._convert_payload_to_dict(entry_payload=new_payload)}"
            )
            print(info_str)
        return new_payload

    def shortener(self, payload_dict: dict) -> dict:
        if not self._compiled:
            return payload_dict
        payload_main_key, payload_main_value = list(payload_dict.items())[0]
        if (
            payload_main_key != self.main_key.item
            and payload_main_key != self.main_key.short_item
        ):
            return self._return_error_payload_dict()
        needed_classification = self._get_needed_classification(
            payload_main_value=payload_main_value, short=False
        )
        if needed_classification is None:
            return self._return_error_payload_dict()
        needed_payload = self._get_needed_payload(
            classification=needed_classification, payload_dict=payload_dict
        )
        if needed_payload is None:
            return self._return_error_payload_dict()
        result_dict = self._convert_payload_to_dict(
            entry_payload=needed_payload,
            entry_dict=payload_dict,
            is_short=True,
        )
        return result_dict

    def add_error_payload(self, payload: str, to_stage: Coroutine):
        if self._compiled:
            raise RuntimeError("Payloads already compiled")
        if self._error_payload != None:
            raise RuntimeError("Error payload already added")
        error_payload = self.add_payload(
            payload=payload, from_stage="any", to_stage=to_stage
        )
        self._error_payload = error_payload
        if self.config.DEBUG_STATE:
            print(f"Added error payload: '{payload}'")

    def compile(self) -> None:
        if self.classes == []:
            error_str = f"Failed to compile payloads. No payloads added"
            raise RuntimeError(error_str)
        if self._error_payload == None:
            error_str = (
                "No error payload added. Use 'add_error_payload' "
                "method before compiling"
            )
            raise RuntimeError(error_str)
        if self._compiled:
            raise RuntimeError("Payloads already compiled")
        self._compiled = True
        if self.config.DEBUG_STATE:
            print(f"\n[SUCCESS] Payloads compiled successfully\n")

    def get_all_source_stages(self) -> List[str]:
        source_stages = []
        for classification in self.classes:
            for payload in classification.payloads:
                source_stages.append(payload.from_stage)
        return source_stages

    async def run(self, entry_dict: dict) -> dict:
        needed_payload = await self._get_payload(entry_dict=entry_dict)
        if not self._compiled or needed_payload == None:
            needed_payload = self._return_error_payload()
        full_dict = self._convert_payload_to_dict(
            entry_payload=needed_payload, entry_dict=entry_dict, is_short=False
        )
        output_keys_list = ["dst", "src", "full_dict"]
        output_data_list = [
            needed_payload.to_stage,
            needed_payload.from_stage,
            full_dict,
        ]
        return dict(zip(output_keys_list, output_data_list))

    def _get_needed_payload(
        self, classification: Classification, payload_dict: dict
    ) -> Payload:
        payload_dict_keys = [key for key, _ in payload_dict.items()]
        for payload in classification.payloads:
            if (
                self._validate_payload_length(
                    payload=payload, payload_dict=payload_dict
                )
                and self._validate_payload_triggers(
                    payload=payload,
                    payload_dict=payload_dict,
                    payload_dict_keys=payload_dict_keys,
                )
                and self._validate_payload_data(
                    payload=payload,
                    payload_dict_keys=payload_dict_keys,
                )
            ):
                return payload
        return None

    def _validate_payload_data(
        self,
        payload: Payload,
        payload_dict_keys: List[str],
    ) -> bool:
        for data_item in payload.data:
            if (
                data_item.item not in payload_dict_keys
                and data_item.short_item not in payload_dict_keys
            ):
                return False
        return True

    def _validate_payload_triggers(
        self,
        payload: Payload,
        payload_dict: dict,
        payload_dict_keys: List[str],
    ) -> bool:
        for trigger in payload.triggers:
            if (
                trigger.key.item not in payload_dict_keys
                and trigger.key.short_item not in payload_dict_keys
            ):
                return False
            if (
                payload_dict.get(trigger.key.item) != trigger.value.item
                and payload_dict.get(trigger.key.item)
                != trigger.value.short_item
                and payload_dict.get(trigger.key.short_item)
                != trigger.value.item
                and payload_dict.get(trigger.key.short_item)
                != trigger.value.short_item
            ):
                return False
        return True

    def _validate_payload_length(
        self, payload: Payload, payload_dict: dict
    ) -> bool:
        if len(list(payload_dict.items())) == 1 + len(payload.triggers) + len(
            payload.data
        ):
            return True
        return False

    async def _get_payload(self, entry_dict: dict) -> Payload:
        payload_main_value = self._get_payload_main_value(entry_dict)
        needed_classification = self._get_needed_classification(
            payload_main_value=payload_main_value, short=True
        )
        if needed_classification is None:
            return self._return_error_payload()
        needed_reference = self._get_needed_reference(
            entry_dict, needed_classification
        )
        if needed_reference is None:
            return self._return_error_payload()
        return needed_reference

    def _get_payload_main_value(self, entry_dict: dict) -> str:
        return list(entry_dict.values())[0]

    def _get_needed_classification(
        self, payload_main_value: str, short: bool = True
    ) -> Classification:
        for classification in self.classes:
            if short:
                if classification.main_value.short_item == payload_main_value:
                    return classification
            else:
                if classification.main_value.item == payload_main_value:
                    return classification
        return None

    def _get_needed_reference(
        self, entry_dict: dict, needed_classification: Classification
    ) -> Payload:
        for payload in needed_classification.payloads:
            if self._is_valid_payload(entry_dict, payload):
                return payload
        return None

    def _is_valid_payload(self, entry_dict: dict, payload: Payload) -> bool:
        triggers_short_keys = [
            trigger.key.short_item for trigger in payload.triggers
        ]
        data_short_keys = [key.short_item for key in payload.data]
        entry_payload_keys = [key for key, _ in entry_dict.items()]
        if len(entry_payload_keys) != 1 + len(triggers_short_keys) + len(
            data_short_keys
        ):
            return False
        for key in triggers_short_keys + data_short_keys:
            if key not in entry_payload_keys:
                return False
        for trigger in payload.triggers:
            if trigger.value.short_item != entry_dict.get(
                trigger.key.short_item
            ):
                return False
        return True

    def _convert_payload_to_dict(
        self,
        entry_payload: Payload,
        entry_dict: dict | None = None,
        is_short: bool = False,
    ) -> dict:
        main_key = (
            entry_payload.main_key.short_item
            if is_short
            else entry_payload.main_key.item
        )
        main_value = (
            entry_payload.main_value.short_item
            if is_short
            else entry_payload.main_value.item
        )
        return_dict = {f"{main_key}": f"{main_value}"}
        for trigger in entry_payload.triggers:
            key = trigger.key.short_item if is_short else trigger.key.item
            value = (
                trigger.value.short_item if is_short else trigger.value.item
            )
            return_dict[key] = value
        for data_item in entry_payload.data:
            key = data_item.short_item if is_short else data_item.item
            entry_dict_key = (
                data_item.item if is_short else data_item.short_item
            )
            if entry_dict != None:
                return_dict[key] = entry_dict.get(entry_dict_key)
            else:
                return_dict[key] = 0
        return return_dict

    def _return_error_payload(self) -> Payload:
        return self._error_payload

    def _return_error_payload_dict(self) -> dict:
        if self.config.DEBUG_STATE:
            print(f"Input resulted as an error")
        return self._convert_payload_to_dict(entry_payload=self._error_payload)

    def _add_new_classification(self, main_value: ShortenedItem) -> None:
        new_classification = Classification(
            rules=self.rules, main_value=main_value, payloads=[]
        )
        self.classes.append(new_classification)

    def _get_classification(self, main_value: ShortenedItem) -> Classification:
        for classification in self.classes:
            if classification.main_value == main_value:
                return classification
        error_str = (
            f"Classification with main value '{main_value}' was not found"
        )
        raise ValueError(error_str)

    def _parse_payload(
        self, payload: str
    ) -> Tuple[ShortenedItem, List[Trigger], List[ShortenedItem]]:
        list_of_kv = payload.strip().replace(" ", "").split("/")
        main_value = ""
        list_of_short_keys = []
        list_of_triggers = []
        list_of_data_items = []
        for num, kv in enumerate(list_of_kv):
            key, value = kv.split(":")
            new_key = ShortenedItem(item=key)
            if new_key.short_item in list_of_short_keys:
                error_str = (
                    f"Short key '{new_key.short_item}' already exists "
                    f"in payload: {payload}"
                )
                raise ValueError(error_str)
            list_of_short_keys.append(new_key.short_item)
            if num == 0:
                main_value = self._change_main_key(
                    value=value, new_key=new_key
                )
                continue
            if value == "":
                list_of_data_items = self._add_new_data_item(
                    key=key,
                    list_of_data_items=list_of_data_items,
                    payload=payload,
                )
            else:
                list_of_triggers = self._add_new_trigger(
                    key=new_key,
                    value=value,
                    list_of_triggers=list_of_triggers,
                    payload=payload,
                )
        if main_value == "":
            raise ValueError("Empty 'main_value' input")
        return (main_value, list_of_triggers, list_of_data_items)

    def _add_new_trigger(
        self,
        key: ShortenedItem,
        value: str,
        list_of_triggers: List[Trigger] | field(default_factory=list),
        payload: str,
    ) -> List[Trigger]:
        if not self._rules_applied:
            self._added_trigger_values_before_autoruling.append(value)
        new_value = ShortenedRuledItem(item=value, rules=self.rules)
        new_trigger = Trigger(rules=self.rules, key=key, value=new_value)
        if new_trigger in list_of_triggers:
            error_str = (
                f"'{new_trigger}' already exists in " f"payload: {payload}"
            )
            raise ValueError(error_str)
        list_of_triggers.append(new_trigger)
        return list_of_triggers

    def _add_new_data_item(
        self, key: str, list_of_data_items: List[ShortenedItem], payload: str
    ) -> List[ShortenedItem]:
        new_data_item = ShortenedItem(item=key)
        if new_data_item in list_of_data_items:
            error_str = (
                f"'{new_data_item}' already exists in payload: '{payload}'"
            )
            raise ValueError(error_str)
        list_of_data_items.append(new_data_item)
        return list_of_data_items

    def _change_main_key(
        self, value: str, new_key: ShortenedItem
    ) -> ShortenedItem:
        main_value = ShortenedItem(item=value)
        if self._main_key_changed >= 1 and self.main_key != new_key:
            error_str = f"'main_key' was already changed"
            raise ValueError(error_str)
        self._main_key_changed += 1
        self.main_key = new_key
        return main_value

    def _set_trigger_values(self) -> None:
        self._added_trigger_values_before_autoruling = list(
            set(self._added_trigger_values_before_autoruling)
        )

    def _split_trigger_values(self) -> None:
        split_list = []
        for word in self._added_trigger_values_before_autoruling:
            for item in word.split("_"):
                split_list.append(item)
        self._added_trigger_values_before_autoruling = split_list

    def _count_items(self) -> None:
        self._added_trigger_values_before_autoruling = dict(
            Counter(self._added_trigger_values_before_autoruling)
        )
        counted_trigger_values = {}
        for key, value in self._added_trigger_values_before_autoruling.items():
            counted_trigger_values[key] = value
        self._added_trigger_values_before_autoruling = dict(
            sorted(
                counted_trigger_values.items(),
                key=lambda item: (
                    item[1],
                    len(item[0]),
                ),
                reverse=True,
            )
        )

    def _auto_add_rules(self) -> None:
        new_rules = []
        list_of_keys = []
        for key, _ in self._added_trigger_values_before_autoruling.items():
            if key[0] not in list_of_keys:
                new_rules.append(key)
                self._add_rule(key)
                list_of_keys.append(key[0])

    def __dict__(self) -> dict:
        self_dict = {
            "classes": [item.__dict__() for item in self.classes],
            "rules_applied": self._rules_applied,
            "compiled": self._compiled,
        }
        return self_dict

    def _payload_args_check(self, func: Coroutine) -> None:
        list_of_args = [
            "user_messenger_id",
            "user_messenger",
            "message",
        ]
        func_args = inspect.getfullargspec(func)[0]
        for arg in list_of_args:
            if arg not in func_args:
                error_str = (
                    f"Payload 'to_stage' should have '{arg}' arg: {func}"
                )
                raise ValueError(error_str)
