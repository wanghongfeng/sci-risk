<template>
  <div class="risk-path-analysis">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>风险传导路径推演</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleSimulate"><el-icon><MagicStick /></el-icon>开始推演</el-button>
            <el-button type="success" size="small" @click="handleExport"><el-icon><Download /></el-icon>导出报告</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <div class="simulation-section">
          <el-card class="simulation-card">
            <template #header><span>推演配置</span></template>
            <el-form :model="simulationForm" label-width="120px">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="风险源">
                    <el-select v-model="simulationForm.riskSource" placeholder="请选择" style="width: 100%;">
                      <el-option label="供应商生产延迟" value="supplier_delay" />
                      <el-option label="原材料价格上涨" value="material_price" />
                      <el-option label="物流运输中断" value="logistics_break" />
                      <el-option label="市场需求下降" value="demand_decline" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="推演深度">
                    <el-select v-model="simulationForm.depth" placeholder="请选择" style="width: 100%;">
                      <el-option label="1级" value="1" />
                      <el-option label="2级" value="2" />
                      <el-option label="3级" value="3" />
                      <el-option label="4级" value="4" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="时间范围">
                    <el-date-picker v-model="simulationForm.timeRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="width: 100%;" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="影响阈值">
                    <el-slider v-model="simulationForm.threshold" :min="0" :max="100" :step="5" show-input />
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </el-card>
        </div>
        <div class="results-section">
          <el-card class="results-card">
            <template #header><span>推演结果</span></template>
            <div class="path-analysis">
              <div class="path-stats">
                <el-row :gutter="20">
                  <el-col :span="6"><div class="stat-card"><div class="stat-icon" style="background: #409eff;"><el-icon><Connection /></el-icon></div><div class="stat-info"><div class="stat-value">{{ pathStats.totalPaths }}</div><div class="stat-label">传导路径数</div></div></div></el-col>
                  <el-col :span="6"><div class="stat-card"><div class="stat-icon" style="background: #f56c6c;"><el-icon><Warning /></el-icon></div><div class="stat-info"><div class="stat-value">{{ pathStats.highRiskNodes }}</div><div class="stat-label">高风险节点</div></div></div></el-col>
                  <el-col :span="6"><div class="stat-card"><div class="stat-icon" style="background: #e6a23c;"><el-icon><Bell /></el-icon></div><div class="stat-info"><div class="stat-value">{{ pathStats.totalNodes }}</div><div class="stat-label">总节点数</div></div></div></el-col>
                  <el-col :span="6"><div class="stat-card"><div class="stat-icon" style="background: #67c23a;"><el-icon><Check /></el-icon></div><div class="stat-info"><div class="stat-value">{{ pathStats.affectedModules }}</div><div class="stat-label">受影响模块</div></div></div></el-col>
                </el-row>
              </div>
              <div class="path-graph">
                <h4>传导路径图</h4>
                <div class="graph-container">
                  <div class="graph-placeholder">
                    <el-empty description="传导路径可视化图表" />
                  </div>
                </div>
              </div>
              <div class="path-list">
                <h4>传导路径列表</h4>
                <el-table :data="pathList" style="width: 100%" border stripe>
                  <el-table-column prop="pathId" label="路径ID" width="120" />
                  <el-table-column prop="pathName" label="路径名称" min-width="200" show-overflow-tooltip />
                  <el-table-column prop="riskLevel" label="风险等级" width="100"><template #default="scope"><el-tag :type="getRiskLevelColor(scope.row.riskLevel)">{{ getRiskLevelName(scope.row.riskLevel) }}</el-tag></template></el-table-column>
                  <el-table-column prop="length" label="路径长度" width="100" align="right" />
                  <el-table-column prop="probability" label="发生概率" width="100" align="right"><template #default="scope">{{ scope.row.probability }}%</template></el-table-column>
                  <el-table-column prop="impact" label="影响程度" width="100" align="right"><template #default="scope">{{ scope.row.impact }}%</template></el-table-column>
                  <el-table-column label="操作" width="150" fixed="right"><template #default="scope"><el-button type="primary" size="small" @click="handleViewPath(scope.row)"><el-icon><View /></el-icon>详情</el-button><el-button type="warning" size="small" @click="handleAnalyzePath(scope.row)"><el-icon><DataAnalysis /></el-icon>分析</el-button></template></el-table-column>
                </el-table>
                <div class="pagination-wrapper"><el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" /></div>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </el-card>
    <el-dialog v-model="pathDialogVisible" title="路径详情" width="800px">
      <el-descriptions v-if="currentPath" :column="1" border>
        <el-descriptions-item label="路径ID">{{ currentPath.pathId }}</el-descriptions-item>
        <el-descriptions-item label="路径名称">{{ currentPath.pathName }}</el-descriptions-item>
        <el-descriptions-item label="风险等级">{{ getRiskLevelName(currentPath.riskLevel) }}</el-descriptions-item>
        <el-descriptions-item label="路径长度">{{ currentPath.length }}级</el-descriptions-item>
        <el-descriptions-item label="发生概率">{{ currentPath.probability }}%</el-descriptions-item>
        <el-descriptions-item label="影响程度">{{ currentPath.impact }}%</el-descriptions-item>
        <el-descriptions-item label="传导路径">{{ currentPath.path }}</el-descriptions-item>
        <el-descriptions-item label="关键节点">{{ currentPath.keyNodes }}</el-descriptions-item>
        <el-descriptions-item label="建议措施">{{ currentPath.suggestions }}</el-descriptions-item>
      </el-descriptions>
      <template #footer><el-button @click="pathDialogVisible = false">关闭</el-button></template>
    </el-dialog>
  </div>
</template>
<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { MagicStick, Download, Connection, Warning, Bell, Check, View, DataAnalysis } from '@element-plus/icons-vue'
export default {
  name: 'RiskPathAnalysis',
  components: { MagicStick, Download, Connection, Warning, Bell, Check, View, DataAnalysis },
  setup() {
    const loading = ref(false)
    const pathDialogVisible = ref(false)
    const currentPath = ref(null)
    const simulationForm = reactive({
      riskSource: 'supplier_delay',
      depth: '3',
      timeRange: null,
      threshold: 30
    })
    const pathStats = reactive({
      totalPaths: 15,
      highRiskNodes: 8,
      totalNodes: 45,
      affectedModules: 6
    })
    const pathList = ref([
      { pathId: 'PA20260409001', pathName: '供应商延迟→生产中断→交付延迟→客户流失', riskLevel: 'high', length: 4, probability: 85, impact: 90, path: '供应商A → 生产线B → 物流中心C → 客户D', keyNodes: '生产线B, 物流中心C', suggestions: '启用备用供应商，调整生产计划' },
      { pathId: 'PA20260409002', pathName: '原材料涨价→成本上升→利润下降', riskLevel: 'medium', length: 3, probability: 75, impact: 65, path: '原材料供应商 → 采购部门 → 财务部门', keyNodes: '采购部门', suggestions: '寻找替代原材料，优化采购策略' },
      { pathId: 'PA20260409003', pathName: '物流中断→库存不足→销售损失', riskLevel: 'high', length: 3, probability: 70, impact: 80, path: '物流公司 → 仓库 → 销售部门', keyNodes: '仓库', suggestions: '建立多物流渠道，增加安全库存' },
      { pathId: 'PA20260409004', pathName: '市场需求下降→产能过剩→设备闲置', riskLevel: 'medium', length: 3, probability: 65, impact: 55, path: '市场 → 销售部门 → 生产部门', keyNodes: '销售部门', suggestions: '开拓新市场，调整生产计划' },
      { pathId: 'PA20260409005', pathName: '供应商延迟→半成品短缺→生产瓶颈', riskLevel: 'high', length: 3, probability: 80, impact: 75, path: '供应商 → 仓库 → 生产线', keyNodes: '仓库, 生产线', suggestions: '紧急采购，调整生产优先级' }
    ])
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(15)
    const handleSimulate = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('推演完成')
        loading.value = false
      }, 2000)
    }
    const handleExport = () => {
      ElMessage.info('导出功能开发中')
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
    const handleViewPath = (path) => {
      currentPath.value = path
      pathDialogVisible.value = true
    }
    const handleAnalyzePath = (path) => {
      ElMessage.info('路径分析功能开发中')
    }
    const handleSizeChange = (size) => {
      pagination.pageSize = size
    }
    const handleCurrentChange = (current) => {
      pagination.currentPage = current
    }
    onMounted(() => {
      console.log('风险传导路径推演页面加载')
    })
    return {
      loading, pathDialogVisible, currentPath, simulationForm, pathStats, pathList, pagination, total, handleSimulate, handleExport, getRiskLevelColor, getRiskLevelName, handleViewPath, handleAnalyzePath, handleSizeChange, handleCurrentChange
    }
  }
}
</script>
<style scoped>
.risk-path-analysis {
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
.simulation-section {
  margin-bottom: 20px;
}
.simulation-card {
  margin-bottom: 20px;
}
.results-section {
  margin-top: 20px;
}
.results-card {
  margin-bottom: 20px;
}
.stat-card {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}
.stat-info {
  flex: 1;
}
.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 4px;
}
.stat-label {
  font-size: 14px;
  color: #606266;
}
.path-graph {
  margin: 30px 0;
}
.path-graph h4,
.path-list h4 {
  margin-bottom: 15px;
  font-size: 16px;
  font-weight: 500;
}
.graph-container {
  height: 400px;
  background: #f9f9f9;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e4e7ed;
}
.graph-placeholder {
  text-align: center;
}
.path-list {
  margin-top: 30px;
}
.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>