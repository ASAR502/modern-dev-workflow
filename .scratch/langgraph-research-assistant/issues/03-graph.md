# Ticket 03: Agents and supervisor graph

Status: resolved

Define the three specialist agents (researcher, analyst, writer) as prebuilt react agents and the supervisor via `langgraph-supervisor`. Supervisor routes only and delivers the final report. Compile the graph with an in-memory checkpointer so follow-up questions retain history within a session.

Spec: ../spec.md

Blocked by: 02
