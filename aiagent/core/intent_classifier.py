from dataclasses import dataclass
from typing import Optional


@dataclass
class Intent:
    agent_id: str
    intent_name: str
    confidence: float
    keywords: list
    message: str


class IntentClassifier:
    """
    伪装意图分类器 - 基于关键词匹配
    后续可替换为真正的LLM意图识别
    """

    def __init__(self):
        self._intent_rules = {
            'tariff': {
                'keywords': ['关税', 'tariff', '税率', '进出口', '贸易战'],
                'agent_id': 'tariff_agent',
                'intent_name': 'tariff_analysis'
            },
            'risk': {
                'keywords': ['风险', 'risk', '评估', '分析'],
                'agent_id': 'default_agent',
                'intent_name': 'risk_assessment'
            }
        }
        self._default_agent = 'default_agent'

    async def classify(self, message: str) -> Intent:
        message_lower = message.lower()

        for rule_key, rule in self._intent_rules.items():
            for keyword in rule['keywords']:
                if keyword in message or keyword in message_lower:
                    return Intent(
                        agent_id=rule['agent_id'],
                        intent_name=rule['intent_name'],
                        confidence=0.95,
                        keywords=[keyword],
                        message=message
                    )

        return Intent(
            agent_id=self._default_agent,
            intent_name='general_query',
            confidence=1.0,
            keywords=[],
            message=message
        )