# Multi-Agent PoC: A2A + MCP

This is a minimal proof-of-concept multi-agent system demonstrating core functionality using the [Agent-to-Agent (A2A)](https://google-a2a.github.io/A2A/specification/) and [Model Context Protocol (MCP)] standards. Built for evaluation by the CTO and engineering team.

## Scenario & Purpose

The system supports a user query such as:

> _"Find recent company news about Acme Inc. and pull CRM history for John Doe from HubSpot."_

The Supervisor Agent parses the query, identifies subtasks, dispatches them to appropriate agents via A2A, and aggregates the results.

> Focus: protocol compliance and clean architecture — not full NLP generalization.

## Key Features

- A2A-compliant Agent Cards
- MCP-style Tool usage (via JSON-RPC 2.0)
- Agent discovery via local registry
- Asynchronous Supervisor Agent with retries, timeouts
- Testable, minimal, idiomatic Python
- Hardcoded user query in `main.py`

## Design Notes

- AgentCard structure strictly follows [A2A §5.5](https://google-a2a.github.io/A2A/specification/#55-agentcard-object-structure)
- Agent communication uses internal JSON-RPC 2.0 message simulation
- Supervisor parses known query formats only (see limitations)
- Skills are dynamically registered from AgentCard JSON
- Agents override a common `BaseAgent` interface
- Tool layers are injected for testability (MCP concept)

## Running the Demo

1. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run the entrypoint:

```bash
python main.py
```

> Output is printed directly to console.

## Running Tests

Run from the project root:

```bash
PYTHONPATH=. pytest
```

## Test Coverage

- SupervisorAgent behavior (task routing, timeout, aggregation)
- Agent Registry loading logic
- Web/CRM agent output via tool layers
- Query parsing logic

## Limitations

- Query parsing is fragile — works only for simple, known phrasing
- No real web/CRM data fetching; mocked tool responses
- No external API integration, UI, or persistent state

## Future Improvements

- Integrate basic LLM for true query understanding (OpenAI or OSS models)
- Expand AgentCard capabilities for streaming/push scenarios
- Add HTTP interface for Supervisor (Flask/FastAPI)
- Expand agent skill registry and support plug-and-play loading
- Add richer error handling and retry policy configurations
