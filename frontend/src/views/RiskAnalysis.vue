<template>
  <div class="risk-analysis-report">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>风险分析报告</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleGenerateReport"><el-icon><DocumentAdd /></el-icon>生成报告</el-button>
            <el-button type="success" size="small" @click="handleExportReport"><el-icon><Download /></el-icon>导出报告</el-button>
            <el-button size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 报告生成配置 -->
        <el-collapse v-model="activeCollapse">
          <el-collapse-item title="报告生成配置" name="config">
            <el-form :model="reportConfig" label-width="120px" class="config-form">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="报告类型">
                    <el-select v-model="reportConfig.reportType" placeholder="请选择" style="width: 100%;">
                      <el-option label="供应链风险报告" value="supply_chain" />
                      <el-option label="供应商风险报告" value="supplier" />
                      <el-option label="物料风险报告" value="material" />
                      <el-option label="区域风险报告" value="region" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="报告周期">
                    <el-select v-model="reportConfig.period" placeholder="请选择" style="width: 100%;">
                      <el-option label="日报告" value="daily" />
                      <el-option label="周报告" value="weekly" />
                      <el-option label="月报告" value="monthly" />
                      <el-option label="季度报告" value="quarterly" />
                      <el-option label="年度报告" value="yearly" />
                      <el-option label="自定义" value="custom" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12" v-if="reportConfig.period === 'custom'">
                  <el-form-item label="开始日期">
                    <el-date-picker v-model="reportConfig.startDate" type="date" placeholder="选择开始日期" style="width: 100%;" />
                  </el-form-item>
                </el-col>
                <el-col :span="12" v-if="reportConfig.period === 'custom'">
                  <el-form-item label="结束日期">
                    <el-date-picker v-model="reportConfig.endDate" type="date" placeholder="选择结束日期" style="width: 100%;" />
                  </el-form-item>
                </el-col>
                <el-col :span="24">
                  <el-form-item label="报告范围">
                    <el-checkbox-group v-model="reportConfig.scope">
                      <el-checkbox label="全球" />
                      <el-checkbox label="亚太" />
                      <el-checkbox label="欧洲" />
                      <el-checkbox label="北美" />
                      <el-checkbox label="中东" />
                      <el-checkbox label="非洲" />
                    </el-checkbox-group>
                  </el-form-item>
                </el-col>
                <el-col :span="24">
                  <el-form-item label="报告内容">
                    <el-checkbox-group v-model="reportConfig.content">
                      <el-checkbox label="风险概览" />
                      <el-checkbox label="风险分布" />
                      <el-checkbox label="风险趋势" />
                      <el-checkbox label="高风险分析" />
                      <el-checkbox label="建议措施" />
                    </el-checkbox-group>
                  </el-form-item>
                </el-col>
                <el-col :span="24">
                  <el-form-item label="接收人">
                    <el-input v-model="reportConfig.recipients" placeholder="多个接收人用逗号分隔" style="width: 100%;" />
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </el-collapse-item>
        </el-collapse>
        
        <!-- 报告列表 -->
        <div class="report-list">
          <h4 style="margin-top: 20px; margin-bottom: 15px;">历史报告</h4>
          <el-table :data="reportList" style="width: 100%" border stripe>
            <el-table-column prop="reportId" label="报告ID" width="120" />
            <el-table-column prop="reportName" label="报告名称" min-width="200" show-overflow-tooltip />
            <el-table-column prop="reportType" label="报告类型" width="120"><template #default="scope">{{ getReportTypeName(scope.row.reportType) }}</template></el-table-column>
            <el-table-column prop="period" label="报告周期" width="120"><template #default="scope">{{ getPeriodName(scope.row.period) }}</template></el-table-column>
            <el-table-column prop="generateTime" label="生成时间" width="180" />
            <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'completed' ? 'success' : 'warning'">{{ scope.row.status === 'completed' ? '已完成' : '生成中' }}</el-tag></template></el-table-column>
            <el-table-column label="操作" width="220" fixed="right">
              <template #default="scope">
                <el-button v-if="scope.row.status === 'completed'" type="primary" size="small" @click="handleViewReport(scope.row)"><el-icon><View /></el-icon>查看</el-button>
                <el-button v-if="scope.row.status === 'completed'" type="success" size="small" @click="handleDownloadReport(scope.row)"><el-icon><Download /></el-icon>下载</el-button>
                <el-button v-if="scope.row.status === 'completed'" type="danger" size="small" @click="handleDeleteReport(scope.row)"><el-icon><Delete /></el-icon>删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div class="pagination-wrapper">
            <el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
          </div>
        </div>
      </div>
    </el-card>
    
    <!-- 报告查看对话框 -->
    <el-dialog v-model="reportDialogVisible" :title="currentReport?.reportName" width="90%" :fullscreen="true">
      <div v-if="currentReport" class="report-content">
        <div class="report-header">
          <h2>{{ currentReport.reportName }}</h2>
          <div class="report-meta">
            <span class="meta-item">报告类型：{{ getReportTypeName(currentReport.reportType) }}</span>
            <span class="meta-item">报告周期：{{ getPeriodName(currentReport.period) }}</span>
            <span class="meta-item">生成时间：{{ currentReport.generateTime }}</span>
            <span class="meta-item">生成人：{{ currentReport.generator }}</span>
          </div>
        </div>
        
        <!-- 风险概览 -->
        <div v-if="currentReport.content.includes('风险概览')" class="report-section">
          <h3>一、风险概览</h3>
          <el-row :gutter="20">
            <el-col :span="6">
              <el-card shadow="hover" class="metric-card">
                <div class="metric-title">总风险数量</div>
                <div class="metric-value">{{ currentReport.overview.totalRisk }}</div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card shadow="hover" class="metric-card">
                <div class="metric-title">高风险数量</div>
                <div class="metric-value high-risk">{{ currentReport.overview.highRisk }}</div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card shadow="hover" class="metric-card">
                <div class="metric-title">中风险数量</div>
                <div class="metric-value medium-risk">{{ currentReport.overview.mediumRisk }}</div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card shadow="hover" class="metric-card">
                <div class="metric-title">低风险数量</div>
                <div class="metric-value low-risk">{{ currentReport.overview.lowRisk }}</div>
              </el-card>
            </el-col>
          </el-row>
        </div>
        
        <!-- 风险分布 -->
        <div v-if="currentReport.content.includes('风险分布')" class="report-section">
          <h3>二、风险分布</h3>
          <div class="distribution-charts">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-card shadow="hover">
                  <template #header>
                    <div class="chart-header">
                      <span>风险类型分布</span>
                    </div>
                  </template>
                  <div class="chart-placeholder">
                    <el-empty description="风险类型分布图表" />
                  </div>
                </el-card>
              </el-col>
              <el-col :span="12">
                <el-card shadow="hover">
                  <template #header>
                    <div class="chart-header">
                      <span>风险等级分布</span>
                    </div>
                  </template>
                  <div class="chart-placeholder">
                    <el-empty description="风险等级分布图表" />
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </div>
        
        <!-- 风险趋势 -->
        <div v-if="currentReport.content.includes('风险趋势')" class="report-section">
          <h3>三、风险趋势</h3>
          <el-card shadow="hover">
            <template #header>
              <div class="chart-header">
                <span>风险数量变化趋势</span>
              </div>
            </template>
            <div class="chart-placeholder">
              <el-empty description="风险趋势图表" />
            </div>
          </el-card>
        </div>
        
        <!-- 高风险分析 -->
        <div v-if="currentReport.content.includes('高风险分析')" class="report-section">
          <h3>四、高风险分析</h3>
          <el-table :data="currentReport.highRisks" style="width: 100%" border stripe>
            <el-table-column prop="riskId" label="风险ID" width="120" />
            <el-table-column prop="riskName" label="风险名称" min-width="200" show-overflow-tooltip />
            <el-table-column prop="riskType" label="风险类型" width="120" />
            <el-table-column prop="riskScore" label="风险得分" width="100" align="right" />
            <el-table-column prop="affectedArea" label="影响范围" min-width="150" show-overflow-tooltip />
            <el-table-column prop="description" label="风险描述" min-width="200" show-overflow-tooltip />
          </el-table>
        </div>
        
        <!-- 建议措施 -->
        <div v-if="currentReport.content.includes('建议措施')" class="report-section">
          <h3>五、建议措施</h3>
          <el-card shadow="hover">
            <div v-for="(suggestion, index) in currentReport.suggestions" :key="index" class="suggestion-item">
              <div class="suggestion-title">{{ index + 1 }}. {{ suggestion.title }}</div>
              <div class="suggestion-content">{{ suggestion.content }}</div>
            </div>
          </el-card>
        </div>
      </div>
      <template #footer>
        <el-button @click="reportDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleDownloadReport(currentReport)">下载报告</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { DocumentAdd, Download, Refresh, View, Delete } from '@element-plus/icons-vue'

export default {
  name: 'RiskAnalysis',
  components: { DocumentAdd, Download, Refresh, View, Delete },
  setup() {
    const loading = ref(false)
    const activeCollapse = ref(['config'])
    const reportDialogVisible = ref(false)
    const currentReport = ref(null)
    
    // 报告配置
    const reportConfig = reactive({
      reportType: 'supply_chain',
      period: 'monthly',
      startDate: null,
      endDate: null,
      scope: ['全球'],
      content: ['风险概览', '风险分布', '风险趋势', '高风险分析', '建议措施'],
      recipients: ''
    })
    
    // 分页配置
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(50)
    
    // 报告列表
    const reportList = ref([
      { reportId: 'REP20260409001', reportName: '2026年4月供应链风险月报', reportType: 'supply_chain', period: 'monthly', generateTime: '2026-04-09 10:00:00', status: 'completed', generator: '系统管理员' },
      { reportId: 'REP20260408001', reportName: '2026年4月第一周供应商风险周报', reportType: 'supplier', period: 'weekly', generateTime: '2026-04-08 09:00:00', status: 'completed', generator: '系统管理员' },
      { reportId: 'REP20260401001', reportName: '2026年3月供应链风险月报', reportType: 'supply_chain', period: 'monthly', generateTime: '2026-04-01 10:00:00', status: 'completed', generator: '系统管理员' },
      { reportId: 'REP20260331001', reportName: '2026年第一季度供应链风险季报', reportType: 'supply_chain', period: 'quarterly', generateTime: '2026-03-31 15:00:00', status: 'completed', generator: '系统管理员' },
      { reportId: 'REP20260409002', reportName: '2026年4月9日区域风险日报', reportType: 'region', period: 'daily', generateTime: '2026-04-09 08:00:00', status: 'completed', generator: '系统管理员' }
    ])
    
    // 模拟报告数据
    const mockReportData = {
      reportId: 'REP20260409001',
      reportName: '2026年4月供应链风险月报',
      reportType: 'supply_chain',
      period: 'monthly',
      generateTime: '2026-04-09 10:00:00',
      generator: '系统管理员',
      content: ['风险概览', '风险分布', '风险趋势', '高风险分析', '建议措施'],
      overview: {
        totalRisk: 125,
        highRisk: 25,
        mediumRisk: 45,
        lowRisk: 55
      },
      highRisks: [
        { riskId: 'RISK001', riskName: '核心芯片供应短缺', riskType: '供应链风险', riskScore: 85, affectedArea: '全球', description: '全球芯片短缺持续，影响生产计划' },
        { riskId: 'RISK002', riskName: '原材料价格上涨', riskType: '市场风险', riskScore: 78, affectedArea: '全球', description: '主要原材料价格大幅上涨，影响成本' },
        { riskId: 'RISK003', riskName: '地缘政治冲突', riskType: '政治风险', riskScore: 90, affectedArea: '中东', description: '中东地区冲突加剧，影响能源供应' }
      ],
      suggestions: [
        { title: '增加安全库存', content: '针对核心芯片等关键物料，建议增加30%的安全库存' },
        { title: '寻找替代供应商', content: '积极寻找芯片和原材料的替代供应商，降低单一供应商依赖' },
        { title: '优化供应链网络', content: '重新评估供应链网络，考虑区域化采购策略' },
        { title: '建立价格波动预警机制', content: '建立原材料价格波动预警机制，及时调整采购策略' }
      ]
    }
    
    const handleGenerateReport = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('报告生成成功')
        loading.value = false
        // 模拟添加新报告到列表
        const newReport = {
          reportId: 'REP' + new Date().getTime(),
          reportName: reportConfig.reportType === 'supply_chain' ? '供应链风险报告' : 
                      reportConfig.reportType === 'supplier' ? '供应商风险报告' :
                      reportConfig.reportType === 'material' ? '物料风险报告' : '区域风险报告',
          reportType: reportConfig.reportType,
          period: reportConfig.period,
          generateTime: new Date().toLocaleString(),
          status: 'completed',
          generator: '当前用户'
        }
        reportList.value.unshift(newReport)
      }, 2000)
    }
    
    const handleExportReport = () => {
      ElMessage.info('导出功能开发中')
    }
    
    const handleRefresh = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('刷新成功')
        loading.value = false
      }, 1000)
    }
    
    const handleViewReport = (report) => {
      currentReport.value = mockReportData
      reportDialogVisible.value = true
    }
    
    const handleDownloadReport = (report) => {
      ElMessage.info('下载功能开发中')
    }
    
    const handleDeleteReport = (report) => {
      ElMessage.confirm('确定要删除这份报告吗？', '删除报告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = reportList.value.findIndex(item => item.reportId === report.reportId)
        if (index !== -1) {
          reportList.value.splice(index, 1)
          ElMessage.success('删除成功')
        }
      })
    }
    
    const getReportTypeName = (type) => {
      switch (type) {
        case 'supply_chain': return '供应链风险报告'
        case 'supplier': return '供应商风险报告'
        case 'material': return '物料风险报告'
        case 'region': return '区域风险报告'
        default: return type
      }
    }
    
    const getPeriodName = (period) => {
      switch (period) {
        case 'daily': return '日报告'
        case 'weekly': return '周报告'
        case 'monthly': return '月报告'
        case 'quarterly': return '季度报告'
        case 'yearly': return '年度报告'
        case 'custom': return '自定义'
        default: return period
      }
    }
    
    const handleSizeChange = (size) => {
      pagination.pageSize = size
    }
    
    const handleCurrentChange = (current) => {
      pagination.currentPage = current
    }
    
    onMounted(() => {
      console.log('风险分析报告页面加载')
    })
    
    return {
      loading, activeCollapse, reportDialogVisible, currentReport, reportConfig, pagination, total, reportList,
      handleGenerateReport, handleExportReport, handleRefresh, handleViewReport, handleDownloadReport, handleDeleteReport,
      getReportTypeName, getPeriodName, handleSizeChange, handleCurrentChange
    }
  }
}
</script>

<style scoped>
.risk-analysis-report {
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
.config-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}
.report-list {
  margin-top: 20px;
}
.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
.report-content {
  padding: 20px;
}
.report-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eaeaea;
}
.report-header h2 {
  margin-bottom: 15px;
  color: #303133;
}
.report-meta {
  display: flex;
  gap: 30px;
  font-size: 14px;
  color: #606266;
}
.meta-item {
  display: flex;
  align-items: center;
}
.report-section {
  margin-bottom: 40px;
}
.report-section h3 {
  margin-bottom: 20px;
  color: #303133;
  font-size: 18px;
  font-weight: 600;
}
.metric-card {
  text-align: center;
  padding: 20px 0;
}
.metric-title {
  font-size: 14px;
  color: #606266;
  margin-bottom: 10px;
}
.metric-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}
.metric-value.high-risk {
  color: #f56c6c;
}
.metric-value.medium-risk {
  color: #e6a23c;
}
.metric-value.low-risk {
  color: #67c23a;
}
.distribution-charts {
  margin-bottom: 20px;
}
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.chart-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.suggestion-item {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
}
.suggestion-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}
.suggestion-title {
  font-weight: 600;
  margin-bottom: 5px;
  color: #303133;
}
.suggestion-content {
  color: #606266;
  line-height: 1.5;
}
</style>
