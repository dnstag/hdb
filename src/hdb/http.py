# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

"""Module representing basic HTTP handling"""

import json
import logging
import urllib.request
import xml.etree.ElementTree as ET
from collections.abc import Mapping
from typing import Any, Protocol
from urllib.error import URLError

from hdb.error import APIRequestError

__all__ = [
    "HttpClient",
    "UrllibHttpClient",
]
logger = logging.getLogger(__name__)


class HttpClient(Protocol):
    """HTTP client for JSON-array API endpoints."""

    def get_json(self, url: str) -> list[Mapping[str, Any]]: ...
    def get_xml(self, url: str) -> ET.Element: ...


class UrllibHttpClient:
    def get_json(self, url: str) -> list[Mapping[str, Any]]:

        try:
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read().decode("utf-8"))
        except URLError as err:
            raise APIRequestError(f"Error fetching JSON from {url}") from err

    def get_xml(self, url: str) -> ET.Element:

        try:
            with urllib.request.urlopen(url) as response:
                return ET.fromstring(response.read().decode("utf-8"))
        except URLError as err:
            raise APIRequestError(f"Error fetching XML from {url}") from err
