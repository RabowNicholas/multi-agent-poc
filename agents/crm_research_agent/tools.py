def fetch_mock_crm_history(contact_name: str) -> dict:
    """
    Simulates CRM history retrieval. Returns a JSON-RPC 2.0 response object.
    """
    return {
        "jsonrpc": "2.0",
        "result": {
            "contact_name": contact_name,
            "interactions": [
                {"date": "2025-05-20", "type": "email", "note": "Initial outreach"},
                {"date": "2025-05-25", "type": "call", "note": "Follow-up on proposal"},
            ],
        },
        "id": "mock-id",
    }
