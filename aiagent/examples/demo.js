import aiService from './aiService.js'

async function demo() {
  console.log('=== AI Agent Gateway 调用示例 ===\n')

  console.log('1. 获取可用智能体列表:')
  const agents = await aiService.getAgents()
  console.log(JSON.stringify(agents, null, 2))
  console.log()

  console.log('2. 测试关税相关问题 (应路由到 tariff_agent):')
  const tariffResult = await aiService.chat('查询美国对中国商品的关税政策')
  console.log('意图:', tariffResult.intent)
  console.log('Agent:', tariffResult.agent_name)
  console.log('响应:', tariffResult.response)
  console.log()

  console.log('3. 测试非关税问题 (应路由到 default_agent):')
  const defaultResult = await aiService.chat('今天天气怎么样')
  console.log('意图:', defaultResult.intent)
  console.log('Agent:', defaultResult.agent_name)
  console.log('响应:', defaultResult.response)
  console.log()

  console.log('4. 仅意图识别测试:')
  const classifyResult = await aiService.classifyIntent('关税税率是多少')
  console.log(JSON.stringify(classifyResult, null, 2))
}

demo().catch(console.error)
