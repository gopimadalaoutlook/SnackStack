"""Tests for centralized logger setup."""

import logging
import unittest

from snackstack.logger import setup_logger


class LoggerTests(unittest.TestCase):
    def test_setup_logger_is_idempotent(self) -> None:
        logger_name = "snackstack.tests.logger"
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()

        first = setup_logger(logger_name)
        second = setup_logger(logger_name)

        self.assertIs(first, second)
        self.assertEqual(len(first.handlers), 1)
        self.assertFalse(first.propagate)
