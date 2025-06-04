def fetch_mock_crm_history(contact_name: str) -> dict:
    """
    This function simulates the CRM tool layer for the agent using dependency injection.
    It aligns with MCP design goals by separating domain logic from data access and enables testability.
    """
    return {
        "contact": contact_name,
        "interactions": [
            {"date": "2025-05-20", "type": "email", "note": "Initial outreach"},
            {"date": "2025-05-25", "type": "call", "note": "Follow-up on proposal"},
        ],
    }
