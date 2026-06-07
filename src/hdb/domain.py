# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

"""Module representing the domain model of the application"""

from dataclasses import dataclass
from enum import Flag, StrEnum, auto

__all__ = [
    "Mode",
    "Reference",
    "ReferenceType",
    "Spot",
    "SpotType",
]


class Mode(StrEnum):
    """Class representing a radio mode value in the domain model"""

    SSB = "SSB"
    AM = "AM"
    FM = "FM"
    CW = "CW"
    FT8 = "FT8"
    FT4 = "FT4"
    RTTY = "RTTY"
    PSK31 = "PSK31"
    NONE = "NONE"

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

        return cls.NONE


class ReferenceType(StrEnum):
    """Class representing a reference type value in the domain model"""

    POTA = "POTA"
    SOTA = "SOTA"
    WWFF = "WWFF"
    WWBOTA = "WWBOTA"


class SpotProgram(Flag):
    """Class representing a specific amateur radio outdor activity program"""

    POTA = auto()
    SOTA = auto()
    WWFF = auto()
    WWBOTA = auto()


class SpotType(StrEnum):
    """Class representing a spot type value in the domain model"""

    PROGRAM = "program"
    CLUSTER = "cluster"


@dataclass(frozen=True)
class Reference:
    """Class representing a reference entity in the domain model"""

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


@dataclass(frozen=True)
class Spot:
    """Class representing a spot entity in the domain model"""

    callsign: str
    frequency_khz: float
    mode: Mode
    type: SpotType
    comments: str | None = None
    reference: Reference | None = None

    def __post_init__(self) -> None:
        if self.frequency_khz <= 0:
            raise ValueError("Frequency must be a positive float")

        if self.mode not in Mode:
            raise ValueError("Invalid mode")

        if not self.callsign.strip():
            raise ValueError("Callsign cannot be empty")

        if self.type == SpotType.CLUSTER and self.reference is not None:
            raise ValueError("Cluster spots should not have a reference")

        if self.type == SpotType.PROGRAM and self.reference is None:
            raise ValueError("Program spots must have a reference")
