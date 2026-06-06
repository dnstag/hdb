# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

import logging
import os

from dotenv import load_dotenv

from hdb.api.http import UrllibHttpClient
from hdb.api.pota import PotaAPIClient
from hdb.config import AppConfig
from hdb.context import AppContext
from hdb.discord.bot import create_bot


def main() -> None:
    load_dotenv()

    config = AppConfig(os.environ["DISCORD_TOKEN"], int(os.environ["DISCORD_GUILD_ID"]))
    ctx = AppContext(pota_client=PotaAPIClient(UrllibHttpClient()))
    _configure_logging()

    bot = create_bot(config=config, context=ctx)
    bot.run(config.discord_token)


def _configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=level.upper(), format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )


if __name__ == "__main__":
    main()
