# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

"""Module representing all errors which can occur during bot operation"""

__all__ = [
    "APIError",
    "APIRequestError",
    "APIDataError",
]


class APIError(Exception):
    """Exception raised when there is an error fetching or parsing API data."""


class APIRequestError(APIError):
    """Exception raised when there is an error fetching API data."""


class APIDataError(APIError):
    """Exception raised when there is an error parsing API data."""
