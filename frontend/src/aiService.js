import axios from 'axios'
import config from './config'

const aiService = {
  async chat(message, sessionId = null) {
    try {
      const requestData = {
        message: message,
        session_id: sessionId
      }

      const response = await axios.post(`${config.aiBaseUrl}/api/ai/chat`, requestData, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${config.token}`
        }
      })

      return response.data
    } catch (error) {
      if (error.response) {
        const { status, data } = error.response
        if (status === 401 || status === 403) {
          throw new Error('Token无效')
        }
        throw new Error(data.message || 'AI服务调用失败')
      }
      throw new Error('网络错误，请检查连接')
    }
  },

  async classify(message) {
    try {
      const response = await axios.post(`${config.aiBaseUrl}/api/ai/classify`, {
        message: message
      }, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${config.token}`
        }
      })

      return response.data
    } catch (error) {
      throw new Error('意图分类失败')
    }
  },

  async getAgents() {
    try {
      const response = await axios.get(`${config.aiBaseUrl}/api/ai/agents`, {
        headers: {
          'Authorization': `Bearer ${config.token}`
        }
      })

      return response.data
    } catch (error) {
      throw new Error('获取Agent列表失败')
    }
  }
}

export default aiService