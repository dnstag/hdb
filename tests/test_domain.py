# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

import pytest

from hdb.domain import Mode, Reference, ReferenceType, Spot, SpotType


@pytest.mark.parametrize("coordinates", [(-91, 0), (91, 0)])
def test_reference_rejects_invalid_latitude(coordinates: tuple[float, float]) -> None:
    with pytest.raises(ValueError, match="Latitude"):
        _valid_reference(coordinates=coordinates)


@pytest.mark.parametrize("coordinates", [(0, -181), (0, 181)])
def test_reference_rejects_invalid_longitude(coordinates: tuple[float, float]) -> None:
    with pytest.raises(ValueError, match="Longitude"):
        _valid_reference(coordinates=coordinates)


@pytest.mark.parametrize("id", ["", " "])
def test_reference_rejects_empty_id(id: str) -> None:
    with pytest.raises(ValueError, match="id"):
        _valid_reference(id=id)


@pytest.mark.parametrize("name", ["", " "])
def test_reference_rejects_empty_name(name: str) -> None:
    with pytest.raises(ValueError, match="name"):
        _valid_reference(name=name)


def test_reference_rejects_invalid_grid4() -> None:
    with pytest.raises(ValueError, match="Grid4"):
        _valid_reference(grid4="JN39mf")


def test_reference_rejects_invalid_grid6() -> None:
    with pytest.raises(ValueError, match="Grid6"):
        _valid_reference(grid6="JN39")


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


def _valid_reference(**overrides: object) -> Reference:
    data = {
        "type": ReferenceType.POTA,
        "id": "DE-1234",
        "coordinates": (0, 0),
    }
    data.update(overrides)
    return Reference(**data)
