"""
Algorithm Framework - 算法服务基础框架
提供算法服务所需的公共功能：注册、发现、异步执行、callback等
"""

from .algorithm_base import AlgorithmBase
from .notification import NotificationContext, NotificationService, notification_service
from .app_factory import create_app
from .service_runner import run_service

__all__ = [
    'AlgorithmBase',
    'NotificationContext', 'NotificationService', 'notification_service',
    'create_app', 'run_service',
]
__version__ = '1.0.0'