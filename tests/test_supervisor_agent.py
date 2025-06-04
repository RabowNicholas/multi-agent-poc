"""
Unit tests for the SupervisorAgent class.

These tests verify multi-task parsing, task delegation, JSON-RPC 2.0 compliance,
timeout handling, and error responses when no agent is found.
"""

from unittest.mock import MagicMock
import asyncio
import pytest
from agents.supervisor_agent import SupervisorAgent
from agent_registry import AgentRegistry


@pytest.fixture
def mock_agent():
    """Mock agent for testing"""

    class MockAgent:
        async def handle_rpc(self, task):
            return {
                "jsonrpc": "2.0",
                "result": {"mocked": True},
                "id": "123",
            }

    return MockAgent()


@pytest.fixture
def registry_with_mock_agent(mock_agent):
    """Agent Registry with Mock Agent for testing"""
    registry = AgentRegistry.from_card_paths([])
    registry.find_agent_for_method = MagicMock(return_value=mock_agent)
    return registry


@pytest.mark.asyncio
async def test_parse_query_multi_task():
    """Parses a query into multiple JSON-RPC tasks."""
    sa = SupervisorAgent(agent_registry=MagicMock())
    query = "Find recent company news about Acme Inc. and pull CRM history for John Doe"
    tasks = sa.parse_query(query)
    assert len(tasks) == 2
    assert all(task["jsonrpc"] == "2.0" for task in tasks)


@pytest.mark.asyncio
async def test_handle_query_success(registry_with_mock_agent):
    """Delegates tasks and returns successful JSON-RPC responses."""
    sa = SupervisorAgent(agent_registry=registry_with_mock_agent)
    query = "company news about Company and crm history for Jane A. Smith"
    responses = await sa.handle_query(query)
    assert len(responses) == 2
    for resp in responses:
        assert resp["jsonrpc"] == "2.0"
        assert "result" in resp


@pytest.mark.asyncio
async def test_delegate_task_timeout():
    """Returns timeout error if agent takes too long to respond."""

    class SlowAgent:
        """Class to simulate a timeout"""

        async def handle_rpc(self, task):
            """Waits for 5 seconds"""
            await asyncio.sleep(5)

    slow_agent = SlowAgent()
    registry = AgentRegistry.from_card_paths([])
    registry.find_agent_for_method = MagicMock(return_value=slow_agent)
    sa = SupervisorAgent(agent_registry=registry)

    task = {
        "jsonrpc": "2.0",
        "method": "get_crm_history",
        "params": {"contact_name": "John"},
        "id": "abc",
    }

    result = await sa.delegate_task(task, timeout=0.1)
    assert result["jsonrpc"] == "2.0"
    assert "error" in result
    assert result["error"]["code"] == -32001


@pytest.mark.asyncio
async def test_delegate_task_invalid_method():
    """Returns method not found error for unknown task."""
    registry = AgentRegistry.from_card_paths([])
    registry.find_agent_for_method = MagicMock(return_value=None)
    sa = SupervisorAgent(agent_registry=registry)

    task = {"jsonrpc": "2.0", "method": "unknown_method", "params": {}, "id": "xyz"}

    result = await sa.delegate_task(task)
    assert result["jsonrpc"] == "2.0"
    assert result["error"]["code"] == -32601


@pytest.mark.asyncio
async def test_parse_query_with_no_task_matches():
    """Returns empty list when no known task is detected."""
    sa = SupervisorAgent(agent_registry=MagicMock())
    query = "Hello world"
    tasks = sa.parse_query(query)
    assert tasks == []


@pytest.mark.asyncio
async def test_extract_company_name_single_word():
    """Extracts single-word company name correctly."""
    sa = SupervisorAgent(agent_registry=MagicMock())
    query = "Find recent company news about Tesla"
    company = sa.extract_company_name(query)
    assert company == "Tesla"


@pytest.mark.asyncio
async def test_extract_company_name_with_and_delimiter():
    """Stops extraction at 'and' when extracting company name."""
    sa = SupervisorAgent(agent_registry=MagicMock())
    query = "Find news about Acme Inc. and CRM history for John Doe"
    company = sa.extract_company_name(query)
    assert company == "Acme Inc."


@pytest.mark.asyncio
async def test_extract_contact_name_single_name():
    """Extracts contact name correctly."""
    sa = SupervisorAgent(agent_registry=MagicMock())
    query = "Get CRM history for John Doe"
    contact = sa.extract_contact_name(query)
    assert contact == "John Doe"
