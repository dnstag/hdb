# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

from typing import Any

import discord
from discord import app_commands

from hdb.config import AppConfig
from hdb.context import AppContext
from hdb.formatting.messages import FormattedTable
from hdb.formatting.records import format_spots_table
from hdb.services.provider import SpotsProvider

has_synced = False


def create_bot(config: AppConfig, context: AppContext) -> Any:
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    pota_group = app_commands.Group(name="pota", description="POTA commands")

    @pota_group.command(name="spots", description="Shows all POTA spots")
    async def pota_spots(interaction: discord.Interaction) -> None:
        message = await handle_pota_spots(context.pota_client)
        await interaction.response.send_message(message)

    @tree.command(name="help", description="Shows this help message")
    async def help_command(interaction: discord.Interaction) -> None:
        help_message = "Not implemented yet!\n"
        await interaction.response.send_message(help_message)

    tree.add_command(pota_group)

    @client.event
    async def on_ready() -> None:
        global has_synced

        if not has_synced:
            guild = discord.Object(id=config.guild_id)
            tree.copy_global_to(guild=guild)
            commands = await tree.sync(guild=guild)

            print(
                f"Synced {len(commands)} command(s): "
                f"{', '.join(command.name for command in commands)}"
            )
            has_synced = True

        print(f"Discord bot ready as {client.user} on guild {config.guild_id}; ")

    return client


async def handle_pota_spots(provider: SpotsProvider) -> str:
    spots = provider.fetch_spots()
    sorted_spots = sorted(
        spots,
        key=lambda spot: spot.frequency_khz,
    )
    table = format_spots_table(sorted_spots, limit=20)

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
