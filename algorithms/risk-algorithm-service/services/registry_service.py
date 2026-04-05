from typing import Dict, List, Optional
from models.base import AlgorithmBase
from models.entities import AlgorithmInfo
from config import settings


# 两级分类的中文标签
CATEGORY_LABELS = {
    'risk': '风险',
    'plan': '计划',
    'inventory': '库存',
    'supply_chain': '供应链',
}

TYPE_LABELS = {
    'simulation': '风险模拟',
    'classification': '风险分类',
    'assessment': '综合评估',
    'order_simulation': '订单模拟',
    'production_transfer': '转产规划',
    'capacity_planning': '产能规划',
    'consumption': '消耗模拟',
    'replenishment': '补货建议',
    'shortage_risk': '短缺风险',
    'disruption': '中断模拟',
    'optimization': '优化建议',
}

# 算法名称 → URL片段的映射（用于端点生成）
_NAME_TO_SLUG: Dict[str, str] = {
    'tariff-risk-algorithm': 'tariff',
    'risk-scenarios-algorithm': 'scenario',
}


class RegistryService:
    def __init__(self):
        self._algorithms: Dict[str, AlgorithmBase] = {}

    def register(self, algorithm: AlgorithmBase) -> None:
        self._algorithms[algorithm.name] = algorithm

    def get(self, name: str) -> Optional[AlgorithmBase]:
        """按算法名或 URL slug 查找"""
        algo = self._algorithms.get(name)
        if algo is None:
            for algo_name, slug in _NAME_TO_SLUG.items():
                if name == slug:
                    algo = self._algorithms.get(algo_name)
                    break
        return algo

    def get_all(self) -> List[AlgorithmBase]:
        return list(self._algorithms.values())

    def get_by_category(self, category: str,
                        algo_type: Optional[str] = None) -> List[AlgorithmBase]:
        """按一级分类（和可选的二级分类）过滤"""
        result = [a for a in self._algorithms.values() if a.category == category]
        if algo_type:
            result = [a for a in result if a.algo_type == algo_type]
        return result

    def get_category_tree(self) -> List[Dict]:
        """返回两级分类树，包含每个叶节点的算法数量"""
        tree: Dict[str, Dict] = {}
        for algo in self._algorithms.values():
            cat = algo.category
            typ = algo.algo_type
            if cat not in tree:
                tree[cat] = {
                    'category': cat,
                    'label': CATEGORY_LABELS.get(cat, cat),
                    'types': {},
                }
            types = tree[cat]['types']
            if typ not in types:
                types[typ] = {
                    'type': typ,
                    'label': TYPE_LABELS.get(typ, typ),
                    'count': 0,
                }
            types[typ]['count'] += 1

        # 转成列表格式
        return [
            {
                'category': v['category'],
                'label': v['label'],
                'types': list(v['types'].values()),
            }
            for v in tree.values()
        ]

    def get_metadata(self) -> List[AlgorithmInfo]:
        slug_base = f'http://localhost:{settings.ALGORITHM_PORT}'
        return [
            AlgorithmInfo(
                name=algo.name,
                version=algo.version,
                endpoint=f'{slug_base}/{_NAME_TO_SLUG.get(algo.name, algo.name.split("-")[0])}',
                supported_params='',          # 已废弃，保留字段兼容旧调用
                description=algo.description,
                category=algo.category,
                algo_type=algo.algo_type,
                label=algo.label,
                params_schema=algo.params_schema,
                output_schema=algo.output_schema,
            )
            for algo in self._algorithms.values()
        ]


registry_service = RegistryService()
