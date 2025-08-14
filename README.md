# AI Assistant

An intelligent assistant built with Google's Agent Development Kit (ADK) featuring a multi-agent architecture to handle complex tasks.

## Overview

This AI Assistant leverages a hierarchical agent structure to break down complex queries into manageable subtasks. The system uses specialized subagents for different capabilities:

- **Root Agent**: Orchestrates task delegation and response synthesis
- **Google Search Agent**: Performs web searches to retrieve relevant information
- **Summarization Agent**: Condenses and formats information for concise responses
- **Image Agent**: Handles image-related tasks (generation/processing)

## Features

- Multi-agent architecture for specialized task handling
- Google Search integration for real-time information retrieval
- Natural language understanding and response generation
- Modular design for easy extension with new capabilities

## Setup

### Prerequisites

- Python 3.9+
- API keys for Google services
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-assistant.git
   cd ai-assistant
   ```

2. Create and activate a virtual environment with uv:
   ```bash
   uv venv
   source .venv/bin/activate  # macOS/Linux
   # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies (from pyproject.toml):
   ```bash
   uv sync --force
   ```

4. Create a `.env` file with your API keys:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

### Run from the CLI (adk run)

- Interactive session:
    ```bash
    adk run --config config.yaml
    ```
    Then type a prompt, for example:
    ```
    What are the latest developments in AI?
    ```

- One‑off prompt:
    ```bash
    adk run --config config.yaml --prompt "What are the latest developments in AI?"
    ```

Guide:
1) Ensure required env vars are set (e.g., GOOGLE_API_KEY).
2) From the project root, run one of the commands above.
3) Review streamed tool output and final answer in the terminal.

### Launch the Web UI (adk web)

- Start a local chat UI:
    ```bash
    adk web --config config.yaml --host 127.0.0.1 --port 3000
    ```
    Open http://127.0.0.1:3000 and chat with the assistant.

Guide:
1) Verify config.yaml points to your root agent and tools.
2) Start the server with adk web.
3) Use the browser UI to send prompts and view results.

## Project Structure

```
ai_assistant/
├── __init__.py
├── agent.py                # Root agent definition
├── config.yaml             # Main configuration
├── subagents/
│   ├── __init__.py
│   ├── google_search_agent/
│   │   ├── __init__.py
│   │   ├── tools.py        # Tool definitions for this agent (e.g., google_search)
│   │   ├── agent.py        # Google search agent (imports from tools.py)
│   │   └── config.yaml
│   ├── summarization_agent/
│   │   ├── __init__.py
│   │   ├── tools.py        # Optional: tools specific to summarization
│   │   ├── agent.py
│   │   └── config.yaml
│   ├── image_agent/
│   │   ├── __init__.py
│   │   ├── tools.py        # Optional: image tools
│   │   ├── agent.py
│   │   └── config.yaml
└── utils.py
```

## Tools per subagent

Keep each subagent’s tools in a local `tools.py` and import them in that agent’s `agent.py`.

Example (google_search_agent):

```python
# filepath: ai_assistant/subagents/google_search_agent/tools.py
from google.adk.tools import google_search

__all__ = ["google_search"]
```

```python
# filepath: ai_assistant/subagents/google_search_agent/agent.py
from pathlib import Path
from google.adk.agents import Agent
from .tools import google_search
from ai_assistant.utils import load_yaml

CONFIG = load_yaml(Path(__file__).parent / "config.yaml")

google_search_agent = Agent(
    name=CONFIG["name"],
    model=CONFIG["model"],
    description=CONFIG["descriptions"],
    tools=[google_search],  # imported from tools.py
    instruction=CONFIG["instructions"],
)
```

Root agent composition (wrap an agent as a tool if desired):

```python
# filepath: ai_assistant/agent.py
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from ai_assistant.subagents.google_search_agent.agent import google_search_agent
from ai_assistant.subagents.summarization_agent.agent import summarization_agent
from ai_assistant.subagents.image_agent.agent import image_agent
from ai_assistant.utils import load_yaml
from pathlib import Path

CONFIG = load_yaml(Path(__file__).parent / "config.yaml")

root_agent = Agent(
    name=CONFIG["name"],
    model=CONFIG["model"],
    description=CONFIG["descriptions"],
    sub_agents=[summarization_agent, image_agent],
    tools=[AgentTool(agent=google_search_agent)],
    instruction=CONFIG["instructions"],
)
```

## Configuration

Each agent can be configured via its respective `config.yaml` file:

- `model`: Specifies which model to use (ensure tool support if using tools)
- `name`: Agent identifier
- `descriptions`: Agent's role and capabilities
- `instructions`: Specific guidance for the agent

## Troubleshooting

- Import errors (module has no attribute 'name'):
  - Import the agent instance directly:
    ```python
    from ai_assistant.subagents.google_search_agent.agent import google_search_agent
    ```
- Validation error for sub_agents:
  - Ensure `sub_agents` contains agent instances, not modules:
    ```python
    from ai_assistant.subagents.summarization_agent.agent import summarization_agent
    ```
- Tool use errors:
  - Use a model that supports tools per ADK docs; function calling support alone may be insufficient.
- uv environment:
  - If packages don’t install, re-run:
    ```bash
    uv sync --force
    ```

## License

[Add your license information here]