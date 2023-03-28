import dataclasses
import ast


def dataclass_from_dict(struct, dictionary) -> dict:
    """
    Convert a dictionary to an instance of a dataclass.

    :param struct: The dataclass structure to be used.
    :type struct: dataclasses

    :param dictionary: The dictionary to convert.
    :type dictionary: dict

    :return: An instance of the dataclass.
    :rtype: dict
    """
    try:
        fieldtypes = {f.name: f.type for f in dataclasses.fields(struct)}
        return struct(
            **{
                f: dataclass_from_dict(fieldtypes[f], dictionary[f])
                for f in dictionary
            }
        )
    except:
        return dictionary


def dataclass_to_dict(cls) -> dict:
    """
    Convert a dataclass to a dictionary.

    :param cls: The dataclass to convert.
    :type cls: dataclasses

    :return: A dictionary representing the dataclass.
    :rtype: dict
    """
    return {k: v for k, v in dataclasses.asdict(cls).items()}


def str_to_dict(string: str) -> dict:
    """
    Convert a string representing a dictionary to an actual dictionary.

    :param string: The string to convert.
    :type string: str

    :return: A dictionary created from the string.
    :rtype: dict
    """
    return ast.literal_eval(string)
