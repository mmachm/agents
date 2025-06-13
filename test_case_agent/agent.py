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

with open("pd_agent/instructions.txt", "r", encoding="utf-8") as f:
    instructions = f.read()

test_agent = Agent(
    name="test_case_generation_agent",
    model=ROOT_AGENT_MODEL,
    description=(
        "Agent that processes data from a given table into a new column based on a query given in natural language."
    ),
    instruction=instructions,
    before_model_callback=table_adder,
)
