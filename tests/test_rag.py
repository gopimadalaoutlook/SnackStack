"""Offline tests for menu documents and RAG-dependent menu search."""

import unittest
from unittest.mock import Mock, patch

from langchain_core.documents import Document

from snackstack.tools.menu_tools import search_menu_catalog
from snackstack.tools.rag import build_menu_documents


class RagTests(unittest.TestCase):
    def test_build_menu_documents_preserves_all_catalog_entries(self) -> None:
        documents = build_menu_documents()

        self.assertEqual(len(documents), 8)
        self.assertEqual(documents[0].metadata["id"], "M001")
        self.assertIn("Price: $16.99", documents[0].page_content)

    def test_build_vector_store_supports_similarity_search(self) -> None:
        class DeterministicEmbeddings:
            def embed_documents(self, texts: list[str]) -> list[list[float]]:
                return [[float(len(text)), 1.0] for text in texts]

            def embed_query(self, text: str) -> list[float]:
                return [float(len(text)), 1.0]

        from snackstack.tools.rag import build_vector_store

        vector_store = build_vector_store(embeddings=DeterministicEmbeddings())
        matches = vector_store.similarity_search("vegan dishes", k=2)

        self.assertEqual(len(matches), 2)
        self.assertIn("name", matches[0].metadata)

    @patch("snackstack.tools.menu_tools.get_menu_retriever")
    def test_search_menu_catalog_formats_retrieved_dishes(self, get_retriever: Mock) -> None:
        get_retriever.return_value.invoke.return_value = [
            Document(
                page_content="Name: Vegan Tofu Banh Mi\nDescription: Crispy tofu sandwich",
                metadata={
                    "name": "Vegan Tofu Banh Mi",
                    "price": 12.49,
                    "cuisine": "Vietnamese",
                    "rating": 4.5,
                    "dietary_tags": "Vegan",
                    "availability": True,
                },
            )
        ]

        result = search_menu_catalog.invoke({"query": "vegan sandwich"})

        self.assertIn("Vegan Tofu Banh Mi ($12.49)", result)
        get_retriever.return_value.invoke.assert_called_once_with("vegan sandwich")
