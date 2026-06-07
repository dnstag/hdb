# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

"""Module for basic Discord bot set-up"""

import logging
from typing import Any

import discord
from discord import app_commands

from hdb.config import AppConfig
from hdb.context import AppContext
from hdb.discord import handle_spots_list

__all__ = [
    "create_bot",
]
has_synced = False
logger = logging.getLogger(__name__)


def create_bot(config: AppConfig, context: AppContext) -> Any:
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    spots_group = app_commands.Group(name="spots", description="Spot commands")

    @spots_group.command(name="list", description="Shows a list of current spots from all sources")
    async def pota_spots(interaction: discord.Interaction) -> None:
        message = handle_spots_list(context.pota_spots, config.max_spots)
        await interaction.response.send_message(message)

    @tree.command(name="help", description="Shows this help message")
    async def help_command(interaction: discord.Interaction) -> None:
        help_message = "Not implemented yet!\n"
        await interaction.response.send_message(help_message)

    tree.add_command(spots_group)

    @client.event
    async def on_ready() -> None:
        global has_synced

        if not has_synced:
            guild = discord.Object(id=config.guild_id)
            tree.copy_global_to(guild=guild)
            commands = await tree.sync(guild=guild)

            logger.info(
                "Synced %d command(s): %s",
                len(commands),
                ", ".join(command.name for command in commands),
            )
            has_synced = True

        logger.info("Discord bot ready as %s on guild %d", client.user, config.guild_id)

    return client
