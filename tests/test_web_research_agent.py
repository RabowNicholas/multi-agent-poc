import pytest
from agents.web_research_agent.agent import WebResearchAgent


def test_get_supported_methods():
    """Ensures supported method is correctly registered."""
    agent = WebResearchAgent()
    methods = agent.get_supported_methods()
    assert "get_company_news" in methods
    assert callable(methods["get_company_news"])


def test_get_company_news_valid_input():
    """Valid input returns expected mock news articles."""
    agent = WebResearchAgent()
    params = {"company_name": "Acme Inc"}
    result = agent.get_company_news(params)
    assert isinstance(result["articles"], list)
    assert all("title" in a and "date" in a for a in result["articles"])


def test_get_company_news_missing_param():
    """Missing company_name param raises ValueError."""
    agent = WebResearchAgent()
    with pytest.raises(ValueError, match="Missing 'company_name' parameter."):
        agent.get_company_news({})
