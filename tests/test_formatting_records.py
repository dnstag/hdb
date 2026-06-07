# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

from hdb.domain import Mode, Reference, ReferenceType, Spot, SpotType
from hdb.formatting.messages import FormattedField, MessageKind
from hdb.formatting.records import format_spot, format_spots_table


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
        FormattedField(name="Reference", value="DE-0693 Biosphärenreservat Bliesgau", inline=True),
        FormattedField(name="Comments", value="TEST", inline=False),
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
        FormattedField(name="Comments", value="TEST", inline=False),
    ]


def test_format_cluster_spots_table() -> None:
    spots = [_valid_spot(type=SpotType.CLUSTER, reference=None)]
    message = format_spots_table(spots)

    assert message.headers == ("CALLSIGN", "MODE", "FREQUENCY")
    assert message.rows == (("DK8YS", "SSB", "14333.00 kHz"),)


def test_format_program_spots_table() -> None:
    spots = [_valid_spot(type=SpotType.PROGRAM, reference=_valid_reference())]
    message = format_spots_table(spots)

    assert message.headers == ("CALLSIGN", "MODE", "FREQUENCY", "REFERENCE")
    assert message.rows == (("DK8YS", "SSB", "14333.00 kHz", "DE-0693"),)


def _valid_spot(*, type: SpotType = SpotType.PROGRAM, reference: Reference | None) -> Spot:
    return Spot(
        callsign="DK8YS",
        frequency_khz=14333.0,
        mode=Mode.SSB,
        type=type,
        comments="TEST",
        reference=reference,
    )


def _valid_reference() -> Reference:
    return Reference(type=ReferenceType.POTA, id="DE-0693", name="Biosphärenreservat Bliesgau")
