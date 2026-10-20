"""JSON Schemas for corpus files."""

from __future__ import annotations

import json
from functools import cache
from importlib import resources

import jsonschema


@cache
def load_schema(name: str) -> dict:
    return json.loads(resources.files(__package__).joinpath(f"{name}.schema.json").read_text())


def validate(data: dict, name: str) -> None:
    jsonschema.validate(data, load_schema(name))
