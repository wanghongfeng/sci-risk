import os
import pkgutil
import importlib
from typing import List, Dict, Any, Optional
from pathlib import Path
from models.base import AlgorithmBase
from models.entities import AlgorithmInfo
from config import settings
import logging

logger = logging.getLogger(__name__)


class AlgorithmDiscoveryService:

    def __init__(self):
        self._remote_services: List[Dict[str, Any]] = []
        self._remote_algorithms_cache: List[AlgorithmInfo] = []
        self._cache_time: float = 0
        self._cache_ttl: float = 300

    def discover_local_algorithms(self, package_name: str = "algorithms") -> List[AlgorithmBase]:
        discovered = []
        try:
            package = importlib.import_module(package_name)
            package_path = Path(package.__file__).parent

            for _, module_name, is_pkg in pkgutil.iter_modules([str(package_path)]):
                if is_pkg:
                    continue
                try:
                    module = importlib.import_module(f"{package_name}.{module_name}")
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and issubclass(attr, AlgorithmBase) and attr is not AlgorithmBase:
                            algo_instance = attr()
                            discovered.append(algo_instance)
                            logger.info(f"Discovered local algorithm: {algo_instance.name}")
                except Exception as e:
                    logger.warning(f"Failed to import algorithm module {module_name}: {e}")

        except Exception as e:
            logger.error(f"Failed to discover local algorithms: {e}")

        return discovered

    def register_remote_service(self, name: str, base_url: str, health_endpoint: str = "/health",
                                algorithms_endpoint: str = "/algorithms",
                                execute_endpoint: str = "/algorithm/execute") -> None:
        self._remote_services.append({
            'name': name,
            'base_url': base_url.rstrip('/'),
            'health_endpoint': health_endpoint,
            'algorithms_endpoint': algorithms_endpoint,
            'execute_endpoint': execute_endpoint,
        })
        logger.info(f"Registered remote algorithm service: {name} at {base_url}")

    def discover_remote_algorithms(self, force_refresh: bool = False) -> List[AlgorithmInfo]:
        import time
        current_time = time.time()

        if not force_refresh and (current_time - self._cache_time) < self._cache_ttl and self._remote_algorithms_cache:
            return self._remote_algorithms_cache

        all_algorithms = []

        for service in self._remote_services:
            try:
                from utils import http_client
                resp = http_client.get(f"{service['base_url']}{service['algorithms_endpoint']}")
                response = resp.json() if hasattr(resp, 'json') else resp
                if response and response.get('algorithms'):
                    for algo in response['algorithms']:
                        algo_info = AlgorithmInfo(
                            name=algo.get('name', ''),
                            version=algo.get('version', '1.0.0'),
                            endpoint=f"{service['base_url']}{service['execute_endpoint']}",
                            supported_params=algo.get('supported_params', ''),
                            description=algo.get('description', ''),
                            category=algo.get('category', ''),
                            algo_type=algo.get('type', ''),
                            label=algo.get('label', ''),
                            params_schema=algo.get('paramsSchema', {}),
                            output_schema=algo.get('outputSchema', {}),
                        )
                        algo_info._source_service = service['name']
                        algo_info._is_remote = True
                        all_algorithms.append(algo_info)
                        logger.info(f"Discovered remote algorithm: {algo_info.name} from {service['name']}")
            except Exception as e:
                logger.warning(f"Failed to discover algorithms from {service['name']}: {e}")

        self._remote_algorithms_cache = all_algorithms
        self._cache_time = current_time
        return all_algorithms

    def execute_remote_algorithm(self, algorithm_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        algo_info = self.get_remote_algorithm_info(algorithm_name)
        if not algo_info:
            raise ValueError(f"Remote algorithm {algorithm_name} not found")

        try:
            from utils import http_client
            task_id = params.get('taskId', '')
            callback_url = params.get('callbackUrl', '')
            notification = params.get('notification')
            inner_params = params.get('params') or {}

            request_body = {
                'algorithmName': algorithm_name,
                'taskId': task_id,
                'callbackUrl': callback_url,
            }
            if notification:
                request_body['notification'] = notification
            request_body.update(inner_params)

            response = http_client.post(algo_info.endpoint, json=request_body, timeout=30)
            return response
        except Exception as e:
            logger.error(f"Failed to execute remote algorithm {algorithm_name}: {e}")
            raise

    def get_remote_algorithm_info(self, algorithm_name: str) -> Optional[AlgorithmInfo]:
        algorithms = self.discover_remote_algorithms()
        for algo in algorithms:
            if algo.name == algorithm_name:
                return algo
        return None

    def get_remote_services(self) -> List[Dict[str, Any]]:
        return self._remote_services.copy()


discovery_service = AlgorithmDiscoveryService()