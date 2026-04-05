# 算法服务 (Algorithm Services)

微服务架构的算法服务集合，支持两级分类、动态参数、执行通知，独立部署和横向扩展。

## 目录

- [1. 架构概述](#1-架构概述)
- [2. 算法两级分类体系](#2-算法两级分类体系)
- [3. 算法基类设计](#3-算法基类设计)
- [4. 通知机制](#4-通知机制)
- [5. 服务列表](#5-服务列表)
- [6. 本地运行](#6-本地运行)
- [7. 算法服务接口规范](#7-算法服务接口规范)
- [8. 如何编写新算法](#8-如何编写新算法)
- [9. 测试用例](#9-测试用例)
- [10. Java后端接入详解](#10-java后端接入详解)

---

## 1. 架构概述

### 1.1 设计原则

- **两级分类**：算法按业务域（一级）和算法用途（二级）组织，前端可按分类筛选和执行
- **参数/返回值均为 JSON**：`execute(params)` 入参和出参均为任意 JSON dict，无固定结构限制
- **执行通知**：调用时可传入通知类型和通知人，算法完成后自动发送通知（接口预留）
- **服务自动注册**：算法服务启动后自动注册到后端管理系统
- **异步执行+回调**：支持同步/异步执行，结果通过 callbackUrl 回调通知

### 1.2 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                  前端 (Vue3 + Element Plus)                   │
│  风险分析页 /risk/analysis    风险场景页 /risk/scenarios       │
│  按 category/type 筛选算法    专注 risk/classification 场景    │
└─────────────────────────┬───────────────────────────────────┘
                          │ POST /api/simulation/execute
┌─────────────────────────▼───────────────────────────────────┐
│                  Java 后端 (localhost:8080)                   │
│  GET  /api/algorithm/categories    算法分类树                 │
│  GET  /api/algorithm/list          算法列表（支持过滤）        │
│  POST /api/simulation/execute      通用执行入口               │
│  POST /api/simulation/status       算法回调（状态）           │
│  POST /api/simulation/result       算法回调（结果）           │
└─────────────────────────┬───────────────────────────────────┘
                          │ POST /algorithm/execute
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ risk-algorithm│ │  risk-ml-     │ │  future-      │
│ -service      │ │  algorithm    │ │  algorithm    │
│ (端口5000)    │ │  (端口5001)   │ │  (端口5xxx)   │
└───────────────┘ └───────────────┘ └───────────────┘
```

---

## 2. 算法两级分类体系

### 2.1 分类定义

| 一级 (category) | 二级 (type) | 说明 | 示例算法 |
|---|---|---|---|
| risk（风险） | simulation | 风险模拟 | 关税风险模拟 |
| risk（风险） | classification | 风险分类定义 | 风险场景分析 |
| risk（风险） | assessment | 综合评估 | ML风险评估 |
| plan（计划） | order_simulation | 订单模拟 | 关税下订单影响模拟 |
| plan（计划） | production_transfer | 转产规划 | 转产可行性评估 |
| plan（计划） | capacity_planning | 产能规划 | 产能优化建议 |
| inventory（库存） | consumption | 消耗模拟 | 库存消耗速度预测 |
| inventory（库存） | replenishment | 补货建议 | 安全库存及补货策略 |
| inventory（库存） | shortage_risk | 短缺风险 | 缺货风险预警 |
| supply_chain（供应链） | disruption | 中断模拟 | 供应链中断影响模拟 |
| supply_chain（供应链） | optimization | 优化建议 | 多供应商优化 |

### 2.2 注意事项

- 每个算法必须声明 `category` 和 `algo_type` 属性
- 前端通过 `GET /api/algorithm/categories` 动态获取分类树，无需硬编码
- `风险分析页` 展示所有分类的算法，`风险场景页` 聚焦 `risk/classification`

---

## 3. 算法基类设计

### 3.1 必须实现的属性

```python
from models.base import AlgorithmBase
from typing import Dict, Any

class MyAlgorithm(AlgorithmBase):
    @property
    def name(self) -> str:
        return "my-algorithm"          # 唯一标识，用于注册和调用

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "我的算法描述"

    @property
    def category(self) -> str:
        return "risk"                  # 一级分类

    @property
    def algo_type(self) -> str:
        return "simulation"            # 二级分类

    # 可选覆盖 ──────────────────────────────────────────────────────
    @property
    def label(self) -> str:
        return "关税风险模拟"           # 前端显示名称（中文）

    @property
    def params_schema(self) -> Dict:
        return {
            "type": "object",
            "required": ["tariffRate"],
            "properties": {
                "tariffRate": {
                    "type": "integer",
                    "description": "关税税率（%）",
                    "example": 25
                }
            }
        }

    @property
    def output_schema(self) -> Dict:
        return {
            "type": "object",
            "properties": {
                "riskScore": {"type": "number"},
                "riskLevel": {"type": "string"}
            }
        }

    # ── 核心：execute 只关注业务逻辑 ─────────────────────────────
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        tariff_rate = params.get("tariffRate", 10)
        risk_score = min(100, tariff_rate * 3)
        return {
            "result": f"关税{tariff_rate}%，风险评分{risk_score}",
            "riskScore": risk_score,
            "riskLevel": "HIGH" if risk_score > 60 else "LOW"
        }
        # 注意：无需返回 taskId/status/duration，由基类负责补充
```

### 3.2 基类提供的方法

| 方法 | 说明 |
|---|---|
| `execute(params)` | **子类实现**，纯业务逻辑，params/返回值均为 JSON dict |
| `run(params, callback_url, notification_context)` | 同步执行，自动补充 taskId/status/duration，支持回调和通知 |
| `run_async(params, callback_url, notification_context)` | 异步执行，立即返回 taskId |
| `get_info()` | 返回算法元信息（含 category/type/paramsSchema/outputSchema） |

---

## 4. 通知机制

### 4.1 调用时传入通知上下文

```json
POST /algorithm/execute
{
  "algorithmName": "tariff-risk-algorithm",
  "callbackUrl": "http://localhost:8080/api/simulation/status",
  "params": {
    "tariffRate": 25
  },
  "notification": {
    "type": "email",
    "recipients": ["user@example.com", "admin@corp.com"],
    "title": "关税风险模拟完成通知"
  }
}
```

### 4.2 支持的通知类型

| type | 说明 |
|---|---|
| `none` | 不通知（默认） |
| `email` | 邮件通知 |
| `sms` | 短信通知 |
| `webhook` | Webhook 回调（recipients 为 URL 列表） |
| `im` | 即时消息（企业微信/钉钉等） |

### 4.3 通知实现状态

`notification.py` 中所有通知方法已定义接口、实现留空，接入消息中台后填充即可：

```python
class NotificationService:
    def notify_email(self, recipients, title, content, task_result): pass   # 待实现
    def notify_sms(self, recipients, content): pass                          # 待实现
    def notify_webhook(self, url, payload): pass                             # 待实现
    def notify_im(self, recipients, content): pass                          # 待实现
```

---

## 5. 服务列表

| 服务 | 端口 | 算法名称 | category | type |
|---|---|---|---|---|
| risk-algorithm-service | 5000 | tariff-risk-algorithm | risk | simulation |
| risk-algorithm-service | 5000 | risk-scenarios-algorithm | risk | classification |
| risk-ml-algorithm | 5001 | risk-ml-algorithm | risk | assessment |

---

## 6. 本地运行

### 6.1 启动风险算法服务 (端口5000)

```bash
cd d:/12.code/test/sci/risk/algorithms/risk-algorithm-service
pip install -r requirements.txt
python main.py
```

### 6.2 启动ML算法服务 (端口5001)

```bash
cd d:/12.code/test/sci/risk/algorithms/risk-ml-algorithm
pip install -r requirements.txt
python main.py
```

### 6.3 访问服务

- API服务：http://localhost:5000
- Swagger UI：http://localhost:5000/apidocs/
- 算法分类树：http://localhost:5000/categories
- 按分类查询：http://localhost:5000/algorithms?category=risk&type=simulation

---

## 7. 算法服务接口规范

### 7.1 获取两级分类树（新）

```
GET /categories
```

**响应：**
```json
{
  "categories": [
    {
      "category": "risk",
      "label": "风险",
      "types": [
        { "type": "simulation", "label": "风险模拟", "count": 1 },
        { "type": "classification", "label": "风险分类", "count": 1 }
      ]
    }
  ]
}
```

### 7.2 获取算法列表（支持过滤）

```
GET /algorithms?category=risk&type=simulation
```

**响应：**
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
      "paramsSchema": {
        "type": "object",
        "required": ["tariffRate"],
        "properties": {
          "tariffRate": { "type": "integer", "description": "关税税率（%）", "example": 25 }
        }
      },
      "outputSchema": { ... }
    }
  ]
}
```

### 7.3 统一执行接口（推荐）

```
POST /algorithm/execute
Content-Type: application/json

{
  "algorithmName": "tariff-risk-algorithm",
  "taskId": "可选",
  "callbackUrl": "http://localhost:8080/api/simulation/status",
  "params": {
    "tariffRate": 25,
    "productId": "P001"
  },
  "notification": {
    "type": "email",
    "recipients": ["user@example.com"],
    "title": "算法执行通知"
  }
}
```

### 7.4 旧版执行接口（保留兼容）

```
POST /{algorithm_name}/execute
Content-Type: application/json

{
  "taskId": "可选",
  "callbackUrl": "http://localhost:8080/api/simulation/status",
  "tariffRate": 20,
  "notification": { "type": "none" }
}
```

---

## 8. 如何编写新算法

### Step 1: 创建算法类

```python
# risk-algorithm-service/algorithms/my_algorithm.py
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
        return "我的自定义算法"

    @property
    def label(self) -> str:
        return "自定义算法"        # 前端展示名（中文）

    @property
    def category(self) -> str:
        return "risk"              # 一级分类

    @property
    def algo_type(self) -> str:
        return "simulation"        # 二级分类

    @property
    def params_schema(self) -> Dict:
        return {
            "type": "object",
            "required": ["param1"],
            "properties": {
                "param1": {
                    "type": "integer",
                    "description": "参数1说明",
                    "example": 50
                }
            }
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        param1 = params.get("param1", 0)
        result = param1 * 2
        return {
            "result": f"计算结果: {result}",
            "riskScore": result,
            "riskLevel": "HIGH" if result > 60 else "LOW"
        }
```

### Step 2: 注册算法

编辑 `risk-algorithm-service/main.py`：

```python
from algorithms.my_algorithm import MyAlgorithm
registry_service.register(MyAlgorithm())
```

### Step 3: 验证

```bash
curl http://localhost:5000/categories
curl http://localhost:5000/algorithms?category=risk
curl -X POST http://localhost:5000/algorithm/execute \
  -H "Content-Type: application/json" \
  -d '{"algorithmName":"my-algorithm","callbackUrl":"http://localhost:8080/api/simulation/status","params":{"param1":50}}'
```

---

## 9. 测试用例

### 9.1 直接测试算法类（无需启动服务）

```python
import sys
sys.path.insert(0, 'd:/12.code/test/sci/risk/algorithms/risk-algorithm-service')

from algorithms.tariff_algorithm import TariffRiskAlgorithm
from algorithms.scenario_algorithm import RiskScenarioAlgorithm

# 测试关税算法
algo = TariffRiskAlgorithm()
result = algo.run({"tariffRate": 25})
print(result)
# 输出: {taskId: ..., status: COMPLETED, riskScore: 80, riskLevel: HIGH, ...}

# 测试场景算法（带通知配置）
algo2 = RiskScenarioAlgorithm()
result2 = algo2.run(
    {"scenarioType": "trade_war"},
    notification_context={"type": "email", "recipients": ["user@example.com"]}
)
print(result2)
```

### 9.2 HTTP 接口测试

```bash
# 获取分类树
curl http://localhost:5000/categories

# 按分类获取算法
curl "http://localhost:5000/algorithms?category=risk&type=simulation"

# 统一执行接口
curl -X POST http://localhost:5000/algorithm/execute \
  -H "Content-Type: application/json" \
  -d '{
    "algorithmName": "tariff-risk-algorithm",
    "callbackUrl": "http://localhost:8080/api/simulation/status",
    "params": {"tariffRate": 25},
    "notification": {"type": "none"}
  }'

# 旧版兼容接口（依然有效）
curl -X POST http://localhost:5000/tariff/execute \
  -H "Content-Type: application/json" \
  -d '{"callbackUrl":"http://localhost:8080/api/simulation/status","tariffRate":20}'
```

---

## 10. Java后端接入详解

### 10.1 新增接口

| 接口 | 方法 | 说明 |
|---|---|---|
| `/api/algorithm/categories` | GET | **新** 获取两级分类树 |
| `/api/algorithm/list` | GET | 获取算法列表，支持 `?category=risk&type=simulation` 过滤 |
| `/api/simulation/execute` | POST | **新** 通用执行入口（含 notification） |

### 10.2 通用执行接口

```bash
POST http://localhost:8080/api/simulation/execute
{
  "algorithmName": "tariff-risk-algorithm",
  "params": { "tariffRate": 25 },
  "notification": {
    "type": "email",
    "recipients": ["user@example.com"],
    "title": "风险模拟完成"
  }
}
```

**响应：**
```json
{ "taskId": "uuid", "status": "EXECUTING", "message": "任务已启动" }
```

### 10.3 接收算法回调

算法执行完成后后端自动收到两个回调：

```
POST /api/simulation/status  → 进度更新 { taskId, status, progress }
POST /api/simulation/result  → 结果回调 { taskId, riskScore, riskLevel, ... }
```

### 10.4 Java后端启动

```bash
cd d:/12.code/test/sci/risk/backend/risk-basic-service
./mvnw spring-boot:run
```

---

## 附录：算法返回值规范

`execute()` 方法返回字典，基类会自动追加以下字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `taskId` | string | 任务ID（基类追加） |
| `status` | string | COMPLETED / FAILED（基类追加） |
| `duration` | number | 执行耗时秒（基类追加） |
| `result` | string | 执行结果描述（算法自定义） |
| `riskScore` | number | 风险评分 0-100（推荐包含） |
| `riskLevel` | string | LOW / MEDIUM / HIGH（推荐包含） |
| `recommendation` | string | 应对建议（推荐包含） |


## 目录

- [1. 架构概述](#1-架构概述)
- [2. 目录结构](#2-目录结构)
- [3. 算法基类设计](#3-算法基类设计)
- [4. 服务列表](#4-服务列表)
- [5. 本地运行](#5-本地运行)
- [6. 后端程序调用算法服务](#6-后端程序调用算法服务)
- [7. 算法服务接口规范](#7-算法服务接口规范)
- [8. 如何编写独立算法](#8-如何编写独立算法)
- [9. 测试用例](#9-测试用例)
- [10. 接入后端系统](#10-接入后端系统)

---

## 1. 架构概述

### 1.1 设计原则

- **算法核心可独立执行**：算法类是纯Python类，不依赖Flask或网络，可直接调用
- **服务自动注册**：算法服务启动后自动注册到后端管理系统
- **异步执行+回调**：支持同步/异步执行，结果通过callback URL回调通知
- **微服务架构**：每个算法服务独立部署，使用不同端口

### 1.2 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     后端管理系统 (localhost:8080)              │
│                   /api/algorithm/register                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ risk-algorithm│ │  risk-ml-     │ │  future-      │
│ -service      │ │  algorithm    │ │  algorithm    │
│ (端口5000)    │ │  (端口5001)   │ │  (端口5xxx)   │
└───────────────┘ └───────────────┘ └───────────────┘
        │                 │
        ▼                 ▼
┌───────────────┐ ┌───────────────┐
│ tariff-risk   │ │ risk-scenarios│
│ -algorithm    │ │ -algorithm    │
└───────────────┘ └───────────────┘
```

---

## 2. 目录结构

```
algorithms/
├── algorithm-framework/              # 算法框架公共模块
│   ├── base/
│   │   ├── algorithm_base.py       # 算法基类 (必须继承)
│   │   ├── app_factory.py          # Flask应用工厂
│   │   └── service_runner.py       # 服务启动器
│   ├── requirements.txt
│   └── README.md
│
├── risk-algorithm-service/           # 风险算法微服务 (端口5000)
│   ├── algorithms/
│   │   ├── tariff_algorithm.py     # 关税风险算法
│   │   └── scenario_algorithm.py   # 风险场景算法
│   ├── models/
│   │   ├── base.py                 # 算法基类
│   │   └── entities.py             # 数据实体
│   ├── services/
│   │   ├── algorithm_service.py    # 算法执行服务
│   │   └── registry_service.py     # 算法注册服务
│   ├── controllers/
│   │   └── api_controller.py        # API控制器
│   ├── config/
│   │   └── settings.py             # 配置管理
│   ├── utils/
│   │   └── http_client.py          # HTTP客户端
│   ├── main.py                      # 入口文件
│   ├── requirements.txt
│   └── ALGORITHM_SPEC.md           # 接入规范文档
│
├── risk-ml-algorithm/               # ML算法服务 (端口5001)
│   ├── main.py
│   └── requirements.txt
│
└── README.md                        # 本文档
```

---

## 3. 算法基类设计

### 3.1 AlgorithmBase 抽象类

所有算法必须继承 `AlgorithmBase` 并实现以下属性和方法：

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

### 3.2 基类提供的方法

| 方法 | 说明 |
|-----|------|
| `execute(params, task_id, callback_url)` | 抽象方法，算法实现者重写此方法 |
| `run(params, callback_url)` | 同步执行，支持callback |
| `run_async(params, callback_url)` | 异步执行，立即返回taskId |
| `get_info()` | 获取算法元信息 |

---

## 4. 服务列表

| 服务 | 端口 | 算法 |
|-----|------|------|
| risk-algorithm-service | 5000 | tariff-risk-algorithm, risk-scenarios-algorithm |
| risk-ml-algorithm | 5001 | risk-ml-algorithm |

---

## 5. 本地运行

### 5.1 启动风险算法服务 (端口5000)

```bash
cd d:/12.code/test/sci/risk/algorithms/risk-algorithm-service
pip install -r requirements.txt
python main.py
```

### 5.2 启动ML算法服务 (端口5001)

```bash
cd d:/12.code/test/sci/risk/algorithms/risk-ml-algorithm
pip install -r requirements.txt
python main.py
```

### 5.3 停止服务

```powershell
# Windows查找占用端口的进程
netstat -ano | findstr :5000
netstat -ano | findstr :5001

# 停止指定进程（假设PID为12345）
taskkill /PID 12345 /F
```

### 5.4 访问服务

- API服务：http://localhost:5000
- Swagger UI：http://localhost:5000/apidocs/

---

## 6. 后端程序调用算法服务

### 6.1 注册算法服务到后端

算法服务启动时会自动注册到后端，调用以下接口：

```
POST /api/algorithm/register
Content-Type: application/json

{
    "name": "tariff-risk-algorithm",
    "version": "1.0.0",
    "endpoint": "http://localhost:5000/tariff",
    "supportedParams": "tariffRate",
    "description": "关税风险模拟算法"
}
```

### 6.2 后端触发算法执行

后端通过HTTP请求调用算法服务：

```python
import requests

def execute_algorithm(algorithm_name: str, params: dict, callback_url: str):
    """调用算法服务执行算法"""
    response = requests.post(
        f"http://localhost:5000/{algorithm_name}/execute",
        json={
            "taskId": "optional-task-id",
            "callbackUrl": callback_url,
            **params
        }
    )
    return response.json()

# 调用关税风险算法
result = execute_algorithm(
    algorithm_name="tariff",
    params={"tariffRate": 25},
    callback_url="http://localhost:8080/api/simulation/status"
)
```

### 6.3 接收算法执行结果

算法执行完成后会回调callback URL：

```python
# 后端接收回调的接口示例
@app.route('/api/simulation/status', methods=['POST'])
def receive_algorithm_result():
    data = request.get_json()
    task_id = data.get('taskId')
    result = data.get('result')
    # 处理结果
    return jsonify({"status": "received"})
```

---

## 7. 算法服务接口规范

### 7.1 健康检查

```
GET /health
```

**响应：**
```json
{
    "status": "healthy",
    "service": "multi-algorithm-service",
    "version": "1.0.0",
    "port": 5000,
    "algorithms": ["tariff-risk-algorithm", "risk-scenarios-algorithm"]
}
```

### 7.2 获取算法列表

```
GET /algorithms
```

**响应：**
```json
{
    "algorithms": [
        {
            "name": "tariff-risk-algorithm",
            "version": "1.0.0",
            "endpoint": "http://localhost:5000/tariff",
            "supported_params": "tariffRate",
            "description": "关税风险模拟算法"
        }
    ]
}
```

### 7.3 执行算法

```
POST /{algorithm_name}/execute
Content-Type: application/json

{
    "taskId": "可选，不提供则自动生成",
    "callbackUrl": "http://localhost:8080/api/simulation/status",
    ...其他算法特定参数
}
```

**响应：**
```json
{
    "taskId": "550e8400-e29b-41d4-a716-446655440000",
    "status": "STARTED"
}
```

---

## 8. 如何编写独立算法

### 8.1 方式一：使用algorithm-framework（推荐）

#### Step 1: 创建算法类

```python
# algorithms/my_algorithm.py
from algorithm_framework.base.algorithm_base import AlgorithmBase
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
        return "我的自定义算法"

    @property
    def supported_params(self) -> List[str]:
        return ["param1", "param2"]

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        param1 = params.get("param1", 0)
        param2 = params.get("param2", 0)
        result = param1 + param2
        return {
            "riskScore": result,
            "level": "HIGH" if result > 50 else "LOW",
            "result": f"计算结果: {result}"
        }
```

#### Step 2: 本地直接执行（不启动服务）

```python
from algorithms.my_algorithm import MyAlgorithm

algo = MyAlgorithm()

# 同步执行
result = algo.run({"param1": 50, "param2": 30})
print(result)
# 输出: {'taskId': 'uuid', 'status': 'COMPLETED', 'duration': 0.001, 'result': '计算结果: 80', 'riskScore': 80, 'level': 'HIGH'}

# 异步执行（带callback）
result = algo.run_async(
    {"param1": 50, "param2": 30},
    callback_url="http://localhost:8080/callback"
)
# 立即返回: {'taskId': 'uuid', 'status': 'EXECUTING', 'message': 'my-algorithm 任务已启动'}
```

#### Step 3: 启动为独立服务

```python
from algorithm_framework.base.service_runner import run_service
from algorithms.my_algorithm import MyAlgorithm

if __name__ == '__main__':
    run_service(
        algorithms=[MyAlgorithm()],
        service_port=5002,
        backend_url="http://localhost:8080"
    )
```

启动后访问：
- API: http://localhost:5002/my-algorithm/execute
- Swagger UI: http://localhost:5002/apidocs/

---

### 8.2 方式二：基于risk-algorithm-service扩展

#### Step 1: 在algorithms目录创建算法

```python
# risk-algorithm-service/algorithms/custom_algorithm.py
from models.base import AlgorithmBase
from typing import Dict, Any, List

class CustomAlgorithm(AlgorithmBase):
    @property
    def name(self) -> str:
        return "custom-algorithm"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "自定义算法"

    @property
    def supported_params(self) -> List[str]:
        return ["param1", "param2"]

    def execute(self, params: Dict[str, Any], task_id: str, callback_url: str) -> Dict[str, Any]:
        param1 = params.get("param1", 0)
        param2 = params.get("param2", 0)
        result = param1 + param2
        return {
            "taskId": task_id,
            "result": f"计算结果: {result}",
            "riskScore": result,
            "level": "HIGH" if result > 50 else "LOW"
        }
```

#### Step 2: 注册算法

编辑 `risk-algorithm-service/main.py`：

```python
from algorithms import TariffRiskAlgorithm, RiskScenarioAlgorithm
from algorithms.custom_algorithm import CustomAlgorithm  # 新增

def create_app():
    registry_service.register(TariffRiskAlgorithm())
    registry_service.register(RiskScenarioAlgorithm())
    registry_service.register(CustomAlgorithm())  # 新增
    ...
```

#### Step 3: 添加API路由

编辑 `risk-algorithm-service/controllers/api_controller.py`：

```python
from models.entities import TaskRequest
from config import settings

@api_blueprint.route('/custom/execute', methods=['POST'])
def execute_custom():
    """执行自定义算法"""
    algorithm = registry_service.get("custom")
    if not algorithm:
        return jsonify({'error': 'Algorithm custom not found'}), 404

    task_request = TaskRequest.from_dict(request.get_json())
    if not task_request.callback_url:
        return jsonify({'error': 'Missing callbackUrl'}), 400

    return jsonify(algorithm_service.execute(algorithm, task_request))
```

#### Step 4: 启动服务

```bash
cd risk-algorithm-service
pip install -r requirements.txt
python main.py
```

---

## 9. 测试用例

### 9.1 直接测试算法类

```python
import sys
sys.path.insert(0, 'd:/12.code/test/sci/risk/algorithms/risk-algorithm-service')

from algorithms.tariff_algorithm import TariffRiskAlgorithm

def test_tariff_algorithm():
    algo = TariffRiskAlgorithm()
    
    # 同步执行测试
    result = algo.run({"tariffRate": 10})
    print(f"同步执行结果: {result}")
    assert result["status"] == "COMPLETED"
    assert "result" in result
    print("✅ 关税算法同步测试通过")

def test_tariff_algorithm_async():
    algo = TariffRiskAlgorithm()
    
    # 异步执行测试
    result = algo.run_async(
        {"tariffRate": 25},
        callback_url="http://localhost:8080/callback"
    )
    print(f"异步执行结果: {result}")
    assert result["status"] == "EXECUTING"
    assert "taskId" in result
    print("✅ 关税算法异步测试通过")

if __name__ == "__main__":
    test_tariff_algorithm()
    test_tariff_algorithm_async()
    print("\n✅ 所有测试通过")
```

### 9.2 测试场景算法

```python
import sys
sys.path.insert(0, 'd:/12.code/test/sci/risk/algorithms/risk-algorithm-service')

from algorithms.scenario_algorithm import RiskScenarioAlgorithm

def test_scenario_algorithm():
    algo = RiskScenarioAlgorithm()
    
    scenarios = ["trade_war", "supply_disruption", "demand_volatility", "logistics_delay"]
    
    for scenario in scenarios:
        result = algo.run({"scenarioType": scenario})
        print(f"场景 {scenario}: {result}")
        assert result["status"] == "COMPLETED"
        assert "riskScore" in result
        assert "riskLevel" in result
    
    print("✅ 场景算法测试通过")

if __name__ == "__main__":
    test_scenario_algorithm()
```

### 9.3 HTTP接口测试

```bash
# 健康检查
curl http://localhost:5000/health

# 获取算法列表
curl http://localhost:5000/algorithms

# 执行关税算法
curl -X POST http://localhost:5000/tariff/execute \
  -H "Content-Type: application/json" \
  -d '{
    "callbackUrl": "http://localhost:8080/api/simulation/status",
    "tariffRate": 20
  }'

# 执行场景算法
curl -X POST http://localhost:5000/scenario/execute \
  -H "Content-Type: application/json" \
  -d '{
    "callbackUrl": "http://localhost:8080/api/simulation/status",
    "scenarioType": "trade_war"
  }'
```

### 9.4 运行所有测试

```bash
cd d:/12.code/test/sci/risk/algorithms/risk-algorithm-service
python -c "
import sys
sys.path.insert(0, '.')
from algorithms.tariff_algorithm import TariffRiskAlgorithm
from algorithms.scenario_algorithm import RiskScenarioAlgorithm

# 测试关税算法
algo1 = TariffRiskAlgorithm()
result1 = algo1.run({'tariffRate': 15})
print(f'关税算法: {result1}')

# 测试场景算法
algo2 = RiskScenarioAlgorithm()
result2 = algo2.run({'scenarioType': 'trade_war'})
print(f'场景算法: {result2}')

print('所有测试完成')
"
```

---

## 10. Java后端接入详解

本项目的Java后端位于 `backend/risk-basic-service`，使用Spring Boot框架。

### 10.1 Java后端目录结构

```
backend/risk-basic-service/src/main/java/com/sci/risk/
├── RiskBackendApplication.java           # 启动类
├── config/
│   ├── AlgorithmInitConfig.java         # 算法初始化配置
│   └── OpenApiConfig.java               # OpenAPI配置
├── controller/
│   ├── AlgorithmController.java         # 算法管理接口
│   └── SimulationController.java        # 模拟任务接口
├── service/
│   ├── AlgorithmRegistryService.java    # 算法注册表服务
│   └── SimulationService.java           # 模拟任务服务
└── model/
    ├── AlgorithmInfo.java               # 算法信息模型
    ├── AlgorithmExecuteRequest.java     # 算法执行请求
    ├── SimulationTask.java             # 模拟任务模型
    ├── SimulationRequest.java          # 模拟请求
    ├── SimulationResponse.java         # 模拟响应
    └── RiskScenarioRequest.java        # 风险场景请求
```

### 10.2 核心服务类

#### AlgorithmRegistryService - 算法注册表

```java
@Service
public class AlgorithmRegistryService {
    private final Map<String, AlgorithmInfo> registry = new ConcurrentHashMap<>();

    // 注册算法
    public void register(AlgorithmInfo algorithm) {
        registry.put(algorithm.getName(), algorithm);
    }

    // 获取算法
    public Optional<AlgorithmInfo> getAlgorithm(String name) {
        return Optional.ofNullable(registry.get(name));
    }

    // 获取所有算法
    public List<AlgorithmInfo> getAllAlgorithms() {
        return new ArrayList<>(registry.values());
    }

    // 更新算法状态
    public void updateStatus(String name, String status) {
        AlgorithmInfo algo = registry.get(name);
        if (algo != null) {
            algo.setStatus(status);
        }
    }
}
```

#### SimulationService - 模拟任务服务

使用 Spring WebClient 调用算法服务：

```java
@Service
public class SimulationService {
    private final Map<String, SimulationTask> tasks = new ConcurrentHashMap<>();
    private final AlgorithmRegistryService algorithmRegistry;
    private final WebClient webClient;

    public SimulationResponse startSimulation(Integer tariffRate) {
        String taskId = UUID.randomUUID().toString();
        SimulationTask task = new SimulationTask(taskId, tariffRate);
        tasks.put(taskId, task);

        // 从注册表获取算法信息
        Optional<AlgorithmInfo> algoOpt = algorithmRegistry.getAlgorithm("tariff-risk-algorithm");
        if (algoOpt.isEmpty()) {
            return new SimulationResponse(taskId, "FAILED", "算法服务未注册");
        }

        // 构建请求
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("taskId", taskId);
        requestBody.put("tariffRate", tariffRate);
        requestBody.put("callbackUrl", "http://localhost:8080/api/simulation/status");

        try {
            // 调用算法服务
            String executeUrl = algoOpt.get().getEndpoint() + "/execute";
            webClient.post()
                .uri(executeUrl)
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(requestBody)
                .retrieve()
                .toEntity(Map.class)
                .block();

            return new SimulationResponse(taskId, "EXECUTING", "模拟任务已启动");
        } catch (Exception e) {
            return new SimulationResponse(taskId, "FAILED", "调用算法服务失败: " + e.getMessage());
        }
    }
}
```

### 10.3 启动时初始化算法

通过 `AlgorithmInitConfig` 在应用启动时预注册算法：

```java
@Configuration
public class AlgorithmInitConfig {

    @Bean
    public CommandLineRunner initAlgorithms(AlgorithmRegistryService registry) {
        return args -> {
            // 关税风险算法
            registry.register(new AlgorithmInfo(
                "tariff-risk-algorithm",
                "1.0.0",
                "http://localhost:5000/tariff",
                "tariffRate",
                "关税风险模拟算法"
            ));

            // 风险场景算法
            registry.register(new AlgorithmInfo(
                "risk-scenarios-algorithm",
                "1.0.0",
                "http://localhost:5000/scenario",
                "scenarioType",
                "风险场景分析算法"
            ));

            // ML风险预测算法
            registry.register(new AlgorithmInfo(
                "risk-ml-algorithm",
                "1.0.0",
                "http://localhost:5001/ml",
                "historicalData,riskFactors",
                "基于机器学习的供应链风险预测算法"
            ));
        };
    }
}
```

### 10.4 后端接口列表

#### 算法管理接口 (AlgorithmController)

| 接口 | 方法 | 说明 |
|-----|------|------|
| `/api/algorithm/register` | POST | 算法服务注册 |
| `/api/algorithm/list` | GET | 获取算法列表 |
| `/api/algorithm/{name}` | GET | 获取算法详情 |
| `/api/algorithm/{name}/status` | PUT | 更新算法状态 |
| `/api/algorithm/{name}/health` | GET | 健康检查 |

#### 模拟任务接口 (SimulationController)

| 接口 | 方法 | 说明 |
|-----|------|------|
| `/api/simulation/start` | POST | 启动关税模拟 |
| `/api/simulation/start-risk-scenario` | POST | 启动风险场景分析 |
| `/api/simulation/ml-risk` | POST | 启动ML风险预测 |
| `/api/simulation/status/{taskId}` | GET | 查询任务状态 |
| `/api/simulation/tasks` | GET | 获取所有任务 |
| `/api/simulation/status` | POST | **接收算法回调的状态更新** |
| `/api/simulation/result` | POST | **接收算法回调的执行结果** |

### 10.5 接收算法回调

算法执行完成后会回调后端接口：

#### 状态更新回调

```java
@PostMapping("/simulation/status")
public void receiveStatus(@RequestBody Map<String, Object> payload) {
    String taskId = (String) payload.get("taskId");
    String status = (String) payload.get("status");
    Integer progress = (Integer) payload.get("progress");
    simulationService.updateTaskStatus(taskId, status, progress != null ? progress : 0);
}
```

#### 结果回调

```java
@PostMapping("/simulation/result")
public void receiveResult(@RequestBody Map<String, Object> payload) {
    String taskId = (String) payload.get("taskId");
    simulationService.updateTaskResult(taskId, payload);
}
```

### 10.6 调用示例

#### 调用关税模拟

```bash
curl -X POST http://localhost:8080/api/simulation/start \
  -H "Content-Type: application/json" \
  -d '{"tariffRate": 20}'
```

**响应：**
```json
{
  "taskId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "EXECUTING",
  "message": "模拟任务已启动"
}
```

#### 调用风险场景分析

```bash
curl -X POST http://localhost:8080/api/simulation/start-risk-scenario \
  -H "Content-Type: application/json" \
  -d '{"scenarioType": "trade_war"}'
```

#### 查询任务状态

```bash
curl http://localhost:8080/api/simulation/status/550e8400-e29b-41d4-a716-446655440000
```

**响应：**
```json
{
  "taskId": "550e8400-e29b-41d4-a716-446655440000",
  "tariffRate": 20,
  "status": "COMPLETED",
  "currentStatus": "【执行完成】关税20%，利润不足，建议转产",
  "result": {...}
}
```

### 10.7 Java后端启动

```bash
cd d:/12.code/test/sci/risk/backend/risk-basic-service

# 使用Maven
./mvnw spring-boot:run

# 或打包后运行
./mvnw clean package
java -jar target/risk-basic-service-1.0.0.jar
```

后端启动后会：
1. 自动初始化注册三个算法服务
2. 监听 8080 端口
3. 等待算法服务注册和回调

---

## 11. 接入后端系统（通用）

### 11.1 后端注册算法服务

后端管理系统需要提供算法注册接口：

```python
# 后端伪代码
@app.route('/api/algorithm/register', methods=['POST'])
def register_algorithm():
    data = request.get_json()
    algorithm_name = data.get('name')
    endpoint = data.get('endpoint')
    # 存储到数据库
    return jsonify({"status": "registered"})
```

### 11.2 后端调用算法流程

```
1. 后端收到前端风险计算请求
2. 后端调用算法服务 POST /{algo_name}/execute
3. 算法服务立即返回 taskId + status=STARTED
4. 算法服务异步执行算法
5. 算法执行完成，POST回调到后端 callbackUrl
6. 后端更新任务状态，前端展示结果
```

### 11.3 完整调用示例

```python
import requests
import time

ALGORITHM_SERVICE_URL = "http://localhost:5000"
BACKEND_URL = "http://localhost:8080"

def call_tariff_algorithm(tariff_rate: int):
    """调用关税风险算法"""
    response = requests.post(
        f"{ALGORITHM_SERVICE_URL}/tariff/execute",
        json={
            "taskId": f"task-{int(time.time())}",
            "callbackUrl": f"{BACKEND_URL}/api/simulation/status",
            "tariffRate": tariff_rate
        },
        timeout=10
    )
    return response.json()

def call_scenario_algorithm(scenario_type: str):
    """调用场景风险算法"""
    response = requests.post(
        f"{ALGORITHM_SERVICE_URL}/scenario/execute",
        json={
            "taskId": f"task-{int(time.time())}",
            "callbackUrl": f"{BACKEND_URL}/api/simulation/status",
            "scenarioType": scenario_type
        },
        timeout=10
    )
    return response.json()

# 使用示例
if __name__ == "__main__":
    result = call_tariff_algorithm(25)
    print(f"关税算法调用结果: {result}")
    # {'taskId': 'task-1234567890', 'status': 'STARTED'}
```

---

## 附录：算法返回值规范

算法执行完成后，返回的字典应包含以下字段：

| 字段 | 类型 | 说明 |
|-----|------|------|
| taskId | string | 任务ID |
| status | string | 状态 (COMPLETED/FAILED) |
| result | string | 执行结果描述 |
| riskScore | number | 风险评分 (0-100) |
| level | string | 风险等级 (LOW/MEDIUM/HIGH) |
| duration | number | 执行耗时(秒) |

**示例：**
```python
{
    "taskId": "550e8400-e29b-41d4-a716-446655440000",
    "status": "COMPLETED",
    "result": "【执行完成】关税25%，利润不足，建议转产",
    "riskScore": 75.5,
    "level": "HIGH",
    "duration": 0.5
}
```
