from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import time


@dataclass
class AlgorithmInfo:
    name: str
    version: str
    endpoint: str
    supported_params: str
    description: str
    category: str = ""
    algo_type: str = ""
    label: str = ""
    params_schema: Dict = field(default_factory=dict)
    output_schema: Dict = field(default_factory=dict)
    status: Optional[str] = None
    registered_time: int = field(default_factory=lambda: int(time.time() * 1000))


@dataclass
class TaskRequest:
    task_id: str
    callback_url: str
    params: Dict[str, Any]
    notification: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskRequest':
        reserved = {'taskId', 'callbackUrl', 'notification'}
        return cls(
            task_id=data.get('taskId', ''),
            callback_url=data.get('callbackUrl', ''),
            params={k: v for k, v in data.items() if k not in reserved},
            notification=data.get('notification'),
        )


@dataclass
class TaskResult:
    task_id: str
    result: str
    extra_data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'taskId': self.task_id,
            'result': self.result,
            **self.extra_data
        }
