import pytest
from langchain_core.messages import HumanMessage

from agent import graph

pytestmark = pytest.mark.anyio


@pytest.mark.langsmith
async def test_agent_simple_passthrough() -> None:
    inputs = {"messages": [HumanMessage(content="Hello, what is 2+2?")]}
    res = await graph.ainvoke(inputs)
    assert res is not None
    assert "messages" in res
    assert len(res["messages"]) > 1
