# 后端服务 (Backend Services)

基于 Spring Boot 的微服务后端，支持多服务扩展和 Swagger API 文档。

## 目录

- [1. 微服务架构规划](#1-微服务架构规划)
- [2. 当前服务列表](#2-当前服务列表)
- [3. 目录结构](#3-目录结构)
- [4. 快速开始](#4-快速开始)
- [5. Swagger API 文档](#5-swagger-api-文档)
- [6. 核心模块详解](#6-核心模块详解)
- [7. 前端调用方式](#7-前端调用方式)
- [8. 新增微服务](#8-新增微服务)
- [9. Docker 部署](#9-docker-部署)

---

## 1. 微服务架构规划

### 1.1 架构设计原则

```
┌─────────────────────────────────────────────────────────────────┐
│                         前端应用                                 │
│                    (Vue/React/移动端)                            │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP/REST
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ risk-basic    │     │ risk-xxx      │     │ risk-xxx      │
│ -service     │     │ -service      │     │ -service      │
│ (端口8080)   │     │ (端口8081)   │     │ (端口8082)   │
└───────────────┘     └───────────────┘     └───────────────┘
        │                     │                     │
        │    ┌─────────────────┴─────────────────┐    │
        │    │                                   │    │
        ▼    ▼                                   ▼    ▼
┌───────────────┐                         ┌───────────────┐
│  算法服务      │                         │  数据库/缓存   │
│ (Python)     │                         │  (待扩展)     │
└───────────────┘                         └───────────────┘
```

### 1.2 服务职责划分

| 服务 | 职责 | 端口 |
|-----|------|------|
| risk-basic-service | 核心业务逻辑、API网关、算法调度 | 8080 |
| risk-xxx-service | 扩展服务1 (如: 报表服务) | 8081 |
| risk-xxx-service | 扩展服务2 (如: 用户服务) | 8082 |

### 1.3 扩展方向

- **risk-report-service**: 报表统计服务
- **risk-user-service**: 用户权限服务
- **risk-notify-service**: 通知服务
- **risk-data-service**: 数据分析服务

---

## 2. 当前服务列表

| 服务 | 描述 | 端口 |
|-----|------|------|
| risk-basic-service | 供应链控制塔基础服务 | 8080 |

---

## 3. 目录结构

```
backend/
├── pom.xml                              # 父项目 POM (多模块Maven)
├── Dockerfile                           # Docker 构建文件
│
├── risk-basic-service/                  # 基础服务模块
│   ├── pom.xml                         # 服务 POM
│   ├── src/main/
│   │   ├── java/com/sci/risk/
│   │   │   ├── RiskBackendApplication.java    # 启动类
│   │   │   │
│   │   │   ├── config/
│   │   │   │   ├── AlgorithmInitConfig.java  # 算法初始化配置
│   │   │   │   └── OpenApiConfig.java       # Swagger配置
│   │   │   │
│   │   │   ├── controller/
│   │   │   │   ├── AlgorithmController.java  # 算法管理接口
│   │   │   │   └── SimulationController.java # 模拟任务接口
│   │   │   │
│   │   │   ├── service/
│   │   │   │   ├── AlgorithmRegistryService.java  # 算法注册表
│   │   │   │   └── SimulationService.java          # 任务调度服务
│   │   │   │
│   │   │   └── model/
│   │   │       ├── AlgorithmInfo.java           # 算法信息
│   │   │       ├── AlgorithmExecuteRequest.java # 算法执行请求
│   │   │       ├── SimulationTask.java         # 任务模型
│   │   │       ├── SimulationRequest.java       # 模拟请求
│   │   │       ├── SimulationResponse.java     # 模拟响应
│   │   │       └── RiskScenarioRequest.java    # 风险场景请求
│   │   │
│   │   └── resources/
│   │       └── application.properties           # 应用配置
│   │
│   └── target/                          # 编译输出
│
└── README.md                            # 本文档
```

---

## 4. 快速开始

### 4.1 环境要求

- JDK 17+
- Maven 3.8+
- Python 3.8+ (用于算法服务)

### 4.2 本地运行

```bash
cd risk-basic-service

# 使用 Maven 运行
./mvnw spring-boot:run

# 或打包后运行
./mvnw clean package
java -jar target/risk-basic-service-1.0.0.jar
```

### 4.3 启动顺序

1. **启动后端服务** (端口8080)
```bash
cd backend/risk-basic-service
./mvnw spring-boot:run
```

2. **启动算法服务** (端口5000/5001)
```bash
# 新开终端
cd algorithms/risk-algorithm-service
python main.py
```

3. **验证服务**
- 后端 API: http://localhost:8080
- Swagger UI: http://localhost:8080/swagger-ui.html
- 算法服务: http://localhost:5000

### 4.4 多环境配置

后端支持**本机环境**和**云端环境**两种配置模式。

#### 配置文件

- `application-local.properties` - 本机环境配置
- `application-cloud.properties` - 云端环境配置

#### 使用方式

```bash
# 本机环境 (默认)
./mvnw spring-boot:run

# 云端环境
set SPRING_PROFILES_ACTIVE=cloud
./mvnw spring-boot:run
```

或设置环境变量：

```powershell
$env:SPRING_PROFILES_ACTIVE="cloud"
./mvnw spring-boot:run
```

#### 环境配置内容

| 配置项 | 本机环境 | 云端环境 |
|--------|----------|----------|
| 回调地址 | http://localhost:8080 | https://weak-zondra-laosha007-8931c4eb.koyeb.app |
| 关税算法端点 | http://localhost:5000/tariff | https://sci-risk.onrender.com/tariff/execute |
| 场景算法端点 | http://localhost:5000/scenario | https://sci-risk.onrender.com/scenario/execute |
| ML算法端点 | http://localhost:5001/ml | https://sci-risk.onrender.com/ml/execute |

### 4.5 端口占用排查

```powershell
# Windows查看端口占用
netstat -ano | findstr :8080
netstat -ano | findstr :5000

# 停止进程
taskkill /PID <PID> /F
```

---

## 5. Swagger API 文档

### 5.1 Swagger 配置

使用 springdoc-openapi 实现 Swagger 3.0：

```java
@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("供应链控制塔 API")
                        .description("供应链控制塔关税风险模拟系统 API 文档")
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("SCI Team")
                                .email("support@sci.com")))
                .servers(List.of(
                        new Server().url("http://localhost:8080").description("本地开发服务器")
                ))
                .tags(List.of(
                        new Tag().name("模拟服务").description("关税风险模拟相关接口"),
                        new Tag().name("算法管理").description("算法注册与发现接口")
                ));
    }
}
```

### 5.2 Swagger UI 访问

| 环境 | 地址 |
|-----|------|
| 本地 | http://localhost:8080/swagger-ui.html |
| 云端 | https://weak-zondra-laosha007-8931c4eb.koyeb.app/swagger-ui.html |
| OpenAPI JSON | http://localhost:8080/v3/api-docs |
| OpenAPI YAML | http://localhost:8080/v3/api-docs.yaml |

### 5.3 接口文档示例

使用 `@Operation` 和 `@ApiResponse` 注解：

```java
@Operation(summary = "启动模拟任务", description = "根据关税税率启动关税风险模拟任务")
@ApiResponses(value = {
    @ApiResponse(responseCode = "200", description = "任务启动成功"),
    @ApiResponse(responseCode = "400", description = "参数错误")
})
@PostMapping("/simulation/start")
public SimulationResponse startSimulation(@RequestBody SimulationRequest request) {
    // ...
}
```

### 5.4 Swagger 分组配置

如果需要为不同服务配置不同的 Swagger 文档：

```java
@Bean
public GroupedOpenApi orderApi() {
    return GroupedOpenApi.builder()
            .group("订单服务")
            .pathsToMatch("/api/orders/**")
            .build();
}

@Bean
public GroupedOpenApi riskApi() {
    return GroupedOpenApi.builder()
            .group("风险管理")
            .pathsToMatch("/api/simulation/**", "/api/algorithm/**")
            .build();
}
```

---

## 6. 核心模块详解

### 6.1 AlgorithmRegistryService - 算法注册表

管理所有注册的算法服务：

```java
@Service
public class AlgorithmRegistryService {
    private final Map<String, AlgorithmInfo> registry = new ConcurrentHashMap<>();

    public void register(AlgorithmInfo algorithm) {
        registry.put(algorithm.getName(), algorithm);
    }

    public Optional<AlgorithmInfo> getAlgorithm(String name) {
        return Optional.ofNullable(registry.get(name));
    }

    public List<AlgorithmInfo> getAllAlgorithms() {
        return new ArrayList<>(registry.values());
    }

    public boolean isAlgorithmOnline(String name) {
        AlgorithmInfo algo = registry.get(name);
        return algo != null && "ONLINE".equals(algo.getStatus());
    }
}
```

### 6.2 SimulationService - 任务调度服务

使用 WebClient 异步调用算法服务：

```java
@Service
public class SimulationService {
    private final Map<String, SimulationTask> tasks = new ConcurrentHashMap<>();
    private final AlgorithmRegistryService algorithmRegistry;
    private final WebClient webClient;

    public SimulationResponse startSimulation(Integer tariffRate) {
        // 1. 创建任务
        String taskId = UUID.randomUUID().toString();
        SimulationTask task = new SimulationTask(taskId, tariffRate);
        tasks.put(taskId, task);

        // 2. 获取算法信息
        Optional<AlgorithmInfo> algoOpt = algorithmRegistry.getAlgorithm("tariff-risk-algorithm");

        // 3. 构建请求
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("taskId", taskId);
        requestBody.put("tariffRate", tariffRate);
        requestBody.put("callbackUrl", "http://localhost:8080/api/simulation/status");

        // 4. 调用算法服务
        String executeUrl = algoOpt.get().getEndpoint() + "/execute";
        webClient.post()
            .uri(executeUrl)
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue(requestBody)
            .retrieve()
            .toEntity(Map.class)
            .block();

        return new SimulationResponse(taskId, "EXECUTING", "模拟任务已启动");
    }
}
```

### 6.3 AlgorithmInitConfig - 启动初始化

应用启动时预注册算法：

```java
@Configuration
public class AlgorithmInitConfig {

    @Bean
    public CommandLineRunner initAlgorithms(AlgorithmRegistryService registry) {
        return args -> {
            registry.register(new AlgorithmInfo(
                "tariff-risk-algorithm",
                "1.0.0",
                "http://localhost:5000/tariff",
                "tariffRate",
                "关税风险模拟算法"
            ));

            registry.register(new AlgorithmInfo(
                "risk-scenarios-algorithm",
                "1.0.0",
                "http://localhost:5000/scenario",
                "scenarioType",
                "风险场景分析算法"
            ));
        };
    }
}
```

### 6.4 CORS 跨域配置

在启动类中配置 CORS：

```java
@SpringBootApplication
public class RiskBackendApplication {

    @Bean
    public CorsFilter corsFilter() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOriginPatterns(Arrays.asList("*"));
        config.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(Arrays.asList("*"));
        config.setAllowCredentials(true);
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return new CorsFilter(source);
    }
}
```

### 6.5 数据库配置

使用 Spring JDBC 连接 PostgreSQL 数据库：

```properties
# application.properties - 使用环境变量，参考项目根目录 .env.example
spring.datasource.url=${DB_URL}
spring.datasource.username=${DB_USERNAME:neondb_owner}
spring.datasource.password=${DB_PASSWORD}
spring.datasource.driver-class-name=org.postgresql.Driver
```

### 6.6 分层架构

采用标准的三层架构设计：

```
┌─────────────────────────────────────────────────────────────┐
│                    Controller 层 (Web)                       │
│              处理 HTTP 请求/响应，参数校验                     │
└─────────────────────────────┬───────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│                    Service 层 (业务逻辑)                      │
│              处理业务逻辑，事务管理                            │
└─────────────────────────────┬───────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│                  Repository 层 (数据访问)                     │
│              使用 JdbcTemplate 执行 SQL                      │
└─────────────────────────────┬───────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────┐
│                      PostgreSQL 数据库                        │
│                    Neon Cloud Database                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. 菜单管理模块

菜单管理是系统的基础模块，用于维护系统的导航菜单结构。

### 7.1 菜单表结构

| 字段名 | 类型 | 说明 |
|-------|------|------|
| menu_id | VARCHAR(50) | 菜单唯一标识 (主键) |
| menu_name | VARCHAR(100) | 菜单名称 |
| menu_code | VARCHAR(50) | 菜单代码 (唯一) |
| parent_id | VARCHAR(50) | 父菜单ID (0表示根菜单) |
| route_path | VARCHAR(255) | 路由路径 |
| icon | VARCHAR(50) | 图标名称 |
| sort_order | INT | 排序号 |
| is_visible | BOOLEAN | 是否显示 |
| permission | VARCHAR(100) | 权限标识 |
| component | VARCHAR(100) | 前端组件 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

**菜单数据：**

| menu_id | menu_name | menu_code | parent_id | route_path |
|---------|-----------|-----------|-----------|------------|
| M001 | 首页 | dashboard | 0 | /dashboard |
| M002 | 关税管理 | tariff | 0 | /tariff |
| M203 | 关税模拟 | tariff-sim | M002 | /tariff/simulation |
| M008 | 系统设置 | system | 0 | /system |

### 7.2 代码结构

```
risk-basic-service/src/main/java/com/sci/risk/
├── model/
│   ├── entity/
│   │   └── Menu.java              # 菜单实体
│   └── dto/
│       └── MenuRequest.java       # 菜单请求DTO
├── repository/
│   └── MenuRepository.java        # 菜单数据访问层
├── service/
│   └── MenuService.java           # 菜单业务逻辑层
└── controller/
    └── MenuController.java        # 菜单接口层
```

### 7.3 MenuRepository - 数据访问层

使用 JdbcTemplate 实现菜单的 CRUD 操作：

```java
@Repository
public class MenuRepository {

    private final JdbcTemplate jdbcTemplate;

    @Autowired
    public MenuRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public List<Menu> findAll() {
        String sql = "SELECT * FROM menu ORDER BY sort_order ASC";
        return jdbcTemplate.query(sql, MENU_ROW_MAPPER);
    }

    public Menu findById(String menuId) {
        String sql = "SELECT * FROM menu WHERE menu_id = ?";
        List<Menu> results = jdbcTemplate.query(sql, MENU_ROW_MAPPER, menuId);
        return results.isEmpty() ? null : results.get(0);
    }

    public int insert(Menu menu) {
        String sql = "INSERT INTO menu (menu_id, menu_name, menu_code, ...) VALUES (?, ?, ...)";
        return jdbcTemplate.update(sql, ...);
    }

    public int update(Menu menu) {
        String sql = "UPDATE menu SET menu_name = ?, ... WHERE menu_id = ?";
        return jdbcTemplate.update(sql, ...);
    }

    public int deleteById(String menuId) {
        String sql = "DELETE FROM menu WHERE menu_id = ?";
        return jdbcTemplate.update(sql, menuId);
    }
}
```

### 7.4 MenuService - 业务逻辑层

```java
@Service
public class MenuService {

    private final MenuRepository menuRepository;

    @Autowired
    public MenuService(MenuRepository menuRepository) {
        this.menuRepository = menuRepository;
    }

    public List<Menu> getAllMenus() {
        return menuRepository.findAll();
    }

    public List<Menu> getRootMenus() {
        return menuRepository.findRootMenus();
    }

    public Optional<Menu> getMenuById(String menuId) {
        return Optional.ofNullable(menuRepository.findById(menuId));
    }

    public Menu createMenu(MenuRequest request) {
        // 校验并创建菜单
    }

    public Optional<Menu> updateMenu(String menuId, MenuRequest request) {
        // 更新菜单
    }

    public boolean deleteMenu(String menuId) {
        return menuRepository.deleteById(menuId) > 0;
    }

    public List<Menu> getMenuTree() {
        // 获取树形菜单结构
    }
}
```

### 7.5 菜单管理接口列表

| 接口 | 方法 | 说明 |
|-----|------|------|
| `/api/menu/list` | GET | 获取所有菜单 |
| `/api/menu/tree` | GET | 获取菜单树 |
| `/api/menu/root` | GET | 获取根菜单 |
| `/api/menu/children/{parentId}` | GET | 获取子菜单 |
| `/api/menu/{menuId}` | GET | 获取菜单详情 |
| `/api/menu/code/{menuCode}` | GET | 根据代码获取菜单 |
| `/api/menu` | POST | 创建菜单 |
| `/api/menu/{menuId}` | PUT | 更新菜单 |
| `/api/menu/{menuId}` | DELETE | 删除菜单 |
| `/api/menu/count` | GET | 获取菜单数量 |

### 7.6 接口调用示例

#### 获取所有菜单

```bash
curl http://localhost:8080/api/menu/list
```

**响应：**
```json
[
  {
    "menuId": "M001",
    "menuName": "首页",
    "menuCode": "dashboard",
    "parentId": "0",
    "routePath": "/dashboard",
    "icon": "Dashboard",
    "sortOrder": 1,
    "isVisible": true,
    "permission": "dashboard:view",
    "component": "Dashboard"
  },
  ...
]
```

#### 创建菜单

```bash
curl -X POST http://localhost:8080/api/menu \
  -H "Content-Type: application/json" \
  -d '{
    "menuId": "M003",
    "menuName": "风险管理",
    "menuCode": "risk",
    "parentId": "0",
    "routePath": "/risk",
    "icon": "RiskIcon",
    "sortOrder": 3,
    "isVisible": true,
    "permission": "risk:manage",
    "component": "RiskLayout"
  }'
```

#### 更新菜单

```bash
curl -X PUT http://localhost:8080/api/menu/M003 \
  -H "Content-Type: application/json" \
  -d '{
    "menuName": "风险管理（新版）",
    "sortOrder": 4
  }'
```

#### 删除菜单

```bash
curl -X DELETE http://localhost:8080/api/menu/M003
```

### 7.7 前端调用菜单接口

```javascript
// src/api/menu.js
import api from './index';

export const menuApi = {
  getAllMenus() {
    return api.get('/api/menu/list');
  },

  getMenuTree() {
    return api.get('/api/menu/tree');
  },

  getMenuById(menuId) {
    return api.get(`/api/menu/${menuId}`);
  },

  createMenu(menuData) {
    return api.post('/api/menu', menuData);
  },

  updateMenu(menuId, menuData) {
    return api.post(`/api/menu/${menuId}`, menuData);
  },

  deleteMenu(menuId) {
    return api.delete(`/api/menu/${menuId}`);
  },
};
```

---

## 8. 前端调用方式

### 7.1 前端项目结构建议

```
frontend/
├── src/
│   ├── api/
│   │   ├── index.js              # API 基础配置
│   │   ├── simulation.js        # 模拟相关接口
│   │   └── algorithm.js         # 算法相关接口
│   │
│   ├── views/
│   │   └── Simulation.vue       # 模拟页面
│   │
│   └── main.js
```

### 7.2 API 基础配置

```javascript
// src/api/index.js
const API_BASE = 'http://localhost:8080';

const api = {
  baseUrl: API_BASE,

  async request(url, options = {}) {
    const response = await fetch(`${this.baseUrl}${url}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });
    return response.json();
  },

  get(url) {
    return this.request(url, { method: 'GET' });
  },

  post(url, data) {
    return this.request(url, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
};

export default api;
```

### 7.3 模拟服务接口

```javascript
// src/api/simulation.js
import api from './index';

export const simulationApi = {
  startSimulation(tariffRate) {
    return api.post('/api/simulation/start', { tariffRate });
  },

  startRiskScenario(scenarioType) {
    return api.post('/api/simulation/start-risk-scenario', { scenarioType });
  },

  startMLRisk(mlParams) {
    return api.post('/api/simulation/ml-risk', mlParams);
  },

  getTaskStatus(taskId) {
    return api.get(`/api/simulation/status/${taskId}`);
  },

  getAllTasks() {
    return api.get('/api/simulation/tasks');
  },
};
```

### 7.4 Vue 组件调用示例

```vue
<template>
  <div>
    <h2>关税风险模拟</h2>
    <button @click="startSimulation">启动模拟</button>
    <div v-if="taskId">
      <p>任务ID: {{ taskId }}</p>
      <p>状态: {{ status }}</p>
      <button @click="checkStatus">查询状态</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { simulationApi } from '@/api/simulation';

const taskId = ref('');
const status = ref('');

const startSimulation = async () => {
  const result = await simulationApi.startSimulation(20);
  taskId.value = result.taskId;
  status.value = result.status;
};

const checkStatus = async () => {
  if (!taskId.value) return;
  const task = await simulationApi.getTaskStatus(taskId.value);
  status.value = task.status;
};
</script>
```

### 7.5 React 组件调用示例

```jsx
import React, { useState } from 'react';
import { simulationApi } from '@/api/simulation';

function SimulationPage() {
  const [taskId, setTaskId] = useState('');
  const [status, setStatus] = useState('');

  const startSimulation = async () => {
    const result = await simulationApi.startSimulation(20);
    setTaskId(result.taskId);
    setStatus(result.status);
  };

  const checkStatus = async () => {
    if (!taskId) return;
    const task = await simulationApi.getTaskStatus(taskId);
    setStatus(task.status);
  };

  return (
    <div>
      <h2>关税风险模拟</h2>
      <button onClick={startSimulation}>启动模拟</button>
      {taskId && (
        <div>
          <p>任务ID: {taskId}</p>
          <p>状态: {status}</p>
          <button onClick={checkStatus}>查询状态</button>
        </div>
      )}
    </div>
  );
}
```

### 7.6 调用流程图

```
前端                      后端                      算法服务
 │                         │                         │
 │  POST /api/simulation/start                       │
 │ ───────────────────────>│                         │
 │                         │                         │
 │                         │  POST /tariff/execute   │
 │                         │ ────────────────────────>│
 │                         │                         │
 │   {taskId, status}       │   {taskId, status}      │
 │ <────────────────────────│                         │
 │                         │                         │
 │                         │        (异步执行中)       │
 │                         │                         │
 │                         │  POST /api/simulation/status (回调)
 │                         │ <────────────────────────│
 │                         │                         │
 │   GET /api/simulation/status/{taskId}             │
 │ ───────────────────────>│                         │
 │                         │                         │
 │   {taskId, status, result}                         │
 │ <────────────────────────│                         │
 │                         │                         │
```

---

## 8. 新增微服务

### 8.1 创建新服务模块

**Step 1: 在父 pom.xml 中添加模块**

```xml
<!-- backend/pom.xml -->
<modules>
    <module>risk-basic-service</module>
    <module>risk-report-service</module>  <!-- 新增 -->
</modules>
```

**Step 2: 创建服务目录结构**

```
backend/
├── risk-report-service/
│   ├── pom.xml
│   └── src/main/
│       ├── java/com/sci/risk/report/
│       │   ├── RiskReportApplication.java
│       │   ├── controller/
│       │   ├── service/
│       │   └── config/
│       └── resources/
│           └── application.properties
```

**Step 3: 创建 pom.xml**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.sci</groupId>
        <artifactId>risk-parent</artifactId>
        <version>1.0.0</version>
    </parent>

    <artifactId>risk-report-service</artifactId>
    <packaging>jar</packaging>
    <name>risk-report-service</name>
    <description>报表统计服务</description>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springdoc</groupId>
            <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
        </dependency>
    </dependencies>
</project>
```

**Step 4: 创建启动类**

```java
package com.sci.risk.report;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class RiskReportApplication {
    public static void main(String[] args) {
        SpringApplication.run(RiskReportApplication.class, args);
    }
}
```

**Step 5: 配置端口**

```properties
# risk-report-service/src/main/resources/application.properties
server.port=8081
spring.application.name=risk-report-service
```

### 8.2 添加 API Controller

```java
package com.sci.risk.report.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/report")
@CrossOrigin(origins = "*")
@Tag(name = "报表服务", description = "数据统计报表接口")
public class ReportController {

    @Operation(summary = "获取风险报表")
    @GetMapping("/risk")
    public Map<String, Object> getRiskReport() {
        return Map.of(
            "totalTasks", 100,
            "completedTasks", 80,
            "avgRiskScore", 65.5
        );
    }
}
```

### 8.3 启动多服务

```bash
# 终端1: 启动基础服务 (8080)
cd risk-basic-service
./mvnw spring-boot:run

# 终端2: 启动报表服务 (8081)
cd risk-report-service
./mvnw spring-boot:run
```

### 8.4 服务间通信

如果新服务需要调用基础服务或算法服务，使用 RestTemplate 或 WebClient：

```java
@Service
public class ReportService {

    private final RestTemplate restTemplate;

    public ReportService(RestTemplateBuilder builder) {
        this.restTemplate = builder.build();
    }

    public Map<String, Object> getCombinedReport() {
        // 调用基础服务的任务列表
        List tasks = restTemplate.getForObject(
            "http://localhost:8080/api/simulation/tasks",
            List.class
        );

        // 获取报表数据
        return Map.of("tasks", tasks, "reportData", computeReport(tasks));
    }
}
```

---

## 9. Docker 部署

### 9.1 构建镜像

```bash
cd backend

# 构建镜像
docker build -t risk-backend:latest .

# 或使用 docker-compose (推荐)
```

### 9.2 Docker Compose 多服务部署

创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
    networks:
      - risk-network

  algorithm-service:
    build: ../algorithms/risk-algorithm-service
    ports:
      - "5000:5000"
    networks:
      - risk-network

networks:
  risk-network:
    driver: bridge
```

### 9.3 运行

```bash
docker-compose up -d
```

---

## 附录：常用命令

```bash
# 清理构建
./mvnw clean

# 编译
./mvnw compile

# 运行测试
./mvnw test

# 打包
./mvnw package

# 跳过测试打包
./mvnw package -DskipTests

# 查看依赖树
./mvnw dependency:tree

# 分析依赖
./mvnw dependency:analyze
```
