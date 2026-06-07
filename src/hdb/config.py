# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

"""Class representing an application configuration"""

from dataclasses import dataclass

__all__ = [
    "AppConfig",
]


@dataclass(frozen=True)
class AppConfig:
    discord_token: str
    guild_id: int
    max_spots: int = 20
