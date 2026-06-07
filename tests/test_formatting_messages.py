# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

import pytest

from hdb.formatting import FormattedField, FormattedMessage, MessageKind


@pytest.mark.parametrize("name", ["", " "])
def test_formatted_field_rejects_invalid_name(name: str) -> None:
    with pytest.raises(ValueError, match="Field name"):
        _valid_field(name=name)


@pytest.mark.parametrize("value", ["", " "])
def test_formatted_field_rejects_invalid_value(value: str) -> None:
    with pytest.raises(ValueError, match="Field value"):
        _valid_field(value=value)


@pytest.mark.parametrize("title", ["", " "])
def test_formatted_message_rejects_invalid_title(title: str) -> None:
    with pytest.raises(ValueError, match="Message title"):
        _valid_message(title=title)


@pytest.mark.parametrize("description", ["", " "])
def test_formatted_message_rejects_invalid_description(description: str) -> None:
    with pytest.raises(ValueError, match="Message description"):
        _valid_message(description=description)


def _valid_field(**overrides: object) -> FormattedField:
    data = {"name": "Valid Name", "value": "Valid Value", "inline": True}
    data.update(overrides)

    return FormattedField(**data)


def _valid_message(**overrides: object) -> FormattedMessage:

    data = {
        "title": "Valid Title",
        "description": "Valid Description",
        "kind": MessageKind.ALERT,
        "fields": None,
        "url": None,
    }
    data.update(overrides)

    return FormattedMessage(**data)
