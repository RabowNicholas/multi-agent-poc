import pytest
from agents.crm_research_agent.agent import CRMResearchAgent


def test_get_supported_methods():
    """Ensures supported method is correctly registered."""
    agent = CRMResearchAgent()
    methods = agent.get_supported_methods()
    assert "get_crm_history" in methods
    assert callable(methods["get_crm_history"])


def test_get_crm_history_valid_input():
    """Valid input returns expected mock CRM data."""
    agent = CRMResearchAgent()
    params = {"contact_name": "Jane Smith"}
    result = agent.get_crm_history(params)
    assert result["contact"] == "Jane Smith"
    assert isinstance(result["interactions"], list)
    assert all(
        "date" in i and "type" in i and "note" in i for i in result["interactions"]
    )


def test_get_crm_history_missing_param():
    """Missing contact_name param raises ValueError."""
    agent = CRMResearchAgent()
    with pytest.raises(ValueError, match="Missing 'contact_name' parameter."):
        agent.get_crm_history({})
