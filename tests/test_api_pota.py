# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT


from collections.abc import Mapping

from hdb.api.pota import PotaAPIClient
from hdb.domain.mode import Mode
from hdb.domain.reference import ReferenceType


class FakeHttpClient:
    def __init__(self, data: list[Mapping[str, object]]) -> None:
        self._data = list(data)

    def get_json(self, url: str) -> list[Mapping[str, object]]:
        return self._data


def test_pota_api_fetches_spots():
    data: list[Mapping[str, object]] = [
        {
            "activator": "DK8YS",
            "frequency": "14.333",
            "mode": "SSB",
            "reference": "DE-0693",
        },
    ]

    client = PotaAPIClient(http=FakeHttpClient(data))
    spots = client.fetch_spots()

    assert len(spots) == 1
    spot = spots[0]
    assert spot.callsign == "DK8YS"
    assert spot.frequency_khz == 14.333
    assert spot.mode == Mode.SSB
    assert spot.reference is not None
    assert spot.reference.type == ReferenceType.POTA
    assert spot.reference.name == "DE-0693"
