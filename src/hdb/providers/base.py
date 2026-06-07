# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

"""Base class for service proviers used as protocol"""

from dataclasses import dataclass
from enum import Flag, auto
from typing import Protocol

from hdb.domain import Spot, SpotType


class ProviderSource(Flag):
    POTA = auto()
    SOTA = auto()
    WWFF = auto()
    WWBOTA = auto()
    DXWATCH = auto()


class SpotProvider(Protocol):
    def fetch_spots(self) -> list[Spot]: ...


class ActivationProvider(Protocol):
    def fetch_activations(self) -> list: ...


class PropagationProvider(Protocol):
    def fetch_propagation(self) -> list: ...


@dataclass(frozen=True)
class ProviderRegistration:
    source: ProviderSource
    spot_type: SpotType
    spot_provider: SpotProvider | None = None
    activation_provider: ActivationProvider | None = None
    propagation_provider: PropagationProvider | None = None
    enabled: bool = True
