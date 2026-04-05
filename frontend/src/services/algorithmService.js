import axios from 'axios'
import config from '../config'

const http = axios.create({ baseURL: config.apiBaseUrl })

const algorithmService = {
  /**
   * 获取两级分类树
   * GET /api/algorithm/categories
   */
  async getCategories() {
    const res = await http.get('/algorithm/categories')
    return res.data.categories || []
  },

  /**
   * 获取算法列表，支持按 category / type 过滤
   * GET /api/algorithm/list?category=risk&type=simulation
   */
  async getAlgorithms({ category, type } = {}) {
    const params = {}
    if (category) params.category = category
    if (type) params.type = type
    const res = await http.get('/algorithm/list', { params })
    return res.data || []
  },

  /**
   * 执行算法（通用入口）
   * POST /api/simulation/execute
   * @param {string} algorithmName  算法名称
   * @param {object} params         算法参数 JSON
   * @param {object} [notification] 通知配置 { type, recipients, title }
   */
  async execute(algorithmName, params = {}, notification = null) {
    const body = { algorithmName, params }
    if (notification && notification.type && notification.type !== 'none') {
      body.notification = notification
    }
    const res = await http.post('/simulation/execute', body)
    return res.data
  },

  /**
   * 查询任务状态
   * GET /api/simulation/status/:taskId
   */
  async getTaskStatus(taskId) {
    const res = await http.get(`/simulation/status/${taskId}`)
    return res.data
  },
}

export default algorithmService
