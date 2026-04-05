# AI Agent Gateway

基于 FastAPI 的智能代理网关，提供两层模型架构：
- **第一层（Core）**: 意图识别 - 识别用户输入并路由到对应的 Agent
- **第二层（Agents）**: 语义执行 - 各垂直领域的智能体，执行具体任务

## 特性

- 两层模型架构（意图识别 + 语义输出）
- 多 Agent 支持，每个 Agent 独立配置
- Token 验证 + 权限控制 + 数据范围
- 支持 OpenAI / OpenRouter / Mock
- 前端 Vue/React 集成示例

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. 测试请求

```bash
curl -X POST "http://localhost:8000/api/ai/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"关税政策\"}"
```

---

## 项目结构

```
aiagent/
├── agents/                    # Agent 实现
│   ├── base_agent.py         # 基类
│   ├── tariff_agent/          # 关税 Agent
│   │   ├── skills/
│   │   ├── prompts/
│   │   └── mcp/
│   └── default_agent/        # 默认 Agent
├── config/
│   └── llm_config.json       # LLM 配置
├── core/
│   └── intent_classifier.py  # 意图分类
├── llm/                       # LLM Provider
│   ├── base.py
│   ├── openai_provider.py
│   ├── openrouter_provider.py
│   ├── mock_provider.py
│   └── service.py
├── security/
│   └── auth_service.py       # 认证服务
├── services/
│   └── agent_factory.py      # Agent 工厂
├── examples/
│   └── aiService.js          # 前端示例
└── main.py                   # API Gateway
```

---

## LLM 配置

配置文件位于 `config/llm_config.json`。

### Mock 模式（默认）

无需配置，直接使用：

```json
{
  "provider": "mock"
}
```

### OpenAI

```json
{
  "provider": "openai",
  "openai": {
    "api_key": "your-openai-api-key",
    "default_model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2048
  }
}
```

### OpenRouter

```json
{
  "provider": "openrouter",
  "openrouter": {
    "api_key": "your-openrouter-api-key",
    "default_model": "anthropic/claude-3-sonnet",
    "temperature": 0.7,
    "max_tokens": 2048
  }
}
```

### 不同 Agent 使用不同模型

```json
{
  "provider": "mock",
  "agents": {
    "tariff_agent": {
      "provider": "openai",
      "model": "gpt-4-turbo"
    },
    "default_agent": {
      "provider": "openrouter",
      "model": "anthropic/claude-3-haiku"
    }
  }
}
```

| 配置项 | 说明 |
|--------|------|
| provider | 全局默认 Provider: `mock`, `openai`, `openrouter` |
| api_key | API Key |
| default_model | 默认模型 |
| temperature | 温度参数（0-1） |
| max_tokens | 最大生成 Token 数 |
| timeout | 请求超时时间（秒） |

---

## API 文档

### 基础信息

| 项目 | 值 |
|------|-----|
| Base URL | `http://localhost:8000` |
| API Version | 1.0.0 |
| 认证方式 | Bearer Token |

### 认证接口

#### 创建测试 Token

```http
POST /api/auth/create_test_token?user_id=001&username=zhangsan&permissions=tariff:read,policy:read&data_scopes=tariff:*,policy:*
```

#### 验证 Token

```http
POST /api/auth/validate
Authorization: Bearer <token>
```

### AI 对话接口

#### 主对话接口

```http
POST /api/ai/chat
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "查询美国对中国商品的关税政策",
  "session_id": "可选的会话ID"
}
```

**响应:**

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
  "success": true,
  "permissions_checked": ["tariff:read"],
  "data_scope_used": ["tariff:*"]
}
```

#### 意图识别接口

```http
POST /api/ai/classify
Authorization: Bearer <token>

{
  "message": "关税政策"
}
```

### Agent 管理接口

| 接口 | 说明 |
|------|------|
| `GET /api/ai/agents` | 获取所有 Agent |
| `GET /api/ai/agent/{agent_id}` | 获取单个 Agent |
| `GET /api/ai/agent/{agent_id}/skills` | 获取 Agent 技能列表 |
| `GET /api/ai/agent/{agent_id}/mcp` | 获取 Agent MCP 配置 |

---

## 路由规则

| 关键词 | 路由到 Agent |
|--------|-------------|
| 关税, tariff, 税率 | tariff_agent |
| 其他 | default_agent |

---

## 前端集成

### JavaScript / Vue / React

将 `examples/aiService.js` 复制到项目中使用。

```javascript
import aiService from '@/services/aiService'

async function sendMessage() {
  const result = await aiService.chat('查询关税政策')
  console.log(result.response)
  console.log(result.agent_name)
}
```

#### Vue 3 组件示例

```vue
<template>
  <div class="ai-chat">
    <div class="messages" ref="messagesRef">
      <div
        v-for="msg in messages"
        :key="msg.id"
        :class="['message', msg.role]"
      >
        <div class="message-content">{{ msg.content }}</div>
        <div v-if="msg.agent" class="message-meta">
          来自 {{ msg.agent }}
        </div>
      </div>
    </div>

    <div class="input-area">
      <input
        v-model="input"
        @keyup.enter="send"
        placeholder="输入消息..."
        :disabled="loading"
      />
      <button @click="send" :disabled="loading">
        {{ loading ? '处理中...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import aiService from '@/services/aiService'

const input = ref('')
const messages = ref([])
const loading = ref(false)
const messagesRef = ref(null)

async function send() {
  if (!input.value.trim() || loading.value) return

  const userMessage = input.value
  input.value = ''

  messages.value.push({
    id: Date.now(),
    role: 'user',
    content: userMessage
  })

  try {
    loading.value = true
    const result = await aiService.chat(userMessage)

    messages.value.push({
      id: Date.now() + 1,
      role: 'assistant',
      content: result.response,
      agent: result.agent_name
    })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.ai-chat {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}
.messages {
  height: 400px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}
.message {
  margin-bottom: 16px;
  padding: 12px;
  border-radius: 8px;
}
.message.user {
  background: #e3f2fd;
  margin-left: 20%;
}
.message.assistant {
  background: #f5f5f5;
  margin-right: 20%;
}
.input-area {
  display: flex;
  gap: 8px;
}
.input-area input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.input-area button {
  padding: 12px 24px;
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
</style>
```

#### React 组件示例

```jsx
import { useState } from 'react'
import aiService from '@/services/aiService'

export default function AIChat() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  async function send() {
    if (!input.trim() || loading) return

    const userMessage = input
    setInput('')

    setMessages(prev => [...prev, { id: Date.now(), role: 'user', content: userMessage }])

    try {
      setLoading(true)
      const result = await aiService.chat(userMessage)

      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'assistant',
        content: result.response,
        agent: result.agent_name
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="ai-chat">
      <div className="messages">
        {messages.map(msg => (
          <div key={msg.id} className={`message ${msg.role}`}>
            <div>{msg.content}</div>
            {msg.agent && <div className="meta">来自 {msg.agent}</div>}
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyUp={e => e.key === 'Enter' && send()}
          disabled={loading}
        />
        <button onClick={send} disabled={loading}>
          {loading ? '处理中...' : '发送'}
        </button>
      </div>
    </div>
  )
}
```

---

## 安全机制

- **Token 验证**: 每次请求需携带有效 Token
- **权限控制**: 基于用户 Token 提取权限，Agent 执行前进行权限校验
- **数据范围**: 支持细粒度的数据访问控制

### Mock Token 格式

开发测试使用 Mock Token：

```
mock_{user_id}_{username}_{permissions}_{data_scopes}
```

示例：
```
mock_001_zhangsan_tariff:read,policy:read_tariff:*,policy:*
```

---

## 错误处理

```javascript
try {
  const result = await aiService.chat('查询关税')
} catch (error) {
  switch (error.message) {
    case 'Token无效':
      // 跳转登录
      break
    case 'Token已过期':
      // 刷新Token
      break
    case '权限不足':
      // 提示用户权限不足
      break
    default:
      // 其他错误
  }
}
```

---

## 测试验证

```bash
# 测试关税查询
curl -X POST "http://localhost:8000/api/ai/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"美国调整了关税，中国怎么办\"}"

# 测试通用查询
curl -X POST "http://localhost:8000/api/ai/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"今天天气怎么样\"}"
```
