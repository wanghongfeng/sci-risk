<template>
  <div class="tariff-simulation">
    <!-- 参数配置区 -->
    <el-row :gutter="12" style="margin-bottom:12px">
      <el-col :span="8">
        <el-card shadow="never">
          <template #header><span class="card-title">模拟参数配置</span></template>

          <el-form label-position="top" size="default">
            <el-form-item label="选择算法">
              <el-select v-model="algorithmName" style="width:100%" :loading="algorithmsLoading" placeholder="请选择算法">
                <el-option
                  v-for="algo in algorithmList"
                  :key="algo.name"
                  :value="algo.name"
                  :label="algo.description ? algo.name + ' — ' + algo.description : algo.name"
                >
                  <div style="display:flex;justify-content:space-between;align-items:center">
                    <span>{{ algo.name }}</span>
                    <span style="font-size:12px;color:#aaa">{{ algo.description }}</span>
                  </div>
                  <div style="font-size:11px;color:#bbb;margin-top:2px">v{{ algo.version }} · <el-tag :type="algo.status === 'ONLINE' ? 'success' : 'danger'" size="small" style="transform:scale(0.85)">{{ algo.status }}</el-tag></div>
                </el-option>
              </el-select>
              <div v-if="selectedAlgo" style="margin-top:4px;font-size:12px;color:#888">
                端点: {{ selectedAlgo.endpoint }}
              </div>
            </el-form-item>

            <!-- tariff-risk-algorithm params -->
            <template v-if="algorithmType === 'tariff'">
              <el-form-item label="关税税率">
                <el-radio-group v-model="tariffRate">
                  <el-radio-button :value="10">10%</el-radio-button>
                  <el-radio-button :value="20">20%</el-radio-button>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="模拟产品">
                <el-select v-model="product" style="width:100%">
                  <el-option label="产品A（家用电器）" value="产品A" />
                  <el-option label="产品B（工业零件）" value="产品B" />
                  <el-option label="产品C（消费电子）" value="产品C" />
                </el-select>
              </el-form-item>
              <el-form-item label="基准利润（万元）">
                <el-input-number v-model="baseProfit" :min="100" :max="10000" :step="100" style="width:100%" />
              </el-form-item>
            </template>

            <!-- risk-scenarios-algorithm params -->
            <template v-else-if="algorithmType === 'scenario'">
              <el-form-item label="风险场景类型">
                <el-select v-model="scenarioType" style="width:100%">
                  <el-option label="供应链中断" value="supply_disruption" />
                  <el-option label="需求骤降" value="demand_shock" />
                  <el-option label="汇率波动" value="fx_volatility" />
                  <el-option label="地缘政治风险" value="geopolitical" />
                  <el-option label="自然灾害" value="natural_disaster" />
                </el-select>
              </el-form-item>
            </template>

            <!-- risk-ml-algorithm params -->
            <template v-else-if="algorithmType === 'ml'">
              <el-form-item label="历史数据点（逗号分隔）">
                <el-input v-model="mlHistoricalData" placeholder="例如: 100,200,150,300" />
              </el-form-item>
              <el-form-item label="风险权重（0~1）">
                <el-slider v-model="mlRiskWeight" :min="0" :max="1" :step="0.1" show-stops />
              </el-form-item>
            </template>

            <el-button type="primary" :loading="running" @click="startSimulation" style="width:100%">
              {{ running ? '模拟执行中...' : '开始模拟' }}
            </el-button>
          </el-form>
        </el-card>
      </el-col>

      <!-- 执行状态 -->
      <el-col :span="16">
        <el-card shadow="never" style="height:100%">
          <template #header>
            <div style="display:flex;align-items:center;justify-content:space-between">
              <span class="card-title">模拟执行状态</span>
              <el-tag v-if="task" :type="statusTagType" size="small">{{ statusLabel }}</el-tag>
            </div>
          </template>

          <div v-if="!task" class="empty-tip">
            <el-icon :size="40" color="#ccc"><DataAnalysis /></el-icon>
            <p>请在左侧配置参数后点击「开始模拟」</p>
          </div>

          <template v-else>
            <div class="progress-block">
              <div class="progress-label">
                <span>{{ task.currentStatus || '等待执行...' }}</span>
                <span>{{ progressVal }}%</span>
              </div>
              <el-progress :percentage="progressVal" :status="progressStatus" :stroke-width="10" />
            </div>

            <el-descriptions :column="2" border size="small" style="margin-top:16px">
              <el-descriptions-item label="任务ID">
                <span class="mono">{{ task.taskId }}</span>
              </el-descriptions-item>
              <el-descriptions-item label="关税税率">{{ tariffRate }}%</el-descriptions-item>
              <el-descriptions-item label="执行状态">
                <el-tag :type="statusTagType" size="small">{{ statusLabel }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="算法">{{ task.algorithmName || 'tariff-risk-algorithm' }}</el-descriptions-item>
            </el-descriptions>
          </template>
        </el-card>
      </el-col>
    </el-row>

    <!-- 模拟结果区 -->
    <el-card v-if="result" shadow="never">
      <template #header><span class="card-title">模拟结果</span></template>

      <el-row :gutter="12">
        <el-col :xs="24" :sm="6">
          <div class="result-metric">
            <div class="rm-label">关税税率</div>
            <div class="rm-val" style="color:#1890ff">{{ result.tariffRate }}%</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="6">
          <div class="result-metric">
            <div class="rm-label">基准利润</div>
            <div class="rm-val">{{ result.originalProfit ?? baseProfit }} 万元</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="6">
          <div class="result-metric">
            <div class="rm-label">税后利润</div>
            <div class="rm-val" :style="{ color: netProfit >= 0 ? '#52c41a' : '#ff4d4f' }">
              {{ netProfit }} 万元
            </div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="6">
          <div class="result-metric">
            <div class="rm-label">建议</div>
            <div class="rm-val" :style="{ color: result.recommendation === '维持生产' ? '#52c41a' : '#faad14', fontSize:'16px' }">
              {{ result.recommendation }}
            </div>
          </div>
        </el-col>
      </el-row>

      <el-alert style="margin-top:12px" :type="result.recommendation === '维持生产' ? 'success' : 'warning'" :closable="false" show-icon>
        <template #title>{{ result.result }}</template>
      </el-alert>

      <!-- result chart -->
      <div ref="resultChart" style="height:240px;margin-top:16px"></div>
    </el-card>

    <!-- 历史任务 -->
    <el-card shadow="never" style="margin-top:12px">
      <template #header>
        <div style="display:flex;align-items:center;justify-content:space-between">
          <span class="card-title">历史模拟任务</span>
          <el-button size="small" text @click="loadHistory">刷新</el-button>
        </div>
      </template>
      <el-table :data="historyList" size="small" max-height="240">
        <el-table-column prop="taskId" label="任务ID" min-width="240">
          <template #default="{ row }">
            <span class="mono">{{ row.taskId }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="tariffRate" label="税率" width="70">
          <template #default="{ row }">{{ row.tariffRate != null ? row.tariffRate + '%' : '-' }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getTagType(row.status)" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="currentStatus" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" width="80">
          <template #default="{ row }">
            <el-button size="small" text type="primary" @click="viewTask(row)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onUnmounted } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'
import { DataAnalysis } from '@element-plus/icons-vue'
import config from '../config'

const api = axios.create({
  baseURL: config.apiBaseUrl,
  headers: { Authorization: `Bearer ${config.token}` }
})

// ── algorithm list ────────────────────────────────────────────
const algorithmList = ref([])
const algorithmsLoading = ref(false)
const algorithmName = ref('')
const selectedAlgo = computed(() => algorithmList.value.find(a => a.name === algorithmName.value) ?? null)

const loadAlgorithms = async () => {
  algorithmsLoading.value = true
  try {
    const res = await api.get('/algorithm/list')
    algorithmList.value = res.data ?? []
    if (algorithmList.value.length > 0 && !algorithmName.value) {
      algorithmName.value = algorithmList.value[0].name
    }
  } catch {
    // backend may be offline; leave list empty
  } finally {
    algorithmsLoading.value = false
  }
}
loadAlgorithms()

// ── form state ────────────────────────────────────────────────
const tariffRate = ref(10)
const product = ref('产品A')
const baseProfit = ref(1000)
const scenarioType = ref('supply_disruption')
const mlHistoricalData = ref('100,200,150,300,250')
const mlRiskWeight = ref(0.5)

// algorithmType derived from algorithmName
const algorithmType = computed(() => {
  const n = algorithmName.value
  if (n.includes('scenario')) return 'scenario'
  if (n.includes('ml')) return 'ml'
  return 'tariff'
})

// ── task / polling ────────────────────────────────────────────
const running = ref(false)
const task = ref(null)
const result = ref(null)
const progressVal = ref(0)
let pollTimer = null
let resultChart = ref(null)
let chartInst = null

const statusLabel = computed(() => {
  const map = { PENDING: '等待中', EXECUTING: '执行中', COMPLETED: '已完成', FAILED: '失败' }
  return map[task.value?.status] ?? task.value?.status ?? '-'
})
const statusTagType = computed(() => {
  const map = { PENDING: 'info', EXECUTING: 'warning', COMPLETED: 'success', FAILED: 'danger' }
  return map[task.value?.status] ?? ''
})
const progressStatus = computed(() => {
  if (task.value?.status === 'FAILED') return 'exception'
  if (task.value?.status === 'COMPLETED') return 'success'
  return ''
})
const netProfit = computed(() => {
  if (!result.value) return 0
  const profit = result.value.originalProfit ?? baseProfit.value
  const cost = Math.round(profit * (tariffRate.value / 100))
  return profit - cost
})

// ── start simulation ──────────────────────────────────────────
const startSimulation = async () => {
  if (!algorithmName.value) {
    return
  }
  running.value = true
  result.value = null
  task.value = null
  progressVal.value = 0
  clearPoll()

  try {
    const type = algorithmType.value
    let params = {}

    if (type === 'tariff') {
      params = { tariffRate: tariffRate.value }
    } else if (type === 'scenario') {
      params = { scenarioType: scenarioType.value }
    } else {
      const historical = mlHistoricalData.value.split(',').map(Number).filter(n => !isNaN(n))
      params = {
        historicalData: historical,
        riskFactors: { weight: mlRiskWeight.value }
      }
    }

    const res = await api.post('/simulation/execute', {
      algorithmName: algorithmName.value,
      params
    })
    task.value = { taskId: res.data.taskId, status: res.data.status, currentStatus: res.data.message }
    pollStatus(res.data.taskId)
  } catch (e) {
    running.value = false
    task.value = { taskId: '-', status: 'FAILED', currentStatus: e.response?.data?.message ?? '请求失败，请确认后端已启动' }
  }
}

const pollStatus = (taskId) => {
  clearPoll()
  pollTimer = setInterval(async () => {
    try {
      const res = await api.get(`/simulation/status/${taskId}`)
      const t = res.data
      task.value = t

      // parse progress from currentStatus text like "进度50%"
      const match = (t.currentStatus ?? '').match(/(\d+)%/)
      if (match) progressVal.value = parseInt(match[1])
      if (t.status === 'COMPLETED') progressVal.value = 100

      if (t.status === 'COMPLETED' || t.status === 'FAILED') {
        clearPoll()
        running.value = false
        if (t.result) {
          result.value = typeof t.result === 'string' ? JSON.parse(t.result) : t.result
          await nextTick()
          renderResultChart()
        }
        loadHistory()
      }
    } catch {
      // ignore transient errors
    }
  }, 1000)
}

const clearPoll = () => { if (pollTimer) { clearInterval(pollTimer); pollTimer = null } }

// ── result chart ──────────────────────────────────────────────
const renderResultChart = () => {
  if (!resultChart.value) return
  if (chartInst) chartInst.dispose()
  chartInst = echarts.init(resultChart.value)

  const profit = result.value?.originalProfit ?? baseProfit.value
  const tax = Math.round(profit * (tariffRate.value / 100))
  const net = profit - tax

  chartInst.setOption({
    tooltip: {},
    legend: { bottom: 0 },
    xAxis: { type: 'category', data: ['基准利润', '关税成本', '税后利润'] },
    yAxis: { type: 'value', name: '万元' },
    series: [{
      name: '金额（万元）',
      type: 'bar',
      barWidth: '40%',
      data: [
        { value: profit, itemStyle: { color: '#1890ff' } },
        { value: tax,    itemStyle: { color: '#ff4d4f' } },
        { value: net,    itemStyle: { color: net >= 0 ? '#52c41a' : '#faad14' } }
      ],
      label: { show: true, position: 'top', formatter: '{c} 万' }
    }]
  })
}

// ── history ───────────────────────────────────────────────────
const historyList = ref([])
const loadHistory = async () => {
  try {
    const res = await api.get('/simulation/tasks')
    historyList.value = (res.data ?? []).slice().reverse()
  } catch { /* backend may be offline */ }
}
loadHistory()

const viewTask = (row) => {
  task.value = row
  progressVal.value = row.status === 'COMPLETED' ? 100 : 0
  if (row.result) {
    result.value = typeof row.result === 'string' ? JSON.parse(row.result) : row.result
    nextTick(renderResultChart)
  } else {
    result.value = null
  }
}

const getTagType = (s) => ({ PENDING: 'info', EXECUTING: 'warning', COMPLETED: 'success', FAILED: 'danger' }[s] ?? '')

onUnmounted(() => {
  clearPoll()
  chartInst?.dispose()
})
</script>

<style scoped>
.tariff-simulation { height: 100%; }

.card-title { font-weight: 600; font-size: 14px; }

.empty-tip {
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; padding: 40px 0; color: #aaa;
  gap: 8px;
}

.progress-block { padding: 8px 0; }
.progress-label { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 13px; color: #555; }

.result-metric {
  text-align: center; padding: 16px 8px;
  background: #fafafa; border-radius: 8px;
}
.rm-label { font-size: 12px; color: #888; margin-bottom: 6px; }
.rm-val { font-size: 22px; font-weight: 700; }

.mono { font-family: monospace; font-size: 12px; color: #666; }
</style>
