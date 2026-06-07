# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

import logging
import os

from dotenv import load_dotenv

from hdb.bot import create_bot
from hdb.config import AppConfig
from hdb.context import AppContext
from hdb.domain import SpotType
from hdb.http import UrllibHttpClient
from hdb.providers import PotaSpotProvider, ProviderRegistration, ProviderSource
from hdb.services import SpotService


def main() -> None:
    load_dotenv()

    registry = frozenset(
        {
            ProviderRegistration(
                source=ProviderSource.POTA,
                spot_type=SpotType.PROGRAM,
                spot_provider=PotaSpotProvider(UrllibHttpClient()),
            )
        },
    )

    config = AppConfig(os.environ["DISCORD_TOKEN"], int(os.environ["DISCORD_GUILD_ID"]))
    ctx = AppContext(spot_service=SpotService(registry))
    _configure_logging()

    bot = create_bot(config=config, context=ctx)
    bot.run(config.discord_token)


def _configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=level.upper(), format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )


if __name__ == "__main__":
    main()
