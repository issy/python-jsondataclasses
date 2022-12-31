from datetime import date
from typing import Literal, Optional

import pytest

from jsondataclasses import jsondataclass, jsonfield


def test_basic_dataclass():
    # Given
    @jsondataclass
    class Car:
        make: str = jsonfield("make")
        model: str = jsonfield("model")

    # When
    car = Car({"make": "ford", "model": "focus"})

    # Then
    assert car.make == "ford"
    assert car.model == "focus"


def test_parser_function():
    # Given
    @jsondataclass
    class Car:
        make: str = jsonfield("vehicleMake")
        model: str = jsonfield("vehicleModel")
        manufactured_at: date = jsonfield("dateOfManufacture", date.fromisoformat)

    # When
    car = Car(
        {
            "vehicleMake": "ford",
            "vehicleModel": "focus",
            "dateOfManufacture": "2018-04-03",
        }
    )

    # Then
    assert car.make == "ford"
    assert car.model == "focus"
    assert car.manufactured_at == date(2018, 4, 3)


def test_optional_dataclass():
    # Given
    @jsondataclass
    class Car:
        make: str = jsonfield("make")
        model: Optional[str] = jsonfield("model")

    # When
    car = Car(
        {
            "make": "ford",
        }
    )

    # Then
    assert car.make == "ford"
    assert car.model is None


def test_literal_field_validation():
    # Given
    @jsondataclass
    class Car:
        make: Literal["ford", "volkswagen"] = jsonfield("make")
        model: str = jsonfield("model")

    # When & Then
    with pytest.raises(ValueError):
        Car({"make": "renault", "model": "clio"})


def test_extra_fields_ignored():
    # Given
    @jsondataclass
    class Car:
        make: str = jsonfield("make")

    # When
    car = Car({"make": "ford", "model": "focus"})

    # Then
    assert car.make == "ford"
    with pytest.raises(AttributeError):
        assert car.model is None


def test_jsonfield_not_needed():
    # Given
    @jsondataclass
    class Car:
        make: str
        model: str = jsonfield("carModel")

    # When
    car = Car({"make": "ford", "carModel": "focus"})

    # Then
    assert car.make == "ford"
    assert car.model == "focus"
