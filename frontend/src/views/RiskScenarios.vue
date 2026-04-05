<template>
  <div class="risk-scenarios">
    <!-- 场景选择区 -->
    <el-card class="scenarios-card">
      <template #header>
        <div class="card-header-row">
          <span class="card-title">风险场景分析</span>
          <el-tag type="info">category: risk / type: classification</el-tag>
        </div>
      </template>

      <el-row :gutter="16">
        <el-col
          v-for="scene in scenarios"
          :key="scene.type"
          :span="6"
        >
          <el-card
            class="scene-card"
            shadow="hover"
            :class="{ selected: selectedScene === scene.type }"
            @click="selectScene(scene)"
          >
            <el-icon :size="32" :color="scene.color" class="scene-icon">
              <component :is="scene.icon" />
            </el-icon>
            <div class="scene-name">{{ scene.name }}</div>
            <div class="scene-desc">{{ scene.desc }}</div>
            <el-tag :type="scene.levelType" size="small" class="scene-level">
              {{ scene.level }}
            </el-tag>
          </el-card>
        </el-col>
      </el-row>
    </el-card>

    <!-- 执行配置区 -->
    <el-row :gutter="16" class="exec-row" v-if="selectedScene">
      <el-col :span="16">
        <el-card>
          <template #header>
            <div class="card-header-row">
              <span class="card-title">执行场景：{{ currentSceneObj?.name }}</span>
              <el-button
                type="primary"
                :loading="executing"
                :disabled="!selectedScene"
                @click="runScenario"
              >
                开始分析
              </el-button>
            </div>
          </template>

          <el-form label-width="90px" size="default">
            <el-form-item label="分析地区">
              <el-select v-model="execParams.region" placeholder="全球" style="width:200px">
                <el-option label="全球" value="全球" />
                <el-option label="北美" value="北美" />
                <el-option label="东南亚" value="东南亚" />
                <el-option label="欧洲" value="欧洲" />
                <el-option label="中东" value="中东" />
              </el-select>
            </el-form-item>
          </el-form>

          <!-- 通知配置 -->
          <el-divider content-position="left">通知配置（可选）</el-divider>
          <el-form label-width="90px" size="small">
            <el-form-item label="通知类型">
              <el-select v-model="notification.type" style="width:200px">
                <el-option label="不通知" value="none" />
                <el-option label="邮件" value="email" />
                <el-option label="短信" value="sms" />
                <el-option label="即时消息" value="im" />
                <el-option label="Webhook" value="webhook" />
              </el-select>
            </el-form-item>
            <el-form-item v-if="notification.type !== 'none'" label="通知人">
              <el-input
                v-model="notification.recipientsText"
                placeholder="多个用逗号分隔"
                style="width:300px"
              />
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 结果区 -->
      <el-col :span="8">
        <el-card class="result-card" style="height:100%">
          <template #header><span class="card-title">分析结果</span></template>

          <div v-if="!taskResult" class="result-empty">
            <el-empty description="选择场景后点击「开始分析」" :image-size="80" />
          </div>

          <template v-else>
            <el-alert
              :type="resultAlertType"
              :title="taskResult.status === 'EXECUTING' ? '分析中...' : `状态：${taskResult.status}`"
              :description="taskResult.result || taskResult.currentStatus"
              show-icon
              :closable="false"
              style="margin-bottom:12px"
            />
            <template v-if="taskResult.status === 'COMPLETED'">
              <div class="result-item">
                <span class="result-label">场景</span>
                <span>{{ taskResult.scenarioName }}</span>
              </div>
              <div class="result-item">
                <span class="result-label">地区</span>
                <span>{{ taskResult.region || '全球' }}</span>
              </div>
              <div class="result-item">
                <span class="result-label">风险评分</span>
                <el-progress
                  :percentage="taskResult.riskScore"
                  :color="riskColor(taskResult.riskScore)"
                  style="flex:1;margin-left:8px"
                />
              </div>
              <div class="result-item">
                <span class="result-label">风险等级</span>
                <el-tag :type="levelTagType(taskResult.riskLevel)" size="default">
                  {{ taskResult.riskLevel }}
                </el-tag>
              </div>
              <div class="result-recommendation">
                <div class="result-label" style="margin-bottom:4px">应对建议</div>
                {{ taskResult.recommendation }}
              </div>
            </template>
          </template>
        </el-card>
      </el-col>
    </el-row>

    <!-- 历史任务 -->
    <el-card class="history-card">
      <template #header>
        <div class="card-header-row">
          <span class="card-title">最近任务</span>
          <el-button size="small" @click="loadHistory">刷新</el-button>
        </div>
      </template>
      <el-table :data="historyTasks" size="small" :max-height="200">
        <el-table-column prop="taskId" label="任务ID" width="280" show-overflow-tooltip />
        <el-table-column prop="algorithmName" label="算法" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="currentStatus" label="进度" show-overflow-tooltip />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Warning, Lightning, TrendCharts, Van } from '@element-plus/icons-vue'
import algorithmService from '../services/algorithmService'
import axios from 'axios'
import config from '../config'

const scenarios = [
  {
    type: 'trade_war',
    name: '贸易战风险',
    desc: '地缘政治冲突导致的贸易壁垒与关税攀升',
    level: 'HIGH',
    levelType: 'danger',
    color: '#f56c6c',
    icon: 'Warning',
  },
  {
    type: 'supply_disruption',
    name: '供应链中断',
    desc: '核心供应商停产、港口关闭或原材料短缺',
    level: 'MEDIUM',
    levelType: 'warning',
    color: '#e6a23c',
    icon: 'Lightning',
  },
  {
    type: 'demand_volatility',
    name: '需求波动',
    desc: '市场需求骤增或骤降影响库存与产能',
    level: 'MEDIUM',
    levelType: 'warning',
    color: '#e6a23c',
    icon: 'TrendCharts',
  },
  {
    type: 'logistics_delay',
    name: '物流延迟',
    desc: '运输中断、仓储不足或清关延误',
    level: 'LOW',
    levelType: 'success',
    color: '#67c23a',
    icon: 'Van',
  },
]

const selectedScene = ref(null)
const execParams = ref({ region: '全球' })
const notification = ref({ type: 'none', recipientsText: '' })
const executing = ref(false)
const taskResult = ref(null)
const historyTasks = ref([])

const currentSceneObj = computed(() =>
  scenarios.find(s => s.type === selectedScene.value)
)

const resultAlertType = computed(() => {
  if (!taskResult.value) return 'info'
  const s = taskResult.value.status
  if (s === 'COMPLETED') return 'success'
  if (s === 'FAILED') return 'error'
  return 'info'
})

function selectScene(scene) {
  selectedScene.value = scene.type
  taskResult.value = null
}

async function runScenario() {
  if (!selectedScene.value) return

  const params = {
    scenarioType: selectedScene.value,
    region: execParams.value.region,
  }
  const notifPayload = notification.value.type !== 'none'
    ? {
        type: notification.value.type,
        recipients: notification.value.recipientsText
          .split(',').map(s => s.trim()).filter(Boolean),
      }
    : null

  executing.value = true
  taskResult.value = { status: 'EXECUTING' }
  try {
    const resp = await algorithmService.execute('risk-scenarios-algorithm', params, notifPayload)
    taskResult.value = { status: resp.status, taskId: resp.taskId }
    pollTask(resp.taskId)
  } catch (e) {
    taskResult.value = { status: 'FAILED', result: e.message || '执行失败' }
    ElMessage.error('执行失败：' + (e.message || ''))
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
        loadHistory()
      }
    } catch {
      clearInterval(interval)
    }
  }, 1500)
  setTimeout(() => clearInterval(interval), 30000)
}

async function loadHistory() {
  try {
    const res = await axios.get(`${config.apiBaseUrl}/simulation/tasks`)
    historyTasks.value = (res.data || [])
      .filter(t => t.algorithmName === 'risk-scenarios-algorithm')
      .slice(-10)
      .reverse()
  } catch {
    // 忽略
  }
}

function riskColor(score) {
  if (score >= 70) return '#f56c6c'
  if (score >= 40) return '#e6a23c'
  return '#67c23a'
}

function levelTagType(level) {
  return { HIGH: 'danger', MEDIUM: 'warning', LOW: 'success' }[level] || 'info'
}

function statusTagType(status) {
  return { COMPLETED: 'success', FAILED: 'danger', EXECUTING: 'warning', STARTED: 'info' }[status] || ''
}

onMounted(() => loadHistory())
</script>

<style scoped>
.risk-scenarios {
  display: flex;
  flex-direction: column;
  gap: 16px;
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
.scene-card {
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s;
  padding: 8px 0;
}
.scene-card.selected {
  border-color: var(--el-color-primary);
  box-shadow: 0 0 0 2px var(--el-color-primary-light-5);
}
.scene-icon {
  display: block;
  margin: 0 auto 8px;
}
.scene-name {
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 4px;
}
.scene-desc {
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
  min-height: 32px;
}
.scene-level {
  margin-top: 4px;
}
.exec-row {
  flex: 1;
}
.result-card {
  height: 100%;
}
.result-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
}
.result-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-size: 13px;
  gap: 8px;
}
.result-label {
  min-width: 70px;
  color: #909399;
  font-size: 12px;
}
.result-recommendation {
  margin-top: 12px;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 4px;
  font-size: 13px;
  color: #303133;
}
.history-card {
  flex-shrink: 0;
}
</style>
