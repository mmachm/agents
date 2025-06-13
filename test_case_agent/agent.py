import pandas as pd
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.genai.types import Part

from config import ROOT_AGENT_MODEL


# --- Define the Callback Function ---
def table_adder(callback_context: CallbackContext, llm_request: LlmRequest) -> LlmResponse | None:
    """Inspects/modifies the LLM request or skips the call."""
    agent_name = callback_context.agent_name
    #example_table = Part(text='[{"name": "Alice", "age": 30, "skill": 42}, {"name": "Bob", "age": 25, "skill": 55}, {"name": "Charlie", "age": 35, "skill": 20}]')  # Example table
    example_table = Part(text=pd.read_csv("sample.csv").to_json())
    if llm_request.contents[-1].parts[0].text is not None:
        llm_request.contents[-1].parts.append(example_table)
        print(f"[Callback] Added data table for agent: {agent_name}")
    return None

with open("test_case_agent/instructions.txt", "r", encoding="utf-8") as f:
    instructions = f.read()

root_agent = Agent(
    name="test_case_generation_agent",
    model=ROOT_AGENT_MODEL,
    description=(
        """This AI agent is a specialized data processor that transforms a data table into a single list of values 
        based on a command given in plain English. It reads a user's query, applies the specified calculation to each 
        row of the provided table, and outputs nothing but a clean JSON list of the results."""
    ),
    instruction=instructions,
    before_model_callback=table_adder,
)
