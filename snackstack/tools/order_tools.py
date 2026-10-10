"""Tool definitions used by the order specialist agent."""

from __future__ import annotations

from typing import Any

from langchain_core.tools import tool

from snackstack.data.orders import ORDER_DATABASE


def _find_order(identifier: Any) -> dict[str, Any] | None:
    """Find an order by order ID, tracking ID, or customer email address."""

    if not isinstance(identifier, str):
        return None

    normalized_identifier = identifier.strip().casefold()
    if not normalized_identifier:
        return None

    for order in ORDER_DATABASE.values():
        candidate_values = {
            str(order.get("order_id", "")).casefold(),
            str(order.get("tracking_id", "")).casefold(),
            str(order.get("customer_email", "")).casefold(),
        }
        if normalized_identifier in candidate_values:
            return order
    return None


@tool
def get_order_status(identifier: str) -> str:
    """Look up an order by its order ID, tracking ID, or customer email address."""

    order = _find_order(identifier)
    if order is None:
        return "No order was found for that order ID, tracking ID, or email address."

    return (
        f"Order {order['order_id']} for {order['item_name']} is {order['status']}. "
        f"Tracking ID: {order['tracking_id']}. "
        f"Estimated delivery: {order['estimated_delivery']}."
    )
