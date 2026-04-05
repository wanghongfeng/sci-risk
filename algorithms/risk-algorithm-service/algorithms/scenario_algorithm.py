from models.base import AlgorithmBase
from typing import Dict, Any
import time


class RiskScenarioAlgorithm(AlgorithmBase):
    SCENARIOS = {
        'trade_war': {
            'name': '贸易战风险', 'risk_score': 80, 'level': 'HIGH',
            'advice': '启动应急预案，考虑多元供应链策略'
        },
        'supply_disruption': {
            'name': '供应链中断', 'risk_score': 60, 'level': 'MEDIUM',
            'advice': '加强监控，准备备选方案'
        },
        'demand_volatility': {
            'name': '需求波动', 'risk_score': 50, 'level': 'MEDIUM',
            'advice': '加强监控，准备备选方案'
        },
        'logistics_delay': {
            'name': '物流延迟', 'risk_score': 40, 'level': 'LOW',
            'advice': '持续关注，维持现有策略'
        },
    }

    @property
    def name(self) -> str:
        return "risk-scenarios-algorithm"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "风险场景分析算法"

    @property
    def label(self) -> str:
        return "风险场景分析"

    @property
    def category(self) -> str:
        return "risk"

    @property
    def algo_type(self) -> str:
        return "classification"

    @property
    def params_schema(self) -> Dict:
        return {
            "type": "object",
            "required": ["scenarioType"],
            "properties": {
                "scenarioType": {
                    "type": "string",
                    "description": "风险场景类型",
                    "enum": list(self.SCENARIOS.keys()),
                    "example": "trade_war"
                },
                "region": {
                    "type": "string",
                    "description": "分析地区（可选）",
                    "example": "东南亚"
                }
            }
        }

    @property
    def output_schema(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "scenarioType": {"type": "string", "description": "场景类型标识"},
                "scenarioName": {"type": "string", "description": "场景名称"},
                "riskScore": {"type": "number", "description": "风险评分 0-100"},
                "riskLevel": {
                    "type": "string",
                    "enum": ["LOW", "MEDIUM", "HIGH"],
                    "description": "风险等级"
                },
                "recommendation": {"type": "string", "description": "应对建议"}
            }
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        scenario_type = params.get('scenarioType', 'trade_war')
        scenario = self.SCENARIOS.get(scenario_type, self.SCENARIOS['trade_war'])

        time.sleep(0.5)

        return {
            'result': f"【执行完成】{scenario['name']}分析完成，风险指数: {scenario['risk_score']}/100",
            'scenarioType': scenario_type,
            'scenarioName': scenario['name'],
            'region': params.get('region', '全球'),
            'riskScore': scenario['risk_score'],
            'riskLevel': scenario['level'],
            'recommendation': scenario['advice'],
        }
