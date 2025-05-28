from google.adk import Agent

from config import SUB_AGENT_MODEL
from tools import get_current_local_time

greeting_agent = Agent(
    name="GreetingAgent",
    model=SUB_AGENT_MODEL,
    description="Handles simple greetings like 'Hi', 'Hello'.",
    instruction="""
    You are a friendly greeting agent. Your only task is to respond to simple greetings. If the user says 'Hi', 
    'Hello', or similar, respond with a friendly and concise greeting. Do not handle any other type of request.
    """,
    tools=[],
)

farewell_agent = Agent(
    name="FarewellAgent",
    model=SUB_AGENT_MODEL,
    description="Handles simple farewells and provides the current time.",
    instruction="""
    You are a polite farewell agent. Your tasks are:
    1. Respond to simple farewells (e.g., 'Bye', 'Goodbye').
    2. When responding to a farewell, ALSO use the 'get_current_local_time_tool' to get the current time and include
     it in your farewell message.
    You MUST provide the 'time_zone' parameter to this tool. If the user does not specify a particular timezone, or 
    if their request for a timezone is unclear, you MUST pass 'UTC' as the value for the 'time_zone' parameter.
    """,
    tools=[get_current_local_time],
)
