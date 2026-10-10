"""Offline tests for direct order lookup."""

import unittest

from snackstack.tools.order_tools import get_order_status


class OrderToolTests(unittest.TestCase):
    def test_lookup_by_order_id(self) -> None:
        result = get_order_status.invoke({"identifier": "ord-201"})

        self.assertIn("Order ORD-201", result)
        self.assertIn("Out for Delivery", result)

    def test_lookup_by_tracking_id(self) -> None:
        result = get_order_status.invoke({"identifier": "SS203TRK"})

        self.assertIn("Classic Cheeseburger", result)

    def test_lookup_by_email(self) -> None:
        result = get_order_status.invoke({"identifier": "sofia.martinez@example.com"})

        self.assertIn("Baja Fish Tacos", result)

    def test_lookup_rejects_unknown_identifier(self) -> None:
        result = get_order_status.invoke({"identifier": "ORD-999"})

        self.assertIn("No order was found", result)

    def test_lookup_ignores_padding_and_case(self) -> None:
        result = get_order_status.invoke({"identifier": "  ss203trk  "})

        self.assertIn("Classic Cheeseburger", result)
