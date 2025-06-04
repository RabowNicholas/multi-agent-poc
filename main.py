import asyncio
import json
from agents.supervisor_agent import SupervisorAgent
from agent_registry import AgentRegistry


async def main():
    # Initialize the agent registry with paths to Agent Cards
    print("Initializing Agent Registry...")
    registry = AgentRegistry.from_card_paths(
        [
            "agent_cards/web_research_agent_card.json",
            "agent_cards/crm_research_agent_card.json",
        ]
    )

    # Create the Supervisor Agent with the registry
    print("Creating Supervisor Agent...")
    supervisor = SupervisorAgent(agent_registry=registry)

    # Define a hardcoded query (simulate CLI input)
    query = "Find recent company news about Acme Inc and pull CRM history for John Doe"
    print(f"\nReceived query: '{query}'")

    # Handle the query and get results
    print("\nDelegating tasks to appropriate agents...")
    results = await supervisor.handle_query(query)

    # Print the JSON-RPC style aggregated responses
    print("\nAggregated Agent Responses:\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
