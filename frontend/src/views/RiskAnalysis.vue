<template>
  <div class="risk-analysis">
    <el-row :gutter="16" style="height:100%">
      <!-- 左侧分类导航 -->
      <el-col :span="5">
        <el-card class="sidebar-card">
          <template #header><span class="card-title">算法分类</span></template>
          <el-tree
            :data="categoryTreeData"
            :props="{ label: 'label', children: 'children' }"
            highlight-current
            default-expand-all
            @node-click="onCategoryClick"
          />
        </el-card>
      </el-col>

      <!-- 右侧内容区 -->
      <el-col :span="19">
        <!-- 算法列表 -->
        <el-card class="algo-list-card">
          <template #header>
            <div class="card-header-row">
              <span class="card-title">
                {{ currentLabel || '全部算法' }}
                <el-tag size="small" type="info" style="margin-left:8px">{{ algorithms.length }}</el-tag>
              </span>
            </div>
          </template>

          <el-empty v-if="!algorithms.length" description="暂无算法" />

          <div v-else class="algo-cards">
            <el-card
              v-for="algo in algorithms"
              :key="algo.name"
              class="algo-item"
              shadow="hover"
              :class="{ selected: selectedAlgo?.name === algo.name }"
              @click="selectAlgo(algo)"
            >
              <div class="algo-item-header">
                <span class="algo-label">{{ algo.label || algo.description }}</span>
                <el-tag size="small" :type="typeTagColor(algo.type)">{{ typeLabel(algo.type) }}</el-tag>
              </div>
              <div class="algo-desc">{{ algo.description }}</div>
              <div class="algo-version">v{{ algo.version }}</div>
            </el-card>
          </div>
        </el-card>

        <!-- 执行面板 -->
        <el-card v-if="selectedAlgo" class="exec-card">
          <template #header>
            <div class="card-header-row">
              <span class="card-title">执行：{{ selectedAlgo.label || selectedAlgo.description }}</span>
              <el-button type="primary" :loading="executing" @click="runAlgorithm">
                立即执行
              </el-button>
            </div>
          </template>

          <el-row :gutter="16">
            <!-- 参数输入 -->
            <el-col :span="12">
              <div class="section-title">算法参数 (JSON)</div>
              <el-input
                v-model="paramsText"
                type="textarea"
                :rows="8"
                placeholder='{"key": "value"}'
                :class="{ 'param-error': paramsError }"
              />
              <div v-if="paramsError" class="error-tip">{{ paramsError }}</div>
              <div class="params-hint" v-if="selectedAlgo.paramsSchema?.properties">
                <div class="hint-title">参数说明：</div>
                <div
                  v-for="(schema, key) in selectedAlgo.paramsSchema.properties"
                  :key="key"
                  class="hint-item"
                >
                  <span class="hint-key">{{ key }}</span>
                  <span class="hint-desc">{{ schema.description }}</span>
                  <el-tag v-if="isRequired(key)" size="small" type="danger">必填</el-tag>
                </div>
              </div>
            </el-col>

            <!-- 通知配置 -->
            <el-col :span="12">
              <div class="section-title">通知配置（可选）</div>
              <el-form label-width="80px" size="small">
                <el-form-item label="通知类型">
                  <el-select v-model="notification.type" style="width:100%">
                    <el-option label="不通知" value="none" />
                    <el-option label="邮件" value="email" />
                    <el-option label="短信" value="sms" />
                    <el-option label="Webhook" value="webhook" />
                    <el-option label="即时消息" value="im" />
                  </el-select>
                </el-form-item>
                <el-form-item v-if="notification.type !== 'none'" label="通知人">
                  <el-input
                    v-model="notification.recipientsText"
                    placeholder="多个用逗号分隔，如 a@b.com, user2"
                  />
                </el-form-item>
                <el-form-item v-if="notification.type !== 'none'" label="通知标题">
                  <el-input v-model="notification.title" placeholder="可选" />
                </el-form-item>
              </el-form>

              <!-- 执行结果 -->
              <div v-if="taskResult" class="result-box">
                <div class="section-title">执行结果</div>
                <el-alert
                  :type="taskResult.status === 'COMPLETED' ? 'success' : taskResult.status === 'FAILED' ? 'error' : 'info'"
                  :title="`状态：${taskResult.status}`"
                  :description="taskResult.result || taskResult.currentStatus"
                  show-icon
                  :closable="false"
                  style="margin-bottom:8px"
                />
                <div v-if="taskResult.riskScore !== undefined" class="metric-row">
                  <span>风险评分</span>
                  <el-progress
                    :percentage="taskResult.riskScore"
                    :color="riskColor(taskResult.riskScore)"
                    style="flex:1;margin:0 12px"
                  />
                  <el-tag :type="levelTagType(taskResult.riskLevel)">{{ taskResult.riskLevel }}</el-tag>
                </div>
                <div v-if="taskResult.recommendation" class="recommendation">
                  建议：{{ taskResult.recommendation }}
                </div>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import algorithmService from '../services/algorithmService'

const categories = ref([])
const algorithms = ref([])
const selectedAlgo = ref(null)
const currentLabel = ref('')
const currentFilter = ref({ category: null, type: null })

const paramsText = ref('{}')
const paramsError = ref('')
const executing = ref(false)
const taskResult = ref(null)

const notification = ref({
  type: 'none',
  recipientsText: '',
  title: '',
})

// 构建树形数据
const categoryTreeData = computed(() => {
  const all = { id: '__all', label: '全部算法', children: [] }
  categories.value.forEach(cat => {
    const node = {
      id: cat.category,
      label: cat.label,
      _category: cat.category,
      children: (cat.types || []).map(t => ({
        id: `${cat.category}__${t.type}`,
        label: `${t.label} (${t.count})`,
        _category: cat.category,
        _type: t.type,
      }))
    }
    all.children.push(node)
  })
  return [all]
})

async function loadCategories() {
  try {
    categories.value = await algorithmService.getCategories()
  } catch {
    ElMessage.error('获取算法分类失败')
  }
}

async function loadAlgorithms(filter = {}) {
  try {
    algorithms.value = await algorithmService.getAlgorithms(filter)
  } catch {
    ElMessage.error('获取算法列表失败')
  }
}

function onCategoryClick(node) {
  if (node.id === '__all') {
    currentLabel.value = ''
    currentFilter.value = {}
  } else if (node._type) {
    currentLabel.value = node.label
    currentFilter.value = { category: node._category, type: node._type }
  } else {
    currentLabel.value = node.label
    currentFilter.value = { category: node._category }
  }
  selectedAlgo.value = null
  taskResult.value = null
  loadAlgorithms(currentFilter.value)
}

function selectAlgo(algo) {
  selectedAlgo.value = algo
  taskResult.value = null
  paramsError.value = ''
  // 用 paramsSchema 的 example 初始化参数
  const defaults = {}
  const props = algo.paramsSchema?.properties || {}
  Object.entries(props).forEach(([k, v]) => {
    if (v.example !== undefined) defaults[k] = v.example
  })
  paramsText.value = JSON.stringify(defaults, null, 2)
}

async function runAlgorithm() {
  paramsError.value = ''
  let params = {}
  try {
    params = JSON.parse(paramsText.value || '{}')
  } catch {
    paramsError.value = 'JSON 格式有误，请检查'
    return
  }

  const notifPayload = notification.value.type !== 'none'
    ? {
        type: notification.value.type,
        recipients: notification.value.recipientsText
          .split(',').map(s => s.trim()).filter(Boolean),
        title: notification.value.title,
      }
    : null

  executing.value = true
  taskResult.value = null
  try {
    const resp = await algorithmService.execute(selectedAlgo.value.name, params, notifPayload)
    taskResult.value = { status: resp.status, taskId: resp.taskId }
    // 轮询任务结果
    pollTask(resp.taskId)
  } catch (e) {
    ElMessage.error('执行失败：' + (e.message || '未知错误'))
  } finally {
    executing.value = false
  }
}

function pollTask(taskId) {
  const interval = setInterval(async () => {
    try {
      const task = await algorithmService.getTaskStatus(taskId)
      if (task && (task.status === 'COMPLETED' || task.status === 'FAILED')) {
        taskResult.value = task.result || task
        clearInterval(interval)
      }
    } catch {
      clearInterval(interval)
    }
  }, 1500)
  // 30s 超时
  setTimeout(() => clearInterval(interval), 30000)
}

function isRequired(key) {
  return (selectedAlgo.value?.paramsSchema?.required || []).includes(key)
}

function typeLabel(type) {
  const map = {
    simulation: '风险模拟', classification: '风险分类', assessment: '综合评估',
    order_simulation: '订单模拟', production_transfer: '转产规划',
    consumption: '消耗模拟', replenishment: '补货建议',
  }
  return map[type] || type
}

function typeTagColor(type) {
  const map = {
    simulation: 'danger', classification: 'warning', assessment: 'success',
    order_simulation: '', production_transfer: 'info',
  }
  return map[type] || ''
}

function riskColor(score) {
  if (score >= 70) return '#f56c6c'
  if (score >= 40) return '#e6a23c'
  return '#67c23a'
}

function levelTagType(level) {
  const map = { HIGH: 'danger', MEDIUM: 'warning', LOW: 'success' }
  return map[level] || 'info'
}

onMounted(() => {
  loadCategories()
  loadAlgorithms()
})
</script>

<style scoped>
.risk-analysis {
  height: 100%;
  padding: 0;
}
.sidebar-card {
  height: 100%;
}
.card-title {
  font-weight: 600;
  font-size: 15px;
}
.card-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.algo-list-card {
  margin-bottom: 16px;
}
.algo-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
.algo-item {
  width: calc(33% - 8px);
  cursor: pointer;
  transition: border-color 0.2s;
}
.algo-item.selected {
  border-color: var(--el-color-primary);
}
.algo-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}
.algo-label {
  font-weight: 600;
  font-size: 14px;
}
.algo-desc {
  font-size: 12px;
  color: #666;
  margin-bottom: 4px;
}
.algo-version {
  font-size: 11px;
  color: #aaa;
}
.exec-card {
  margin-top: 0;
}
.section-title {
  font-weight: 600;
  font-size: 13px;
  margin-bottom: 8px;
  color: #303133;
}
.param-error {
  --el-input-border-color: var(--el-color-danger);
}
.error-tip {
  color: var(--el-color-danger);
  font-size: 12px;
  margin-top: 4px;
}
.params-hint {
  margin-top: 12px;
  font-size: 12px;
}
.hint-title {
  color: #666;
  margin-bottom: 4px;
}
.hint-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}
.hint-key {
  font-family: monospace;
  color: var(--el-color-primary);
  min-width: 100px;
}
.hint-desc {
  color: #666;
  flex: 1;
}
.result-box {
  margin-top: 16px;
}
.metric-row {
  display: flex;
  align-items: center;
  margin-top: 8px;
  font-size: 13px;
}
.recommendation {
  margin-top: 8px;
  padding: 8px;
  background: #f5f7fa;
  border-radius: 4px;
  font-size: 13px;
}
</style>
