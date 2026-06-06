# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

from hdb.api.pota import PotaAPIClient


@dataclass(frozen=True)
class AppContext:
    pota_client: PotaAPIClient
