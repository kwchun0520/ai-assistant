from google.adk.agents import Agent
from pathlib import Path
from ai_assistant.utils import load_yaml
from google.adk.tools import google_search


prompt_config_path = Path(__file__).parent / "config.yaml"
CONFIG = load_yaml(prompt_config_path)

google_search_agent = Agent(
    name=CONFIG["name"],
    model=CONFIG["model"],
    description=CONFIG["descriptions"],
    tools=[google_search],
    instruction=CONFIG["instructions"],
)

__all__ = ["google_search_agent"]