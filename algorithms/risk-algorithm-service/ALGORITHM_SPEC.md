# 算法服务接入规范

## 概述

本文档定义了算法服务（Algorithm Service）的接入规范，所有接入供应链控制塔的算法服务必须遵循此规范。

## 目录

- [1. 快速开始](#1-快速开始)
- [2. 接口规范](#2-接口规范)
- [3. 算法基类](#3-算法基类)
- [4. 请求响应格式](#4-请求响应格式)
- [5. 回调协议](#5-回调协议)
- [6. 算法注册中心](#6-算法注册中心)
- [7. 远程算法服务](#7-远程算法服务)
- [8. 横向扩展](#8-横向扩展)
- [9. 错误处理](#9-错误处理)
- [10. 安全建议](#10-安全建议)

---

## 1. 快速开始

### 1.1 环境要求

```
Python >= 3.8
flask >= 2.3.0
flasgger >= 0.9.7
requests >= 2.31.0
```

### 1.2 项目结构

```
algorithm-service/
├── config/
│   ├── __init__.py
│   └── settings.py          # 配置管理
├── models/
│   ├── __init__.py
│   ├── base.py              # 算法基类 (必须继承)
│   └── entities.py          # 数据实体
├── services/
│   ├── __init__.py
│   ├── registry_service.py  # 算法注册服务（统一注册中心）
│   ├── algorithm_service.py # 算法执行服务
│   └── discovery_service.py # 算法发现服务（自动发现本地/远程）
├── controllers/
│   ├── __init__.py
│   └── api_controller.py    # API控制器
├── utils/
│   ├── __init__.py
│   └── http_client.py       # HTTP客户端
├── algorithms/               # 算法实现目录（自动发现）
│   ├── __init__.py
│   └── your_algorithm.py    # 你的算法实现
├── main.py                   # 入口文件
└── requirements.txt
```

### 1.3 启动服务

```bash
# 设置环境变量
export BACKEND_URL=http://localhost:8080
export ALGORITHM_PORT=5000
export REMOTE_ALGORITHM_SERVICES=risk-ml-algorithm:http://localhost:5001

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

服务启动后访问：
- API服务：http://localhost:5000
- Swagger UI：http://localhost:5000/apidocs/

---

## 2. 接口规范

### 2.1 必须实现的接口

| 接口 | 方法 | 路径 | 说明 |
|-----|------|------|------|
| 健康检查 | GET | `/health` | 服务健康状态 |
| 算法执行 | POST | `/{algorithm_name}/execute` | 执行具体算法 |
| 算法列表 | GET | `/algorithms` | 获取所有算法列表 |
| 分类树 | GET | `/categories` | 获取分类层级结构 |
| 远程服务管理 | GET/POST | `/remote-services` | 管理远程算法服务 |
| 统一执行 | POST | `/algorithm/execute` | 统一执行入口（自动路由） |

### 2.2 健康检查接口

**请求**
```
GET /health
```

**响应**
```json
{
  "status": "healthy",
  "service": "algorithm-registry-center",
  "version": "2.0.0",
  "port": 5000,
  "algorithms": [
    "tariff-risk-algorithm",
    "risk-scenarios-algorithm"
  ],
  "remoteAlgorithms": [
    "ml-risk-prediction",
    "ml-demand-forecast"
  ]
}
```

### 2.3 算法列表接口

**请求**
```
GET /algorithms?includeRemote=true&category=risk&type=simulation
```

**响应**
```json
{
  "algorithms": [
    {
      "name": "tariff-risk-algorithm",
      "version": "1.0.0",
      "label": "关税风险模拟",
      "category": "risk",
      "type": "simulation",
      "description": "关税风险模拟算法",
      "isRemote": false,
      "paramsSchema": {...},
      "outputSchema": {...}
    },
    {
      "name": "ml-risk-prediction",
      "version": "1.0.0",
      "label": "ML风险预测",
      "category": "risk",
      "type": "classification",
      "description": "基于机器学习的风险预测",
      "isRemote": true,
      "endpoint": "http://localhost:5001/algorithm/execute"
    }
  ]
}
```

### 2.4 统一算法执行接口

**请求**
```
POST /algorithm/execute
Content-Type: application/json

{
  "algorithmName": "ml-risk-prediction",
  "taskId": "optional-task-id",
  "callbackUrl": "http://localhost:8080/api/simulation/status",
  "params": {
    "productId": "P001",
    "region": "APAC"
  }
}
```

**响应 (200 OK)**
```json
{
  "taskId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "STARTED"
}
```

---

## 3. 算法基类

### 3.1 AlgorithmBase 抽象类

所有算法必须继承 `AlgorithmBase` 并实现以下接口：

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class AlgorithmBase(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """算法唯一名称"""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """算法版本"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """算法描述"""
        pass

    @property
    @abstractmethod
    def category(self) -> str:
        """一级分类: risk / plan / inventory / supply_chain"""
        pass

    @property
    @abstractmethod
    def algo_type(self) -> str:
        """二级分类: simulation / classification / assessment / ..."""
        pass

    @property
    def params_schema(self) -> Dict:
        """输入参数 JSON Schema"""
        return {"type": "object", "properties": {}}

    @property
    def output_schema(self) -> Dict:
        """输出结果 JSON Schema"""
        return {"type": "object", "properties": {}}

    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """算法核心逻辑"""
        pass
```

### 3.2 算法实现示例

```python
from models.base import AlgorithmBase
from typing import Dict, Any

class MyAlgorithm(AlgorithmBase):
    @property
    def name(self) -> str:
        return "my-algorithm"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "我的算法"

    @property
    def category(self) -> str:
        return "risk"

    @property
    def algo_type(self) -> str:
        return "simulation"

    @property
    def params_schema(self) -> Dict:
        return {
            "type": "object",
            "required": ["param1"],
            "properties": {
                "param1": {"type": "string", "description": "参数1"}
            }
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {'result': '执行完成', 'data': params}
```

### 3.3 自动注册

算法只需放在 `algorithms/` 目录下，服务启动时会自动发现并注册：

```
algorithms/
├── __init__.py
├── tariff_algorithm.py      # 自动发现
├── scenario_algorithm.py    # 自动发现
└── your_algorithm.py        # 自动发现
```

---

## 4. 请求响应格式

### 4.1 关税风险算法

**算法名称**: `tariff-risk-algorithm`
**端点**: `http://localhost:5000/tariff/execute`

**请求参数**
| 参数 | 类型 | 必填 | 说明 |
|-----|------|------|------|
| taskId | string | 否 | 任务ID |
| callbackUrl | string | 是 | 回调URL |
| tariffRate | integer | 是 | 关税税率 (10 或 20) |

**请求示例**
```json
{
  "taskId": "task-001",
  "callbackUrl": "http://localhost:8080/api/simulation/status",
  "tariffRate": 20
}
```

**响应格式**
```json
{
  "taskId": "task-001",
  "result": "【执行完成】关税20%，利润不足，建议转产",
  "tariffRate": 20,
  "product": "产品A",
  "originalProfit": 1000,
  "recommendation": "转产"
}
```

### 4.2 风险场景算法

**算法名称**: `risk-scenarios-algorithm`
**端点**: `http://localhost:5000/scenario/execute`

**请求参数**
| 参数 | 类型 | 必填 | 说明 |
|-----|------|------|------|
| taskId | string | 否 | 任务ID |
| callbackUrl | string | 是 | 回调URL |
| scenarioType | string | 是 | 场景类型 |

**场景类型枚举值**
| 值 | 说明 |
|---|---|
| trade_war | 贸易战风险 |
| supply_disruption | 供应链中断 |
| demand_volatility | 需求波动 |
| logistics_delay | 物流延迟 |

**请求示例**
```json
{
  "taskId": "task-002",
  "callbackUrl": "http://localhost:8080/api/simulation/status",
  "scenarioType": "trade_war"
}
```

**响应格式**
```json
{
  "taskId": "task-002",
  "result": "【执行完成】贸易战风险分析完成，风险指数: 80/100",
  "scenarioType": "trade_war",
  "scenarioName": "贸易战风险",
  "riskScore": 80.0,
  "riskLevel": "HIGH",
  "recommendation": "启动应急预案，考虑多元供应链策略"
}
```

---

## 5. 回调协议

算法执行过程中需要回调后端服务，报告状态和结果。

### 5.1 状态回调

算法执行过程中定期调用此接口报告进度：

```
POST {callbackUrl}
Content-Type: application/json

{
  "taskId": "task-001",
  "status": "【执行中】处理数据，进度50%",
  "progress": 50
}
```

### 5.2 结果回调

算法执行完成后调用此接口提交结果：

```
POST {callbackUrl}/result
Content-Type: application/json

{
  "taskId": "task-001",
  "result": "【执行完成】...",
  ...其他结果字段
}
```

### 5.3 回调时机建议

| 阶段 | 建议进度 | 说明 |
|-----|---------|------|
| 开始 | 10% | 初始化 |
| 数据加载 | 30% | 读取输入数据 |
| 处理中 | 50-70% | 核心计算 |
| 生成结果 | 90% | 整理输出 |
| 完成 | 100% | 执行完成 |

---

## 6. 算法注册中心

### 6.1 架构概述

`risk-algorithm-service` 作为算法注册中心，支持：
- **本地算法自动发现**：扫描 `algorithms/` 目录自动注册
- **远程算法服务代理**：发现并代理调用其他算法服务（如 `risk-ml-algorithm`）
- **统一执行入口**：`/algorithm/execute` 自动路由到本地或远程算法
- **后端直连模式**：后端 Java 服务通过注册中心同步算法元数据，直接调用算法执行端点

### 6.2 架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           供应链控制塔系统                                │
│                                                                         │
│  ┌──────────────┐    ┌──────────────────┐    ┌─────────────────────────┐ │
│  │    前端      │───▶│  后端 Java       │───▶│  算法注册中心            │ │
│  │  (Vue)      │    │  (risk-basic)    │    │  (risk-algorithm-svc)   │ │
│  │             │    │                  │    │  端口: 5000              │ │
│  │             │◀───│  同步算法列表     │◀───│  • 本地算法自动发现      │ │
│  │             │    │  每60秒刷新       │    │  • 远程算法代理          │ │
│  └──────────────┘    └──────────────────┘    └───────────┬─────────────┘ │
│                                                          │               │
│                                    ┌─────────────────────┼─────────────┐ │
│                                    │                     │             │ │
│                                    ▼                     ▼             │ │
│                         ┌──────────────────┐   ┌────────────────────┐  │ │
│                         │   本地算法        │   │   远程算法服务       │  │ │
│                         │  • tariff-risk   │   │  risk-ml-algorithm │  │ │
│                         │  • risk-scenarios│   │  端口: 5001        │  │ │
│                         └──────────────────┘   └─────────┬──────────┘  │ │
│                                                         │              │ │
│                                    ┌────────────────────┴───────────┐   │ │
│                                    │  回调 (callbackUrl)              │   │ │
│                                    │  POST /api/simulation/status    │   │ │
│                                    │  POST /api/simulation/result   │   │ │
│                                    └────────────────────────────────┘   │ │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.3 核心服务

#### DiscoveryService（发现服务）

```python
class AlgorithmDiscoveryService:
    def discover_local_algorithms(self, package_name: str = "algorithms") -> List[AlgorithmBase]:
        """自动发现本地 algorithms/ 目录下的算法"""

    def register_remote_service(self, name: str, base_url: str, ...) -> None:
        """注册远程算法服务"""

    def discover_remote_algorithms(self, force_refresh: bool = False) -> List[AlgorithmInfo]:
        """从远程服务获取算法列表（缓存5分钟）"""

    def execute_remote_algorithm(self, algorithm_name: str, params: Dict) -> Dict:
        """代理执行远程算法，保持 callbackUrl 透传"""
```

#### RegistryService（注册服务）

```python
class RegistryService:
    def register(self, algorithm: AlgorithmBase) -> None:
        """注册本地算法"""

    def register_remote(self, algorithm_info: AlgorithmInfo) -> None:
        """注册远程算法元数据"""

    def get(self, name: str) -> Optional[AlgorithmBase]:
        """获取本地算法"""

    def get_remote(self, name: str) -> Optional[AlgorithmInfo]:
        """获取远程算法信息"""

    def get_all_algorithms(self) -> List[Dict]:
        """获取所有算法（含本地和远程）"""
```

### 6.4 后端集成流程

后端 Java 服务通过以下方式与算法注册中心集成：

1. **启动时同步**：后端启动时从注册中心获取算法列表
2. **定时刷新**：每60秒自动同步算法列表和分类树
3. **统一执行**：后端直接调用算法注册中心提供的执行端点

```java
// 后端配置 (application.properties)
app.algorithm.registry-url=http://localhost:5000
app.algorithm.sync-interval=60000
```

后端通过 `SimulationController.executeAlgorithm()` 统一入口，查询注册中心获取算法端点，然后直接调用执行。

---

## 7. 远程算法服务

### 7.1 注册远程服务

#### 通过环境变量配置

```bash
export REMOTE_ALGORITHM_SERVICES=risk-ml-algorithm:http://localhost:5001,other-service:http://localhost:5002
```

多个服务用逗号分隔，格式：`服务名:URL`

#### 通过 API 动态添加

```bash
POST /remote-services
Content-Type: application/json

{
  "name": "risk-ml-algorithm",
  "baseUrl": "http://localhost:5001",
  "algorithmsEndpoint": "/algorithms",
  "executeEndpoint": "/algorithm/execute"
}
```

### 7.2 远程服务要求

远程算法服务需要提供以下接口：

| 接口 | 方法 | 路径 | 说明 |
|-----|------|------|------|
| 健康检查 | GET | `/health` | 服务健康状态 |
| 算法列表 | GET | `/algorithms` | 获取算法元数据 |
| 算法执行 | POST | `/algorithm/execute` | 执行算法 |

### 7.3 远程服务示例 (risk-ml-algorithm)

```python
# risk-ml-algorithm/main.py
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/algorithms')
def list_algorithms():
    return jsonify({
        'algorithms': [
            {
                'name': 'ml-risk-prediction',
                'version': '1.0.0',
                'description': 'ML风险预测',
                'category': 'risk',
                'type': 'classification',
                'label': 'ML风险预测',
                'paramsSchema': {...},
                'outputSchema': {...}
            }
        ]
    })

@app.route('/algorithm/execute', methods=['POST'])
def execute():
    data = request.get_json()
    # 执行ML算法
    return jsonify({'taskId': data.get('taskId'), 'status': 'COMPLETED', 'result': {...}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
```

---

## 8. 横向扩展

### 8.1 多实例部署

```
                    ┌─────────────────┐
                    │   Load Balancer │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Algorithm Svc  │ │  Algorithm Svc  │ │  Algorithm Svc  │
│   Instance 1   │ │   Instance 2    │ │   Instance N    │
│   Port: 5001    │ │   Port: 5002    │ │   Port: 5xxx    │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

### 8.2 端口配置

```bash
# 实例1
export ALGORITHM_PORT=5001
python main.py

# 实例2
export ALGORITHM_PORT=5002
python main.py
```

---

## 9. 错误处理

### 9.1 错误响应格式

```json
{
  "error": "错误描述",
  "code": "ERROR_CODE",
  "details": {}
}
```

### 9.2 错误码

| 错误码 | HTTP状态 | 说明 |
|-------|---------|------|
| ALGORITHM_NOT_FOUND | 404 | 算法不存在 |
| MISSING_CALLBACK_URL | 400 | 缺少回调URL |
| INVALID_PARAMS | 400 | 参数无效 |
| EXECUTION_ERROR | 500 | 算法执行错误 |
| CALLBACK_FAILED | 500 | 回调后端失败 |
| REMOTE_SERVICE_UNAVAILABLE | 503 | 远程服务不可用 |

---

## 10. 安全建议

1. **回调URL验证**: 生产环境应验证回调URL来源
2. **参数校验**: 严格校验输入参数
3. **超时控制**: 设置合理的执行超时时间
4. **日志记录**: 记录完整的执行日志
5. **远程服务认证**: 远程服务间通信建议使用API Key或JWT认证

---

## 11. 联系支持

如有问题，请联系：algorithm@example.com