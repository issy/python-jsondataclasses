import types
import typing
from typing import Any, Callable, Optional, TypeVar

__all__ = ("jsonfield", "jsondataclass")


_T = TypeVar("_T")


def _parse_field(
    data: dict, json_key: str, field_type: type[_T], field_parser: Optional[Callable[[Any], _T]], default_value: Any
) -> _T:
    type_of_type = type(field_type)

    if json_key not in data and type_of_type is not typing._UnionGenericAlias and default_value is not None:
        return (field_parser or field_type)(default_value)
    elif type_of_type is type:
        if field_parser:
            return field_parser(data[json_key])
        else:
            return data[field_type(json_key)]
    elif type_of_type is typing._UnionGenericAlias and isinstance(None, field_type.__args__[1]):  # Parse Optional[Any]
        return _parse_field(data, json_key, field_type.__args__[0], field_parser, default_value) if json_key in data else None
    elif type_of_type is typing._LiteralGenericAlias:  # Parse Literal[...]
        parsed_value = _parse_field(data, json_key, type(field_type.__args__[0]), field_parser, default_value)
        if parsed_value not in field_type.__args__:
            raise ValueError(f"{getattr(data, json_key, default_value)} not of literal {field_type.__args__!r}")
        return parsed_value
    elif type_of_type is types.GenericAlias:  # Parse list[Any]
        return [(field_parser or field_type.__args__[0])(i) for i in data[json_key]]


def jsonfield(
    key: str, parser: Optional[Callable[[Any], Any]] = None, *, default_value: Any = None
) -> tuple[str, Optional[Callable[[Any], Any]], Any]:
    """
    :param key: The key in the dictionary to pick
    :param parser: Function that takes in a single value and returns a value of the desired type
    :param default_value: If the key is not found in the json object, the default value will be passed to the parser instead
    """
    return key, parser, default_value


def jsondataclass(cls: type) -> type:
    """
    Returns the same class that is passed in, with a special __init__ method added
    to construct an instance of the class from a dictionary structure that complies with the class annotations ::

        @jsondataclass
        class Car:
            colour: str = jsonfield("colour")
            number_of_wheels: int = jsonfield("numberOfWheels")
    """
    field_types = {k: t for k, t in cls.__annotations__.items() if not (k.startswith("__") and k.endswith("__"))}
    fields = {k: v for k, v in cls.__dict__.items() if k in field_types}

    def __init__(self, data: dict):
        for key, field_type in field_types.items():
            field_meta = fields.get(key, jsonfield(key))
            setattr(
                self,
                key,
                _parse_field(data, field_meta[0], field_type, field_meta[1], field_meta[2]),
            )

    def __repr__(self: cls) -> str:
        return cls.__name__ + "(" + ", ".join(f"{k}={getattr(self, k)!r}" for k in fields) + ")"

    cls.__init__ = __init__
    cls.__repr__ = __repr__
    return cls
