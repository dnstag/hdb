# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from enum import StrEnum


class MessageKind(StrEnum):
    ALERT = "alert"
    CONFIG = "config"
    EMPTY = "empty"
    ERROR = "error"
    PROFILE = "profile"
    REFERENCE = "reference"
    SPOT = "spot"


@dataclass(frozen=True)
class FormattedField:
    """A compact label/value pair for later conversion to Discord embeds."""

    name: str
    value: str
    inline: bool = True

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Field name must not be empty.")
        if not self.value.strip():
            raise ValueError("Field value must not be empty.")


@dataclass(frozen=True)
class FormattedTable:
    headers: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class FormattedMessage:
    """A Discord-neutral representation of a compact bot response."""

    title: str
    description: str
    kind: MessageKind
    fields: list[FormattedField] | None = None
    table: FormattedTable | None = None
    url: str | None = None

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Message title must not be empty.")
        if not self.description.strip():
            raise ValueError("Message description must not be empty.")
