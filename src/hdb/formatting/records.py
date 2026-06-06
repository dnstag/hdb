# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

from collections.abc import Callable

from hdb.domain.spot import Spot, SpotType
from hdb.formatting.messages import FormattedField, FormattedMessage, FormattedTable, MessageKind


def _format_program_spot(spot: Spot) -> FormattedMessage:
    if spot.reference is None:
        raise ValueError("Program spots must have a reference")

    title = f"{spot.reference.type} Spot"
    description = f"{spot.callsign} at {spot.reference.id}"
    fields = [
        FormattedField(name="Callsign", value=spot.callsign),
        FormattedField(name="Frequency", value=f"{spot.frequency_khz:.2f} kHz"),
        FormattedField(name="Mode", value=spot.mode),
        FormattedField(name="Reference", value=f"{spot.reference.id} {spot.reference.name}"),
    ]
    if spot.comments:
        fields.append(FormattedField(name="Comments", value=spot.comments, inline=False))

    return FormattedMessage(
        kind=MessageKind.SPOT, title=title, description=description, fields=fields
    )


def _format_cluster_spot(spot: Spot) -> FormattedMessage:
    if spot.reference is not None:
        raise ValueError("Cluster spots should not have a reference")

    title = "Cluster Spot"
    description = f"{spot.callsign}"
    fields = [
        FormattedField(name="Callsign", value=spot.callsign),
        FormattedField(name="Frequency", value=f"{spot.frequency_khz:.2f} kHz"),
        FormattedField(name="Mode", value=spot.mode),
    ]
    if spot.comments:
        fields.append(FormattedField(name="Comments", value=spot.comments, inline=False))

    return FormattedMessage(
        kind=MessageKind.SPOT, title=title, description=description, fields=fields
    )


def _format_program_spots_table(spots: list[Spot]) -> FormattedTable:
    rows = tuple(
        (
            spot.callsign,
            spot.mode.value,
            f"{spot.frequency_khz:.2f} kHz",
            spot.reference.id if spot.reference else "-",
        )
        for spot in spots
    )

    return FormattedTable(
        headers=("CALLSIGN", "MODE", "FREQUENCY", "REFERENCE"),
        rows=rows,
    )


def _format_cluster_spots_table(spots: list[Spot]) -> FormattedTable:
    rows = tuple(
        (
            spot.callsign,
            spot.mode.value,
            f"{spot.frequency_khz:.2f} kHz",
        )
        for spot in spots
    )

    return FormattedTable(
        headers=("CALLSIGN", "MODE", "FREQUENCY"),
        rows=rows,
    )


_SPOT_FORMATTERS: dict[SpotType, Callable[[Spot], FormattedMessage]] = {
    SpotType.PROGRAM: _format_program_spot,
    SpotType.CLUSTER: _format_cluster_spot,
}

_SPOTS_TABLE_FORMATTERS: dict[SpotType, Callable[[list[Spot]], FormattedTable]] = {
    SpotType.PROGRAM: _format_program_spots_table,
    SpotType.CLUSTER: _format_cluster_spots_table,
}


def format_spot(spot: Spot) -> FormattedMessage:
    try:
        formatter = _SPOT_FORMATTERS[spot.type]
    except KeyError as exc:
        raise ValueError(f"No formatter registered for {spot.type}") from exc

    return formatter(spot)


def format_spots_table(spots: list[Spot]) -> FormattedTable:
    if not spots:
        raise ValueError("Cannot format empty spot list.")

    try:
        formatter = _SPOTS_TABLE_FORMATTERS[spots[0].type]
    except KeyError as exc:
        raise ValueError(f"No formatter registered for {spots[0].type}") from exc

    return formatter(spots)
