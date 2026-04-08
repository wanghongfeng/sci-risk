# 供应链控制塔   - 关税风险模拟系统

## 系统架构

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                              云端部署                                      │
│  ┌─────────────┐     ┌─────────────────────────────────────┐     ┌──────────────────┐  │
│  │ GitHub      │     │         Koyeb (Java Backend)        │     │   Render         │  │
│  │ Pages       │────▶│  https://weak-zondra-laosha007     │────▶│  算法注册中心     │  │
│  │ (Frontend)  │     │           -8931c4eb.koyeb.app      │     │  sci-risk        │  │
│  │             │◀────│         :8080                       │◀────│  .onrender.com   │  │
│  └─────────────┘     └─────────────────────────────────────┘     │  :5000           │  │
│                                                                      │                  │  │
│                                                                      │  本地算法:       │  │
│                                                                      │  - tariff        │  │
│                                                                      │  - scenario      │  │
│                                                                      └──────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                              本地开发                                      │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────────────┐     ┌─────────────┐  │
│  │   Vue3      │     │   Java      │     │   Python Flask      │     │   FastAPI   │  │
│  │   前端      │────▶│   Spring    │────▶│   算法注册中心       │     │   AI Agent │  │
│  │   :3000     │     │   Boot      │     │   :5000             │     │   :8000    │  │
│  │             │◀────│   :8080     │◀────│                     │     │            │  │
│  └─────────────┘     └─────────────┘     └─────────────────────┘     └─────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🚀 云端服务

| 服务 | 平台 | URL | 说明 |
|------|------|-----|------|
| 前端 | GitHub Pages | https://wanghongfeng.github.io/sci-risk/ | Vue3 单页应用 |
| Java 后端 | Koyeb | https://weak-zondra-laosha007-8931c4eb.koyeb.app | Spring Boot API |
| 算法注册中心 | Render | https://sci-risk.onrender.com | 算法统一入口 |

---

## 🚀 本地快速启动

### 一键启动（Windows）

```bash
start-all.bat
```

### 手动启动

```bash
# 1. AI Agent (端口8000)
cd aiagent && pip install -r requirements.txt && python main.py

# 2. 算法注册中心 (端口5000)
cd algorithms/risk-algorithm-service && pip install -r requirements.txt && python main.py

# 3. ML算法服务 (端口5001)
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
│   │   └── intent_classifier.py  # 意图识别
│   ├── llm/                      # LLM Provider
│   │   ├── mock_provider.py      # Mock 模式
│   │   ├── openai_provider.py    # OpenAI
│   │   └── openrouter_provider.py
│   └── security/                 # 认证服务
│
├── algorithms/                   # Python 算法服务
│   ├── risk-algorithm-service/   # 算法注册中心 (端口5000)
│   │   ├── main.py               # Flask 入口
│   │   ├── config/settings.py    # 配置管理
│   │   ├── models/               # 数据模型
│   │   │   └── base.py           # 算法基类
│   │   ├── services/             # 核心服务
│   │   │   ├── registry_service.py   # 算法注册服务
│   │   │   ├── discovery_service.py # 算法发现服务
│   │   │   └── algorithm_service.py # 算法执行服务
│   │   ├── controllers/
│   │   │   └── api_controller.py     # API控制器
│   │   ├── algorithms/            # 本地算法（自动发现）
│   │   │   ├── tariff_algorithm.py
│   │   │   └── scenario_algorithm.py
│   │   └── ALGORITHM_SPEC.md      # 算法接入规范
│   │
│   └── risk-ml-algorithm/        # ML算法服务 (端口5001)
│       ├── main.py               # Flask 入口
│       └── models/               # ML模型
│
├── backend/                      # Java 后端服务 (端口8080)
│   ├── risk-basic-service/       # Spring Boot 主服务
│   │   ├── src/main/java/com/sci/risk/
│   │   │   ├── controller/       # REST 控制器
│   │   │   ├── service/          # 业务服务
│   │   │   └── model/            # 数据模型
│   │   └── src/main/resources/
│   │       ├── application.properties       # 通用配置
│   │       ├── application-local.properties  # 本机环境
│   │       └── application-cloud.properties    # 云端环境
│   └── pom.xml                   # 父 POM
│
└── frontend/                     # Vue3 前端 (端口3000)
    ├── src/
    │   ├── App.vue               # 主组件
    │   ├── main.js               # 入口文件
    │   ├── config.js             # 统一配置
    │   ├── services/
    │   │   ├── algorithmService.js   # 算法服务
    │   │   └── simulationService.js  # 仿真服务
    │   └── views/
    │       ├── TariffSimulation.vue  # 关税模拟
    │       ├── RiskScenario.vue      # 风险场景
    │       └── ...
    ├── .env.local               # 本机环境变量
    ├── .env.cloud               # 云端环境变量
    ├── .env.production          # 生产环境变量
    ├── vite.config.js
    └── package.json
```

---

## 服务端口一览

| 服务 | 端口 | 技术栈 | 说明 |
|------|------|--------|------|
| Vue3 前端 | 3000 | Vue3 + Vite | 用户界面 |
| Java 后端 | 8080 | Spring Boot | API 网关 |
| 算法注册中心 | 5000 | Flask | 算法统一入口，本地算法+远程代理 |
| ML算法服务 | 5001 | Flask | 独立ML算法，被注册中心发现 |
| AI Agent | 8000 | FastAPI | 智能对话 |

---

## 云端部署

### 部署架构

| 平台 | 服务 | 仓库分支 | 说明 |
|------|------|----------|------|
| GitHub Pages | 前端 | main | 自动部署 frontend/ 目录 |
| Koyeb | Java 后端 | main | 自动从 GitHub 构建 |
| Render | 算法注册中心 | main | 自动从 GitHub 构建 |

### GitHub Pages 前端部署

1. 进入 GitHub 仓库 **Settings → Pages**
2. **Source** 选择 **GitHub Actions**
3. 推送前端代码到 main 分支，自动触发部署

**前端环境变量** (GitHub Actions workflow 中配置):
```yaml
VITE_API_BASE_URL: https://weak-zondra-laosha007-8931c4eb.koyeb.app/api
```

### Koyeb 后端部署

1. 连接 GitHub 仓库: `wanghongfeng/sci-risk`
2. 构建命令: Maven 命令
3. 运行命令: `java -jar backend/risk-basic-service/target/*.jar`
4. 环境变量:

| Key | Value |
|-----|-------|
| `SPRING_PROFILES_ACTIVE` | `cloud` |
| `DB_URL` | `postgresql://neondb_owner:密码@host/neondb?sslmode=require` |

### Render 算法服务部署

1. 连接 GitHub 仓库
2. 构建命令: 空或 `pip install -r requirements.txt`
3. 运行命令: `python main.py`
4. 环境变量:

| Key | Value |
|-----|-------|
| `ENVIRONMENT` | `cloud` |
| `BACKEND_URL` | `https://weak-zondra-laosha007-8931c4eb.koyeb.app` |
| `ALGORITHM_BASE_URL` | `https://sci-risk.onrender.com` |

---

## 环境配置

### 环境地址对照表

| 服务 | 本机环境 | 云端环境 |
|------|----------|----------|
| Vue3 前端 | http://localhost:3000 | https://wanghongfeng.github.io/sci-risk/ |
| Java 后端 | http://localhost:8080 | https://weak-zondra-laosha007-8931c4eb.koyeb.app |
| 算法注册中心 | http://localhost:5000 | https://sci-risk.onrender.com |
| ML算法服务 | http://localhost:5001 | (随注册中心) |
| AI Agent | http://localhost:8000 | (与后端同域名) |

### 配置文件

| 服务 | 本机配置 | 云端配置 | 生产配置 |
|------|----------|----------|----------|
| 前端 | `.env.local` | `.env.cloud` | `.env.production` |
| Java 后端 | `application-local.properties` | `application-cloud.properties` | - |
| Python 算法 | `.env.local` | `.env.cloud` | - |

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
# 本机环境
curl http://localhost:5000/algorithms

# 云端环境
curl https://sci-risk.onrender.com/algorithms
```

### 验证后端同步

```bash
# 本机环境
curl http://localhost:8080/api/algorithm/list

# 云端环境
curl https://weak-zondra-laosha007-8931c4eb.koyeb.app/api/algorithm/list
```

### 验证完整流程

1. 打开前端
   - 本机: http://localhost:3000/sci-risk/
   - 云端: https://wanghongfeng.github.io/sci-risk/
2. 选择算法并执行
3. 观察执行结果

---

## 故障排查

### 算法执行返回 404

1. 检查算法注册中心是否运行
2. 检查算法是否在列表中: `GET /algorithms`
3. 检查后端同步: `GET /api/algorithm/list`

### 后端同步失败

1. 检查注册中心可访问
2. 查看后端日志中的同步错误
3. 确认 `SPRING_PROFILES_ACTIVE=cloud` 已设置

### 数据库连接失败

1. 检查 `DB_URL` 格式是否正确
2. 确认数据库密码正确
3. 检查 Neon PostgreSQL 连接字符串

---

## 相关文档

- [算法服务接入规范](algorithms/risk-algorithm-service/ALGORITHM_SPEC.md) - 详细的算法接入规范
- [算法服务 README](algorithms/README.md) - Python算法服务详情
- [后端 README](backend/README.md) - Java后端详情
- [前端 README](frontend/README.md) - Vue3前端详情
