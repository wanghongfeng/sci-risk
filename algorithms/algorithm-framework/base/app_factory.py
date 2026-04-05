import os
import requests
import threading
from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS


class AlgorithmApp:
    def __init__(self, algorithms: list, service_port: int = 5000,
                 backend_url: str = "http://localhost:8080"):
        self.algorithms = {algo.name: algo for algo in algorithms}
        self.service_port = service_port
        self.backend_url = backend_url
        self.app = self._create_app()

    def _create_app(self) -> Flask:
        app = Flask(__name__)
        CORS(app)

        for algo in self.algorithms.values():
            algo.endpoint = f"http://localhost:{self.service_port}/{algo.name}"

        self._register_routes(app)
        self._start_registration(app)

        return app

    def _register_routes(self, app: Flask):
        @app.route("/health", methods=["GET"])
        def health():
            return jsonify({"status": "healthy", "service": "algorithm-service"})

        @app.route("/algorithms", methods=["GET"])
        def list_algorithms():
            return jsonify({
                "algorithms": [algo.get_info() for algo in self.algorithms.values()]
            })

        @app.route("/<algo_name>/execute", methods=["POST"])
        def execute(algo_name):
            if algo_name not in self.algorithms:
                return jsonify({"error": f"Algorithm {algo_name} not found"}), 404

            algo = self.algorithms[algo_name]
            params = request.get_json() or {}
            callback_url = params.pop("callbackUrl", None)

            return jsonify(algo.run_async(params, callback_url))

        @app.route("/apispec.json")
        def apispec():
            paths = {
                "/health": {"get": {"tags": ["系统接口"], "summary": "健康检查",
                                     "responses": {"200": {"description": "服务正常"}}}},
                "/algorithms": {"get": {"tags": ["系统接口"], "summary": "获取算法列表",
                                        "responses": {"200": {"description": "算法列表"}}}}
            }

            for name, algo in self.algorithms.items():
                paths[f"/{name}/execute"] = {
                    "post": {
                        "tags": ["算法执行"],
                        "summary": f"执行{name}算法",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "callbackUrl": {"type": "string"},
                                            "params": {"type": "object"}
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {"200": {"description": "执行成功"}}
                    }
                }

            spec = {
                "openapi": "3.0.0",
                "info": {"title": "算法服务 API", "description": "供应链控制塔算法服务",
                         "version": "1.0.0"},
                "paths": paths,
                "tags": [
                    {"name": "系统接口", "description": "健康检查、算法列表等"},
                    {"name": "算法执行", "description": "算法执行相关接口"}
                ]
            }
            return jsonify(spec)

        @app.route("/apidocs/")
        def apidocs():
            return send_file("static/apidocs.html")

        @app.route("/apidocs/<path:filename>")
        def apidocs_static(filename):
            return send_from_directory("static", filename)

    def _start_registration(self, app: Flask):
        def register():
            for i in range(30):
                try:
                    all_success = True
                    for algo in self.algorithms.values():
                        resp = requests.post(
                            f"{self.backend_url}/api/algorithm/register",
                            json=algo.get_info(),
                            timeout=5
                        )
                        if resp.status_code not in [200, 201]:
                            all_success = False
                    if all_success:
                        print(f"Algorithms registered successfully")
                        return
                except Exception as e:
                    print(f"Registration attempt {i+1}/30 failed: {e}")
                threading.Event().wait(2)
            print("Failed to register algorithms")

        threading.Thread(target=register, daemon=True).start()

    def run(self, host: str = "0.0.0.0", debug: bool = False):
        self.app.run(host=host, port=self.service_port, debug=debug)


def create_app(algorithms: list, service_port: int = 5000,
               backend_url: str = None) -> AlgorithmApp:
    if backend_url is None:
        backend_url = os.environ.get("BACKEND_URL", "http://localhost:8080")

    service_port = int(os.environ.get("SERVICE_PORT", service_port))

    return AlgorithmApp(algorithms, service_port, backend_url)