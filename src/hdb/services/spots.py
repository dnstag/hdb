# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

"""Class describing a Spot service."""

from hdb.domain import Spot, SpotType
from hdb.providers import ProviderRegistration, ProviderSource


class SpotService:
    def __init__(self, providers: frozenset[ProviderRegistration]) -> None:
        self._providers = providers

    def collect_spots(
        self,
        sources: ProviderSource | None = None,
        spot_type: SpotType | None = None,
    ) -> list[Spot]:
        spots: list[Spot] = []

        for registration in self._providers:
            if not registration.enabled:
                continue

            if sources is not None and not (registration.source & sources):
                continue

            if registration.spot_provider is None:
                continue

            if spot_type is not None and spot_type not in registration.spot_type:
                continue

            fetched_spots = registration.spot_provider.fetch_spots()

            # Defensive filter in case a provider returns an unexpected spot type.
            if spot_type is not None:
                fetched_spots = [spot for spot in fetched_spots if spot.type == spot_type]

            spots.extend(fetched_spots)

        return spots
