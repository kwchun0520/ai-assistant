# AI Assistant

An intelligent assistant built with Google's Agent Development Kit (ADK) featuring a multi-agent architecture to handle complex tasks.

## Overview

This AI Assistant leverages a hierarchical agent structure to break down complex queries into manageable subtasks. The system uses specialized subagents for different capabilities:

- **Root Agent**: Orchestrates task delegation and response synthesis
- **Google Search Agent**: Performs web searches to retrieve relevant information
- **Summarization Agent**: Condenses and formats information for concise responses

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
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   uv sync
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
├── __init__.py             # Package init
├── agent.py                # Root agent definition
├── config.yaml             # Main configuration
├── subagents/
│   ├── __init__.py         # Subpackage init
│   ├── google_search_agent/
│   │   ├── __init__.py     # Subpackage init
│   │   ├── agent.py        # Google search agent
│   │   └── config.yaml     # Search agent configuration
│   ├── summarization_agent/
│   │   ├── __init__.py     # Subpackage init
│   │   ├── agent.py        # Summarization agent
│   │   └── config.yaml     # Summarization agent configuration
└── utils.py                # Utility functions
```

## Configuration

Each agent can be configured via its respective `config.yaml` file:

- `model`: Specifies which Gemini model to use
- `name`: Agent identifier
- `descriptions`: Agent's role and capabilities
- `instructions`: Specific guidance for the agent

## Extending

Add new subagents by:

1. Creating a new directory under `subagents/`
2. Implementing an agent definition and configuration
3. Importing and adding to the root agent

## Troubleshooting

- **Tool use errors**: Ensure the model specified in config supports tool use (e.g., gemini-1.5-pro-latest)
- **Import errors**: Check that agent instances are imported correctly from their modules

## License