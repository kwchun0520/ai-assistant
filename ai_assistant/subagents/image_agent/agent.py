from pathlib import Path

from google.adk.agents import Agent

from ai_assistant.subagents.image_agent.tools import (enhance_prompt_tool,
                                                      generate_image_tool)
from ai_assistant.utils import load_yaml

prompt_config_path = Path(__file__).parent / "config.yaml"
CONFIG = load_yaml(prompt_config_path)


image_agent = Agent(
    name=CONFIG["name"],
    model=CONFIG["model"],
    description=CONFIG["descriptions"],
    instruction=CONFIG["instructions"],
    tools=[enhance_prompt_tool,
           generate_image_tool]
)

__all__ = ["image_agent"]