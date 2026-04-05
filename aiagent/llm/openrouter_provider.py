import httpx
from typing import List, Optional, Dict, Any
from .base import BaseLLMProvider, LLMResponse


class OpenRouterProvider(BaseLLMProvider):

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key', '')
        self.base_url = config.get('base_url', 'https://openrouter.ai/api/v1')
        self.model = config.get('default_model', 'anthropic/claude-3-sonnet')

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        if not self.api_key or self.api_key == 'YOUR_OPENROUTER_API_KEY':
            raise ValueError("OpenRouter API key 未配置，请在 config/llm_config.json 中设置")

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/",
            "X-Title": "AI Agent Gateway"
        }

        payload = {
            "model": model or self.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.temperature,
            "max_tokens": max_tokens if max_tokens is not None else self.max_tokens
        }
        payload.update(kwargs)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

        return LLMResponse(
            content=data['choices'][0]['message']['content'],
            model=data.get('model', model or self.model),
            provider='openrouter',
            usage={
                'prompt_tokens': data.get('usage', {}).get('prompt_tokens', 0),
                'completion_tokens': data.get('usage', {}).get('completion_tokens', 0),
                'total_tokens': data.get('usage', {}).get('total_tokens', 0)
            },
            finish_reason=data['choices'][0].get('finish_reason', 'stop'),
            raw_response=data
        )

    async def complete(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        messages = [{"role": "user", "content": prompt}]
        return await self.chat(messages, model, temperature, max_tokens, **kwargs)
