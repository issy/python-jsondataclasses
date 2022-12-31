# JSON Dataclasses

![GitHub](https://img.shields.io/github/license/issy/python-jsondataclasses?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/jsondataclasses?style=flat-square)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/issy/python-jsondataclasses/lint.yml?style=flat-square)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/issy/python-jsondataclasses/unit-tests.yml?label=tests&style=flat-square)

Typed JSON dataclasses for Python 3.9+

[Check out the docs](https://issy.github.io/python-jsondataclasses)

# Installation

`pip install jsondataclasses`

# Usage

```py
from datetime import date
from typing import Literal, Optional

from jsondataclasses import jsondataclass, jsonfield


def parse_date(date_string: str) -> date:
    return date.fromisoformat(date_string.replace(".", "-"))


@jsondataclass
class Car:
    make: Literal["Ford", "Renault", "Volkswagen"] = jsonfield("carMake")
    model: str = jsonfield("model")
    manufactured_at: date = jsonfield("dateOfManufacture", parse_date)
    num_of_wheels: Optional[int] = jsonfield("numberOfWheels", default_value=4)


car = Car({
    "carMake": "Ford",
    "model": "Focus",
    "dateOfManufacture": "2018.03.14"
})
print(car)  # Car(make='Ford', model='Focus', manufactured_at=datetime.date(2018, 3, 14), num_of_wheels=4)
```

Class field types can be any primitive type (eg. `str`, `int`, `datetime`),
a variadic generic (eg. `list[str]`, `Optional[int]`, `Literal["hello", "world"]`),
or even another jsondataclass. The `default_value` argument of `jsonfield` will be used
if the specified key is not found in the dictionary *and* the type of the class field is not `Optional[...]`.
In this case, the value of `default_value` will be passed to the supplied parser function.
