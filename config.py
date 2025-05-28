import os

DEFAULT_AGENT_MODEL = "gemini-2.0-flash"
SUB_AGENT_MODEL = os.getenv("ADK_AGENT_LLM_MODEL", DEFAULT_AGENT_MODEL)
ROOT_AGENT_MODEL = os.getenv("ADK_ROOT_AGENT_LLM_MODEL", DEFAULT_AGENT_MODEL)


APP_NAME = "HackathonApp"
DEFAULT_USER_ID = "hackathon_user"
DEFAULT_SESSION_ID_PREFIX = "hackathon_session_"


print(f"[Config] Root Agent Model: {ROOT_AGENT_MODEL}")
print(f"[Config] Sub-Agent Model: {SUB_AGENT_MODEL}")
