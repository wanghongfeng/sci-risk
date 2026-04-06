from flask import Flask, send_from_directory, jsonify
from config import settings
from controllers import api_blueprint, register_algorithms
from services import registry_service, discovery_service
import os
import threading
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')


def discover_and_register_local_algorithms():
    discovered = discovery_service.discover_local_algorithms('algorithms')
    for algo in discovered:
        registry_service.register(algo)
    logger.info(f"Auto-discovered {len(discovered)} local algorithms")
    return discovered


def register_remote_services_from_env():
    remote_services_config = os.environ.get('REMOTE_ALGORITHM_SERVICES', '')
    if not remote_services_config:
        default_ml_service = os.environ.get('ML_ALGORITHM_SERVICE_URL', '')
        if default_ml_service:
            remote_services_config = f"risk-ml-algorithm:{default_ml_service}"
    if not remote_services_config:
        return
    for entry in remote_services_config.split(','):
        if ':' not in entry:
            continue
        name, url = entry.split(':', 1)
        discovery_service.register_remote_service(name=name.strip(), base_url=url.strip())
    remote_algos = discovery_service.discover_remote_algorithms(force_refresh=True)
    registry_service.sync_remote_algorithms(remote_algos)
    logger.info(f"Registered {len(remote_algos)} remote algorithms from environment config")


def create_app():
    app = Flask(__name__)

    discover_and_register_local_algorithms()

    register_remote_services_from_env()

    app.register_blueprint(api_blueprint, url_prefix='/')

    @app.route('/apidocs/')
    def apidocs():
        return send_from_directory(STATIC_DIR, 'apidocs.html')

    @app.route('/apidocs/<path:filename>')
    def apidocs_static(filename):
        return send_from_directory(STATIC_DIR, filename)

    @app.route('/apispec.json')
    def apispec():
        local_algos = registry_service.get_all()
        remote_algos = registry_service.get_all_remote()

        paths = {
            "/health": {
                "get": {
                    "tags": ["系统接口"],
                    "summary": "健康检查",
                    "responses": {"200": {"description": "服务正常"}}
                }
            },
            "/algorithms": {
                "get": {
                    "tags": ["系统接口"],
                    "summary": "获取算法列表（含远程算法）",
                    "parameters": [
                        {"name": "includeRemote", "in": "query", "schema": {"type": "boolean"}, "description": "是否包含远程算法"},
                        {"name": "category", "in": "query", "schema": {"type": "string"}},
                        {"name": "type", "in": "query", "schema": {"type": "string"}},
                    ],
                    "responses": {"200": {"description": "算法列表"}}
                }
            },
            "/categories": {
                "get": {
                    "tags": ["系统接口"],
                    "summary": "获取分类树",
                    "responses": {"200": {"description": "分类树"}}
                }
            },
            "/remote-services": {
                "get": {
                    "tags": ["远程服务管理"],
                    "summary": "获取已注册的远程算法服务",
                    "responses": {"200": {"description": "远程服务列表"}}
                }
            },
            "/algorithm/execute": {
                "post": {
                    "tags": ["算法执行"],
                    "summary": "统一算法执行（自动路由本地/远程）",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["algorithmName", "callbackUrl"],
                                    "properties": {
                                        "algorithmName": {"type": "string"},
                                        "taskId": {"type": "string"},
                                        "callbackUrl": {"type": "string"},
                                        "params": {"type": "object"},
                                        "notification": {"type": "object"},
                                    }
                                }
                            }
                        }
                    },
                    "responses": {"200": {"description": "执行成功"}}
                }
            },
        }

        for algo in local_algos:
            slug = algo.name.split('-')[0]
            paths[f"/{slug}/execute"] = {
                "post": {
                    "tags": ["本地算法执行"],
                    "summary": f"执行{algo.label}",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["callbackUrl"],
                                    "properties": algo.params_schema.get('properties', {})
                                }
                            }
                        }
                    },
                    "responses": {"200": {"description": "执行成功"}}
                }
            }

        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "算法服务 API（注册中心）",
                "description": "供应链控制塔算法服务接口文档，支持本地算法自动发现和远程算法服务代理",
                "version": "2.0.0"
            },
            "paths": paths,
            "tags": [
                {"name": "系统接口", "description": "健康检查、算法列表等"},
                {"name": "远程服务管理", "description": "远程算法服务的注册与管理"},
                {"name": "算法执行", "description": "统一算法执行接口（自动路由）"},
                {"name": "本地算法执行", "description": "本地算法直接执行"},
            ]
        }
        return jsonify(spec)

    return app


if __name__ == '__main__':
    print(f"Starting algorithm registry center on port {settings.ALGORITHM_PORT}")
    print(f"Swagger UI: http://localhost:{settings.ALGORITHM_PORT}/apidocs/")
    app = create_app()
    app.run(host='0.0.0.0', port=settings.ALGORITHM_PORT, debug=settings.DEBUG)