# Algorithm Framework - 算法服务基础框架

提供算法服务的公共功能，算法开发者只需专注算法逻辑本身。

## 框架功能

- ✅ 服务注册/发现（自动注册到后端）
- ✅ `/health` 健康检查
- ✅ `/algorithms` 算法列表
- ✅ `/apispec.json` API文档
- ✅ `/apidocs/` Swagger UI
- ✅ 异步执行 + callback回调
- ✅ CORS跨域

## 目录结构

```
algorithm-framework/
├── base/
│   ├── __init__.py
│   ├── algorithm_base.py      # 算法基类
│   ├── app_factory.py         # Flask应用工厂
│   └── service_runner.py      # 服务启动器
├── requirements.txt
└── README.md
```

## 核心设计原则

### 1. 算法核心可独立执行

算法类本身是纯Python类，不依赖Flask或网络，可直接调用。

### 2. 算法基类方法

| 方法 | 说明 |
|-----|------|
| `execute(params)` | 抽象方法，算法实现者重写此方法 |
| `run(params, callback_url)` | 同步执行，支持callback |
| `run_async(params, callback_url)` | 异步执行，立即返回taskId |

---

## 本地直接执行

不启动服务，直接调用算法类方法。

### 方式一：同步执行

```python
from algorithms.my_algorithm import MyAlgorithm

algo = MyAlgorithm()

result = algo.run({"param1": 50, "param2": 30})
print(result)
```

**输出：**
```python
{
    'taskId': 'uuid-string',
    'status': 'COMPLETED',
    'duration': 0.001,
    'result': '计算结果: 80',
    'riskScore': 80,
    'level': 'HIGH'
}
```

### 方式二：异步执行（带callback）

```python
from algorithms.my_algorithm import MyAlgorithm

algo = MyAlgorithm()

# 立即返回，后台异步执行
result = algo.run_async(
    {"param1": 50, "param2": 30},
    callback_url="http://localhost:8080/callback"
)

print(result)
```

**立即返回：**
```python
{'taskId': 'uuid-string', 'status': 'EXECUTING', 'message': 'my-algorithm 任务已启动'}
```

**Callback收到结果：**
```python
{
    'taskId': 'uuid-string',
    'status': 'COMPLETED',
    'duration': 2.001,
    'result': '计算结果: 80',
    'riskScore': 80,
    'level': 'HIGH'
}
```

### execute方法规范

算法只需实现`execute`方法，接收params字典，返回结果字典：

```python
def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
    # params: 输入参数，如 {"tariffRate": 0.25, "tradeVolume": 1000000}
    # return: 结果字典，如 {"riskScore": 75.5, "level": "HIGH"}
    pass
```

---

## 远程API调用

启动服务后，通过HTTP请求调用算法。

### 启动服务

```bash
pip install -r requirements.txt
python main.py --port 5002 --backend http://localhost:8080
```

### API接口列表

| 接口 | 方法 | 说明 |
|-----|------|------|
| `/health` | GET | 健康检查 |
| `/algorithms` | GET | 获取所有算法列表 |
| `/{algo_name}/execute` | POST | 执行指定算法 |
| `/apispec.json` | GET | OpenAPI规范 |
| `/apidocs/` | GET | Swagger UI文档 |

### 执行算法请求

```bash
curl -X POST http://localhost:5002/my-algorithm/execute \
  -H "Content-Type: application/json" \
  -d '{
    "param1": 50,
    "param2": 30,
    "callbackUrl": "http://localhost:8080/api/task/callback"
  }'
```

**响应（立即返回）：**
```json
{
    "taskId": "uuid-string",
    "status": "EXECUTING",
    "message": "my-algorithm 任务已启动"
}
```

### 获取算法列表

```bash
curl http://localhost:5002/algorithms
```

**响应：**
```json
{
    "algorithms": [
        {
            "name": "my-algorithm",
            "version": "1.0.0",
            "endpoint": "http://localhost:5002/my-algorithm",
            "supported_params": "param1,param2",
            "description": "我的算法"
        }
    ]
}
```

### 健康检查

```bash
curl http://localhost:5002/health
```

**响应：**
```json
{
    "status": "healthy",
    "service": "algorithm-service"
}
```

---

## 算法实现示例

### Step 1: 实现算法类

```python
# algorithms/my_algorithm.py
from algorithm_framework.base import AlgorithmBase
from typing import Dict, Any

class MyAlgorithm(AlgorithmBase):
    def __init__(self):
        super().__init__(
            name="my-algorithm",
            version="1.0.0",
            description="我的算法",
            supported_params="param1,param2"
        )

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        param1 = params.get("param1", 0)
        param2 = params.get("param2", 0)

        risk_score = param1 + param2

        return {
            "result": f"计算结果: {risk_score}",
            "riskScore": risk_score,
            "level": "HIGH" if risk_score > 70 else "MEDIUM" if risk_score > 40 else "LOW"
        }
```

### Step 2: 创建启动入口

```python
# main.py
from algorithm_framework.base import run_service
from algorithms.my_algorithm import MyAlgorithm

if __name__ == "__main__":
    run_service([MyAlgorithm()], service_port=5002)
```

---

## 开发新算法

1. 创建 `algorithms/` 目录
2. 实现算法类继承 `AlgorithmBase`
3. 实现 `execute(params)` 方法（纯算法逻辑）
4. 可选：创建 `main.py` 调用 `run_service([算法实例])` 启动服务

---

## 框架参数说明

| 参数 | 说明 | 默认值 |
|-----|------|-------|
| `name` | 算法唯一标识 | 必需 |
| `version` | 算法版本 | "1.0.0" |
| `description` | 算法描述 | "" |
| `supported_params` | 支持的参数列表 | "" |

---

## 完整示例

参考 `risk-ml-algorithm` 项目：
- algorithms/ml_algorithm.py - 机器学习算法实现
- main.py - 服务启动入口