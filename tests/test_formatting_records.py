# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

from hdb.domain.mode import Mode
from hdb.domain.reference import Reference, ReferenceType
from hdb.domain.spot import Spot, SpotType
from hdb.formatting.messages import FormattedField, MessageKind
from hdb.formatting.records import format_spot


def test_format_program_spot_returns_formatted_message() -> None:
    spot = _valid_spot(reference=_valid_reference())

    message = format_spot(spot)

    assert message.kind is MessageKind.SPOT
    assert message.title == "POTA Spot"
    assert message.description == "DK8YS at DE-0693"
    assert message.fields == [
        FormattedField(name="Callsign", value="DK8YS", inline=True),
        FormattedField(name="Frequency", value="14333.00 kHz", inline=True),
        FormattedField(name="Mode", value="SSB", inline=True),
        FormattedField(name="Reference", value="DE-0693", inline=True),
    ]


def test_format_cluster_spot_returns_formatted_message() -> None:
    spot = _valid_spot(type=SpotType.CLUSTER, reference=None)

    message = format_spot(spot)

    assert message.kind is MessageKind.SPOT
    assert message.title == "Cluster Spot"
    assert message.description == "DK8YS"
    assert message.fields == [
        FormattedField(name="Callsign", value="DK8YS", inline=True),
        FormattedField(name="Frequency", value="14333.00 kHz", inline=True),
        FormattedField(name="Mode", value="SSB", inline=True),
    ]


def _valid_spot(*, type: SpotType = SpotType.PROGRAM, reference: Reference | None) -> Spot:
    return Spot(
        callsign="DK8YS",
        frequency_khz=14333.0,
        mode=Mode.SSB,
        type=type,
        reference=reference,
    )


def _valid_reference() -> Reference:
    return Reference(type=ReferenceType.POTA, id="DE-0693", name="Biosphärenreservat Bliesgau")
