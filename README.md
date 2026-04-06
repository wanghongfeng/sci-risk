# 供应链控制塔 - 关税风险模拟系统

## 系统架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────────┐     ┌─────────────┐
│   Vue3      │     │   Java      │     │   Python Flask      │     │   FastAPI   │
│   前端      │────▶│   Spring    │────▶│   算法注册中心       │     │   AI Agent │
│   :3000     │     │   Boot      │     │   :5000             │     │   :8000    │
│             │◀────│   :8080     │◀────│  ┌───────────────┐  │     │            │
└─────────────┘     └─────────────┘     │  │ 本地算法      │  │     └─────────────┘
                                        │  │ (自动发现)    │  │
                                        │  ├───────────────┤  │
                                        │  │ 远程服务代理  │  │
                                        │  │ risk-ml-algo  │  │
                                        │  │ (端口5001)    │  │
                                        │  └───────────────┘  │
                                        └─────────────────────┘
```

### 核心设计：算法注册中心

算法注册中心是整个算法的核心枢纽，负责：
- **自动发现本地算法**：启动时扫描 `algorithms/` 目录，自动注册所有算法
- **代理远程算法服务**：如 `risk-ml-algorithm` (端口5001)，通过注册中心统一暴露
- **统一执行入口**：前端/后端只需调用 `/algorithm/execute`，自动路由到正确算法
- **后端同步**：后端定期从注册中心同步算法列表，无需硬编码

## 🚀 快速启动

### 一键启动（Windows）

```bash
# 双击运行，或在命令行执行
start-all.bat
```

### 手动启动

```bash
# 1. AI Agent (端口8000)
cd aiagent && pip install -r requirements.txt && python main.py

# 2. 算法注册中心 (端口5000) - 核心服务
cd algorithms/risk-algorithm-service && pip install -r requirements.txt && python main.py

# 3. ML算法服务 (端口5001) - 被注册中心发现
cd algorithms/risk-ml-algorithm && pip install -r requirements.txt && python main.py

# 4. Java后端 (端口8080)
cd backend/risk-basic-service && mvn spring-boot:run

# 5. 前端 (端口3000)
cd frontend && npm install && npm run dev
```

### 启动顺序
**AI Agent → 算法注册中心 → ML算法服务 → Java后端 → 前端**

### 访问地址
- 前端: http://localhost:3000/sci-risk/
- 后端API: http://localhost:8080
- 算法注册中心: http://localhost:5000
- ML算法服务: http://localhost:5001
- AI Agent: http://localhost:8000

---

## 目录结构

```
sci/risk/
├── aiagent/                      # AI Agent Gateway (端口8000)
│   ├── main.py                   # FastAPI 入口
│   ├── config/llm_config.json    # LLM 配置
│   ├── agents/                   # Agent 实现
│   │   ├── tariff_agent/         # 关税 Agent
│   │   └── default_agent/        # 默认 Agent
│   ├── core/                     # 核心模块
│   │   └── intent_classifier.py # 意图识别
│   ├── llm/                      # LLM Provider
│   │   ├── mock_provider.py      # Mock 模式
│   │   ├── openai_provider.py   # OpenAI
│   │   └── openrouter_provider.py
│   └── security/                  # 认证服务
│
├── algorithms/                   # Python 算法服务
│   ├── risk-algorithm-service/   # 算法注册中心 (端口5000)
│   │   ├── main.py              # Flask 入口
│   │   ├── config/settings.py   # 配置管理
│   │   ├── models/              # 数据模型
│   │   │   └── base.py          # 算法基类
│   │   ├── services/            # 核心服务
│   │   │   ├── registry_service.py   # 算法注册服务
│   │   │   ├── discovery_service.py  # 算法发现服务
│   │   │   └── algorithm_service.py  # 算法执行服务
│   │   ├── controllers/
│   │   │   └── api_controller.py     # API控制器
│   │   ├── algorithms/           # 本地算法（自动发现）
│   │   │   ├── tariff_algorithm.py
│   │   │   └── scenario_algorithm.py
│   │   └── ALGORITHM_SPEC.md    # 算法接入规范
│   │
│   └── risk-ml-algorithm/        # ML算法服务 (端口5001)
│       ├── main.py              # Flask 入口
│       └── models/              # ML模型
│
├── backend/                      # Java 后端服务 (端口8080)
│   ├── risk-basic-service/       # Spring Boot 主服务
│   │   ├── src/main/java/com/sci/risk/
│   │   │   ├── controller/      # REST 控制器
│   │   │   │   ├── AlgorithmController.java  # 算法管理
│   │   │   │   └── SimulationController.java # 仿真执行
│   │   │   ├── service/        # 业务服务
│   │   │   │   ├── AlgorithmRegistryService.java  # 算法同步
│   │   │   │   └── SimulationService.java        # 仿真执行
│   │   │   └── model/          # 数据模型
│   │   └── pom.xml
│   └── pom.xml                  # 父 POM
│
└── frontend/                    # Vue3 前端 (端口3000)
    ├── src/
    │   ├── App.vue              # 主组件
    │   ├── main.js              # 入口文件
    │   ├── config.js            # 统一配置
    │   ├── services/
    │   │   ├── algorithmService.js   # 算法服务
    │   │   └── simulationService.js  # 仿真服务
    │   └── views/
    │       ├── TariffSimulation.vue   # 关税模拟
    │       └── RiskScenario.vue      # 风险场景
    ├── vite.config.js
    └── package.json
```

## 服务端口一览

| 服务 | 端口 | 技术栈 | 说明 |
|------|------|--------|------|
| Vue3 前端 | 3000 | Vue3 + Vite | 用户界面 |
| Java 后端 | 8080 | Spring Boot | API 网关 |
| 算法注册中心 | 5000 | Flask | 算法统一入口，本地算法+远程代理 |
| ML算法服务 | 5001 | Flask | 独立ML算法，被注册中心发现 |
| AI Agent | 8000 | FastAPI | 智能对话 |

---

## 架构详解

### 算法注册中心

算法注册中心是整个算法的核心，负责统一管理所有算法的注册、发现和执行。

#### 核心功能

1. **自动发现本地算法**
   - 启动时扫描 `algorithms/` 目录
   - 实例化所有继承 `AlgorithmBase` 的类
   - 自动注册到本地注册表

2. **代理远程算法服务**
   - 支持注册外部算法服务（如 ML 服务）
   - 自动发现远程服务的算法列表
   - 统一暴露为本地算法

3. **统一执行入口**
   - `POST /algorithm/execute` - 自动路由到正确算法
   - 支持本地和远程算法透明调用

4. **后端同步**
   - 后端定期从注册中心同步算法列表
   - `GET /api/algorithm/sync` 手动触发同步
   - 无需在后端硬编码算法

#### API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `GET /algorithms` | 算法列表 | 返回所有算法（含远程） |
| `POST /algorithm/execute` | 统一执行 | 自动路由执行算法 |
| `GET /<slug>/execute` | 直接执行 | 本地算法直接执行 |
| `POST /remote-services` | 注册远程服务 | 添加远程算法服务 |
| `GET /remote-services` | 远程服务列表 | 查看已注册的远程服务 |

### 后端集成

后端通过算法注册中心同步算法信息，流程如下：

```
后端启动
    │
    ├─▶ GET http://localhost:5000/algorithms
    │       返回: [{name, endpoint, ...}, ...]
    │
    ├─▶ 解析算法信息，缓存到本地
    │
    └─▶ 定时同步 (默认60秒)
            │
            └─▶ 更新算法列表
```

前端执行算法时，后端从缓存获取算法 endpoint，转发请求到算法注册中心。

---

## 环境配置

本系统支持**本机环境**和**云端环境**两套配置。

### 环境地址对照表

| 服务 | 本机环境 | 云端环境 |
|------|----------|----------|
| Vue3 前端 | http://localhost:3000 | https://wanghongfeng.github.io/sci-risk/ |
| Java 后端 | http://localhost:8080 | https://weak-zondra-laosha007-8931c4eb.koyeb.app |
| 算法注册中心 | http://localhost:5000 | https://sci-risk.onrender.com |
| ML算法服务 | http://localhost:5001 | (随注册中心) |
| AI Agent | http://localhost:8000 | (与后端同域名) |

### 使用方式

#### 本机环境 (默认)

```bash
# AI Agent
cd aiagent && python main.py

# 算法注册中心
cd algorithms/risk-algorithm-service && python main.py

# ML算法服务
cd algorithms/risk-ml-algorithm && python main.py

# Java 后端
cd backend/risk-basic-service && mvn spring-boot:run

# Vue3 前端
cd frontend && npm run dev
```

#### 云端环境

启动前设置环境变量 `ENVIRONMENT=cloud`：

```bash
# 各服务分别设置环境变量后启动
cd <service> && set ENVIRONMENT=cloud && <start-command>
```

### 环境配置文件

| 服务 | 本机配置 | 云端配置 |
|------|----------|----------|
| 前端 | `.env.local` | `.env.cloud` |
| Java 后端 | `application-local.properties` | `application-cloud.properties` |
| Python 算法 | `.env.local` | `.env.cloud` |
| AI Agent | `.env.local` | `.env.cloud` |

---

## 快速启动

### 启动顺序（重要）

**必须按以下顺序启动服务：**

1. **AI Agent (8000)** → 2. **算法注册中心 (5000)** → 3. **ML算法服务 (5001)** → 4. **Java 后端 (8080)** → 5. **Vue3 前端 (3000)**

### 1. 启动 AI Agent Gateway

```bash
cd aiagent
pip install -r requirements.txt
python main.py
```

### 2. 启动算法注册中心

```bash
cd algorithms/risk-algorithm-service
pip install -r requirements.txt
python main.py
```

### 3. 启动 ML算法服务（可选）

```bash
cd algorithms/risk-ml-algorithm
pip install -r requirements.txt
python main.py
```

### 4. 启动 Java 后端

```bash
cd backend/risk-basic-service
mvn spring-boot:run
```

### 5. 启动前端

```bash
cd frontend
npm install
npm run dev
```

---

## 算法开发

### 添加新算法

1. 在 `algorithms/risk-algorithm-service/algorithms/` 目录创建新算法类

```python
from models.base import AlgorithmBase

class NewAlgorithm(AlgorithmBase):
    @property
    def name(self) -> str:
        return "new-algorithm"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def label(self) -> str:
        return "新算法"

    @property
    def category(self) -> str:
        return "risk"

    @property
    def algo_type(self) -> str:
        return "simulation"

    @property
    def description(self) -> str:
        return "这是一个新算法"

    def execute(self, params: dict, task_request=None) -> dict:
        # 算法逻辑
        return {"result": "success"}
```

2. 重启算法注册中心，新算法会自动被发现

### 接入远程算法服务

1. 确保远程服务实现了 `/algorithms` 接口

```python
@app.route("/algorithms", methods=["GET"])
def list_algorithms():
    return jsonify({
        "algorithms": [{
            "name": "remote-algorithm",
            "version": "1.0.0",
            "endpoint": f"http://localhost:5001/algorithm/execute"
        }]
    })
```

2. 注册到算法注册中心

```bash
curl -X POST http://localhost:5000/remote-services \
  -H "Content-Type: application/json" \
  -d '{"name":"my-service","baseUrl":"http://localhost:5001","executeEndpoint":"/algorithm/execute"}'
```

---

## 测试验证

### 验证算法注册中心

```bash
# 查看算法列表
curl http://localhost:5000/algorithms

# 测试执行
curl -X POST http://localhost:5000/algorithm/execute \
  -H "Content-Type: application/json" \
  -d '{"algorithmName":"tariff-risk-algorithm","callbackUrl":"http://localhost:8080/api/simulation/status","params":{"tariffRate":25}}'
```

### 验证后端同步

```bash
# 手动触发同步
curl -X POST http://localhost:8080/api/algorithm/sync

# 查看同步后的算法列表
curl http://localhost:8080/api/algorithm/list
```

### 验证完整流程

1. 打开前端 http://localhost:3000/sci-risk/
2. 选择算法并执行
3. 观察执行结果

---

## 故障排查

### 算法执行返回 404

1. 检查算法注册中心是否运行：`curl http://localhost:5000/health`
2. 检查算法是否在列表中：`curl http://localhost:5000/algorithms`
3. 检查后端同步：`curl http://localhost:8080/api/algorithm/list`

### 远程算法未发现

1. 检查远程服务是否运行：`curl http://localhost:5001/health`
2. 检查远程服务算法端点：`curl http://localhost:5001/algorithms`
3. 手动刷新注册：`curl -X POST http://localhost:5000/remote-services/<name>/refresh`

### 后端同步失败

1. 检查注册中心可访问：`curl http://localhost:5000/algorithms`
2. 查看后端日志中的同步错误
3. 手动触发同步：`curl -X POST http://localhost:8080/api/algorithm/sync`

---

## 相关文档

- [算法服务接入规范](algorithms/risk-algorithm-service/ALGORITHM_SPEC.md) - 详细的算法接入规范
- [算法服务 README](algorithms/README.md) - Python算法服务详情
- [后端 README](backend/README.md) - Java后端详情
- [前端 README](frontend/README.md) - Vue3前端详情
