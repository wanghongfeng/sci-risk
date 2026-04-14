<template>
  <div class="global-risk-collection">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>全球风险数据采集</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleSync">
              <el-icon><Refresh /></el-icon>
              同步数据
            </el-button>
            <el-button type="success" size="small" @click="handleAdd">
              <el-icon><Plus /></el-icon>
              手动采集
            </el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <div class="stats-container">
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: #409eff;">
                  <el-icon><DataBoard /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.totalCount }}</div>
                  <div class="stat-label">数据总量</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: #67c23a;">
                  <el-icon><CircleCheck /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.normalCount }}</div>
                  <div class="stat-label">正常</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: #e6a23c;">
                  <el-icon><Warning /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.warningCount }}</div>
                  <div class="stat-label">预警</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: #f56c6c;">
                  <el-icon><CircleClose /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.dangerCount }}</div>
                  <div class="stat-label">危险</div>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="search-container">
          <el-form :inline="true" :model="searchForm" class="search-form">
            <el-form-item label="数据来源">
              <el-select v-model="searchForm.source" placeholder="请选择" clearable style="width: 150px;">
                <el-option label="海关数据" value="customs" />
                <el-option label="物流数据" value="logistics" />
                <el-option label="舆情数据" value="public_opinion" />
                <el-option label="气象数据" value="weather" />
                <el-option label="新闻数据" value="news" />
              </el-select>
            </el-form-item>
            <el-form-item label="风险等级">
              <el-select v-model="searchForm.riskLevel" placeholder="请选择" clearable style="width: 120px;">
                <el-option label="正常" value="normal" />
                <el-option label="预警" value="warning" />
                <el-option label="危险" value="danger" />
              </el-select>
            </el-form-item>
            <el-form-item label="采集时间">
              <el-date-picker v-model="searchForm.dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="width: 240px;" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button>
              <el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button>
              <el-button type="success" @click="handleExport"><el-icon><Download /></el-icon>导出</el-button>
            </el-form-item>
          </el-form>
        </div>

        <el-table :data="riskDataList" style="width: 100%" border stripe class="data-table">
          <el-table-column prop="dataId" label="数据ID" width="180" />
          <el-table-column prop="source" label="数据来源" width="120">
            <template #default="scope">
              <el-tag :type="getSourceType(scope.row.source)">{{ getSourceName(scope.row.source) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="title" label="数据标题" min-width="200" show-overflow-tooltip />
          <el-table-column prop="region" label="区域" width="100" />
          <el-table-column prop="riskLevel" label="风险等级" width="100">
            <template #default="scope">
              <el-tag :type="getRiskType(scope.row.riskLevel)">{{ getRiskName(scope.row.riskLevel) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="collectTime" label="采集时间" width="160" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'collected' ? 'success' : 'info'">
                {{ scope.row.status === 'collected' ? '已采集' : '采集中' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleView(scope.row)"><el-icon><View /></el-icon>查看</el-button>
              <el-button type="warning" size="small" @click="handleAnalyze(scope.row)"><el-icon><DataAnalysis /></el-icon>分析</el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-wrapper">
          <el-pagination
            v-model:current-page="pagination.currentPage"
            v-model:page-size="pagination.pageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="800px">
      <el-descriptions v-if="currentData" :column="2" border>
        <el-descriptions-item label="数据ID">{{ currentData.dataId }}</el-descriptions-item>
        <el-descriptions-item label="数据来源">{{ getSourceName(currentData.source) }}</el-descriptions-item>
        <el-descriptions-item label="数据标题" :span="2">{{ currentData.title }}</el-descriptions-item>
        <el-descriptions-item label="风险等级">
          <el-tag :type="getRiskType(currentData.riskLevel)">{{ getRiskName(currentData.riskLevel) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="区域">{{ currentData.region }}</el-descriptions-item>
        <el-descriptions-item label="采集时间">{{ currentData.collectTime }}</el-descriptions-item>
        <el-descriptions-item label="详细描述" :span="2">{{ currentData.description }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleAnalyzeFromDialog">发起分析</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="analysisDialogVisible" title="风险分析结果" width="900px">
      <div v-loading="analysisLoading" class="analysis-container">
        <div class="analysis-header">
          <h3>{{ analysisData?.title || '风险分析' }}</h3>
          <div class="analysis-meta">
            <span class="meta-item">分析时间: {{ analysisData?.analysisTime || new Date().toLocaleString() }}</span>
            <span class="meta-item">分析类型: {{ analysisData?.analysisType || '综合分析' }}</span>
          </div>
        </div>

        <div class="analysis-content">
          <el-card shadow="hover" class="analysis-card">
            <template #header>
              <div class="card-header">
                <span>风险评估</span>
              </div>
            </template>
            <div class="risk-assessment">
              <div class="assessment-item">
                <span class="assessment-label">风险等级:</span>
                <el-tag :type="analysisData?.riskLevelType || 'danger'" size="large">{{ analysisData?.riskLevel || '高' }}</el-tag>
              </div>
              <div class="assessment-item">
                <span class="assessment-label">影响范围:</span>
                <span class="assessment-value">{{ analysisData?.impactScope || '全球' }}</span>
              </div>
              <div class="assessment-item">
                <span class="assessment-label">影响程度:</span>
                <el-progress :percentage="analysisData?.impactLevel || 75" :status="analysisData?.impactStatus || 'warning'" />
              </div>
              <div class="assessment-item">
                <span class="assessment-label">预测持续时间:</span>
                <span class="assessment-value">{{ analysisData?.duration || '30天' }}</span>
              </div>
            </div>
          </el-card>

          <el-card shadow="hover" class="analysis-card">
            <template #header>
              <div class="card-header">
                <span>风险分析</span>
              </div>
            </template>
            <div class="analysis-details">
              <h4>风险概述</h4>
              <p>{{ analysisData?.riskOverview || '该风险事件可能对全球供应链产生重大影响，需要密切关注发展态势。' }}</p>
              
              <h4>潜在影响</h4>
              <ul class="impact-list">
                <li v-for="(impact, index) in analysisData?.potentialImpacts" :key="index">{{ impact }}</li>
              </ul>
              
              <h4>应对建议</h4>
              <ul class="suggestion-list">
                <li v-for="(suggestion, index) in analysisData?.suggestions" :key="index">{{ suggestion }}</li>
              </ul>
            </div>
          </el-card>

          <el-card shadow="hover" class="analysis-card">
            <template #header>
              <div class="card-header">
                <span>影响分析</span>
              </div>
            </template>
            <div class="impact-analysis">
              <el-table :data="analysisData?.impactDetails" style="width: 100%" border stripe>
                <el-table-column prop="category" label="影响类别" width="150" />
                <el-table-column prop="level" label="影响等级" width="120">
                  <template #default="scope">
                    <el-tag :type="scope.row.levelType">{{ scope.row.level }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="description" label="影响描述" min-width="400" />
                <el-table-column prop="probability" label="发生概率" width="120">
                  <template #default="scope">
                    <el-progress :percentage="scope.row.probability" :status="scope.row.probabilityStatus" />
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-card>
        </div>
      </div>
      <template #footer>
        <el-button @click="analysisDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleExportAnalysis">导出分析报告</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, Plus, Search, Download, View, DataAnalysis, DataBoard, CircleCheck, Warning, CircleClose } from '@element-plus/icons-vue'

export default {
  name: 'GlobalRiskCollection',
  components: {
    Refresh, Plus, Search, Download, View, DataAnalysis, DataBoard, CircleCheck, Warning, CircleClose
  },
  setup() {
    const loading = ref(false)
    const dialogVisible = ref(false)
    const dialogTitle = ref('数据详情')
    const currentData = ref(null)
    const analysisDialogVisible = ref(false)
    const analysisLoading = ref(false)
    const analysisData = ref(null)

    const stats = reactive({
      totalCount: 1256,
      normalCount: 892,
      warningCount: 298,
      dangerCount: 66
    })

    const searchForm = reactive({
      source: '',
      riskLevel: '',
      dateRange: []
    })

    const pagination = reactive({
      currentPage: 1,
      pageSize: 10
    })

    const total = ref(0)

    const riskDataList = ref([
      { dataId: 'RISK20260409001', source: 'customs', title: '美国对华加征关税商品清单更新', region: '北美', riskLevel: 'danger', collectTime: '2026-04-09 10:30:00', status: 'collected', description: '美国贸易代表办公室宣布更新对华加征关税商品清单。' },
      { dataId: 'RISK20260409002', source: 'logistics', title: '红海航运风险预警', region: '中东', riskLevel: 'warning', collectTime: '2026-04-09 09:15:00', status: 'collected', description: '红海地区安全形势持续紧张。' },
      { dataId: 'RISK20260409003', source: 'public_opinion', title: '东南亚政局变动影响供应链', region: '东南亚', riskLevel: 'warning', collectTime: '2026-04-09 08:00:00', status: 'collected', description: '东南亚部分国家政局变动可能影响产品供应。' },
      { dataId: 'RISK20260409004', source: 'weather', title: '极端天气影响货物运输', region: '欧洲', riskLevel: 'normal', collectTime: '2026-04-08 16:45:00', status: 'collected', description: '欧洲多国遭遇极端天气，物流运输受到影响。' },
      { dataId: 'RISK20260409005', source: 'news', title: '原材料价格波动预警', region: '全球', riskLevel: 'warning', collectTime: '2026-04-08 14:20:00', status: 'collected', description: '国际原材料市场价格出现波动。' }
    ])

    const sourceMap = {
      customs: '海关数据',
      logistics: '物流数据',
      public_opinion: '舆情数据',
      weather: '气象数据',
      news: '新闻数据'
    }

    const riskMap = {
      normal: '正常',
      warning: '预警',
      danger: '危险'
    }

    const sourceTypeMap = {
      customs: '',
      logistics: 'success',
      public_opinion: 'warning',
      weather: 'info',
      news: ''
    }

    const riskTypeMap = {
      normal: 'success',
      warning: 'warning',
      danger: 'danger'
    }

    const getSourceName = (source) => sourceMap[source] || source
    const getSourceType = (source) => sourceTypeMap[source] || ''
    const getRiskName = (level) => riskMap[level] || level
    const getRiskType = (level) => riskTypeMap[level] || ''

    const loadData = async () => {
      loading.value = true
      try {
        await new Promise(resolve => setTimeout(resolve, 500))
        total.value = riskDataList.value.length
      } finally {
        loading.value = false
      }
    }

    const handleSync = () => {
      ElMessage.success('数据同步中...')
      setTimeout(() => {
        ElMessage.success('数据同步完成')
        loadData()
      }, 1000)
    }

    const handleAdd = () => {
      ElMessage.info('手动采集功能开发中')
    }

    const handleSearch = () => {
      ElMessage.success('搜索功能开发中')
      loadData()
    }

    const resetForm = () => {
      searchForm.source = ''
      searchForm.riskLevel = ''
      searchForm.dateRange = []
      ElMessage.info('重置筛选条件')
      loadData()
    }

    const handleExport = () => {
      ElMessage.success('导出功能开发中')
    }

    const handleView = (row) => {
      currentData.value = row
      dialogTitle.value = '数据详情'
      dialogVisible.value = true
    }

    const handleAnalyze = (row) => {
      currentData.value = row
      performAnalysis(row)
    }

    const handleAnalyzeFromDialog = () => {
      if (currentData.value) {
        performAnalysis(currentData.value)
        dialogVisible.value = false
      }
    }

    const performAnalysis = (data) => {
      analysisLoading.value = true
      setTimeout(() => {
        analysisData.value = {
          title: data.title,
          analysisTime: new Date().toLocaleString(),
          analysisType: '综合分析',
          riskLevel: getRiskName(data.riskLevel),
          riskLevelType: getRiskType(data.riskLevel),
          impactScope: data.region === '全球' ? '全球' : `${data.region}及周边地区`,
          impactLevel: data.riskLevel === 'danger' ? 85 : data.riskLevel === 'warning' ? 65 : 35,
          impactStatus: data.riskLevel === 'danger' ? 'danger' : data.riskLevel === 'warning' ? 'warning' : 'success',
          duration: data.riskLevel === 'danger' ? '60天' : data.riskLevel === 'warning' ? '30天' : '15天',
          riskOverview: `该风险事件发生在${data.region}地区，属于${getSourceName(data.source)}类型数据。根据分析，该事件可能对全球供应链产生${getRiskName(data.riskLevel)}程度的影响，需要密切关注其发展态势。`,
          potentialImpacts: [
            '可能导致相关区域的供应链中断',
            '可能引起原材料价格波动',
            '可能影响产品交付时间',
            '可能增加运营成本'
          ],
          suggestions: [
            '建立风险预警机制，及时监控事件发展',
            '优化供应链结构，减少对受影响地区的依赖',
            '制定应急响应计划，提高应对能力',
            '加强与供应商和客户的沟通，保持信息透明'
          ],
          impactDetails: [
            {
              category: '供应链',
              level: '高',
              levelType: 'danger',
              description: '可能导致原材料供应中断，影响生产计划',
              probability: 80,
              probabilityStatus: 'warning'
            },
            {
              category: '财务',
              level: '中',
              levelType: 'warning',
              description: '可能导致成本上升，影响利润',
              probability: 65,
              probabilityStatus: 'warning'
            },
            {
              category: '运营',
              level: '中',
              levelType: 'warning',
              description: '可能影响生产和交付计划',
              probability: 70,
              probabilityStatus: 'warning'
            },
            {
              category: '市场',
              level: '低',
              levelType: 'info',
              description: '可能对市场信心产生一定影响',
              probability: 40,
              probabilityStatus: 'success'
            }
          ]
        }
        analysisLoading.value = false
        analysisDialogVisible.value = true
      }, 1500)
    }

    const handleExportAnalysis = () => {
      ElMessage.success('分析报告导出成功')
    }

    const handleSizeChange = (val) => {
      pagination.pageSize = val
      loadData()
    }

    const handleCurrentChange = (val) => {
      pagination.currentPage = val
      loadData()
    }

    onMounted(() => {
      loadData()
    })

    return {
      loading,
      dialogVisible,
      dialogTitle,
      currentData,
      analysisDialogVisible,
      analysisLoading,
      analysisData,
      stats,
      searchForm,
      pagination,
      total,
      riskDataList,
      getSourceName,
      getSourceType,
      getRiskName,
      getRiskType,
      handleSync,
      handleAdd,
      handleSearch,
      resetForm,
      handleExport,
      handleView,
      handleAnalyze,
      handleAnalyzeFromDialog,
      handleExportAnalysis,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.global-risk-collection {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.stats-container {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  margin-right: 15px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.search-container {
  margin-bottom: 20px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.analysis-container {
  padding: 20px 0;
}

.analysis-header {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.analysis-header h3 {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 10px;
}

.analysis-meta {
  display: flex;
  gap: 20px;
  font-size: 14px;
  color: #909399;
}

.analysis-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.analysis-card {
  margin-bottom: 0;
}

.risk-assessment {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 10px 0;
}

.assessment-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.assessment-label {
  font-size: 14px;
  color: #606266;
  width: 120px;
  flex-shrink: 0;
}

.assessment-value {
  font-size: 14px;
  color: #303133;
  flex: 1;
}

.analysis-details {
  padding: 10px 0;
}

.analysis-details h4 {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  margin: 15px 0 10px 0;
}

.analysis-details p {
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
  margin-bottom: 10px;
}

.impact-list,
.suggestion-list {
  padding-left: 20px;
  margin-bottom: 15px;
}

.impact-list li,
.suggestion-list li {
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
  margin-bottom: 8px;
}

.impact-analysis {
  padding: 10px 0;
}

.impact-analysis .el-table {
  margin-top: 10px;
}
</style>
