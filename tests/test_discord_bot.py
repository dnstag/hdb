# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

from hdb.discord.bot import handle_pota_spots
from hdb.domain import Mode, Reference, ReferenceType, Spot, SpotType


class FakeSpotProvider:
    def fetch_spots(self) -> list[Spot]:
        return [_valid_spot()]


def test_handle_pota_spots() -> None:
    message = handle_pota_spots(FakeSpotProvider(), 20)
    assert message == (
        "```text\n"
        "CALLSIGN | MODE | FREQUENCY    | REFERENCE\n"
        "---------+------+--------------+----------\n"
        "DK8YS    | FT8  | 14074.00 kHz | DE-1234  \n"
        "```"
    )


def _valid_reference() -> Reference:
    return Reference(ReferenceType.POTA, id="DE-1234", name="Testpark")


def _valid_spot(**overrides: object) -> Spot:
    data = {
        "callsign": "DK8YS",
        "frequency_khz": 14074,
        "mode": Mode.FT8,
        "type": SpotType.PROGRAM,
        "reference": _valid_reference(),
    }
    data.update(overrides)
    return Spot(**data)
