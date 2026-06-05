# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

import pytest

from hdb.domain.reference import Reference, ReferenceType
from hdb.domain.spot import Spot, SpotType


@pytest.mark.parametrize("frequency_khz", [0, -1])
def test_spot_rejects_non_positive_frequency(frequency_khz: int) -> None:
    with pytest.raises(ValueError, match="Frequency"):
        _valid_spot(frequency_khz=frequency_khz)


@pytest.mark.parametrize("callsign", ["", " "])
def test_spot_rejects_empty_callsign(callsign: str) -> None:
    with pytest.raises(ValueError, match="Callsign"):
        _valid_spot(callsign=callsign)


def test_spot_rejects_invalid_mode() -> None:
    with pytest.raises(ValueError, match="Invalid mode"):
        _valid_spot(mode="INVALID_MODE")


def test_cluster_spot_rejects_reference() -> None:
    with pytest.raises(ValueError, match="Cluster"):
        _valid_spot(type=SpotType.CLUSTER, reference=_valid_reference())


def test_program_spot_requires_reference() -> None:
    with pytest.raises(ValueError, match="reference"):
        _valid_spot(type=SpotType.PROGRAM, reference=None)


def test_valid_cluster_spot_without_reference_is_allowed() -> None:
    spot = _valid_spot(type=SpotType.CLUSTER, reference=None)

    assert spot.type is SpotType.CLUSTER
    assert spot.reference is None


def _valid_reference() -> Reference:
    return Reference(ReferenceType.POTA, id="DE-1234", name="Testpark")


def _valid_spot(**overrides: object) -> Spot:
    data = {
        "callsign": "DK8YS",
        "frequency_khz": 14074,
        "mode": "FT8",
        "type": SpotType.PROGRAM,
        "reference": _valid_reference(),
    }
    data.update(overrides)
    return Spot(**data)
