from models.base import AlgorithmBase
from typing import Dict, Any
import time


class TariffRiskAlgorithm(AlgorithmBase):

    @property
    def name(self) -> str:
        return "tariff-risk-algorithm"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "关税风险模拟算法"

    @property
    def label(self) -> str:
        return "关税风险模拟"

    @property
    def category(self) -> str:
        return "risk"

    @property
    def algo_type(self) -> str:
        return "simulation"

    @property
    def params_schema(self) -> Dict:
        return {
            "type": "object",
            "required": ["tariffRate"],
            "properties": {
                "tariffRate": {
                    "type": "integer",
                    "description": "关税税率（%）",
                    "minimum": 0,
                    "maximum": 100,
                    "example": 25
                },
                "productId": {
                    "type": "string",
                    "description": "产品ID（可选）",
                    "example": "P001"
                },
                "baseProfit": {
                    "type": "number",
                    "description": "基准利润（元，可选）",
                    "example": 1000
                }
            }
        }

    @property
    def output_schema(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "tariffRate": {"type": "integer", "description": "输入的关税税率"},
                "product": {"type": "string", "description": "产品标识"},
                "originalProfit": {"type": "number", "description": "基准利润"},
                "recommendation": {"type": "string", "description": "建议措施"},
                "riskScore": {"type": "number", "description": "风险评分 0-100"},
                "riskLevel": {
                    "type": "string",
                    "enum": ["LOW", "MEDIUM", "HIGH"],
                    "description": "风险等级"
                }
            }
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        tariff_rate = params.get('tariffRate', 10)
        base_profit = params.get('baseProfit', 1000)

        time.sleep(0.5)

        if tariff_rate <= 10:
            risk_score = 20
            risk_level = "LOW"
            result_text = f"关税{tariff_rate}%，利润充足，建议维持生产"
            recommendation = "维持生产"
        elif tariff_rate <= 20:
            risk_score = 55
            risk_level = "MEDIUM"
            result_text = f"关税{tariff_rate}%，利润偏低，需要关注"
            recommendation = "关注风险"
        else:
            risk_score = 80
            risk_level = "HIGH"
            result_text = f"关税{tariff_rate}%，利润不足，建议转产"
            recommendation = "转产"

        return {
            'result': f"【执行完成】{result_text}",
            'tariffRate': tariff_rate,
            'product': params.get('productId', '产品A'),
            'originalProfit': base_profit,
            'recommendation': recommendation,
            'riskScore': risk_score,
            'riskLevel': risk_level,
        }
