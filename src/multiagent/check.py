"""Verify the OpenAI API key and LLM access. Runnable via `uv run check`."""

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

PLACEHOLDERS = {"", "api_key", "your_api_key_here", "your_openai_api_key_here"}


def main() -> None:
    # 1. Load environment variables from .env
    load_dotenv()

    # 2. Validate the API key
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if api_key.lower() in PLACEHOLDERS:
        sys.exit("ERROR: OPENAI_API_KEY is missing or still a placeholder in .env")

    print(f"OPENAI_API_KEY found (masked): {api_key[:4]}...{api_key[-4:]}")

    try:
        # 3. Initialize the official OpenAI client
        client = OpenAI()

        # 4. Create a chat completion using the OpenAI SDK
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Explain how AI works in a few words."}
            ],
        )
    except Exception as error:
        sys.exit(f"LLM check FAILED: {error}")

    # 5. Extract and print the response content
    print(f"LLM check OK: {response.choices[0].message.content}")


if __name__ == "__main__":
    main()
