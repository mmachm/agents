import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from config import ROOT_AGENT_MODEL
from pd_agent.agent import pandas_agent
from test_case_agent.agent import test_agent


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

with open("pd_agent/instructions.txt", "r", encoding="utf-8") as f:
    instructions = f.read()

description = """

An orchestrator agent that manages the creation and validation of a new feature column for a DataFrame. 
It takes a natural language request from a user and delegates the task to two specialized sub-agents: 
one that generates the required Pandas code, and another that directly calculates the feature's data. 
Its primary function is to coordinate these agents, oversee the execution of the generated code, and compare 
the results from both methods to ensure correctness and consistency.

"""

root_agent = Agent(
    name="root_agent",
    model=ROOT_AGENT_MODEL,
    description=description,
    instruction=instructions,
    tools=[
        AgentTool(agent=pandas_agent, skip_summarization=True), 
        AgentTool(agent=test_agent, skip_summarization=True)
        
    ],
)
#flash-preview-05-20