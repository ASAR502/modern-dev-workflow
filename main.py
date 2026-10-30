import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types

from multiagent.tools import (
    calculate,
    estimate_tokens,
    get_current_time,
    pick_random,
    text_stats,
)

# 1. Load your local .env file
load_dotenv(Path(__file__).resolve().parent / ".env")

# 2. Directly configure your AQ. API key
# os.environ["GOOGLE_API_KEY"] = API_KEY

# 3. Use the current active model identifier
agent = Agent(
    name="researcher",
    model="gemini/gemini-3.5-flash-lite", # Updated to current active model endpoint
    instruction=(
        "You help users research topics thoroughly. "
        "You have tiny local tools (calculate, get_current_time, text_stats, "
        "estimate_tokens, pick_random) — call them whenever a query needs an exact "
        "value instead of guessing."
    ),
    tools=[calculate, get_current_time, text_stats, estimate_tokens, pick_random],
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(initial_delay=1, attempts=3),
        ),
    ),
)

async def main():
    print("Research assistant ready. Ask a question, or type 'exit' to quit.")
    runner = InMemoryRunner(agent=agent, app_name="research_chat")
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="terminal_user"
    )

    try:
        while True:
            try:
                question = input("\nYou: ").strip()
            except EOFError:
                break
            if question.lower() in {"exit", "quit"}:
                break
            if not question:
                continue

            print("Researching...", flush=True)
            try:
                answered = False
                async for event in runner.run_async(
                    user_id=session.user_id,
                    session_id=session.id,
                    new_message=types.Content(
                        role="user", parts=[types.Part(text=question)]
                    ),
                ):
                    if event.is_final_response() and event.content:
                        response = "\n".join(
                            part.text for part in event.content.parts or []
                            if part.text and not getattr(part, 'thought', False)
                        )
                        if response:
                            print(f"\nAssistant: {response}")
                            answered = True
                if not answered:
                    print("Assistant: No text response received. Try another question.")
            except Exception as error:
                print(f"Could not get a response: {error}")
    finally:
        await runner.close()
        print("\nGoodbye!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass