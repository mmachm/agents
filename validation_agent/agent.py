import json
from typing import Any

import pandas as pd
import numpy as np
from google.adk.agents import Agent

from config import SUB_AGENT_MODEL


def tester(code_string: str, result_json_string: str, column_name: str) -> dict[str, Any]:
    """Takes code_string and uses it to add a column to a DataFrame df. Then it compares this result to the expected result.
    Args:
        code_string (str): A string containing Python code that adds a new column to the DataFrame df.
        result_json_string (str): A JSON string representing the expected result of applying code_string to df.
        column_name (str): The name of the column that is being added to the DataFrame.

    Returns:
        dict: A dict showing if the result of applying code_string to a df is the same as expected based on result_json_string.
    """
    df = pd.read_csv("sample.csv")
    try:
        code_string = code_string.replace("\\n", "\n")  # Ensure newlines are correctly interpreted
        # Execute the code string to add a new column to the DataFrame
        exec(code_string)
        result = df[column_name].tolist()
    except Exception as e:
        return {"status": "error", "message": "Execution error: " + str(e)}
    try:
        result_json = json.loads(result_json_string)
        if len(result_json) != len(result):
            return {
                "status": "error",
                "message": f"Length mismatch: expected {len(result)}, given list had {len(result_json)}"
            }
        for i, (test_case, generated) in enumerate(zip(result_json, result)):
            if str(test_case) == str(generated):
                continue
            # extra check for numeric values
            if test_case is None:
                test_case = "nan"
            if generated is None:
                generated = "nan"
            try:
                tc_float = float(test_case)
                gen_float = float(generated)
                if np.isnan(tc_float) and np.isnan(gen_float):
                    continue
                if abs(tc_float - gen_float) < 1e-6:
                    continue
                return {
                "status": "error",
                "message": f"Number mismatch at position {i}: code gave {gen_float}, but the result_json_string had {tc_float}."
                }
            except Exception as e:
                # If conversion to float fails, treat as a non-numeric comparison
                return {
                    "status": "error",
                    "message": f"Data mismatch at position {i}: code gave {generated}, but the result_json_string had {test_case}."
                }
    except json.JSONDecodeError as e:
        return {"status": "error", "message": "JSON parsing error: " + str(e)}
    # all looks OK, save the code and return success
    with open(f"df_code_snippets/{column_name}.py", "w") as f:
        f.write(code_string)
    return {"status": "success"}


with open("validation_agent/instructions.txt", "r", encoding="utf-8") as f:
    instructions = f.read()


root_agent = Agent(
    name="validation_agent",
    model=SUB_AGENT_MODEL,
    description=(
        "This agent validates consistency of the given code and then runs a tester tool that checks if the code produces the expected results."
    ),
    instruction=instructions,
    tools=[tester],
)

