def fetch_mock_articles(company_name: str) -> dict:
    """
    Simulates news article retrieval. Returns a JSON-RPC 2.0 response object.
    """
    return {
        "jsonrpc": "2.0",
        "result": {
            "company_name": company_name,
            "articles": [
                {
                    "title": f"{company_name} announces new AI initiative",
                    "date": "2025-06-01",
                },
                {
                    "title": f"{company_name} Q2 earnings exceed expectations",
                    "date": "2025-06-03",
                },
            ],
        },
        "id": "mock-id",
    }
