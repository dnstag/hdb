# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

from enum import StrEnum


class Mode(StrEnum):
    SSB = "SSB"
    AM = "AM"
    FM = "FM"
    CW = "CW"
    FT8 = "FT8"
    FT4 = "FT4"
    RTTY = "RTTY"
    PSK31 = "PSK31"

    @classmethod
    def parse(cls, value: str) -> Mode:
        normalized = value.strip().upper().replace(" ", "")
        aliases = {
            "PHONE": cls.SSB,
            "VOICE": cls.SSB,
        }
        if normalized in aliases:
            return aliases[normalized]

        for mode in cls:
            if mode.value == normalized:
                return mode

        raise ValueError(f"Unsupported mode: {value}")
