const config = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || '/api',
  aiBaseUrl: import.meta.env.VITE_AI_BASE_URL || '/ai',
  token: 'mock_001_zhangsan_tariff:read,policy:read_tariff:*,policy:*'
}

export default config
