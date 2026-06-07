# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

import pytest

from hdb.domain import Reference, ReferenceType


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


def _valid_reference(**overrides: object) -> Reference:
    data = {
        "type": ReferenceType.POTA,
        "id": "DE-1234",
        "coordinates": (0, 0),
    }
    data.update(overrides)
    return Reference(**data)
