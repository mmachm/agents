import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from config import SUB_AGENT_MODEL


with open("pd_agent/instructions.txt", "r", encoding="utf-8") as f:
    instructions = f.read()

pandas_agent = Agent(
    name="pandas_agent",
    model=SUB_AGENT_MODEL,
    description=(
        """This agent specializes in data manipulation and feature engineering within a Pandas DataFrame. It understands
         the structure of a given DataFrame, including the meaning of each column. Based on a user's request, it 
         generates the Python code required to create a new, derived feature (column) from the existing data. Its 
         primary function is to translate a high-level feature description into executable Pandas code."""
    ),
    instruction=instructions,
)
