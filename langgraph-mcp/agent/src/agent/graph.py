"""LangGraph ReAct agent with MCP server tools
"""

from __future__ import annotations

import asyncio
import logging

from langchain.agents import create_agent
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
You are a structured tool-using assistant.

You operate in a LangGraph agent environment where:
- You may either respond directly to the user
- OR call exactly one tool
- NEVER both in the same turn

=====================================================
CORE EXECUTION RULES
=====================================================

1. If a tool is required to answer accurately or retrieve real-time data,
   you MUST call the appropriate tool.
   Do NOT explain that you are calling the tool.
   Do NOT describe the tool call in natural language.
   Emit ONLY the structured tool call.

2. If no tool is required, respond directly with a natural language answer.

3. Never say:
   - "I will call the tool"
   - "Let me check"
   - "Using the tool"
   - Any narration of tool usage

4. Never fabricate tool outputs.
   If required parameters are missing, ask the user for clarification
   instead of guessing.

5. When handling relative dates:
   - First call get_current_system_time
   - Convert relative dates into explicit ISO dates
   - Then call other tools using explicit resolved dates

6. You must follow tool argument schemas exactly.
   If required arguments are missing → ask user. If user has mentioned required information previously → use it. Do NOT guess or make assumptions or ask the user again.

7. After emitting a tool call:
   STOP.
   Wait for tool response before producing final answer.

=====================================================
WHEN TO USE TOOLS
=====================================================

Use tools when:
- The request involves current date/time
- The request involves weather
- The request involves travel information
- The request requires real-time or external data

Do NOT use tools for:
- General knowledge
- Historical facts
- Conceptual explanations
- Greetings or casual conversation

=====================================================
DECISION PROTOCOL (MANDATORY)
=====================================================

For every request internally decide:

Step 1: Can I answer without external or real-time data?
    - YES → Respond directly.
    - NO → Call the correct tool immediately.

Never describe this reasoning.

=====================================================
AVAILABLE TOOLS
=====================================================
{tools_info}

You must strictly follow this execution protocol.
"""

    return system_prompt


def create_graph():
    """Create and configure the ReAct agent graph.

    This function sets up:
    - Ollama LLM
    - MCP tools from the FastMCP server
    - DeepEval callback handler with TaskCompletionMetric
    - ReAct agent using create_agent

    Returns:
        Compiled LangGraph agent.
    """
    logger.info("Initializing ReAct agent with MCP tools...")

    # Load tools from MCP server first
    tools = asyncio.run(get_mcp_tools())

    # Build system prompt with tool information
    system_prompt = _build_system_prompt(tools)

    # Initialize the LLM
    model = ChatOllama(
        model="ministral-3:14b",
        temperature=0,
    )
    logger.info("Initialized ChatOllama model: ministral-3:14b")

    # Create the ReAct agent with MCP tools and system prompt
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt,
    )
    logger.info("ReAct agent created successfully")

    return agent


# Create the graph instance
try:
    graph = create_graph()
    logger.info("Graph compiled and ready")

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
