# 算法服务接入规范

## 概述

本文档定义了算法服务（Algorithm Service）的接入规范，所有接入供应链控制塔的算法服务必须遵循此规范。

## 目录

- [1. 快速开始](#1-快速开始)
- [2. 接口规范](#2-接口规范)
- [3. 算法基类](#3-算法基类)
- [4. 请求响应格式](#4-请求响应格式)
- [5. 回调协议](#5-回调协议)
- [6. 注册到后端](#6-注册到后端)

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
│   ├── registry_service.py  # 算法注册服务
│   └── algorithm_service.py # 算法执行服务
├── controllers/
│   ├── __init__.py
│   └── api_controller.py    # API控制器
├── utils/
│   ├── __init__.py
│   └── http_client.py       # HTTP客户端
├── algorithms/               # 算法实现目录
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

### 2.2 健康检查接口

**请求**
```
GET /health
```

**响应**
```json
{
  "status": "healthy",
  "service": "multi-algorithm-service",
  "version": "1.0.0",
  "port": 5000,
  "algorithms": [
    "tariff-risk-algorithm",
    "risk-scenarios-algorithm"
  ]
}
```

### 2.3 算法执行接口

**请求**
```
POST /{algorithm_name}/execute
Content-Type: application/json

{
  "taskId": "可选，不提供则自动生成",
  "callbackUrl": "http://localhost:8080/api/simulation/status",
  ...其他算法特定参数
}
```

**响应 (200 OK)**
```json
{
  "taskId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "STARTED"
}
```

**响应 (404 Not Found)**
```json
{
  "error": "Algorithm tariff not found"
}
```

---

## 3. 算法基类

### 3.1 AlgorithmBase 抽象类

所有算法必须继承 `AlgorithmBase` 并实现以下接口：

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

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
    def supported_params(self) -> List[str]:
        """支持的参数列表"""
        pass

    @abstractmethod
    def execute(self, params: Dict[str, Any], task_id: str, callback_url: str) -> Dict[str, Any]:
        """
        执行算法

        Args:
            params: 执行参数 (字典)
            task_id: 任务ID
            callback_url: 状态回调URL

        Returns:
            执行结果字典
        """
        pass
```

### 3.2 算法实现示例

```python
from models.base import AlgorithmBase
from typing import Dict, Any, List

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
    def supported_params(self) -> List[str]:
        return ["param1", "param2"]

    def execute(self, params: Dict[str, Any], task_id: str, callback_url: str) -> Dict[str, Any]:
        # 算法逻辑
        return {
            'taskId': task_id,
            'result': '执行完成',
            'data': {}
        }
```

### 3.3 注册算法

在 `main.py` 中注册算法：

```python
from algorithms import MyAlgorithm

def create_app():
    app = Flask(__name__)
    registry_service.register(MyAlgorithm())
    # ...
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

## 6. 注册到后端

### 6.1 注册接口

启动时自动向控制塔后端注册：

```
POST http://localhost:8080/api/algorithm/register
Content-Type: application/json

{
  "name": "my-algorithm",
  "version": "1.0.0",
  "endpoint": "http://localhost:5000/my",
  "supportedParams": "param1,param2",
  "description": "我的算法"
}
```

### 6.2 注册时机

- 服务启动时注册
- 建议添加重试机制
- 注册失败不影响本地服务运行

---

## 7. 横向扩展

### 7.1 多实例部署

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

### 7.2 端口配置

```bash
# 实例1
export ALGORITHM_PORT=5001
python main.py

# 实例2
export ALGORITHM_PORT=5002
python main.py
```

每个实例启动后会自动注册到后端，后端会根据负载情况选择调用。

---

## 8. 错误处理

### 8.1 错误响应格式

```json
{
  "error": "错误描述",
  "code": "ERROR_CODE",
  "details": {}
}
```

### 8.2 错误码

| 错误码 | HTTP状态 | 说明 |
|-------|---------|------|
| ALGORITHM_NOT_FOUND | 404 | 算法不存在 |
| MISSING_CALLBACK_URL | 400 | 缺少回调URL |
| INVALID_PARAMS | 400 | 参数无效 |
| EXECUTION_ERROR | 500 | 算法执行错误 |
| CALLBACK_FAILED | 500 | 回调后端失败 |

---

## 9. 安全建议

1. **回调URL验证**: 生产环境应验证回调URL来源
2. **参数校验**: 严格校验输入参数
3. **超时控制**: 设置合理的执行超时时间
4. **日志记录**: 记录完整的执行日志

---

## 10. 联系支持

如有问题，请联系：algorithm@example.com