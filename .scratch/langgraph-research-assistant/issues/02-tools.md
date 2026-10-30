# Ticket 02: Tools

Status: resolved

Expose the existing local tools (calculate, get_current_time, text_stats, estimate_tokens, pick_random) to LangChain without changing their behavior. Add a web search tool backed by DuckDuckGo (no API key), isolated behind a single tool function so the provider can be swapped later.

Spec: ../spec.md

Blocked by: 01
