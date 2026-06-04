# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

from collections.abc import Mapping

from hdb.api.http import HttpClient
from hdb.domain.mode import Mode
from hdb.domain.reference import Reference, ReferenceType
from hdb.domain.spot import Spot, SpotType
from hdb.parsing import require_string

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
        frequency_khz=_parse_frequency(item, "frequency"),
        mode=Mode.parse(require_string(item, "mode")),
        reference=Reference(type=ReferenceType.POTA, name=require_string(item, "reference")),
        type=SpotType.PROGRAM,
    )


def _parse_frequency(item: Mapping[str, object], key: str) -> float:
    value = require_string(item, key)
    return float(value)
