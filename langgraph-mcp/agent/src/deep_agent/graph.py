"""LangGraph ReAct agent with MCP server tools
"""

from __future__ import annotations

import asyncio
import logging

from deepagents import create_deep_agent
from langchain.agents import create_agent
from deepagents.backends import FilesystemBackend
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def get_mcp_tools():
    """Load tools from the MCP server.

    Returns:
        List of LangChain-compatible tools from the MCP server.
    """
    logger.info("Connecting to MCP server at http://localhost:8000/mcp")

    # Configure MCP client to connect to local FastMCP server
    client = MultiServerMCPClient({
        "langgraph-mcp-server": {
            "url": "http://localhost:8000/mcp",
            "transport": "http",
        }
    })

    # Get tools from the MCP server
    tools = await client.get_tools()
    logger.info(f"Loaded {len(tools)} tools from MCP server: {[tool.name for tool in tools]}")

    return tools


def _build_system_prompt(tools: list) -> str:
    """Build dynamic system prompt with available tools and their signatures."""

    tools_info = ""
    if tools:
        tools_info = "\n\nAVAILABLE TOOLS:\n"
        for tool in tools:
            tool_name = tool.name
            tool_description = tool.description or "No description available"
            tools_info += f"\n- {tool_name}: {tool_description}"
    else:
        tools_info = "\n\nNo tools currently available."

    system_prompt = f"""
                    You are a helpful assistant that can use the following tools to answer user queries.
                    {tools}
                    """

    return system_prompt


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

    # Build system prompt with tool information
    system_prompt = _build_system_prompt(tools)

    # Initialize the LLM
    model = ChatOllama(
        model="ministral-3:14b", #qwen3:8b
        temperature=0,
    )
    logger.info("Initialized ChatOllama model...")

    # Create the Deep agent with MCP tools and system prompt
    agent = create_deep_agent( #create_agent
        model=model,
        tools=tools,
        system_prompt=system_prompt,
        backend=FilesystemBackend(root_dir="/Users/kunalpatil/genai-playground/langraph-code-examples/langgraph-mcp/agent/filesystem/",virtual_mode=True),
        debug=True,
    )
    logger.info("Deep agent created successfully")

    return agent


# Create the graph instance
try:
    graph = create_graph()
    logger.info("Deep AgentGraph compiled and ready")

except Exception as e:
    logger.error(f"Error creating graph: {e}")
    import traceback
    traceback.print_exc()

    # Fallback: create a simple agent without MCP tools if connection fails
    logger.warning("Creating fallback agent without MCP tools")
    model = ChatOllama(model="llama3.1")
    graph = create_agent(
        model=model,
        tools=[],  # Empty tools list as fallback
    )
