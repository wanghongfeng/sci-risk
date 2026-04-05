<template>
  <div class="algorithm-overview">
    <el-row :gutter="16" class="header-row">
      <el-col :span="12">
        <h2 class="page-title">算法总览</h2>
        <p class="page-desc">查看系统中所有已注册的算法服务</p>
      </el-col>
      <el-col :span="12" style="text-align:right">
        <el-button :loading="loading" @click="loadAlgorithms">
          <el-icon><Refresh /></el-icon> 刷新
        </el-button>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="stats-row">
      <el-col :span="6">
        <el-card shadow="never" class="stat-card">
          <div class="stat-value">{{ algorithms.length }}</div>
          <div class="stat-label">算法总数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="never" class="stat-card">
          <div class="stat-value stat-online">{{ onlineCount }}</div>
          <div class="stat-label">在线</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="never" class="stat-card">
          <div class="stat-value stat-offline">{{ offlineCount }}</div>
          <div class="stat-label">离线</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="never" class="stat-card">
          <div class="stat-value">{{ categoryCount }}</div>
          <div class="stat-label">分类数</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="filter-card">
      <el-row :gutter="16" align="middle">
        <el-col :span="6">
          <el-input v-model="filterName" placeholder="搜索算法名称" clearable prefix-icon="Search" />
        </el-col>
        <el-col :span="4">
          <el-select v-model="filterCategory" placeholder="一级分类" clearable>
            <el-option v-for="cat in categories" :key="cat" :label="cat" :value="cat" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filterStatus" placeholder="状态" clearable>
            <el-option label="在线" value="ONLINE" />
            <el-option label="离线" value="OFFLINE" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button @click="clearFilters">清除筛选</el-button>
        </el-col>
      </el-row>
    </el-card>

    <el-row :gutter="16" class="algorithm-grid">
      <el-col v-for="algo in filteredAlgorithms" :key="algo.name" :span="8">
        <el-card class="algorithm-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <div class="algo-name">{{ algo.label || algo.name }}</div>
              <el-tag :type="algo.status === 'ONLINE' ? 'success' : 'danger'" size="small">
                {{ algo.status === 'ONLINE' ? '在线' : '离线' }}
              </el-tag>
            </div>
          </template>

          <div class="algo-info">
            <div class="info-row">
              <span class="info-label">名称</span>
              <span class="info-value">{{ algo.name }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">版本</span>
              <span class="info-value">{{ algo.version }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">分类</span>
              <span class="info-value">
                <el-tag size="small" type="info">{{ algo.category }}</el-tag>
                <span v-if="algo.type"> / {{ algo.type }}</span>
              </span>
            </div>
            <div class="info-row">
              <span class="info-label">类型</span>
              <span class="info-value">{{ algo.type || '-' }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">描述</span>
              <span class="info-value desc-text">{{ algo.description || '-' }}</span>
            </div>
            <div class="info-row endpoint-row">
              <span class="info-label">端点</span>
              <a :href="algo.endpoint" target="_blank" class="endpoint-link">
                {{ algo.endpoint }}
              </a>
            </div>
            <div class="info-row">
              <span class="info-label">注册时间</span>
              <span class="info-value">{{ formatTime(algo.registeredTime) }}</span>
            </div>
          </div>

          <div class="card-footer">
            <el-button size="small" type="primary" plain @click="checkHealth(algo)">
              <el-icon><Monitor /></el-icon> 健康检查
            </el-button>
            <el-button size="small" type="success" @click="showExecuteDialog(algo)" :disabled="algo.status !== 'ONLINE'">
              <el-icon><VideoPlay /></el-icon> 执行
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-empty v-if="filteredAlgorithms.length === 0 && !loading" description="没有找到匹配的算法" />

    <el-dialog v-model="healthDialogVisible" title="健康检查" width="400px">
      <div v-if="healthLoading" style="text-align:center;padding:20px">
        <el-icon class="is-loading" :size="32"><Loading /></el-icon>
        <p>检查中...</p>
      </div>
      <div v-else-if="healthResult">
        <el-result
          :icon="healthResult.ok ? 'success' : 'error'"
          :title="healthResult.ok ? '服务在线' : '服务离线'"
          :sub-title="healthResult.message"
        />
      </div>
    </el-dialog>

    <el-dialog v-model="executeDialogVisible" title="执行算法" width="500px">
      <el-form label-width="100px">
        <el-form-item label="算法名称">
          <el-input :value="currentAlgo?.name" disabled />
        </el-form-item>
        <el-form-item label="端点">
          <el-input :value="currentAlgo?.endpoint" disabled style="font-size:12px" />
        </el-form-item>
        <el-form-item label="回调地址">
          <el-input :value="callbackUrl" disabled style="font-size:12px" />
        </el-form-item>
        <el-form-item label="参数">
          <el-input v-model="executeParams" type="textarea" :rows="4" placeholder='{"key": "value"}' />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="executeDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="executeLoading" @click="executeAlgorithm">确认执行</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, Search, Monitor, VideoPlay, Loading } from '@element-plus/icons-vue'
import axios from 'axios'
import config from '../config'

const loading = ref(false)
const algorithms = ref([])
const categories = ref([])

const filterName = ref('')
const filterCategory = ref('')
const filterStatus = ref('')

const healthDialogVisible = ref(false)
const healthLoading = ref(false)
const healthResult = ref(null)

const executeDialogVisible = ref(false)
const currentAlgo = ref(null)
const executeParams = ref('{}')
const executeLoading = ref(false)
const callbackUrl = computed(() => window.location.origin)

const onlineCount = computed(() => algorithms.value.filter(a => a.status === 'ONLINE').length)
const offlineCount = computed(() => algorithms.value.filter(a => a.status === 'OFFLINE').length)
const categoryCount = computed(() => new Set(algorithms.value.map(a => a.category)).size)

const filteredAlgorithms = computed(() => {
  return algorithms.value.filter(algo => {
    const matchName = !filterName.value || algo.name.toLowerCase().includes(filterName.value.toLowerCase()) || (algo.label || '').toLowerCase().includes(filterName.value.toLowerCase())
    const matchCategory = !filterCategory.value || algo.category === filterCategory.value
    const matchStatus = !filterStatus.value || algo.status === filterStatus.value
    return matchName && matchCategory && matchStatus
  })
})

async function loadAlgorithms() {
  loading.value = true
  try {
    const res = await axios.get(`${config.apiBaseUrl}/algorithm/list`)
    algorithms.value = res.data || []
    categories.value = [...new Set(algorithms.value.map(a => a.category))].filter(Boolean)
  } catch (e) {
    ElMessage.error('加载算法列表失败：' + (e.message || ''))
  } finally {
    loading.value = false
  }
}

async function checkHealth(algo) {
  healthDialogVisible.value = true
  healthLoading.value = true
  healthResult.value = null
  try {
    const res = await axios.get(`${config.apiBaseUrl}/algorithm/${algo.name}/health`)
    healthResult.value = { ok: true, message: '算法服务正常运行' }
  } catch {
    healthResult.value = { ok: false, message: '无法连接到算法服务' }
  } finally {
    healthLoading.value = false
  }
}

function showExecuteDialog(algo) {
  currentAlgo.value = algo
  executeParams.value = '{}'
  executeDialogVisible.value = true
}

async function executeAlgorithm() {
  executeLoading.value = true
  try {
    const params = JSON.parse(executeParams.value || '{}')
    const res = await axios.post(`${config.apiBaseUrl}/simulation/execute`, {
      algorithmName: currentAlgo.value.name,
      params,
      notification: null
    })
    ElMessage.success('任务已启动：' + res.data.taskId)
    executeDialogVisible.value = false
  } catch (e) {
    ElMessage.error('执行失败：' + (e.message || ''))
  } finally {
    executeLoading.value = false
  }
}

function clearFilters() {
  filterName.value = ''
  filterCategory.value = ''
  filterStatus.value = ''
}

function formatTime(timestamp) {
  if (!timestamp) return '-'
  return new Date(timestamp).toLocaleString('zh-CN')
}

onMounted(() => loadAlgorithms())
</script>

<style scoped>
.algorithm-overview {
  padding: 16px;
}
.header-row {
  margin-bottom: 16px;
}
.page-title {
  margin: 0 0 4px;
  font-size: 20px;
  font-weight: 600;
}
.page-desc {
  margin: 0;
  color: #909399;
  font-size: 13px;
}
.stats-row {
  margin-bottom: 16px;
}
.stat-card {
  text-align: center;
}
.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #303133;
}
.stat-online {
  color: #67c23a;
}
.stat-offline {
  color: #f56c6c;
}
.stat-label {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}
.filter-card {
  margin-bottom: 16px;
}
.algorithm-grid {
  margin-bottom: 16px;
}
.algorithm-card {
  height: 100%;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.algo-name {
  font-weight: 600;
  font-size: 15px;
}
.algo-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.info-row {
  display: flex;
  font-size: 13px;
}
.info-label {
  min-width: 70px;
  color: #909399;
}
.info-value {
  flex: 1;
  color: #303133;
}
.desc-text {
  color: #606266;
  line-height: 1.4;
}
.endpoint-row .info-value {
  word-break: break-all;
}
.endpoint-link {
  color: #409eff;
  text-decoration: none;
  font-size: 12px;
}
.endpoint-link:hover {
  text-decoration: underline;
}
.card-footer {
  display: flex;
  gap: 8px;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}
</style>
