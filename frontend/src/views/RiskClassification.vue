<template>
  <div class="risk-classification">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>风险自动分类分级</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleAnalyze"><el-icon><DataAnalysis /></el-icon>开始分析</el-button>
            <el-button type="success" size="small" @click="handleExport"><el-icon><Download /></el-icon>导出报告</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <div class="analysis-section">
          <el-card class="analysis-card">
            <template #header><span>分析配置</span></template>
            <el-form :model="analysisForm" label-width="120px">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="分析范围">
                    <el-select v-model="analysisForm.scope" placeholder="请选择" style="width: 100%;">
                      <el-option label="全部风险" value="all" />
                      <el-option label="供应链风险" value="supply_chain" />
                      <el-option label="市场风险" value="market" />
                      <el-option label="政策风险" value="policy" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="时间范围">
                    <el-date-picker v-model="analysisForm.timeRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="width: 100%;" />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="分析模型">
                    <el-select v-model="analysisForm.model" placeholder="请选择" style="width: 100%;">
                      <el-option label="机器学习模型" value="machine_learning" />
                      <el-option label="规则引擎" value="rule_engine" />
                      <el-option label="混合模型" value="hybrid" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="置信度阈值">
                    <el-slider v-model="analysisForm.confidence" :min="0" :max="100" :step="1" show-input />
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </el-card>
        </div>
        <div class="results-section">
          <el-card class="results-card">
            <template #header><span>分析结果</span></template>
            <div class="classification-results">
              <el-row :gutter="20">
                <el-col :span="8"><div class="result-card"><div class="result-icon" style="background: #409eff;"><el-icon><Histogram /></el-icon></div><div class="result-info"><div class="result-value">{{ classificationStats.total }}</div><div class="result-label">风险总数</div></div></div></el-col>
                <el-col :span="8"><div class="result-card"><div class="result-icon" style="background: #f56c6c;"><el-icon><Warning /></el-icon></div><div class="result-info"><div class="result-value">{{ classificationStats.high }}</div><div class="result-label">高风险</div></div></div></el-col>
                <el-col :span="8"><div class="result-card"><div class="result-icon" style="background: #e6a23c;"><el-icon><Bell /></el-icon></div><div class="result-info"><div class="result-value">{{ classificationStats.medium }}</div><div class="result-label">中风险</div></div></div></el-col>
              </el-row>
              <div class="risk-types">
                <h4>风险类型分布</h4>
                <div class="type-chart">
                  <div v-for="type in riskTypes" :key="type.type" class="type-item">
                    <div class="type-name">{{ type.name }}</div>
                    <div class="type-bar"><div class="type-fill" :style="{ width: type.percentage + '%', backgroundColor: type.color }"></div></div>
                    <div class="type-count">{{ type.count }} ({{ type.percentage }}%)</div>
                  </div>
                </div>
              </div>
              <div class="classification-table">
                <h4>风险分类详情</h4>
                <el-table :data="riskList" style="width: 100%" border stripe>
                  <el-table-column prop="riskId" label="风险ID" width="180" />
                  <el-table-column prop="riskTitle" label="风险标题" min-width="200" show-overflow-tooltip />
                  <el-table-column prop="riskType" label="风险类型" width="120"><template #default="scope"><el-tag :type="getRiskTypeColor(scope.row.riskType)">{{ scope.row.riskType }}</el-tag></template></el-table-column>
                  <el-table-column prop="riskLevel" label="风险等级" width="100"><template #default="scope"><el-tag :type="getRiskLevelColor(scope.row.riskLevel)">{{ getRiskLevelName(scope.row.riskLevel) }}</el-tag></template></el-table-column>
                  <el-table-column prop="confidence" label="置信度" width="100" align="right"><template #default="scope">{{ scope.row.confidence }}%</template></el-table-column>
                  <el-table-column prop="analysisTime" label="分析时间" width="160" />
                  <el-table-column label="操作" width="200" fixed="right"><template #default="scope"><el-button type="primary" size="small" @click="handleView(scope.row)"><el-icon><View /></el-icon>详情</el-button><el-button type="warning" size="small" @click="handleEdit(scope.row)"><el-icon><Edit /></el-icon>调整</el-button></template></el-table-column>
                </el-table>
                <div class="pagination-wrapper"><el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" /></div>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </el-card>
    <el-dialog v-model="detailDialogVisible" title="风险详情" width="800px">
      <el-descriptions v-if="currentRisk" :column="1" border>
        <el-descriptions-item label="风险ID">{{ currentRisk.riskId }}</el-descriptions-item>
        <el-descriptions-item label="风险标题">{{ currentRisk.riskTitle }}</el-descriptions-item>
        <el-descriptions-item label="风险类型">{{ currentRisk.riskType }}</el-descriptions-item>
        <el-descriptions-item label="风险等级">{{ getRiskLevelName(currentRisk.riskLevel) }}</el-descriptions-item>
        <el-descriptions-item label="置信度">{{ currentRisk.confidence }}%</el-descriptions-item>
        <el-descriptions-item label="风险描述">{{ currentRisk.description }}</el-descriptions-item>
        <el-descriptions-item label="影响范围">{{ currentRisk.impactScope }}</el-descriptions-item>
        <el-descriptions-item label="分析时间">{{ currentRisk.analysisTime }}</el-descriptions-item>
        <el-descriptions-item label="分析模型">{{ getModelName(currentRisk.analysisModel) }}</el-descriptions-item>
      </el-descriptions>
      <template #footer><el-button @click="detailDialogVisible = false">关闭</el-button></template>
    </el-dialog>
  </div>
</template>
<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { DataAnalysis, Download, Histogram, Warning, Bell, View, Edit } from '@element-plus/icons-vue'
export default {
  name: 'RiskClassification',
  components: { DataAnalysis, Download, Histogram, Warning, Bell, View, Edit },
  setup() {
    const loading = ref(false)
    const detailDialogVisible = ref(false)
    const currentRisk = ref(null)
    const analysisForm = reactive({
      scope: 'all',
      timeRange: null,
      model: 'hybrid',
      confidence: 70
    })
    const classificationStats = reactive({
      total: 256,
      high: 45,
      medium: 120,
      low: 91
    })
    const riskTypes = ref([
      { type: 'supply', name: '供应链风险', count: 89, percentage: 35, color: '#409eff' },
      { type: 'market', name: '市场风险', count: 67, percentage: 26, color: '#67c23a' },
      { type: 'policy', name: '政策风险', count: 45, percentage: 18, color: '#e6a23c' },
      { type: 'finance', name: '财务风险', count: 32, percentage: 12, color: '#f56c6c' },
      { type: 'other', name: '其他风险', count: 23, percentage: 9, color: '#909399' }
    ])
    const riskList = ref([
      { riskId: 'RC20260409001', riskTitle: '供应商生产延迟', riskType: '供应链风险', riskLevel: 'high', confidence: 95, analysisTime: '2026-04-09 10:00:00', analysisModel: 'machine_learning', description: '主要供应商因设备故障导致生产延迟', impactScope: '原材料供应' },
      { riskId: 'RC20260409002', riskTitle: '市场需求下降', riskType: '市场风险', riskLevel: 'medium', confidence: 85, analysisTime: '2026-04-09 10:15:00', analysisModel: 'hybrid', description: '目标市场需求出现明显下降趋势', impactScope: '销售业绩' },
      { riskId: 'RC20260409003', riskType: '政策风险', riskLevel: 'high', confidence: 90, analysisTime: '2026-04-09 10:30:00', analysisModel: 'rule_engine', riskTitle: '贸易政策变化', description: '进口国贸易政策发生重大变化', impactScope: '国际贸易' },
      { riskId: 'RC20260409004', riskType: '财务风险', riskLevel: 'medium', confidence: 80, analysisTime: '2026-04-09 10:45:00', analysisModel: 'machine_learning', riskTitle: '汇率波动', description: '主要结算货币汇率出现大幅波动', impactScope: '财务成本' },
      { riskId: 'RC20260409005', riskType: '供应链风险', riskLevel: 'low', confidence: 75, analysisTime: '2026-04-09 11:00:00', analysisModel: 'hybrid', riskTitle: '物流运输延迟', description: '部分地区物流运输出现轻微延迟', impactScope: '货物交付' }
    ])
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(256)
    const handleAnalyze = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('分析完成')
        loading.value = false
      }, 2000)
    }
    const handleExport = () => {
      ElMessage.info('导出功能开发中')
    }
    const getRiskTypeColor = (type) => {
      switch (type) {
        case '供应链风险': return 'primary'
        case '市场风险': return 'success'
        case '政策风险': return 'warning'
        case '财务风险': return 'danger'
        default: return 'info'
      }
    }
    const getRiskLevelColor = (level) => {
      switch (level) {
        case 'high': return 'danger'
        case 'medium': return 'warning'
        case 'low': return 'success'
        default: return 'info'
      }
    }
    const getRiskLevelName = (level) => {
      switch (level) {
        case 'high': return '高风险'
        case 'medium': return '中风险'
        case 'low': return '低风险'
        default: return level
      }
    }
    const getModelName = (model) => {
      switch (model) {
        case 'machine_learning': return '机器学习模型'
        case 'rule_engine': return '规则引擎'
        case 'hybrid': return '混合模型'
        default: return model
      }
    }
    const handleView = (risk) => {
      currentRisk.value = risk
      detailDialogVisible.value = true
    }
    const handleEdit = (risk) => {
      ElMessage.info('调整功能开发中')
    }
    const handleSizeChange = (size) => {
      pagination.pageSize = size
    }
    const handleCurrentChange = (current) => {
      pagination.currentPage = current
    }
    onMounted(() => {
      console.log('风险自动分类分级页面加载')
    })
    return {
      loading, detailDialogVisible, currentRisk, analysisForm, classificationStats, riskTypes, riskList, pagination, total, handleAnalyze, handleExport, getRiskTypeColor, getRiskLevelColor, getRiskLevelName, getModelName, handleView, handleEdit, handleSizeChange, handleCurrentChange
    }
  }
}
</script>
<style scoped>
.risk-classification {
  padding: 20px;
}
.page-card {
  margin-bottom: 20px;
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
.analysis-section {
  margin-bottom: 20px;
}
.analysis-card {
  margin-bottom: 20px;
}
.results-section {
  margin-top: 20px;
}
.results-card {
  margin-bottom: 20px;
}
.result-card {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.result-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}
.result-info {
  flex: 1;
}
.result-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 4px;
}
.result-label {
  font-size: 14px;
  color: #606266;
}
.risk-types {
  margin: 30px 0;
}
.risk-types h4,
.classification-table h4 {
  margin-bottom: 15px;
  font-size: 16px;
  font-weight: 500;
}
.type-chart {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.type-item {
  margin-bottom: 15px;
}
.type-name {
  margin-bottom: 5px;
  font-size: 14px;
}
.type-bar {
  height: 20px;
  background: #e4e7ed;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 5px;
}
.type-fill {
  height: 100%;
  border-radius: 10px;
  transition: width 0.3s ease;
}
.type-count {
  font-size: 12px;
  color: #909399;
  text-align: right;
}
.classification-table {
  margin-top: 30px;
}
.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>