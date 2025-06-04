import pytest
from agent_registry import AgentRegistry
from agents.web_research_agent.agent import WebResearchAgent
from agents.crm_research_agent.agent import CRMResearchAgent


@pytest.fixture
def registry():
    card_paths = [
        "agent_cards/web_research_agent_card.json",
        "agent_cards/crm_research_agent_card.json",
    ]
    return AgentRegistry.from_card_paths(card_paths)


def test_find_agent_for_web_research(registry):
    agent = registry.find_agent_for_method("get_company_news")
    assert isinstance(agent, WebResearchAgent)


def test_find_agent_for_crm_research(registry):
    agent = registry.find_agent_for_method("get_crm_history")
    assert isinstance(agent, CRMResearchAgent)


def test_unknown_method_returns_none(registry):
    agent = registry.find_agent_for_method("unknown_method")
    assert agent is None
