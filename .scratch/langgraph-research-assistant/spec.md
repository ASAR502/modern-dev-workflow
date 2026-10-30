# Spec: LangGraph Multi-Agent Research Assistant

Status: ready-for-agent

## Problem Statement

The repo currently has a single Google ADK agent (`main.py`) with a few local tools. The user wants a real multi-agent system built with LangGraph and LangChain — a team of specialist agents that cooperate to research a topic — architected clearly enough that it can be built directly from this document with OpenCode.

## Solution

A supervisor-orchestrated multi-agent research assistant, run from an interactive CLI. The user asks a research question; a supervisor agent decomposes the work and routes it to specialist agents (researcher, analyst, writer); the system returns a structured research report. The system is built with LangGraph + LangChain on OpenAI models, and lives alongside the existing Google ADK agent, which is left untouched.

## User Stories

1. As a user, I want to start an interactive research CLI with a single command, so that I can ask questions without writing code.
2. As a user, I want to type a research question in plain language, so that the system researches it for me.
3. As a user, I want a supervisor agent to break my question into subtasks, so that complex questions are handled systematically.
4. As a user, I want the supervisor to delegate web research to a researcher agent, so that the report is grounded in real sources.
5. As a user, I want an analyst agent to synthesize and summarize the researcher's raw findings, so that the noise is filtered out.
6. As a user, I want a writer agent to produce a final, readable report, so that I get a polished answer rather than raw notes.
7. As a user, I want the supervisor to decide when enough work is done and end the workflow, so that agents don't loop forever.
8. As a user, I want to see which agent is working at each step, so that I can follow the system's reasoning as it runs.
9. As a user, I want to see tool calls (e.g. web searches) as they happen, so that I can verify the research is real.
10. As a user, I want to ask follow-up questions in the same session that remember the previous conversation, so that I can drill into a topic.
11. As a user, I want to type `exit` or `quit` to leave the CLI cleanly, so that the session ends without errors.
12. As a user, I want empty input to be ignored, so that accidental Enter presses don't trigger agent runs.
13. As a user, I want a clear error message if my OpenAI API key is missing or invalid, so that I know how to fix the setup.
14. As a user, I want a graceful error message if an agent run fails mid-way (rate limit, network), so that the CLI stays usable.
15. As a user, I want to reuse the existing local tools (calculate, get_current_time, text_stats, estimate_tokens, pick_random) inside the LangGraph system, so that exact values are computed rather than guessed.
16. As a user, I want web search to work without needing another API key, so that setup stays as simple as it is today.
17. As a user, I want the model name configurable via environment variable, so that I can switch models without editing code.
18. As a user, I want the existing Google ADK assistant to keep working as before, so that I can compare the two approaches.
19. As a user, I want the README updated with setup and run instructions for the new system, so that I can get started quickly.

## Implementation Decisions

- **Framework**: LangGraph (`langgraph`) + LangChain. Add `langgraph` and `langgraph-supervisor` to project dependencies. `langchain-openai` is already present and provides the chat model.
- **Orchestration pattern**: Supervisor. A supervisor agent receives the user request and routes work to specialist agents via handoff tools, deciding when the task is complete. Built with the `langgraph-supervisor` package's prebuilt supervisor over `langgraph.prebuilt` react agents — no hand-rolled StateGraph unless the prebuilt proves insufficient.
- **Agents**:
  - **Supervisor**: routes only; never answers the user directly except to deliver the final report.
  - **Researcher**: has the web search tool plus the existing local tools; returns raw findings with source URLs.
  - **Analyst**: synthesizes findings, deduplicates, resolves conflicts, extracts key facts.
  - **Writer**: turns the analysis into the final structured report (summary, key findings, sources).
- **LLM**: `ChatOpenAI` from `langchain-openai`. Model name read from an environment variable (e.g. `OPENAI_MODEL`, default a current low-cost model). API key from `OPENAI_API_KEY` in `.env`, loaded with `python-dotenv` (already a dependency).
- **Web search**: DuckDuckGo via LangChain's DuckDuckGo search integration — free, no API key required. The search tool is isolated behind a single tool function so it can be swapped for Tavily or another provider later via configuration.
- **Shared tools**: the existing local tools module is reused as-is; tools are exposed to LangChain via its tool decorator/wrappers without changing their behavior.
- **State and memory**: the compiled graph uses LangGraph's in-memory checkpointer, keyed by a session/thread ID, so follow-up questions retain conversation history within one CLI session. Nothing is persisted across runs.
- **CLI entry point**: a new, separate entry point (new module + `uv run` command), mirroring the existing interactive loop style: prompt, run, print, repeat until `exit`/`quit`. The existing ADK entry point is untouched.
- **Observability**: the CLI streams graph events and prints the name of the active agent and each tool call as it happens, so the routing between agents is visible.
- **Error handling**: missing/placeholder API key exits at startup with a clear message (matching the existing `check.py` style); per-run exceptions are caught and printed, and the loop continues.
- **README**: updated with the new dependency setup, the new run command, and a note that two assistant implementations coexist.

## Testing Decisions

- **No automated tests for now.** The repo has no test infrastructure, and the user explicitly chose to validate manually via the CLI first.
- Verification is a manual checklist run against the CLI:
  1. Starts with a valid `.env`; exits cleanly with a clear message without one.
  2. A simple question ("What is LangGraph?") produces a report with visible agent routing.
  3. A question needing live facts triggers visible web search tool calls.
  4. A follow-up question ("tell me more about the second point") uses conversation history.
  5. `exit`, empty input, and a mid-run interruption all behave gracefully.
- When automated tests are added later, the agreed seam is the compiled graph's public interface (invoke/stream) with a fake chat model, testing external behavior only — never node internals.

## Out of Scope

- Removing or modifying the existing Google ADK agent and its dependencies.
- Hierarchical teams, network/swarm routing, or any non-supervisor orchestration.
- Persistent memory across sessions, database checkpointing, or multi-user support.
- A web UI, API server, or notebook interface.
- Automated tests, evals, CI, and LangSmith/LangFuse tracing setup.
- Paid search providers (Tavily, SerpAPI) — the swap point is built, but not configured.

## Further Notes

- Two assistant implementations will coexist: the ADK one for reference, the LangGraph one as the main path forward. Keep their code fully separate so either can be deleted independently.
- The supervisor/specialist split is deliberately small (3 specialists). New specialists (e.g. fact-checker, coder) should be addable by defining a new react agent and registering it with the supervisor — no other changes.
