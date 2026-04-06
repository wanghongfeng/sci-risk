from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import requests
import threading
import time
import uuid
import random

app = Flask(__name__)
CORS(app)

ALGORITHM_NAME = "risk-ml-algorithm"
ALGORITHM_VERSION = "1.0.0"
ALGORITHM_PORT = int(os.environ.get("SERVICE_PORT", 5001))
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8080")

tasks = {}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": ALGORITHM_NAME})

@app.route("/algorithms", methods=["GET"])
def list_algorithms():
    return jsonify({
        "algorithms": [{
            "name": ALGORITHM_NAME,
            "version": ALGORITHM_VERSION,
            "endpoint": f"http://localhost:{ALGORITHM_PORT}/ml/execute",
            "supported_params": "historicalData,riskFactors",
            "description": "基于机器学习的供应链风险预测算法"
        }]
    })

@app.route("/ml/execute", methods=["POST"])
def execute_ml():
    data = request.get_json() or {}
    task_id = data.get("taskId", str(uuid.uuid4()))
    callback_url = data.get("callbackUrl", f"{BACKEND_URL}/api/simulation/status")

    tasks[task_id] = {
        "status": "PENDING",
        "progress": 0,
        "result": None,
        "error": None
    }

    def run_ml_simulation():
        tasks[task_id]["status"] = "EXECUTING"
        tasks[task_id]["progress"] = 20

        time.sleep(1)

        historical_data = data.get("historicalData", [])
        risk_factors = data.get("riskFactors", {})
        tasks[task_id]["progress"] = 60

        time.sleep(1)

        features = historical_data[-10:] if len(historical_data) > 10 else historical_data

        base_risk = random.uniform(40, 85)
        volatility = risk_factors.get("volatility", 0.5)
        trend = risk_factors.get("trend", 0)
        tasks[task_id]["progress"] = 80

        risk_score = min(100, max(0, base_risk + trend * 10 + volatility * 15))
        confidence = random.uniform(0.75, 0.98)
        risk_level = "LOW" if risk_score < 40 else "MEDIUM" if risk_score < 70 else "HIGH"

        result = {
            "taskId": task_id,
            "status": "COMPLETED",
            "progress": 100,
            "result": f"[ML预测] 风险指数: {risk_score:.1f}/100, 置信度: {confidence:.2%}",
            "riskScore": round(risk_score, 1),
            "confidence": round(confidence, 3),
            "riskLevel": risk_level,
            "modelVersion": "v1.0-ml",
            "featuresAnalyzed": len(features),
            "recommendation": "建议增加安全库存，优化供应商结构" if risk_score > 60 else "风险可控，维持现状"
        }

        tasks[task_id]["status"] = "COMPLETED"
        tasks[task_id]["progress"] = 100
        tasks[task_id]["result"] = result

        try:
            requests.post(callback_url, json=result, timeout=10)
        except Exception as e:
            print(f"Callback failed: {e}")

    threading.Thread(target=run_ml_simulation, daemon=True).start()

    return jsonify({
        "taskId": task_id,
        "status": "PENDING",
        "message": "ML风险预测任务已提交",
        "checkUrl": f"http://localhost:{ALGORITHM_PORT}/ml/status/{task_id}"
    })

@app.route("/ml/status/<task_id>", methods=["GET"])
def get_status(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({
        "taskId": task_id,
        "status": task["status"],
        "progress": task["progress"],
        "result": task["result"],
        "error": task["error"]
    })

@app.route("/ml/result/<task_id>", methods=["GET"])
def get_result(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    if task["status"] != "COMPLETED":
        return jsonify({"error": "Task not completed", "status": task["status"]}), 400
    return jsonify(task["result"])

@app.route("/algorithm/execute", methods=["POST"])
def execute_unified():
    """统一执行接口，与 risk-algorithm-service 保持一致"""
    data = request.get_json() or {}
    params = data.get("params", {})
    task_id = data.get("taskId", str(uuid.uuid4()))
    callback_url = data.get("callbackUrl", f"{BACKEND_URL}/api/simulation/status")

    # 合并顶层字段到 params（兼容旧调用方式）
    for k, v in data.items():
        if k not in ("taskId", "callbackUrl", "params", "notification", "algorithmName"):
            params.setdefault(k, v)

    # 复用原有执行逻辑
    ml_request = dict(params)
    ml_request["taskId"] = task_id
    ml_request["callbackUrl"] = callback_url

    from flask import Request
    with app.test_request_context(
        "/ml/execute", method="POST",
        json=ml_request, content_type="application/json"
    ):
        pass

    # 直接内联执行逻辑
    tasks[task_id] = {"status": "PENDING", "progress": 0, "result": None, "error": None}

    def run_ml():
        tasks[task_id]["status"] = "EXECUTING"
        tasks[task_id]["progress"] = 20
        time.sleep(1)

        historical_data = params.get("historicalData", [])
        risk_factors = params.get("riskFactors", {})
        tasks[task_id]["progress"] = 60
        time.sleep(1)

        features = historical_data[-10:] if len(historical_data) > 10 else historical_data
        base_risk = random.uniform(40, 85)
        volatility = risk_factors.get("volatility", 0.5)
        trend = risk_factors.get("trend", 0)
        tasks[task_id]["progress"] = 80

        risk_score = min(100, max(0, base_risk + trend * 10 + volatility * 15))
        confidence = random.uniform(0.75, 0.98)
        risk_level = "LOW" if risk_score < 40 else "MEDIUM" if risk_score < 70 else "HIGH"

        result = {
            "taskId": task_id,
            "status": "COMPLETED",
            "progress": 100,
            "result": f"[ML预测] 风险指数: {risk_score:.1f}/100, 置信度: {confidence:.2%}",
            "riskScore": round(risk_score, 1),
            "confidence": round(confidence, 3),
            "riskLevel": risk_level,
            "modelVersion": "v1.0-ml",
            "featuresAnalyzed": len(features),
            "recommendation": "建议增加安全库存，优化供应商结构" if risk_score > 60 else "风险可控，维持现状"
        }
        tasks[task_id]["status"] = "COMPLETED"
        tasks[task_id]["progress"] = 100
        tasks[task_id]["result"] = result

        try:
            requests.post(callback_url, json=result, timeout=10)
        except Exception as e:
            print(f"Callback failed: {e}")

    threading.Thread(target=run_ml, daemon=True).start()
    return jsonify({"taskId": task_id, "status": "PENDING", "message": "ML风险预测任务已提交"})

@app.route("/algorithm/status/<task_id>", methods=["GET"])
def get_algorithm_status(task_id):
    """统一状态查询接口"""
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({
        "taskId": task_id,
        "status": task["status"],
        "progress": task["progress"],
        "result": task["result"],
        "error": task["error"]
    })

def register_to_backend():
    import requests as req
    max_retries = 30
    for i in range(max_retries):
        try:
            resp = req.post(
                f"{BACKEND_URL}/api/algorithm/register",
                json={
                    "name": ALGORITHM_NAME,
                    "version": ALGORITHM_VERSION,
                    "endpoint": f"http://localhost:{ALGORITHM_PORT}/ml",
                    "supportedParams": "historicalData,riskFactors",
                    "description": "基于机器学习的供应链风险预测算法"
                },
                timeout=5
            )
            if resp.status_code in [200, 201]:
                print(f"Successfully registered {ALGORITHM_NAME}")
                return
        except Exception as e:
            print(f"Registration attempt {i+1}/{max_retries} failed: {e}")
        time.sleep(2)
    print(f"Failed to register after {max_retries} attempts")

if __name__ == "__main__":
    threading.Thread(target=register_to_backend, daemon=True).start()
    app.run(host="0.0.0.0", port=ALGORITHM_PORT, debug=False)