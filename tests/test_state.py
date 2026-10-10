"""Tests for the shared graph-state shape."""

import unittest

from snackstack.state import StackState


class StackStateTests(unittest.TestCase):
    def test_state_accepts_required_phase_one_fields(self) -> None:
        state: StackState = {
            "messages": [],
            "user_query": "Show vegan dishes",
            "route": ["menu_agent"],
            "menu_response": "",
            "order_response": "",
            "final_answer": "",
        }

        self.assertEqual(state["route"], ["menu_agent"])
