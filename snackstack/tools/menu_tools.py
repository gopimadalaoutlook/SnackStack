"""Tool definitions used by the menu specialist agent."""

from __future__ import annotations

from langchain_core.documents import Document
from langchain_core.tools import tool

from snackstack.tools.rag import get_menu_retriever


def _format_menu_result(document: Document) -> str:
    """Create a concise, user-facing representation of a retrieved menu item."""

    metadata = document.metadata
    availability = "available" if metadata["availability"] else "unavailable"
    dietary_tags = metadata["dietary_tags"]
    return (
        f"{metadata['name']} (${metadata['price']:.2f}) - {metadata['cuisine']}; "
        f"rated {metadata['rating']}; {dietary_tags}; {availability}. "
        f"{document.page_content.splitlines()[1].removeprefix('Description: ')}"
    )


@tool
def search_menu_catalog(query: str) -> str:
    """Search SnackStack's menu for dishes matching a natural-language request."""

    cleaned_query = query.strip()
    if not cleaned_query:
        return "Please provide a dish, cuisine, dietary preference, or budget to search for."

    documents = get_menu_retriever().invoke(cleaned_query)
    if not documents:
        return "I could not find a menu item matching that request."

    return "\n".join(_format_menu_result(document) for document in documents)
