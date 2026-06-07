# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

"""Base class for service proviers used as protocol"""

from typing import Protocol

from hdb.domain import Spot


class SpotsProvider(Protocol):
    def fetch_spots(self) -> list[Spot]: ...
