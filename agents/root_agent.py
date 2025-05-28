from google.adk import Agent
from config import ROOT_AGENT_MODEL
from tools import get_weather
from agents.agents import greeting_agent, farewell_agent


weather_agent_team_instruction = f"""
    You are the main Weather Agent coordinating a team. Your primary responsibility is to provide weather information.
    Use the 'get_weather' tool ONLY for specific weather requests (e.g., 'weather in London').
    
    You have specialized sub-agents:
    1. '{greeting_agent.name}': {greeting_agent.description}. Delegate to it for these.
    2. '{farewell_agent.name}': {farewell_agent.description}. It will also provide the current time upon farewell 
    (ensure it receives 'time_zone'=\"UTC\" if user doesn't specify). Delegate to it for these.
    
    Analyze the user's query.
    If it's a greeting, delegate to 'GreetingAgent'.
    If it's a farewell, delegate to 'FarewellAgent'.
    If it's a weather request, handle it yourself using 'get_weather'.
    For anything else, politely state that you can only handle greetings, farewells, and weather requests
    """

weather_agent_team_description = """
    The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists.
    Farewell includes current time.
    """

weather_agent_team = Agent(
    name="WeatherAgentTeam",
    model=ROOT_AGENT_MODEL,
    description=weather_agent_team_description,
    instruction=weather_agent_team_instruction,
    tools=[get_weather],
    sub_agents=[greeting_agent, farewell_agent],
)
