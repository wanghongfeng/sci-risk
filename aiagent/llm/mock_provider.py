from typing import List, Optional, Dict, Any
from .base import BaseLLMProvider, LLMResponse


class MockProvider(BaseLLMProvider):

    MOCK_RESPONSES = {
        'tariff_agent': "这是关税智能体的模拟响应。关税政策正在发展中，无法通过当前接口提供实时分析。建议访问官方海关网站获取最新税率。",
        'default_agent': "正在建设中...当前版本暂不支持该类查询。我们将持续更新，敬请期待更多智能功能。",
        'intent_classifier': '{"intent_name": "tariff_analysis", "confidence": 0.95, "keywords": ["关税"]}'
    }

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        user_message = ""
        for msg in reversed(messages):
            if msg.get('role') == 'user':
                user_message = msg.get('content', '')
                break

        content = self._generate_mock_response(user_message, model)

        return LLMResponse(
            content=content,
            model=model or self.model,
            provider='mock',
            usage={
                'prompt_tokens': 100,
                'completion_tokens': 50,
                'total_tokens': 150
            },
            finish_reason='stop',
            raw_response={}
        )

    async def complete(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        content = self._generate_mock_response(prompt, model)

        return LLMResponse(
            content=content,
            model=model or self.model,
            provider='mock',
            usage={
                'prompt_tokens': 100,
                'completion_tokens': 50,
                'total_tokens': 150
            },
            finish_reason='stop',
            raw_response={}
        )

    def _generate_mock_response(self, user_message: str, model: Optional[str]) -> str:
        msg_lower = user_message.lower()

        if any(k in msg_lower for k in ['关税', 'tariff', '税率']):
            return self.MOCK_RESPONSES['tariff_agent']

        return self.MOCK_RESPONSES['default_agent']
