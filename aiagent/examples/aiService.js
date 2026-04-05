class AIService {
  constructor(baseURL = 'http://localhost:8000') {
    this.baseURL = baseURL
    this.token = null
  }

  setToken(token) {
    this.token = token
  }

  clearToken() {
    this.token = null
  }

  getHeaders() {
    const headers = { 'Content-Type': 'application/json' }
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }
    return headers
  }

  async chat(message, sessionId = null, context = {}) {
    const response = await fetch(`${this.baseURL}/api/ai/chat`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ message, session_id: sessionId, context })
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: '请求失败' }))
      throw new Error(error.detail || `HTTP error! status: ${response.status}`)
    }
    return response.json()
  }

  async classifyIntent(message) {
    const response = await fetch(`${this.baseURL}/api/ai/classify`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ message })
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return response.json()
  }

  async getAgents() {
    const response = await fetch(`${this.baseURL}/api/ai/agents`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return response.json()
  }

  async getAgent(agentId) {
    const response = await fetch(`${this.baseURL}/api/ai/agent/${agentId}`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return response.json()
  }

  async getAgentSkills(agentId) {
    const response = await fetch(`${this.baseURL}/api/ai/agent/${agentId}/skills`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return response.json()
  }

  async getAgentMcp(agentId) {
    const response = await fetch(`${this.baseURL}/api/ai/agent/${agentId}/mcp`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return response.json()
  }

  async validateToken() {
    if (!this.token) {
      throw new Error('未设置Token')
    }
    const response = await fetch(`${this.baseURL}/api/auth/validate`, {
      method: 'POST',
      headers: this.getHeaders()
    })
    return response.json()
  }

  async createTestToken(userId, username, permissions, dataScopes) {
    const params = new URLSearchParams({
      user_id: userId,
      username: username,
      permissions: permissions,
      data_scopes: dataScopes
    })
    const response = await fetch(`${this.baseURL}/api/auth/create_test_token?${params}`, {
      method: 'POST'
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return response.json()
  }
}

const aiService = new AIService()

export default aiService