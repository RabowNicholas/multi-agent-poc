import asyncio
import re
import uuid
from typing import List, Dict
from agent_registry import AgentRegistry

from protocol.base_agent import BaseAgent


class SupervisorAgent:
    """
    SupervisorAgent handles user queries by parsing them into JSON-RPC tasks,
    delegating to appropriate agents via an AgentRegistry, and aggregating responses.

    This class supports basic NLP simulation, asynchronous task execution,
    error handling, and retry logic. Designed for PoC demonstration of A2A and MCP protocols.
    """

    def __init__(self, agent_registry: AgentRegistry) -> None:
        self.registry: AgentRegistry = agent_registry

    async def handle_query(self, query: str) -> List[Dict]:
        """
        Parses a natural language query, delegates tasks to appropriate agents asynchronously,
        and returns a list of JSON-RPC 2.0 compliant responses.
        """
        tasks = self.parse_query(query)
        coroutines = [self.delegate_task(task) for task in tasks]
        responses = await asyncio.gather(*coroutines)
        return responses

    def extract_company_name(self, query: str) -> str:
        """
        Naively extracts company name after 'news about' by taking the next two words.
        Note: This is a placeholder and should be replaced with proper NLP.
        """
        words = query.lower().split()
        if "news" in words and "about" in words:
            try:
                idx = words.index("about")
                return " ".join(words[idx + 1 : idx + 3]).title()
            except IndexError:
                return ""
        return ""

    def extract_contact_name(self, query: str) -> str:
        """
        Naively extracts contact name after 'crm history for' by taking the next two words.
        Note: This is a placeholder and should be replaced with proper NLP.
        """
        words = query.lower().split()
        if "crm" in words and "history" in words and "for" in words:
            try:
                idx = words.index("for")
                return " ".join(words[idx + 1 : idx + 3]).title()
            except IndexError:
                return ""
        return ""

    # NOTE:
    # This rule-based parser simulates basic NLP functionality by extracting intents
    # and simple entities (company, contact) using regex patterns. In a production
    # environment, this would be replaced with proper NLU tooling (e.g., spaCy, LLMs)
    # capable of multi-intent detection and Named Entity Recognition.
    #
    # TODO:
    # - Replace regex with spaCy or a lightweight intent + NER model.
    # - Improve intent mapping with configurable patterns or ML-based classifier.
    # - Add fallback and clarification mechanism for ambiguous queries.
    def parse_query(self, query: str) -> List[Dict]:
        """
        Parses a natural language query into one or more JSON-RPC 2.0 task objects.
        This is a minimal simulation of NLP, suitable for PoC.
        """
        query = re.sub(r"[^\w\s]", "", query)
        tasks = []

        if "news about" in query.lower():
            company = self.extract_company_name(query)
            if company:
                tasks.append(
                    {
                        "jsonrpc": "2.0",
                        "method": "get_company_news",
                        "params": {"company_name": company},
                        "id": str(uuid.uuid4()),
                    }
                )

        if "crm history for" in query.lower():
            contact = self.extract_contact_name(query)
            if contact:
                tasks.append(
                    {
                        "jsonrpc": "2.0",
                        "method": "get_crm_history",
                        "params": {"contact_name": contact},
                        "id": str(uuid.uuid4()),
                    }
                )

        return tasks

    async def delegate_task(self, task: Dict, timeout: float = 3.0) -> Dict:
        """
        Finds the agent that supports the given method and simulates an async JSON-RPC call.
        Includes timeout and retry handling.
        """
        agent: BaseAgent | None = self.registry.find_agent_for_method(task["method"])
        if not agent:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32601,
                    "message": f"Method {task['method']} not found",
                },
                "id": task["id"],
            }

        async def attempt():
            try:
                return await agent.handle_rpc(task)
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32000,
                        "message": str(e),
                    },
                    "id": task["id"],
                }

        for attempt_count in range(2):  # Initial + one retry
            try:
                return await asyncio.wait_for(attempt(), timeout=timeout)
            except asyncio.TimeoutError:
                if attempt_count == 1:
                    return {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32001,
                            "message": f"Timeout after {timeout} seconds",
                        },
                        "id": task["id"],
                    }

        # Safety fallback (should never happen)
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32002,
                "message": "Unexpected error: task handling failed without timeout",
            },
            "id": task["id"],
        }
