from typing import Dict, Optional
from llm import get_provider, BaseLLMProvider
from config import config


class LLMService:
    _providers: Dict[str, BaseLLMProvider] = {}
    _agent_providers: Dict[str, BaseLLMProvider] = {}

    @classmethod
    def get_provider(cls, provider_name: Optional[str] = None) -> BaseLLMProvider:
        if provider_name is None:
            provider_name = config.get_default_provider()

        if provider_name not in cls._providers:
            provider_config = config.get_provider_config(provider_name)
            provider_name = cls._resolve_provider_name(provider_name, provider_config)
            provider_config = config.get_provider_config(provider_name)
            cls._providers[provider_name] = get_provider(provider_name, provider_config)

        return cls._providers[provider_name]

    @classmethod
    def get_agent_provider(cls, agent_id: str) -> BaseLLMProvider:
        if agent_id not in cls._agent_providers:
            agent_config = config.get_agent_config(agent_id)
            provider_name = agent_config.get('provider', config.get_default_provider())
            provider_config = config.get_provider_config(provider_name)

            resolved_provider = cls._resolve_provider_name(provider_name, provider_config)
            provider_config = config.get_provider_config(resolved_provider)

            merged_config = {**provider_config, **agent_config}
            cls._agent_providers[agent_id] = get_provider(resolved_provider, merged_config)

        return cls._agent_providers[agent_id]

    @classmethod
    def _resolve_provider_name(cls, provider_name: str, provider_config: dict) -> str:
        if provider_name in ['openai', 'openrouter']:
            api_key = provider_config.get('api_key', '')
            if not api_key or api_key.startswith('YOUR_'):
                return 'mock'
        return provider_name

    @classmethod
    def clear_cache(cls):
        cls._providers.clear()
        cls._agent_providers.clear()


llm_service = LLMService()
