import json
from typing import Any

import pandas as pd
from google.adk.agents import Agent, SequentialAgent, ParallelAgent
from google.adk.tools import FunctionTool
from google.adk.tools.agent_tool import AgentTool

from config import ROOT_AGENT_MODEL
from pd_agent.agent import root_agent as pandas_agent
from test_case_agent.agent import root_agent as test_agent
from validation_agent.agent import root_agent as validation_agent

def evaluate_code(code_string: str, result_json_string: str) -> dict[str, Any]:
    """Takes code_string and applies it to the sample dataframe. Then it compares this result to the expected result.

    Returns:
        dict: A dict showing if the result of applying code_string to a df is the same as expected based on result_json_string.
    """
    df = pd.read_csv("sample.csv")
    result = None
    eval(code_string)

    result_json = json.loads(result_json_string)
    return {"status": "success" if result_json == result else "error"}


with open("root_agent/instructions.txt", "r", encoding="utf-8") as f:
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
    #tools=[
        #AgentTool(agent=pandas_agent, skip_summarization=True),
        #AgentTool(agent=test_agent, skip_summarization=True),
        #AgentTool(agent=validation_agent, skip_summarization=True),
    #],
    sub_agents=[
        SequentialAgent(
            name="sequential_agent",
            sub_agents=[        
                ParallelAgent(
                    name="ResearchAndSynthesisPipeline",
                    sub_agents=[pandas_agent, test_agent],
                    description="Coordinates the generation of code and research and synthesizes the results.",
                ),
                validation_agent,
            ]
        )
    ],
)
#flash-preview-05-20