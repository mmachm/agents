import json
from typing import Any

import pandas as pd
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from config import SUB_AGENT_MODEL, ROOT_AGENT_MODEL


def evaluate_code(code_string: str, result_json_string: str) -> dict[str, Any]:
    """Takes code_string and applies it to the sample dataframe. Then it compares this result to the expected result.

    Returns:
        dict: A dict showing if the result of applying code_string to a df is the same as expected based on result_json_string.
    """
    df = pd.read_csv("sample.csv")
    result = None
    eval(code_string)

    result_json = json.loads(result_json_string)
    return {"status": "success" if result_json == result else f"error got {result} expected {result_json}"}


with open("validation_agent/instructions.txt", "r", encoding="utf-8") as f:
    instructions = f.read()

root_agent = Agent(
    name="validation_agent",
    model=ROOT_AGENT_MODEL,
    description=(
        #"""
        #This agent validates that a given string of Python code produces an output identical to a provided JSON 
        #list of values. It executes the code, compares the result to the JSON content, and confirms if they match.
        #"""
        "this agent provides validation that you are on the right track"
    ),
    instruction=instructions,
    #tools=[FunctionTool(func=evaluate_code)],
)

