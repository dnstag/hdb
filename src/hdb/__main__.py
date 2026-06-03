# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

import os

from hdb.discord.bot import create_bot


def main() -> None:
    token = os.environ["DISCORD_TOKEN"]
    create_bot(token)


if __name__ == "__main__":
    main()
