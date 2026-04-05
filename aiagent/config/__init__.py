import json
import os
from typing import Dict, Any, Optional


class Config:
    _instance: Optional['Config'] = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'llm_config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        else:
            self._config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "provider": "mock",
            "agents": {}
        }

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    def get_agent_config(self, agent_id: str) -> Dict[str, Any]:
        return self.get(f'agents.{agent_id}', {})

    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        return self.get(provider, {})

    def get_default_provider(self) -> str:
        return self.get('provider', 'mock')

    @property
    def config(self) -> Dict[str, Any]:
        return self._config

    def reload(self):
        self._load_config()


config = Config()