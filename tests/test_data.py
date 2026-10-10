"""Direct integrity checks for the static menu and order sources."""

import unittest

from snackstack.data.menu import MENU_CATALOG
from snackstack.data.orders import ORDER_DATABASE


class DataIntegrityTests(unittest.TestCase):
    def test_menu_catalog_has_eight_complete_items_with_unique_ids(self) -> None:
        required_fields = {
            "id",
            "name",
            "category",
            "cuisine",
            "price",
            "rating",
            "dietary_tags",
            "description",
            "availability",
        }

        self.assertEqual(len(MENU_CATALOG), 8)
        menu_ids = [item["id"] for item in MENU_CATALOG]
        self.assertEqual(len(menu_ids), len(set(menu_ids)))
        for item in MENU_CATALOG:
            self.assertTrue(required_fields.issubset(item))
            self.assertIsInstance(item["price"], (int, float))
            self.assertIsInstance(item["dietary_tags"], list)
            self.assertIsInstance(item["availability"], bool)

    def test_order_database_has_five_complete_keyed_orders(self) -> None:
        required_fields = {
            "order_id",
            "item_id",
            "item_name",
            "customer_name",
            "customer_email",
            "status",
            "price",
            "order_date",
            "estimated_delivery",
            "tracking_id",
        }

        self.assertEqual(len(ORDER_DATABASE), 5)
        for order_id, order in ORDER_DATABASE.items():
            self.assertEqual(order_id, order["order_id"])
            self.assertTrue(required_fields.issubset(order))
            self.assertIsInstance(order["price"], (int, float))

    def test_orders_reference_existing_menu_items(self) -> None:
        menu_items = {item["id"]: item for item in MENU_CATALOG}

        for order in ORDER_DATABASE.values():
            self.assertIn(order["item_id"], menu_items)
            self.assertEqual(
                order["item_name"], menu_items[order["item_id"]]["name"]
            )


if __name__ == "__main__":
    unittest.main()
