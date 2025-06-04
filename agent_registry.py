import importlib
import json
import os

from protocol.base_agent import BaseAgent

# Map agent identifiers to fully qualified class paths
AGENT_CLASS_REGISTRY = {}  # TODO: add to registry


def load_class_from_path(dotted_path: str):
    """
    Dynamically import a class from a dotted module path.
    """
    module_path, class_name = dotted_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def extract_agent_id(path: str) -> str:
    """
    Extract agent ID slug from card path.
    """
    folder_name = os.path.basename(os.path.dirname(path))
    return folder_name.replace("_agent", "").replace("_", "-")


class AgentRegistry:
    """
    Loads agent cards and maps skill IDs to agent instances, simulating agent discovery as described in the A2A (Agent-to-Agent) specification.
    For local development, this enables deterministic resolution of agent skills without requiring distributed infrastructure.
    """

    def __init__(self, agent_card_paths: list[str]):
        self.skill_map = {}  # TODO: add method_name → agent_instance
        self.load_agents(agent_card_paths)

    def load_agents(self, paths: list[str]):
        """
        Loads AgentCards and binds skill IDs to in-memory agent instances.
        """
        for path in paths:
            with open(path, "r") as f:
                card = json.load(f)

            agent_id = extract_agent_id(path)

            class_path = AGENT_CLASS_REGISTRY.get(agent_id)
            if not class_path:
                print(f"No class registered for agent: {agent_id}")
                continue

            AgentClass = load_class_from_path(class_path)
            agent_instance = AgentClass()

            for skill in card.get("skills", []):
                skill_id = skill["id"]
                self.skill_map[skill_id] = agent_instance

    def find_agent_for_method(self, method: str) -> BaseAgent | None:
        """
        Given a skill ID, return the agent that supports it.
        """
        return self.skill_map.get(method)
