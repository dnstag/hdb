# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT


from collections.abc import Mapping

from hdb.domain import Mode, ReferenceType
from hdb.providers import PotaSpotProvider


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
            "name": "Biosphärenreservat Bliesgau",
            "grid4": "JN39",
            "grid6": "JN39of",
            "latitude": 49.2116,
            "longitude": 7.19818,
            "comments": "TEST",
        },
    ]

    client = PotaSpotProvider(http=FakeHttpClient(data))
    spots = client.fetch_spots()

    assert len(spots) == 1
    spot = spots[0]
    assert spot.callsign == "DK8YS"
    assert spot.frequency_khz == 14.333
    assert spot.mode == Mode.SSB
    assert spot.reference is not None
    assert spot.reference.type == ReferenceType.POTA
    assert spot.reference.id == "DE-0693"
    assert spot.reference.name == "Biosphärenreservat Bliesgau"
    assert spot.reference.grid4 == "JN39"
    assert spot.reference.grid6 == "JN39of"
    assert spot.reference.coordinates == (49.2116, 7.19818)
    assert spot.comments == "TEST"
