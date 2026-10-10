"""Tests for configuration validation that do not require external services."""

import unittest

from snackstack.config import get_settings


class SettingsTests(unittest.TestCase):
    def test_get_settings_reads_api_key_and_uses_required_models(self) -> None:
        settings = get_settings({"OPENAI_API_KEY": "test-key"})

        self.assertEqual(settings.openai_api_key, "test-key")
        self.assertEqual(settings.chat_model, "gpt-4o")
        self.assertEqual(settings.embedding_model, "text-embedding-3-small")

    def test_get_settings_rejects_missing_api_key(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "OPENAI_API_KEY is required"):
            get_settings({})
