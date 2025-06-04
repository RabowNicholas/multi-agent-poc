from protocol.base_agent import BaseAgent
from .tools import fetch_mock_articles


class WebResearchAgent(BaseAgent):
    """
    Specialized agent for handling web-based research tasks.

    This agent supports the 'get_company_news' method, which fetches simulated recent news articles
    for a specified company.
    """

    def __init__(self):
        super().__init__(tool_layer=fetch_mock_articles)

    def get_supported_methods(self):
        return {"get_company_news": self.get_company_news}

    def get_company_news(self, params: dict) -> dict:
        """
        Handles the 'get_company_news' method.

        Expects a 'company_name' parameter in the input dictionary.
        Returns mock news article data for the specified company using the injected tool layer.

        Raises:
            ValueError: If 'company_name' is not provided in params.
        """
        company_name = params.get("company_name")
        if not company_name:
            raise ValueError("Missing 'company_name' parameter.")
        articles = self.tool_layer(company_name)
        return {"articles": articles}
