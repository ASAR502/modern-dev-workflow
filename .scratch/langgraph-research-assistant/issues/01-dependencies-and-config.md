# Ticket 01: Dependencies and config

Status: resolved

Add `langgraph`, `langgraph-supervisor`, and the DuckDuckGo search package to the project dependencies and install them. Add config loading: `OPENAI_API_KEY` and `OPENAI_MODEL` (with a sensible low-cost default model) from `.env` via python-dotenv, with a startup check that exits with a clear message when the key is missing or a placeholder (matching `check.py` style).

Spec: ../spec.md

Blocked by: none
