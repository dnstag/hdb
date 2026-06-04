# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

from typing import Any

import discord
from discord import app_commands

has_synced = False


def create_bot(guild_id: int) -> Any:
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    pota_group = app_commands.Group(name="pota", description="POTA commands")

    @pota_group.command(name="spots", description="Shows all POTA spots")
    async def pota_spots(interaction: discord.Interaction) -> None:
        help_message = "Not implemented yet!\n"
        await interaction.response.send_message(help_message)

    @tree.command(name="help", description="Shows this help message")
    async def help_command(interaction: discord.Interaction) -> None:
        help_message = "Not implemented yet!\n"
        await interaction.response.send_message(help_message)

    tree.add_command(pota_group)

    @client.event
    async def on_ready() -> None:
        global has_synced

        if not has_synced:
            guild = discord.Object(id=guild_id)
            tree.copy_global_to(guild=guild)
            commands = await tree.sync(guild=guild)

            print(
                f"Synced {len(commands)} command(s): "
                f"{', '.join(command.name for command in commands)}"
            )
            has_synced = True

        print(f"Discord bot ready as {client.user} on guild {guild_id}; ")

    return client
