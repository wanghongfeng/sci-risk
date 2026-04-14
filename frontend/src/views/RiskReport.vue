<template>
  <div class="page-container">
    <h2 class="page-title">风险分析报告</h2>
    
    <!-- 搜索和筛选 -->
    <div class="search-container">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="报告名称">
          <el-input v-model="searchForm.reportName" placeholder="请输入" clearable style="width: 250px;" />
        </el-form-item>
        <el-form-item label="报告类型">
          <el-select v-model="searchForm.reportType" placeholder="请选择" clearable style="width: 200px;">
            <el-option label="月度报告" value="monthly" />
            <el-option label="季度报告" value="quarterly" />
            <el-option label="年度报告" value="annual" />
            <el-option label="专项报告" value="special" />
          </el-select>
        </el-form-item>
        <el-form-item label="生成时间">
          <el-date-picker v-model="searchForm.timeRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="width: 300px;" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button>
          <el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button>
          <el-button type="success" @click="handleGenerateReport"><el-icon><DocumentAdd /></el-icon>生成报告</el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <!-- 报告列表 -->
    <el-card shadow="hover" class="report-list-card">
      <template #header>
        <div class="card-header">
          <span>报告列表</span>
        </div>
      </template>
      <el-table :data="reportList" style="width: 100%" border stripe>
        <el-table-column prop="reportId" label="报告ID" width="120" />
        <el-table-column prop="reportName" label="报告名称" min-width="250" show-overflow-tooltip />
        <el-table-column prop="reportType" label="报告类型" width="120">
          <template #default="scope">
            {{ getReportTypeName(scope.row.reportType) }}
          </template>
        </el-table-column>
        <el-table-column prop="riskLevel" label="风险等级" width="100">
          <template #default="scope">
            <el-tag :type="getRiskLevelType(scope.row.riskLevel)">{{ scope.row.riskLevel }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="generator" label="生成人" width="120" />
        <el-table-column prop="generateTime" label="生成时间" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'completed' ? 'success' : 'warning'">
              {{ scope.row.status === 'completed' ? '已完成' : '生成中' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleViewReport(scope.row)">
              <el-icon><View /></el-icon>查看
            </el-button>
            <el-button type="warning" size="small" @click="handleDownloadReport(scope.row)">
              <el-icon><Download /></el-icon>下载
            </el-button>
            <el-button type="danger" size="small" @click="handleDeleteReport(scope.row)">
              <el-icon><Delete /></el-icon>删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 生成报告对话框 -->
    <el-dialog
      v-model="generateDialogVisible"
      title="生成风险分析报告"
      width="600px"
    >
      <el-form :model="generateForm" label-width="120px">
        <el-form-item label="报告名称">
          <el-input v-model="generateForm.reportName" placeholder="请输入报告名称" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="报告类型">
          <el-select v-model="generateForm.reportType" placeholder="请选择" style="width: 100%;">
            <el-option label="月度报告" value="monthly" />
            <el-option label="季度报告" value="quarterly" />
            <el-option label="年度报告" value="annual" />
            <el-option label="专项报告" value="special" />
          </el-select>
        </el-form-item>
        <el-form-item label="报告周期">
          <el-date-picker v-model="generateForm.period" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="报告内容">
          <el-checkbox-group v-model="generateForm.content">
            <el-checkbox label="风险概览" />
            <el-checkbox label="风险趋势分析" />
            <el-checkbox label="风险分布分析" />
            <el-checkbox label="重点风险分析" />
            <el-checkbox label="应对建议" />
            <el-checkbox label="预测分析" />
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="生成方式">
          <el-radio-group v-model="generateForm.generateType">
            <el-radio label="自动生成" />
            <el-radio label="手动生成" />
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="generateDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitGenerate">生成</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'

// 搜索表单
const searchForm = ref({
  reportName: '',
  reportType: '',
  timeRange: []
})

// 报告列表
const reportList = ref([
  { reportId: 'R001', reportName: '2026年3月风险分析报告', reportType: 'monthly', riskLevel: '中', generator: '张三', generateTime: '2026-04-01 10:00:00', status: 'completed' },
  { reportId: 'R002', reportName: '2026年第一季度风险分析报告', reportType: 'quarterly', riskLevel: '高', generator: '李四', generateTime: '2026-04-05 14:30:00', status: 'completed' },
  { reportId: 'R003', reportName: '地缘政治风险专项分析报告', reportType: 'special', riskLevel: '极高', generator: '王五', generateTime: '2026-04-10 09:15:00', status: 'completed' },
  { reportId: 'R004', reportName: '供应链风险分析报告', reportType: 'special', riskLevel: '高', generator: '赵六', generateTime: '2026-04-12 16:45:00', status: 'completed' },
  { reportId: 'R005', reportName: '2026年4月风险分析报告', reportType: 'monthly', riskLevel: '中', generator: '张三', generateTime: '2026-04-15 11:20:00', status: 'completed' }
])

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(reportList.value.length)

// 生成报告对话框
const generateDialogVisible = ref(false)
const generateForm = ref({
  reportName: '',
  reportType: '',
  period: [],
  content: [],
  generateType: '自动生成'
})

// 处理搜索
const handleSearch = () => {
  console.log('搜索条件:', searchForm.value)
  // 这里可以添加搜索逻辑
}

// 重置表单
const resetForm = () => {
  searchForm.value = {
    reportName: '',
    reportType: '',
    timeRange: []
  }
}

// 生成报告
const handleGenerateReport = () => {
  generateDialogVisible.value = true
}

// 提交生成报告
const handleSubmitGenerate = () => {
  console.log('生成报告:', generateForm.value)
  // 这里可以添加生成报告的逻辑
  generateDialogVisible.value = false
  ElMessageBox.success('报告生成成功')
}

// 查看报告
const handleViewReport = (report) => {
  console.log('查看报告:', report)
  // 这里可以添加查看报告的逻辑
  ElMessageBox.alert(`查看报告: ${report.reportName}`, '报告详情', {
    confirmButtonText: '确定'
  })
}

// 下载报告
const handleDownloadReport = (report) => {
  console.log('下载报告:', report)
  // 这里可以添加下载报告的逻辑
  ElMessageBox.success('报告下载成功')
}

// 删除报告
const handleDeleteReport = (report) => {
  ElMessageBox.confirm(`确定要删除报告 ${report.reportName} 吗？`, '删除报告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    console.log('删除报告:', report)
    // 这里可以添加删除报告的逻辑
    ElMessageBox.success('报告删除成功')
  }).catch(() => {
    // 取消删除
  })
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
}

const handleCurrentChange = (current) => {
  currentPage.value = current
}

// 获取报告类型名称
const getReportTypeName = (type) => {
  const typeMap = {
    monthly: '月度报告',
    quarterly: '季度报告',
    annual: '年度报告',
    special: '专项报告'
  }
  return typeMap[type] || type
}

// 获取风险等级类型
const getRiskLevelType = (level) => {
  const typeMap = {
    '低': 'info',
    '中': 'warning',
    '高': 'danger',
    '极高': 'danger'
  }
  return typeMap[level] || 'info'
}
</script>

<style scoped>
.page-container {
  padding: 20px;
}

.page-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.search-container {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.search-form {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.report-list-card {
  margin-bottom: 20px;
}

.card-header {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

@media (max-width: 768px) {
  .search-form {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .pagination-container {
    justify-content: center;
  }
}
</style>
