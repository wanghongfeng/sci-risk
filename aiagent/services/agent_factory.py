from typing import Dict, List
from agents.base_agent import BaseAgent
from agents.tariff_agent import TariffAgent
from agents.default_agent import DefaultAgent


class AgentFactory:

    _agents: Dict[str, BaseAgent] = {}

    @classmethod
    def initialize(cls):
        if not cls._agents:
            cls._agents = {
                'tariff_agent': TariffAgent(),
                'default_agent': DefaultAgent()
            }

    @classmethod
    def get_agent(cls, agent_id: str) -> BaseAgent:
        if not cls._agents:
            cls.initialize()

        agent = cls._agents.get(agent_id)
        if agent is None:
            agent = cls._agents.get('default_agent')

        return agent

    @classmethod
    def list_agents(cls) -> List[Dict]:
        if not cls._agents:
            cls.initialize()

        return [agent.get_info() for agent in cls._agents.values()]


AgentFactory.initialize()
