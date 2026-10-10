
"""Application configuration and OpenAI client factories."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class Settings:
    """Configuration needed by SnackStack's language and embedding clients."""

    openai_api_key: str
    chat_model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"


def load_environment() -> None:
    """Load local environment values from .env when python-dotenv is installed."""

    try:
        from dotenv import load_dotenv
    except ImportError as error:
        raise RuntimeError(
            "python-dotenv is required. Install the project dependencies before running SnackStack."
        ) from error

    load_dotenv()


def get_settings(environment: Mapping[str, str] | None = None) -> Settings:
    """Return validated settings from an environment mapping or the process environment."""

    source = environment if environment is not None else os.environ
    api_key = source.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required. Add it to .env or your environment.")

    return Settings(openai_api_key=api_key)


def create_llm(settings: Settings):
    """Create the chat model used by agent nodes without making a network request."""

    try:
        from langchain_openai import ChatOpenAI
    except ImportError as error:
        raise RuntimeError(
            "langchain-openai is required. Install the project dependencies before running SnackStack."
        ) from error

    return ChatOpenAI(model=settings.chat_model, api_key=settings.openai_api_key, temperature=0)


def create_embeddings(settings: Settings):
    """Create the embeddings client used for menu semantic search."""

    try:
        from langchain_openai import OpenAIEmbeddings
    except ImportError as error:
        raise RuntimeError(
            "langchain-openai is required. Install the project dependencies before running SnackStack."
        ) from error

    return OpenAIEmbeddings(model=settings.embedding_model, api_key=settings.openai_api_key)
