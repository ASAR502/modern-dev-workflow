# Ticket 04: CLI entry point

Status: resolved

New separate interactive CLI entry point (existing ADK entry point untouched): prompt loop, streams graph events printing the active agent name and each tool call as it happens, thread ID per session for memory, ignores empty input, `exit`/`quit` to leave, per-run exceptions caught and printed without killing the loop.

Spec: ../spec.md

Blocked by: 03
