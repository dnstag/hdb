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
