# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    discord_token: str
    guild_id: int
