# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

import discord


def create_bot(token: str) -> None:
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready() -> None:
        print(f"Angemeldet als {client.user}")

    client.run(token)
