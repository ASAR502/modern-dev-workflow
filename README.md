# Research Multi-Agent

This repo contains two independent assistant implementations:

1. **LangGraph research assistant** (`src/multiagent/research/`) — a supervisor
   agent orchestrating three specialists (researcher, analyst, writer) built
   with LangGraph + LangChain on OpenAI. This is the main implementation.
2. **Google ADK assistant** (`main.py`) — a single agent with local tools,
   kept for reference and comparison.

## Setup

1. Copy `.env.example` to `.env` and set your keys:

   - `OPENAI_API_KEY` for the LangGraph assistant
     (get one at https://platform.openai.com/api-keys). Optionally set
     `OPENAI_MODEL` (defaults to `gpt-4o-mini`).
   - `GEMINI_API_KEY` for the ADK assistant
     (get one at https://ai.google.dev/gemini-api/docs/api-key).

   Never commit `.env` — it is already in `.gitignore`.

2. Verify the key and LLM access:

   ```
   uv run check.py
   ```

## Run the LangGraph research assistant

```
uv run research
```

Ask a research question and watch the supervisor route work between the
researcher (web search), analyst, and writer agents. Follow-up questions in
the same session remember the conversation. Type `exit` to quit.

## Run the ADK assistant

```
uv run main.py
```
