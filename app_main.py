import asyncio
import os
import uuid
import traceback

from google.adk import Runner

from config import (
    APP_NAME,
    DEFAULT_USER_ID,
    DEFAULT_SESSION_ID_PREFIX,
    SUB_AGENT_MODEL,
)
from agents.root_agent import coordinator_team
from core import call_agent_turn, session_service


async def run_conversation_loop():
    session_id_for_this_run = f"{DEFAULT_SESSION_ID_PREFIX}{uuid.uuid4()}"
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=DEFAULT_USER_ID,
        session_id=session_id_for_this_run,
    )

    print(
        f"Session '{session_id_for_this_run}' created for app '{APP_NAME}', user '{DEFAULT_USER_ID}'."
    )

    app_runner = Runner(
        agent=coordinator_team,
        app_name=APP_NAME,
        session_service=session_service,
    )
    print(f"Runner created for root agent '{app_runner.agent.name}'.")

    print(
        f"  (Coordinator Model: {coordinator_team.model}, Base Sub-Agent Model: {SUB_AGENT_MODEL})"
    )
    print("-" * 70)
    print(f"Starting chat with {coordinator_team.name}. Type 'quit' or 'exit' to end.")
    print("-" * 70)

    while True:
        try:
            user_query = input("You: ").strip()
            if user_query.lower() in ["quit", "exit"]:
                print("Exiting chat...")
                break
            if not user_query:
                continue

            await call_agent_turn(
                query=user_query,
                runner=app_runner,
                user_id=DEFAULT_USER_ID,
                session_id_to_use=session_id_for_this_run,
            )
        except KeyboardInterrupt:
            print("\nExiting chat due to user interrupt...")
            break
        except Exception as e:
            print(f"\n[Chat Loop Error]: An unexpected error occurred: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    print(f"--- Initializing application: {APP_NAME} ---")

    # Basic check for critical environment variables
    # config.py already attempts to load .env and prints info.
    if not os.getenv("ADK_AGENT_LLM_MODEL"):
        print(
            "⚠️ APP WARNING: ADK_AGENT_LLM_MODEL environment variable is not set. Agents will use defaults from config.py."
        )

    api_key_found = any(
        os.getenv(key)
        for key in [
            "GOOGLE_API_KEY",
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
        ]
    )
    if not api_key_found:
        print(
            "❌ APP ERROR: No common LLM API Key (e.g., GOOGLE_API_KEY) found in environment variables."
        )
        print(
            "         Please ensure your .env file is correctly set up and loaded, and contains the required API key."
        )
    else:
        print(
            "✅ LLM API Key seems to be present in environment (ADK/LiteLLM will attempt to use it)."
        )
        try:
            asyncio.run(run_conversation_loop())
        except Exception as e:
            print(f"A top-level error occurred in app_main: {e}")
            traceback.print_exc()
