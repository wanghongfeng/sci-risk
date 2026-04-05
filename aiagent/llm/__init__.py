from .base import BaseLLMProvider, LLMResponse
from .openai_provider import OpenAIProvider
from .openrouter_provider import OpenRouterProvider
from .mock_provider import MockProvider

__all__ = ['BaseLLMProvider', 'LLMResponse', 'OpenAIProvider', 'OpenRouterProvider', 'MockProvider', 'get_provider']


def get_provider(provider_name: str, config: dict) -> BaseLLMProvider:
    providers = {
        'openai': OpenAIProvider,
        'openrouter': OpenRouterProvider,
        'mock': MockProvider
    }

    provider_class = providers.get(provider_name.lower())
    if provider_class is None:
        provider_class = MockProvider

    return provider_class(config)