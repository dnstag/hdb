# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

from collections.abc import Mapping

from hdb.api.http import HttpClient
from hdb.domain import Mode, Reference, ReferenceType, Spot, SpotType
from hdb.parsing import require_float, require_string

POTA_SPOTS_URL = "https://api.pota.app/spot/activator"


class PotaAPIClient:
    def __init__(
        self,
        http: HttpClient,
    ) -> None:
        self._http = http

    def fetch_spots(self) -> list[Spot]:
        data = self._http.get_json(POTA_SPOTS_URL)

        return [_parse_spot(item) for item in data]


def _parse_spot(item: Mapping[str, object]) -> Spot:
    return Spot(
        callsign=require_string(item, "activator"),
        frequency_khz=_parse_float(item, "frequency"),
        mode=Mode.parse(require_string(item, "mode")),
        comments=require_string(item, "comments"),
        reference=Reference(
            type=ReferenceType.POTA,
            id=require_string(item, "reference"),
            name=require_string(item, "name"),
            grid4=require_string(item, "grid4"),
            grid6=require_string(item, "grid6"),
            coordinates=(require_float(item, "latitude"), require_float(item, "longitude")),
        ),
        type=SpotType.PROGRAM,
    )


def _parse_float(item: Mapping[str, object], key: str) -> float:
    value = require_string(item, key)
    return float(value)
