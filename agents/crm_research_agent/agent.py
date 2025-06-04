from protocol.base_agent import BaseAgent
from .tools import fetch_mock_crm_history


class CRMResearchAgent(BaseAgent):
    """
    Specialized agent for handling CRM-related tasks.

    This agent supports the 'get_crm_history' method, which retrieves simulated CRM interaction history
    for a given contact.
    """

    def __init__(self):
        super().__init__(tool_layer=fetch_mock_crm_history)

    def get_supported_methods(self):
        return {"get_crm_history": self.get_crm_history}

    def get_crm_history(self, params: dict) -> dict:
        """
        Handles the 'get_crm_history' method.

        Expects a 'contact_name' parameter in the input dictionary.
        Returns mock CRM interaction data for the specified contact by calling the injected tool layer.

        Raises:
            ValueError: If 'contact_name' is not provided in params.
        """
        contact_name = params.get("contact_name")
        if not contact_name:
            raise ValueError("Missing 'contact_name' parameter.")
        return self.tool_layer(contact_name)
