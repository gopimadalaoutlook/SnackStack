"""Lazy ChromaDB retrieval support for the SnackStack menu catalog."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from langchain_chroma import Chroma
from langchain_core.documents import Document

from snackstack.config import create_embeddings, get_settings, load_environment
from snackstack.data.menu import MENU_CATALOG
from snackstack.logger import setup_logger


logger = setup_logger("snackstack.rag")


def build_menu_documents() -> list[Document]:
    """Transform each menu record into a searchable LangChain document."""

    documents: list[Document] = []
    for item in MENU_CATALOG:
        dietary_tags = ", ".join(item["dietary_tags"]) or "None"
        page_content = "\n".join(
            (
                f"Name: {item['name']}",
                f"Description: {item['description']}",
                f"Category: {item['category']}",
                f"Cuisine: {item['cuisine']}",
                f"Price: ${item['price']:.2f}",
                f"Rating: {item['rating']}",
                f"Dietary tags: {dietary_tags}",
                f"Available: {'Yes' if item['availability'] else 'No'}",
            )
        )
        metadata = {
            "id": item["id"],
            "name": item["name"],
            "category": item["category"],
            "cuisine": item["cuisine"],
            "price": item["price"],
            "rating": item["rating"],
            "dietary_tags": dietary_tags,
            "availability": item["availability"],
        }
        documents.append(Document(page_content=page_content, metadata=metadata))

    return documents


def build_vector_store(embeddings: Any | None = None) -> Chroma:
    """Create an in-memory Chroma collection from the current menu catalog."""

    if embeddings is None:
        load_environment()
        embeddings = create_embeddings(get_settings())

    documents = build_menu_documents()
    logger.info("Building menu vector store with %d documents.", len(documents))
    return Chroma.from_documents(documents=documents, embedding=embeddings)


@lru_cache(maxsize=1)
def get_menu_vector_store() -> Chroma:
    """Build the menu vector store once, on its first use."""

    return build_vector_store()


def get_menu_retriever() -> Any:
    """Return a retriever configured to return the four closest menu matches."""

    return get_menu_vector_store().as_retriever(search_kwargs={"k": 4})
