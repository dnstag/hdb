# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

import logging

from hdb.error import APIError
from hdb.formatting import FormattedTable, format_spots_table
from hdb.services import SpotService

logger = logging.getLogger(__name__)


def handle_spots_list(spot_service: SpotService, limit: int) -> str:
    try:
        spots = spot_service.collect_spots()
    except APIError:
        msg = "Unable to fetch POTA spots"
        logger.exception(msg)
        return msg

    sorted_spots = sorted(spots[:limit], key=lambda spot: spot.frequency_khz)
    table = format_spots_table(sorted_spots)

    return _to_discord_table(table)


def _to_discord_table(table: FormattedTable) -> str:
    all_rows = (table.headers, *table.rows)

    widths = tuple(
        max(len(row[column]) for row in all_rows) for column in range(len(table.headers))
    )

    lines = [
        " | ".join(value.ljust(widths[index]) for index, value in enumerate(table.headers)),
        "-+-".join("-" * width for width in widths),
    ]

    for row in table.rows:
        lines.append(" | ".join(value.ljust(widths[index]) for index, value in enumerate(row)))

    return "```text\n" + "\n".join(lines) + "\n```"
