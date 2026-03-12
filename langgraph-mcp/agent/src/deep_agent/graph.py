"""LangGraph ReAct agent with MCP server tools
"""

from __future__ import annotations

import asyncio
import logging
import os

from deepagents import create_deep_agent
from dotenv import load_dotenv, dotenv_values
from deepagents.backends import FilesystemBackend
from langchain_ollama import ChatOllama
from datetime import datetime

from deep_agent.prompts import (
    RESEARCHER_INSTRUCTIONS,
    RESEARCH_WORKFLOW_INSTRUCTIONS,
    SUBAGENT_DELEGATION_INSTRUCTIONS,
    HOTEL_SEARCH_INSTRUCTIONS,
)
from deep_agent.tools import (
    internet_search,
    think_tool,
    get_mcp_tools,
)

# Load environment variables from the project's .env file (root of the agent package)
# Use override=True so values in .env take precedence over any existing env vars.
env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(env_path, override=True)

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def _build_system_prompt(tools: list) -> str:
    """Build system prompt based on shared prompts in prompts.py."""

    current_date = datetime.now().strftime("%Y-%m-%d")
    logger.info("Researcher instructions:\n%s", RESEARCHER_INSTRUCTIONS.format(date=current_date))

    INSTRUCTIONS = (
        RESEARCH_WORKFLOW_INSTRUCTIONS
        + "\n\n"
        + "=" * 80
        + "\n\n"
        + SUBAGENT_DELEGATION_INSTRUCTIONS.format(
            max_concurrent_research_units=3,
            max_researcher_iterations=3,
        )
    )

    return INSTRUCTIONS


def create_graph():
    """Create and configure the Deep agent graph.

    This function sets up:
    - Ollama LLM
    - MCP tools from the FastMCP server
    - Deep agent using create_deep_agent

    Returns:
        Compiled LangGraph agent.
    """
    logger.info("Initializing Deep agent with MCP tools...")

    # Load tools from MCP server first
    tools = asyncio.run(get_mcp_tools())

    # Add local tools (not served by MCP)
    tools.append(internet_search)
    tools.append(think_tool)

    current_date = datetime.now().strftime("%Y-%m-%d")

    research_sub_agent = {
        "name": "research-agent",
        "description": "Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
        "system_prompt": RESEARCHER_INSTRUCTIONS.format(date=current_date),
        "tools": [internet_search, think_tool],
    }

    hotel_search_sub_agent = {
        "name": "hotel-search-agent",
        "description": "Delegate hotel search to the sub-agent hotel searcher. Only give this hotel searcher one topic at a time.",
        "system_prompt": HOTEL_SEARCH_INSTRUCTIONS.format(date=current_date),
        "tools": [internet_search, think_tool],
    }

    # Build system prompt with tool information
    system_prompt = _build_system_prompt(tools)

    dotenv_vars = dotenv_values(env_path)

    ollama_api_key = (dotenv_vars.get("OLLAMA_API_KEY") or "").strip()

    if ollama_api_key.endswith("%"):
        ollama_api_key = ollama_api_key.rstrip("%\n \t").strip()

    if not ollama_api_key:
        raise RuntimeError("OLLAMA_API_KEY not found in .env. Please add a valid key to .env so the Ollama client can authenticate.")

    client_kwargs = {
        "headers": {"Authorization": f"Bearer {ollama_api_key}"},
    }

    model = ChatOllama(
        model="nemotron-3-super:cloud", #gpt-oss:120b-cloud, qwen3.5, deepseek-r1:14b, granite3.3, qwen3, gpt-oss:20b, qwen3:14b, qwen3:8b, ministral-3:14b
        temperature=0,
        context_window=262144,
        thiking=True,
        disable_streaming=False,
        client_kwargs=client_kwargs,
        validate_model_on_init=True,
    )
    logger.info("Initialized ChatOllama model...")

    # Create the Deep agent with MCP tools, system prompt, and sub-agent config
    agent = create_deep_agent( #create_agent
        model=model,
        tools=tools,
        system_prompt=system_prompt,
        subagents=[research_sub_agent, hotel_search_sub_agent],
        backend=FilesystemBackend(root_dir="./filesystem/",virtual_mode=True),
        debug=True,
        )
    logger.info("Deep agent created successfully")

    return agent


# Create the graph instance
try:
    graph = create_graph()
    logger.info("Deep Agent Graph compiled and ready")

except Exception as e:
    logger.error(f"Error creating graph: {e}")
    import traceback
    traceback.print_exc()