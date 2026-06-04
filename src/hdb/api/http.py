# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

import json
import urllib.request
from collections.abc import Mapping
from typing import Any, Protocol
from urllib.error import URLError

from hdb.api.error import APIDataError


class HttpClient(Protocol):
    """HTTP client for JSON-array API endpoints."""

    def get_json(self, url: str) -> list[Mapping[str, Any]]: ...


class UrllibHttpClient:
    def get_json(self, url: str) -> list[Mapping[str, Any]]:

        try:
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read().decode("utf-8"))
        except URLError as err:
            raise APIDataError(f"Error fetching JSON from {url}") from err
