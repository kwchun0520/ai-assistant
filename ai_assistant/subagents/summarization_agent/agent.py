from pathlib import Path

from google.adk.agents import Agent

from ai_assistant.subagents.summarization_agent.tools import (
    load_text_tool, load_weblink_tool,
    summarize_document_tool)
from ai_assistant.utils import load_yaml

prompt_config_path = Path(__file__).parent / "config.yaml"
CONFIG = load_yaml(prompt_config_path)


summarization_agent = Agent(
    name=CONFIG["name"],
    model=CONFIG["model"],
    description=CONFIG["description"],
    instruction=CONFIG["instruction"],
    tools=[
        load_text_tool,
        load_weblink_tool,
        summarize_document_tool
    ]
)

__all__ = ["summarization_agent"]