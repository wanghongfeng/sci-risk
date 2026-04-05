from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class LLMResponse:
    content: str
    model: str
    provider: str
    usage: Dict[str, int]
    finish_reason: str
    raw_response: Optional[Dict[str, Any]] = None


class BaseLLMProvider(ABC):

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = config.get('default_model', 'gpt-4')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 2048)
        self.timeout = config.get('timeout', 60)

    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        pass

    @abstractmethod
    async def complete(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        pass

    def build_messages(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, str]]:
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        if context and context.get('history'):
            messages.extend(context['history'])

        messages.append({
            "role": "user",
            "content": user_message
        })

        return messages
