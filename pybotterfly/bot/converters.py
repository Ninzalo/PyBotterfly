import dataclasses
import json
import ast
import base64
import importlib
import sys
import pickle


def dataclass_object_dump(obj) -> dict:
    datacls = type(obj)
    if not dataclasses.is_dataclass(datacls):
        raise TypeError(
            f"Expected dataclass instance, got '{datacls!r}' object"
        )
    mod = sys.modules.get(datacls.__module__)
    if mod is None or not hasattr(mod, datacls.__qualname__):
        raise ValueError(f"Can't resolve '{datacls!r}' reference")
    ref = f"{datacls.__module__}.{datacls.__qualname__}"
    fields = (f.name for f in dataclasses.fields(obj))
    return {**{f: getattr(obj, f) for f in fields}, "__dataclass__": ref}


def dataclass_object_load(dictionary: dict):
    ref = dictionary.pop("__dataclass__", None)
    if ref is None:
        return dictionary
    try:
        modname, _, qualname = ref.rpartition(".")
        module = importlib.import_module(modname)
        datacls = getattr(module, qualname)
        if not dataclasses.is_dataclass(datacls) or not isinstance(
            datacls, type
        ):
            raise ValueError
        return datacls(**dictionary)
    except (ModuleNotFoundError, ValueError, AttributeError, TypeError):
        raise ValueError(f"Invalid dataclass reference {ref!r}") from None


def str_to_dict(string: str) -> dict:
    """
    Convert a string representing a dictionary to an actual dictionary.

    :param string: The string to convert.
    :type string: str

    :return: A dictionary created from the string.
    :rtype: dict
    """
    return ast.literal_eval(string)


def file_to_string(file: bytes) -> str:
    """
    Convert a file to a string.

    :param file: The file to convert.
    :type file: bytearray

    :return: The file as a string.
    :rtype: str
    """
    return base64.b64encode(file).decode()


def string_to_file(string: str) -> bytes:
    """
    Convert a string to a file.

    :param string: The string to convert.
    :type string: str

    :return: The string as a file.
    :rtype: bytes
    """
    return base64.b64decode(string)


def dataclass_to_str(obj) -> str:
    """
    Convert a dataclass to a string.

    :param object: The dataclass to convert.

    :return: The dataclass as a string.
    :rtype: str
    """
    return json.dumps(obj, default=dataclass_object_dump)


def str_to_bytes(string: str) -> bytes:
    """
    Convert a string to a file.

    :param string: The string to convert.
    :type string: str

    :return: bytes
    :rtype: bytes
    """
    return pickle.dumps(string)


def bytearray_to_str(file: bytes) -> str:
    """
    Convert a file to a string.

    :param file: The file to convert.
    :type file: bytes

    :return: The file as a string.
    :rtype: str
    """
    return pickle.loads(file)


def str_to_dataclass(string: str):
    """
    Convert a string to a dataclass.

    :param string: The string to convert.

    :return: The dataclass you've encoded
    """
    return json.loads(string, object_hook=dataclass_object_load)


def dataclass_to_bytes(obj) -> bytes:
    """
    Convert a dataclass to a file.

    :param obj: The dataclass to convert.

    :return: The dataclass as bytes.
    :rtype: bytes
    """
    return str_to_bytes(dataclass_to_str(obj))


def bytes_to_dataclass(encoded_obj: bytes):
    """
    Convert a file to a dataclass.

    :param encoded_obj: The file to convert.
    :type encoded_obj: bytes

    :return: The dataclass you've encoded
    """
    return str_to_dataclass(bytearray_to_str(encoded_obj))
