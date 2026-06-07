# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

"""Class representing an application context"""

from dataclasses import dataclass

from hdb.services import SpotService

__all__ = [
    "AppContext",
]


@dataclass(frozen=True)
class AppContext:
    spot_service: SpotService
