
"""Shared state passed between SnackStack graph nodes."""

from __future__ import annotations

from typing import Any, TypedDict


class StackState(TypedDict, total=False):
    """The information agents exchange during one assistant interaction."""

    messages: list[Any]
    user_query: str
    route: list[str]
    menu_response: str
    order_response: str
    final_answer: str
