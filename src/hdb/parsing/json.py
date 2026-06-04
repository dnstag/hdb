# Copyright (c) 2026 Yannick Seibert
# SPDX-License-Identifier: MIT

from collections.abc import Mapping


def require_string(item: Mapping[str, object], key: str) -> str:
    value = item.get(key)
    if not isinstance(value, str):
        raise ValueError(f"Expected a string for key '{key}', got {type(value).__name__}")
    return value


def require_float(item: Mapping[str, object], key: str) -> float:
    value = item.get(key)
    if not isinstance(value, (int, float)):
        raise ValueError(f"Expected a float for key '{key}', got {type(value).__name__}")
    return float(value)
