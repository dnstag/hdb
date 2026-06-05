# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

from collections.abc import Callable

from hdb.domain.spot import Spot, SpotType
from hdb.formatting.messages import FormattedField, FormattedMessage, MessageKind


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
    if spot.comments is not None:
        fields.append(FormattedField(name="Comments", value=spot.comments))

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
    if spot.comments is not None:
        fields.append(FormattedField(name="Comments", value=spot.comments))

    return FormattedMessage(
        kind=MessageKind.SPOT, title=title, description=description, fields=fields
    )


_FORMATTERS: dict[SpotType, Callable[[Spot], FormattedMessage]] = {
    SpotType.PROGRAM: _format_program_spot,
    SpotType.CLUSTER: _format_cluster_spot,
}


def format_spot(spot: Spot) -> FormattedMessage:
    try:
        formatter = _FORMATTERS[spot.type]
    except KeyError as exc:
        raise ValueError(f"No formatter registered for {spot.type}") from exc

    return formatter(spot)
