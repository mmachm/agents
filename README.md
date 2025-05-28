# Hackathon Agent Team Starter (ADK) 🚀

Welcome to the Hackathon Agent Team Starter project! This template provides a robust foundation for building multi-agent systems using the **Google Agent Development Kit (ADK)**. It features a central **Coordinator Agent** that intelligently delegates tasks to specialized sub-agents for greetings, farewells (including current time), and weather information.

This project is designed to help participants in **[Your Hackathon Name/Event - e.g., AI Innovators 2025]** hit the ground running with ADK and focus on creating innovative agent functionalities.

## ✨ Core Functionality at a Glance

The pre-built agent team demonstrates key ADK concepts:

* **Coordinator Agent (`WeatherAgentTeam`):**
    * Acts as the primary interface for user queries.
    * **Delegates** greetings to the `GreetingAgent`.
    * **Delegates** farewells (which includes telling the time) to the `FarewellAgent`.
    * Handles weather information requests **directly** using its own `get_weather` tool.
    * Provides a polite "cannot handle" response for out-of-scope queries.
* **Specialist Agents (Sub-Agents):**
    * `GreetingAgent`: Offers a friendly welcome.
    * `FarewellAgent`: Provides a polite goodbye and uses its `get_current_local_time_tool` to state the current time (defaults to UTC if not specified).
* **Tools:**
    * `get_weather`: A demonstration tool (currently mock data) to fetch weather information for a city. *Hackathon idea: Make this call a real weather API!*
    * `get_current_local_time_tool`: A tool to fetch the current time, utilized by the `FarewellAgent`.

## 🛠️ Project Structure Highlights

Understanding this structure will help you extend the project:

* **`config.py`**: config file with LLM model names (configurable via environment variables) and application constants.
* **`tools/`**: Directory for all tool definitions.
    * `get_weather.py`, `get_current_time.py`: Individual tool files. Add new tool files here!
* **`agents/`**: Directory for agent definitions.
    * `agents.py`: Defines `GreetingAgent`, `FarewellAgent`. Add more specialists here!
    * `root_agent.py`: Defines the `WeatherAgentTeam` (root/orchestrator). Modify its `instruction` to integrate new sub-agents.
* **`core/`**: Contains core application logic.
    * `interaction_handler.py`: Manages a single turn of agent interaction (`call_agent_turn`).
    * `services.py`: Initializes shared services like `InMemorySessionService`.
* **`app_main.py`**: The main executable script to run the agent team and interact via the command line.
* **`.env.example`**: Template for your `.env` file (for API keys and secrets).

## 📋 Prerequisites

* Python (>=3.10 recommended,`pyproject.toml` specifies >=3.12)
* An active API Key from a supported LLM provider (e.g., Google AI Studio for Gemini models).


## 🚀 Quick Start & Setup

1.  **Clone the Repository:**
    ```bash
    git clone [your-repository-url]
    cd agents
    ```

2.  **Set up Virtual Environment & Install Dependencies:**
    (We assume you are using `uv` as per your example, but `pip` is also common.)
    ```bash
    uv sync
    ```

3.  **Configure Environment Variables:**
    * Copy `.env.example` to `.env`: `cp .env.example .env`
    * **Edit `.env`** and add your actual API keys. This file is in `.gitignore` and should NOT be committed.
        ```env
        # .env
        ADK_AGENT_LLM_MODEL="gemini-2.0-flash"
        ADK_ROOT_AGENT_LLM_MODEL="gemini-2.0-flash"
        GOOGLE_API_KEY="YOUR_ACTUAL_GOOGLE_AI_API_KEY"
        GOOGLE_GENAI_USE_VERTEXAI="False" # Important for Google AI Studio keys
        ```

4.  **Run the Application:**
    ```bash
    python app_main.py
    ```

## 💬 How to Interact

Once running, the application will prompt for your input. Try these:

* `Hello`
* `What is the weather like in London?`
* `How about Dublin?`
* `What's the capital of Ireland?` (Tests out-of-scope handling)
* `Goodbye`
* `OK see you, tell me the current UTC time as you say bye.`

Type `quit` or `exit` to stop.

## 💡 Extending for the Hackathon (Your Playground!)

This starter is designed for easy extension. Here's how to add your own magic:

* **✨ Add New Tools:**
    1.  Create your tool function in a new `.py` file within the `tools/` directory (e.g., `tools/my_amazing_tool.py`).
    2.  **Crucial:** Provide a clear docstring and type hints for your function. ADK uses these to inform the LLM.
    3.  Import and export your tool in `tools/__init__.py`.
* **🤖 Create New Specialist Agents:**
    1.  Define your new `Agent` in `agents/agents.py` or a new file (e.g., `agents/my_new_agent.py`).
    2.  Import necessary tools and assign them to your agent's `tools` list.
    3.  Craft a clear `instruction` prompt for your agent, telling it its purpose and how to use its tools.
* **🔗 Integrate New Agents into the Coordinator:**
    1.  Import your new specialist agent into `agents/root_agent.py`.
    2.  Add your agent instance to the `sub_agents` list when defining `WeatherAgentTeam`.
    3.  **Most Importantly:** Update the `instruction` of `WeatherAgentTeam` to teach it:
        * What your new sub-agent does.
        * When to delegate to it.
        * What parameters (if any) need to be extracted from the user query and passed to the sub-agent.
* **🧠 Experiment with LLM Models:**
    * Adjust model names in `config.py` (which reads from environment variables like `ADK_ROOT_AGENT_LLM_MODEL`, `ADK_SUB_AGENT_LLM_MODEL`). Try different models for different roles!
    * To list available Google AI models (replace `YOUR_API_KEY`):
        ```bash
        curl "[https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_API_KEY](https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_API_KEY)"
        ```

## ⁉️ Troubleshooting Common Issues

* **`ModuleNotFoundError` (e.g., for `google.adk`):**
    * Ensure your virtual environment is activated.
    * Verify `google-adk` is installed in that environment (`uv pip list | grep google-adk`).


* **`ValueError: Missing key inputs argument!...` (API Key issues):**
    * Double-check your `.env` file has the correct API key under the right variable name (e.g., `GOOGLE_API_KEY`).
    * Ensure `GOOGLE_GENAI_USE_VERTEXAI="False"` is set in your `.env` if using Google AI Studio API keys.


* **Tool Schema Errors / Agent Not Using Tool Correctly:**
    * **Simplify Tool Signatures:** ADK's automatic schema generation works best with basic type hints (e.g., `str`, `float`, `bool`). Avoid `Optional[str]=None` or default values in function signatures that the LLM needs to understand.
    * **Clear Agent Instructions:** The agent's `instruction` prompt must clearly state when and how to use a tool, including all required parameters and how the LLM should derive them (e.g., "If the user doesn't specify a timezone for `get_current_local_time_tool`, you MUST pass 'UTC' as the `time_zone` parameter.").
