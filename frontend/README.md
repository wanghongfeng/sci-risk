# 供应链控制塔前端

基于 Vue3  + Vite + Element Plus 的风险模拟平台前端应用。

## 项目结构

```
frontend/
├── src/
│   ├── App.vue                 # 主应用入口
│   ├── main.js                 # 应用初始化
│   ├── config.js               # 统一配置文件
│   ├── aiService.js            # AI 服务调用模块
│   ├── router/
│   │   └── index.js            # 路由配置
│   ├── views/
│   │   ├── Layout.vue          # 经典后台布局
│   │   ├── Dashboard.vue       # 首页 Dashboard
│   │   └── MenuManage.vue      # 菜单管理页面
│   └── components/
│       └── AIChat.vue           # AI 助手组件
├── index.html
├── vite.config.js              # Vite 配置
└── package.json
```

## 技术栈

| 技术           | 说明                                 |
| ------------ | ---------------------------------- |
| Vue 3        | 渐进式 JavaScript 框架（Composition API） |
| Vite         | 新一代前端构建工具                          |
| Element Plus | Vue 3 UI 组件库                       |
| ECharts      | 数据可视化图表库                           |
| D3.js        | 数据驱动文档（全球旋转地图）                     |
| Axios        | HTTP 请求客户端                         |
| Vue Router   | Vue 官方路由管理器                        |

## 统一配置

所有 API 配置集中在 `src/config.js` 文件中管理：

```javascript
const config = {
  apiBaseUrl: '/api',           // Java 后端接口地址
  aiBaseUrl: '/ai',             // AI Agent 接口地址
  token: 'mock_...'             // 认证 Token
}
```

修改接口地址只需更新此文件即可。

## 跨域处理

通过 Vite Proxy 解决跨域问题，配置见 `vite.config.js`：

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8080',  // Java 后端
    changeOrigin: true
  },
  '/ai': {
    target: 'http://localhost:8000',  // AI Agent
    changeOrigin: true
  }
}
```

## 页面路由

| 路径           | 页面         | 说明            |
| ------------ | ---------- | ------------- |
| `/dashboard` | Dashboard  | 首页（风险图表+旋转地球） |
| `/menu`      | MenuManage | 菜单管理（增删改查+导出） |

## 页面功能

### 1. Dashboard 首页

- **统计卡片**：风险事件、受影响区域、高风险企业、涉及金额
- **风险趋势图**：ECharts 折线图，展示关税/供应链/物流风险趋势
- **全球风险分布**：D3.js 3D 旋转地球仪
- **风险类型分布**：ECharts 饼图
- **地区风险排名**：ECharts 柱状图
- **风险预警列表**：显示各地区风险级别

### 2. 菜单管理

调用后端 `/api/menu/*` 接口实现菜单维护：

| 接口                   | 方法     | 功能    |
| -------------------- | ------ | ----- |
| `/api/menu/tree`     | GET    | 获取菜单树 |
| `/api/menu`          | POST   | 创建菜单  |
| `/api/menu/{menuId}` | PUT    | 更新菜单  |
| `/api/menu/{menuId}` | DELETE | 删除菜单  |

功能特性：

- 树形表格展示菜单结构
- 新增顶级菜单/子菜单
- 编辑菜单信息
- 删除菜单（带确认）
- 导出菜单为 JSON 文件

## AI 助手组件

### 功能特性

- 悬浮式 AI 助手窗口，点击按钮展开/收起
- 支持回车发送消息
- 显示 AI 响应及来源 Agent 信息
- 优雅的渐变色 UI 设计

### 使用方式

全局注册后可在任意页面使用 `<AIChat />` 组件。

### AI 服务调用

`src/aiService.js` 提供统一的 AI 服务调用接口：

```javascript
import aiService from './aiService'

const result = await aiService.chat('关税政策是什么？')
console.log(result.response)    // AI 响应内容
console.log(result.agent_name) // 来源 Agent 名称
```

### AI 接口响应示例

```json
{
  "response": "关税政策正在发展...",
  "intent": {
    "intent_name": "tariff_analysis",
    "confidence": 0.95,
    "keywords": ["关税"]
  },
  "agent_id": "tariff_agent",
  "agent_name": "关税政策分析智能体",
  "skills_used": ["tariff_analysis"],
  "success": true
}
```

## 开发命令

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## 环境要求

- Node.js >= 14
- npm >= 6

## 后端依赖

前端正常运行需要以下后端服务：

| 服务       | 地址                      | 说明        |
| -------- | ----------------------- | --------- |
| Java 后端  | <http://localhost:8080> | 供应链风险模拟接口 |
| AI Agent | <http://localhost:8000> | 智能对话服务    |

