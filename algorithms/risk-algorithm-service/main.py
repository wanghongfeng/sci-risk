from flask import Flask, send_from_directory, jsonify
from config import settings
from controllers import api_blueprint, register_algorithms
from services import registry_service
from algorithms import TariffRiskAlgorithm, RiskScenarioAlgorithm
import os
import threading
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')


def create_app():
    app = Flask(__name__)

    registry_service.register(TariffRiskAlgorithm())
    registry_service.register(RiskScenarioAlgorithm())

    app.register_blueprint(api_blueprint, url_prefix='/')

    @app.route('/apidocs/')
    def apidocs():
        return send_from_directory(STATIC_DIR, 'apidocs.html')

    @app.route('/apidocs/<path:filename>')
    def apidocs_static(filename):
        return send_from_directory(STATIC_DIR, filename)

    @app.route('/apispec.json')
    def apispec():
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "算法服务 API",
                "description": "供应链控制塔算法服务接口文档",
                "version": "1.0.0"
            },
            "paths": {
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
                        "summary": "获取算法列表",
                        "responses": {"200": {"description": "算法列表"}}
                    }
                },
                "/tariff/execute": {
                    "post": {
                        "tags": ["算法执行"],
                        "summary": "关税风险算法执行",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["callbackUrl"],
                                        "properties": {
                                            "taskId": {"type": "string"},
                                            "callbackUrl": {"type": "string"},
                                            "tariffRate": {"type": "integer", "example": 20}
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {"200": {"description": "执行成功"}}
                    }
                },
                "/scenario/execute": {
                    "post": {
                        "tags": ["算法执行"],
                        "summary": "风险场景算法执行",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": ["callbackUrl"],
                                        "properties": {
                                            "taskId": {"type": "string"},
                                            "callbackUrl": {"type": "string"},
                                            "scenarioType": {
                                                "type": "string",
                                                "enum": ["trade_war", "supply_disruption", "demand_volatility", "logistics_delay"],
                                                "example": "trade_war"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {"200": {"description": "执行成功"}}
                    }
                }
            },
            "tags": [
                {"name": "系统接口", "description": "健康检查、算法列表等"},
                {"name": "算法执行", "description": "算法执行相关接口"}
            ]
        }
        return jsonify(spec)

    return app


if __name__ == '__main__':
    print(f"Starting multi-algorithm-service on port {settings.ALGORITHM_PORT}")
    print(f"Swagger UI: http://localhost:{settings.ALGORITHM_PORT}/apidocs/")
    app = create_app()
    
    def register_after_startup():
        try:
            time.sleep(2)
            register_algorithms()
        except Exception as e:
            print(f"Registration thread error (non-critical): {e}")
    
    threading.Thread(target=register_after_startup, daemon=True).start()
    app.run(host='0.0.0.0', port=settings.ALGORITHM_PORT, debug=settings.DEBUG)
