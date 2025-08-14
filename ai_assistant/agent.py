from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from ai_assistant.subagents import (google_search_agent, image_agent,
                                    summarization_agent)
from ai_assistant.utils import load_yaml

load_dotenv()

prompt_config_path = Path(__file__).parent / "config.yaml"
CONFIG = load_yaml(prompt_config_path)

root_agent = Agent(
    name=CONFIG["name"],
    model=CONFIG["model"],
    description=CONFIG["descriptions"],
    sub_agents=[
        summarization_agent,
        image_agent,
    ],
    tools=[AgentTool(agent=google_search_agent)],
    instruction=CONFIG["instructions"]
)