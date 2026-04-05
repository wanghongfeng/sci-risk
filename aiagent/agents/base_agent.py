from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import os


@dataclass
class AgentResponse:
    response: str
    agent_id: str
    intent_name: str
    skills_used: List[str]
    success: bool
    error: str = None
    permissions_checked: List[str] = field(default_factory=list)
    data_scope_used: List[str] = field(default_factory=list)
    model: str = None
    provider: str = None
    usage: Dict[str, int] = field(default_factory=dict)


@dataclass
class Skill:
    skill_id: str
    skill_name: str
    description: str
    enabled: bool = True
    permissions_required: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Skill':
        return cls(
            skill_id=data.get('skill_id', ''),
            skill_name=data.get('skill_name', ''),
            description=data.get('description', ''),
            enabled=data.get('enabled', True),
            permissions_required=data.get('permissions_required', []),
            parameters=data.get('parameters', {})
        )


class BaseAgent(ABC):

    def __init__(self, agent_id: str, agent_name: str):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.skills: List[Skill] = []
        self._system_prompt: Optional[str] = None
        self._llm_provider = None

    def set_system_prompt(self, prompt: str):
        self._system_prompt = prompt

    def load_system_prompt(self, prompt_path: str):
        full_path = os.path.join(os.path.dirname(__file__), '..', prompt_path)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                self._system_prompt = f.read()

    @abstractmethod
    async def execute(
        self,
        message: str,
        context: Dict = None,
        user_permissions: Any = None
    ) -> AgentResponse:
        pass

    async def call_llm(
        self,
        message: str,
        context: Dict = None,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None
    ) -> AgentResponse:
        from llm.service import llm_service

        provider = llm_service.get_agent_provider(self.agent_id)

        agent_config = provider.config if hasattr(provider, 'config') else {}
        if model is None:
            model = agent_config.get('model')
        if temperature is None:
            temperature = agent_config.get('temperature', 0.7)
        if max_tokens is None:
            max_tokens = agent_config.get('max_tokens', 2048)

        messages = provider.build_messages(
            user_message=message,
            system_prompt=self._system_prompt,
            context=context
        )

        llm_response = await provider.chat(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return AgentResponse(
            response=llm_response.content,
            agent_id=self.agent_id,
            intent_name=self.__class__.__name__,
            skills_used=[],
            success=True,
            model=llm_response.model,
            provider=llm_response.provider,
            usage=llm_response.usage
        )

    def get_info(self) -> Dict[str, Any]:
        return {
            'agent_id': self.agent_id,
            'agent_name': self.agent_name,
            'skills': [
                {
                    'skill_id': s.skill_id,
                    'skill_name': s.skill_name,
                    'description': s.description,
                    'enabled': s.enabled,
                    'permissions_required': s.permissions_required
                }
                for s in self.skills
            ]
        }

    def get_skill(self, skill_id: str) -> Optional[Skill]:
        for skill in self.skills:
            if skill.skill_id == skill_id:
                return skill
        return None

    def get_enabled_skills(self) -> List[Skill]:
        return [s for s in self.skills if s.enabled]
