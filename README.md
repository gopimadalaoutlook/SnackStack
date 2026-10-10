# SnackStack

SnackStack is a planned multi-agent food delivery assistant built with LangGraph.
It will route food and order-tracking questions to specialist agents, use semantic
menu search, and support human-in-the-loop order clarification.

## Current status

Phase 1 is complete: project metadata, environment-backed settings, OpenAI client
factories, centralized logging, and the shared graph-state type are in place.
The interactive CLI, agents, RAG tools, and graph are not implemented yet.

## Prerequisites

- Python 3.11+
- An OpenAI API key

## Setup

1. Create and activate a virtual environment.
2. Install the project in editable mode: `pip install -e .`
3. Copy `.env.example` to `.env`.
4. Set `OPENAI_API_KEY` in `.env`.

## Development checks

Run the Phase 1 unit tests with:

```text
python -m unittest discover -s tests -v
```
