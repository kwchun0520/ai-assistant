from google.adk.agents import Agent
from ai_assistant.utils import load_yaml
from pathlib import Path


prompt_config_path = Path(__file__).parent / "config.yaml"
CONFIG = load_yaml(prompt_config_path)


summarization_agent = Agent(
    name=CONFIG["name"],
    model=CONFIG["model"],
    description=CONFIG["descriptions"],
    instruction=CONFIG["instructions"],
)

__all__ = ["summarization_agent"]