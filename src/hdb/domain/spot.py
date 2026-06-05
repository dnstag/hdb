# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from enum import StrEnum

from hdb.domain.mode import Mode
from hdb.domain.reference import Reference


class SpotType(StrEnum):
    PROGRAM = "program"
    CLUSTER = "cluster"


@dataclass(frozen=True)
class Spot:
    callsign: str
    frequency_khz: float
    mode: Mode
    type: SpotType
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
