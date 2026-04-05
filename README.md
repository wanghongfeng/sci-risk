# 供应链控制塔 - 关税风险模拟系统

## 系统架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Vue3      │     │   Java      │     │   Python    │     │   FastAPI   │
│   前端      │────▶│   Spring    │───▶│   Flask     │     │   AI Agent │
│   :3000     │     │   Boot      │     │   算法      │     │   :8000    │
│             │◀────│   :8080     │◀───│   :5000     │     │            │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

## 目录结构

```
sci/risk/
├── aiagent/                      # AI Agent Gateway (端口8000)
│   ├── main.py                   # FastAPI 入口
│   ├── config/llm_config.json    # LLM 配置
│   ├── agents/                   # Agent 实现
│   │   ├── tariff_agent/         # 关税 Agent
│   │   └── default_agent/       # 默认 Agent
│   ├── core/                     # 核心模块
│   │   └── intent_classifier.py # 意图识别
│   ├── llm/                      # LLM Provider
│   │   ├── mock_provider.py      # Mock 模式
│   │   ├── openai_provider.py   # OpenAI
│   │   └── openrouter_provider.py
│   └── security/                  # 认证服务
│
├── algorithms/                   # Python 算法服务 (端口5000)
│   ├── risk-algorithm-service/   # 风险算法服务
│   │   ├── main.py              # Flask 入口
│   │   ├── algorithms/          # 算法实现
│   │   │   ├── tariff_algorithm.py
│   │   │   └── scenario_algorithm.py
│   │   └── config/settings.py
│   └── risk-ml-algorithm/       # ML 算法服务
│
├── backend/                      # Java 后端服务 (端口8080)
│   ├── risk-basic-service/      # Spring Boot 主服务
│   │   ├── src/main/java/com/sci/risk/
│   │   │   ├── controller/      # REST 控制器
│   │   │   ├── service/        # 业务服务
│   │   │   └── model/          # 数据模型
│   │   └── pom.xml
│   └── pom.xml                  # 父 POM
│
└── frontend/                    # Vue3 前端 (端口3000)
    ├── src/
    │   ├── App.vue              # 主组件
    │   ├── config.js            # 统一配置
    │   ├── aiService.js         # AI 服务调用
    │   └── components/
    │       └── AIChat.vue       # AI 助手组件
    ├── vite.config.js           # Vite 配置
    └── package.json
```

## 服务端口一览

| 服务 | 端口 | 技术栈 | 说明 |
|------|------|--------|------|
| Vue3 前端 | 3000 | Vue3 + Vite | 用户界面 |
| Java 后端 | 8080 | Spring Boot | API 网关 |
| Python 算法 | 5000 | Flask | 关税/场景算法 |
| AI Agent | 8000 | FastAPI | 智能对话 |

## 快速启动

### 启动顺序（重要）

**必须按以下顺序启动服务：**

1. **AI Agent (8000)** → 2. **Python 算法 (5000)** → 3. **Java 后端 (8080)** → 4. **Vue3 前端 (3000)**

### 1. 启动 AI Agent Gateway

```bash
cd d:\12.code\test\sci\risk\aiagent
pip install -r requirements.txt
python main.py
# 服务地址: http://localhost:8000
# Swagger文档: http://localhost:8000/docs
```

### 2. 启动 Python 算法服务

```bash
cd d:\12.code\test\sci\risk\algorithms\risk-algorithm-service
pip install -r requirements.txt
set BACKEND_URL=http://localhost:8080
python main.py
# 服务地址: http://localhost:5000
# Swagger文档: http://localhost:5000/apidocs/
```

### 3. 启动 Java 后端服务

```bash
cd d:\12.code\test\sci\risk\backend\risk-basic-service
mvn spring-boot:run
# 服务地址: http://localhost:8080
# Swagger文档: http://localhost:8080/swagger-ui.html
```

### 4. 启动 Vue3 前端

```bash
cd d:\12.code\test\sci\risk\frontend
npm install
npm run dev
# 访问地址: http://localhost:3000
```

## 注意事项

### 1. 启动前置条件

- **Java 后端启动前**：确保 Python 算法服务已启动并监听 5000 端口
  - Java 后端启动时会自动向算法服务注册
  - 如算法服务未运行，注册会失败，但后端仍可启动

- **Vue3 前端启动前**：确保 Java 后端已启动（8000端口可用）
  - 前端通过 Vite 代理访问后端 API
  - 代理配置在 `vite.config.js` 中

### 2. 跨域配置

前端已配置代理解决跨域问题：

| 前端路径 | 代理目标 | 说明 |
|---------|---------|------|
| `/api/*` | `localhost:8080/api/*` | Java 后端 |
| `/ai/*` | `localhost:8000/api/*` | AI Agent |

### 3. 代理路径重写

**重要**：`/ai` 路径会被重写为 `/api/ai`

- 前端调用: `POST /ai/chat`
- 实际请求: `POST http://localhost:8000/api/ai/chat`

如需修改，编辑 `frontend/vite.config.js`：

```javascript
'/ai': {
  target: 'http://localhost:8000',
  changeOrigin: true,
  rewrite: (path) => `/api${path}`  // /ai/chat → /api/ai/chat
}
```

### 4. 环境变量

| 变量 | 服务 | 说明 |
|------|------|------|
| `BACKEND_URL` | Python 算法 | 后端服务地址，默认 `http://localhost:8080` |
| `ALGORITHM_PORT` | Python 算法 | 算法服务端口，默认 `5000` |

### 5. Token 配置

前端默认使用测试 Token，位于 `frontend/src/config.js`：

```javascript
token: 'mock_001_zhangsan_tariff:read,policy:read_tariff:*,policy:*'
```

AI Agent 支持 Mock 模式，无需真实 API Key 即可测试。

## 各服务详解

### AI Agent Gateway (端口8000)

基于 FastAPI 的智能代理网关，提供两层模型架构。

#### 功能特性

- 意图识别：识别用户输入并路由到对应 Agent
- 多 Agent 支持：tariff_agent（关税）、default_agent（默认）
- Token 验证 + 权限控制
- 支持 Mock/OpenAI/OpenRouter 三种模式

#### LLM 配置

编辑 `aiagent/config/llm_config.json`：

**Mock 模式（默认，无需配置）**
```json
{
  "provider": "mock"
}
```

**OpenAI 模式**
```json
{
  "provider": "openai",
  "openai": {
    "api_key": "your-api-key",
    "default_model": "gpt-4"
  }
}
```

**OpenRouter 模式**
```json
{
  "provider": "openrouter",
  "openrouter": {
    "api_key": "your-api-key",
    "default_model": "anthropic/claude-3-sonnet"
  }
}
```

### Python 算法服务 (端口5000)

基于 Flask 的算法服务框架。

#### 内置算法

| 算法 | 路径 | 说明 |
|------|------|------|
| tariff-risk-algorithm | `/tariff` | 关税风险模拟 |
| risk-scenarios-algorithm | `/scenario` | 风险场景分析 |

#### 算法执行接口

```bash
# 关税风险模拟
POST http://localhost:5000/tariff/execute
Content-Type: application/json

{
  "taskId": "task-001",
  "callbackUrl": "http://localhost:8080/api/simulation/status",
  "tariffRate": 10
}

# 风险场景分析
POST http://localhost:5000/scenario/execute
Content-Type: application/json

{
  "taskId": "task-002",
  "callbackUrl": "http://localhost:8080/api/simulation/status",
  "scenarioType": "trade_war"
}
```

### Java 后端服务 (端口8080)

基于 Spring Boot 的 REST API 服务。

#### 核心接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/algorithm/list` | GET | 获取已注册算法列表 |
| `/api/simulation/start` | POST | 启动关税模拟任务 |
| `/api/simulation/start-risk-scenario` | POST | 启动风险场景分析 |
| `/api/simulation/status/{taskId}` | GET | 查询任务状态 |

### Vue3 前端 (端口3000)

基于 Vue 3 + Vite 的单页应用。

#### 配置文件

`frontend/src/config.js`：

```javascript
const config = {
  apiBaseUrl: '/api',       // 后端 API 地址（已配置代理）
  aiBaseUrl: '/ai',         // AI 服务地址（已配置代理）
  token: 'mock_...'         // 认证 Token
}
```

## API 接口文档

### 后端接口

#### 1. 获取算法列表

```http
GET http://localhost:8080/api/algorithm/list
```

**响应**
```json
[
  {
    "name": "tariff-risk-algorithm",
    "version": "1.0.0",
    "endpoint": "http://localhost:5000/tariff",
    "description": "关税风险模拟算法",
    "status": "ONLINE"
  }
]
```

#### 2. 启动关税模拟

```http
POST http://localhost:8080/api/simulation/start
Content-Type: application/json

{"tariffRate": 10}
```

**响应**
```json
{
  "taskId": "083ce810-e82a-4aed-8cea-826ba59ea8af",
  "status": "EXECUTING",
  "message": "模拟任务已启动"
}
```

#### 3. 查询任务状态

```http
GET http://localhost:8080/api/simulation/status/{taskId}
```

**响应**
```json
{
  "taskId": "083ce810-e82a-4aed-8cea-826ba59ea8af",
  "status": "COMPLETED",
  "result": {
    "tariffRate": 10,
    "recommendation": "维持生产"
  }
}
```

### AI Agent 接口

#### 1. 对话接口

```http
POST http://localhost:8000/api/ai/chat
Content-Type: application/json
Authorization: Bearer mock_001_zhangsan_tariff:read,policy:read_tariff:*,policy:*

{
  "message": "关税政策是什么？",
  "session_id": "可选"
}
```

**响应**
```json
{
  "response": "关税政策正在发展中...",
  "intent": {
    "intent_name": "tariff_analysis",
    "confidence": 0.95
  },
  "agent_id": "tariff_agent",
  "agent_name": "关税政策分析智能体",
  "success": true
}
```

## 关税规则

| 关税税率 | 模拟结果 |
|---------|---------|
| 10% | 维持生产 |
| 20% | 转产 |

## 数据架构

本系统使用 Neon PostgreSQL 数据库管理海尔集团全球供应链风险数据。

### 核心数据表

| 表名 | 说明 |
|------|------|
| factory_master | 工厂主数据 |
| supplier_master | 供应商主数据 |
| product_master | 产品主数据 |
| bom_master | 物料清单 |
| supply_path | 供应路径 |
| tariff_rule | 关税规则 |
| risk_mapping | 风险映射 |

详细说明见 `data/README.md` 和 `data/schema.sql`。

### 前端菜单表

| 菜单ID | 菜单名称 | 父菜单 | 路由路径 | 权限标识 |
|--------|---------|--------|---------|---------|
| M001 | 首页 | - | /dashboard | dashboard:view |
| M002 | 关税管理 | - | /tariff | tariff:manage |
| M203 | 关税模拟 | M002 | /tariff/simulation | tariff:sim |
| M008 | 系统设置 | - | /system | system:manage |
| M804 | 菜单管理 | M008 | /system/menu | system:menu |

详细SQL定义见 `data/schema.sql` 和 `data/seed_data.sql`。

## 常见问题

### 1. 前端页面加载失败

**检查事项**：
- 确认所有后端服务已启动
- 检查浏览器控制台错误
- 确认 8080、8000、5000 端口未被占用

### 2. AI 助手无响应

**检查事项**：
- 确认 AI Agent 服务已启动（8000端口）
- 检查 `vite.config.js` 代理配置是否正确
- 确认 `/ai/chat` 路径重写正确

### 3. 算法服务注册失败

**原因**：Java 后端启动时 Python 算法服务未运行

**解决**：先启动 Python 算法服务，再重启 Java 后端

### 4. 端口占用

如端口被占用，使用以下命令查找并关闭：

```powershell
# 查找端口占用
netstat -ano | findstr :8080

# 关闭进程（替换 PID）
taskkill /PID <PID> /F
```

## 扩展开发

### 添加新算法

1. 在 `algorithms/risk-algorithm-service/algorithms/` 创建算法类
2. 继承 `AlgorithmBase` 并实现 `execute` 方法
3. 在 `main.py` 中注册算法

### 添加新 Agent

1. 在 `aiagent/agents/` 创建 Agent 目录
2. 继承 `BaseAgent` 并实现 `execute` 方法
3. 在 `agent_factory.py` 中注册 Agent

### 添加新微服务

1. 在 `backend/` 创建新服务模块
2. 配置 Maven 多模块结构
3. 在父 `pom.xml` 中添加模块引用

## 技术栈

| 组件 | 技术 |
|------|------|
| 前端 | Vue 3, Vite, Axios |
| 后端 | Java Spring Boot 3.x |
| 算法 | Python Flask |
| AI | FastAPI, Pydantic |
| 文档 | Swagger/OpenAPI |

## 联系与支持

如有问题，请检查：
1. 各服务日志输出
2. 浏览器开发者工具控制台
3. `data/README.md` 数据说明
