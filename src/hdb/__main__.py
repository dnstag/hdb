# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

import os

from dotenv import load_dotenv

from hdb.discord.bot import create_bot


def main() -> None:
    load_dotenv()
    token = os.environ["DISCORD_TOKEN"]
    guild_id = int(os.environ["DISCORD_GUILD_ID"])

    bot = create_bot(guild_id)
    bot.run(token)


if __name__ == "__main__":
    main()
