import json
from collections.abc import Sequence
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class Cat(BaseModel):
    pet_type: Literal['cat']
    meows: int


class Dog(BaseModel):
    pet_type: Literal['dog']
    barks: float


class Lizard(BaseModel):
    pet_type: Literal['reptile', 'lizard']
    scales: bool


def test_stuff():
    def with_type():
        type Pet = Annotated[Cat | Dog | Lizard, Field(discriminator='pet_type')]

        class Model(BaseModel):
            pet: Sequence[Pet]
            n: int

        return Model

    def without_type():
        Pet = Annotated[Cat | Dog | Lizard, Field(discriminator='pet_type')]

        class Model(BaseModel):
            pet: Sequence[Pet]
            n: int

        return Model

    with open('type.json', 'w') as f:
        f.write(json.dumps(with_type().model_json_schema(), indent=4))
    with open('no-type.json', 'w') as f:
        f.write(json.dumps(without_type().model_json_schema(), indent=4))
    # assert without_type().model_fields == with_type().model_fields
    # ^ this will fail because the json schemas don't match exactly
