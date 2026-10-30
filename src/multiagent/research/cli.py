"""Interactive CLI for the LangGraph research assistant."""

import json

from langchain_core.messages import AIMessage, ToolMessage

from .config import MODEL_NAME, require_api_key
from .graph import build_graph

_CONFIG = {"configurable": {"thread_id": "cli-session"}}


def _print_update(node: str, update: dict) -> None:
    """Show which agent is working and what tools it calls, as events stream in."""
    for message in update.get("messages", []):
        if isinstance(message, AIMessage) and message.tool_calls:
            for call in message.tool_calls:
                args = json.dumps(call["args"], default=str)
                if len(args) > 120:
                    args = args[:117] + "..."
                print(f"[{node}] → {call['name']}({args})")
        elif isinstance(message, ToolMessage):
            result = message.content
            if not isinstance(result, str):
                result = str(result)
            if len(result) > 200:
                result = result[:197] + "..."
            print(f"[{node}] ← {message.name}: {result}")


def main() -> None:
    require_api_key()
    graph = build_graph()

    print(f"Research assistant ready (model: {MODEL_NAME}).")
    print("Ask a question, or type 'exit' to quit.")

    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            continue

        print("Researching...", flush=True)
        try:
            for chunk in graph.stream(
                {"messages": [{"role": "user", "content": question}]},
                config=_CONFIG,
                stream_mode="updates",
            ):
                for node, update in chunk.items():
                    _print_update(node, update)

            final = graph.get_state(_CONFIG).values["messages"][-1]
            print(f"\nAssistant: {final.content}")
        except KeyboardInterrupt:
            print("\nRun interrupted — ask another question or type 'exit'.")
        except Exception as error:
            print(f"Research failed: {error}")

    print("\nGoodbye!")


if __name__ == "__main__":
    main()
