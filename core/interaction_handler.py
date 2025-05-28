import traceback

from google.adk import Runner
from google.genai import types as genai_types


async def call_agent_turn(
    query: str,
    runner: Runner,
    user_id: str,
    session_id_to_use: str,
) -> str:
    """
    Handles a single turn of interaction with the ADK agent.
    Sends a query to the agent via the runner and returns the final text response.
    """
    print(f"\n>>> User Query: {query}")

    # Prepare the user's message in the expected format
    new_message = genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=query)],
    )

    final_response_text = "Agent did not produce a final text response."

    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id_to_use,
            new_message=new_message,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    # Assuming the text response is in the first part for simplicity
                    final_response_text = event.content.parts[0].text
                elif (
                    event.actions
                    and event.actions.escalate
                    and hasattr(event, "error_message")
                ):
                    final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
                elif event.actions and event.actions.escalate:
                    final_response_text = "Agent escalated with an unspecified action."
                break

    except Exception as e:
        print(f"\n[call_agent_turn Error]: An error occurred during agent run: {e}")
        traceback.print_exc()
        final_response_text = "An error occurred while processing your request."

    print(f"<<< Agent Response: {final_response_text}")
    return final_response_text
