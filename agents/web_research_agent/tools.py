def fetch_mock_articles(company_name: str) -> list[dict]:
    """
    This function simulates the Tool layer for the agent using dependency injection.
    """
    return [
        {"title": f"{company_name} announces new AI initiative", "date": "2025-06-01"},
        {
            "title": f"{company_name} Q2 earnings exceed expectations",
            "date": "2025-06-03",
        },
    ]
