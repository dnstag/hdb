# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from enum import StrEnum


class ReferenceType(StrEnum):
    POTA = "POTA"
    SOTA = "SOTA"
    WWFF = "WWFF"
    WWBOTA = "WWBOTA"


@dataclass(frozen=True)
class Reference:
    type: ReferenceType
    id: str
    name: str | None = None
    coordinates: tuple[float, float] | None = None
    grid4: str | None = None
    grid6: str | None = None

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Reference id cannot be empty")

        if self.name is not None and not self.name.strip():
            raise ValueError("Reference name cannot be empty if provided")

        if self.coordinates is not None:
            latitude, longitude = self.coordinates
            if not -90 <= latitude <= 90:
                raise ValueError("Latitude must be between -90 and 90")
            if not -180 <= longitude <= 180:
                raise ValueError("Longitude must be between -180 and 180")

        if self.grid4 is not None and len(self.grid4) != 4:
            raise ValueError("Grid4 must be exactly 4 characters long")

        if self.grid6 is not None and len(self.grid6) != 6:
            raise ValueError("Grid6 must be exactly 6 characters long")
