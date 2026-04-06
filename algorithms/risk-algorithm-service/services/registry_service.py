from typing import Dict, List, Optional
from models.base import AlgorithmBase
from models.entities import AlgorithmInfo
from config import settings


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

_NAME_TO_SLUG: Dict[str, str] = {
    'tariff-risk-algorithm': 'tariff',
    'risk-scenarios-algorithm': 'scenario',
}


class RegistryService:
    def __init__(self):
        self._algorithms: Dict[str, AlgorithmBase] = {}
        self._remote_algorithms: Dict[str, AlgorithmInfo] = {}

    def register(self, algorithm: AlgorithmBase) -> None:
        self._algorithms[algorithm.name] = algorithm

    def register_remote(self, algorithm_info: AlgorithmInfo) -> None:
        self._remote_algorithms[algorithm_info.name] = algorithm_info

    def get(self, name: str) -> Optional[AlgorithmBase]:
        algo = self._algorithms.get(name)
        if algo is None:
            for algo_name, slug in _NAME_TO_SLUG.items():
                if name == slug:
                    algo = self._algorithms.get(algo_name)
                    break
        return algo

    def get_remote(self, name: str) -> Optional[AlgorithmInfo]:
        return self._remote_algorithms.get(name)

    def get_all(self) -> List[AlgorithmBase]:
        return list(self._algorithms.values())

    def get_all_remote(self) -> List[AlgorithmInfo]:
        return list(self._remote_algorithms.values())

    def get_all_algorithms(self) -> List[Dict]:
        slug_map = {
            'tariff-risk-algorithm': 'tariff',
            'risk-scenarios-algorithm': 'scenario',
        }
        slug_base = settings.ALGORITHM_BASE_URL
        local_algos = [
            {
                'name': a.name,
                'version': a.version,
                'label': a.label,
                'category': a.category,
                'type': a.algo_type,
                'description': a.description,
                'paramsSchema': a.params_schema,
                'outputSchema': a.output_schema,
                'isRemote': False,
                'endpoint': f"{slug_base}/{slug_map.get(a.name, a.name.split('-')[0])}/execute",
            }
            for a in self._algorithms.values()
        ]
        remote_algos = [
            {
                'name': a.name,
                'version': a.version,
                'label': a.label,
                'category': a.category,
                'type': a.algo_type,
                'description': a.description,
                'paramsSchema': a.params_schema,
                'outputSchema': a.output_schema,
                'isRemote': True,
                'endpoint': a.endpoint,
            }
            for a in self._remote_algorithms.values()
        ]
        return local_algos + remote_algos

    def get_by_category(self, category: str,
                        algo_type: Optional[str] = None) -> List[AlgorithmBase]:
        result = [a for a in self._algorithms.values() if a.category == category]
        if algo_type:
            result = [a for a in result if a.algo_type == algo_type]
        return result

    def get_category_tree(self) -> List[Dict]:
        tree: Dict[str, Dict] = {}
        all_algos = self.get_all_algorithms()

        for algo in all_algos:
            cat = algo.get('category', '')
            typ = algo.get('type', '')

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
        local_metadata = [
            AlgorithmInfo(
                name=algo.name,
                version=algo.version,
                endpoint=f'{slug_base}/{_NAME_TO_SLUG.get(algo.name, algo.name.split("-")[0])}',
                supported_params='',
                description=algo.description,
                category=algo.category,
                algo_type=algo.algo_type,
                label=algo.label,
                params_schema=algo.params_schema,
                output_schema=algo.output_schema,
            )
            for algo in self._algorithms.values()
        ]
        return local_metadata + list(self._remote_algorithms.values())

    def sync_remote_algorithms(self, remote_algos: List[AlgorithmInfo]) -> None:
        for algo in remote_algos:
            self._remote_algorithms[algo.name] = algo


registry_service = RegistryService()