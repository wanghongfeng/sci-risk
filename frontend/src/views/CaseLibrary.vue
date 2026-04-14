<template>
  <div class="case-library">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>案例库管理</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleCreateCase"><el-icon><Plus /></el-icon>新增案例</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 搜索和筛选 -->
        <div class="search-container">
          <el-form :inline="true" :model="searchForm" class="search-form">
            <el-form-item label="案例ID"><el-input v-model="searchForm.caseId" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="案例名称"><el-input v-model="searchForm.caseName" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="风险类型"><el-select v-model="searchForm.riskType" placeholder="请选择" clearable style="width: 150px;"><el-option label="供应链风险" value="supply_chain" /><el-option label="市场风险" value="market" /><el-option label="政策风险" value="policy" /><el-option label="地缘政治风险" value="geopolitical" /></el-select></el-form-item>
            <el-form-item label="风险等级"><el-select v-model="searchForm.riskLevel" placeholder="请选择" clearable style="width: 120px;"><el-option label="高风险" value="high" /><el-option label="中风险" value="medium" /><el-option label="低风险" value="low" /></el-select></el-form-item>
            <el-form-item><el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
          </el-form>
        </div>
        
        <!-- 案例列表 -->
        <el-table :data="caseList" style="width: 100%" border stripe>
          <el-table-column prop="caseId" label="案例ID" width="120" />
          <el-table-column prop="caseName" label="案例名称" min-width="200" show-overflow-tooltip />
          <el-table-column prop="riskType" label="风险类型" width="120"><template #default="scope">{{ getRiskTypeName(scope.row.riskType) }}</template></el-table-column>
          <el-table-column prop="riskLevel" label="风险等级" width="100"><template #default="scope"><el-tag :type="getRiskLevelColor(scope.row.riskLevel)">{{ getRiskLevelName(scope.row.riskLevel) }}</el-tag></template></el-table-column>
          <el-table-column prop="industry" label="所属行业" width="120" />
          <el-table-column prop="createTime" label="创建时间" width="180" />
          <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'published' ? 'success' : 'info'"> {{ getStatusName(scope.row.status) }}</el-tag></template></el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleViewCase(scope.row)"><el-icon><View /></el-icon>查看</el-button>
              <el-button type="warning" size="small" @click="handleEditCase(scope.row)"><el-icon><Edit /></el-icon>编辑</el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination-wrapper"><el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" /></div>
      </div>
    </el-card>
    
    <!-- 案例对话框 -->
    <el-dialog v-model="caseDialogVisible" :title="caseDialogTitle" width="800px">
      <el-form :model="caseForm" label-width="120px" class="case-form">
        <el-form-item label="案例名称" required><el-input v-model="caseForm.caseName" placeholder="请输入案例名称" style="width: 100%;" /></el-form-item>
        <el-form-item label="风险类型" required><el-select v-model="caseForm.riskType" placeholder="请选择风险类型" style="width: 100%;"><el-option label="供应链风险" value="supply_chain" /><el-option label="市场风险" value="market" /><el-option label="政策风险" value="policy" /><el-option label="地缘政治风险" value="geopolitical" /><el-option label="财务风险" value="financial" /><el-option label="质量风险" value="quality" /></el-select></el-form-item>
        <el-form-item label="风险等级" required><el-select v-model="caseForm.riskLevel" placeholder="请选择风险等级" style="width: 100%;"><el-option label="高风险" value="high" /><el-option label="中风险" value="medium" /><el-option label="低风险" value="low" /></el-select></el-form-item>
        <el-form-item label="所属行业" required><el-input v-model="caseForm.industry" placeholder="请输入所属行业" style="width: 100%;" /></el-form-item>
        <el-form-item label="发生时间" required><el-date-picker v-model="caseForm.occurTime" type="date" placeholder="选择发生时间" style="width: 100%;" /></el-form-item>
        <el-form-item label="案例描述"><el-input v-model="caseForm.description" type="textarea" :rows="4" placeholder="请输入案例描述" style="width: 100%;" /></el-form-item>
        <el-form-item label="应对措施"><el-input v-model="caseForm.measures" type="textarea" :rows="4" placeholder="请输入应对措施" style="width: 100%;" /></el-form-item>
        <el-form-item label="经验教训"><el-input v-model="caseForm.lessons" type="textarea" :rows="4" placeholder="请输入经验教训" style="width: 100%;" /></el-form-item>
        <el-form-item label="状态"><el-select v-model="caseForm.status" placeholder="请选择状态" style="width: 100%;"><el-option label="草稿" value="draft" /><el-option label="已发布" value="published" /></el-select></el-form-item>
      </el-form>
      <template #footer><el-button @click="caseDialogVisible = false">取消</el-button><el-button type="primary" @click="handleSaveCase">保存</el-button></template>
    </el-dialog>
    
    <!-- 案例详情对话框 -->
    <el-dialog v-model="detailDialogVisible" :title="'案例详情 - ' + (currentCase?.caseId || '')" width="800px">
      <div v-if="currentCase" class="detail-dialog">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="案例ID">{{ currentCase.caseId }}</el-descriptions-item>
          <el-descriptions-item label="案例名称">{{ currentCase.caseName }}</el-descriptions-item>
          <el-descriptions-item label="风险类型">{{ getRiskTypeName(currentCase.riskType) }}</el-descriptions-item>
          <el-descriptions-item label="风险等级">{{ getRiskLevelName(currentCase.riskLevel) }}</el-descriptions-item>
          <el-descriptions-item label="所属行业">{{ currentCase.industry }}</el-descriptions-item>
          <el-descriptions-item label="发生时间">{{ currentCase.occurTime }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ getStatusName(currentCase.status) }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentCase.createTime }}</el-descriptions-item>
          <el-descriptions-item label="案例描述">{{ currentCase.description }}</el-descriptions-item>
          <el-descriptions-item label="应对措施">{{ currentCase.measures }}</el-descriptions-item>
          <el-descriptions-item label="经验教训">{{ currentCase.lessons }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer><el-button @click="detailDialogVisible = false">关闭</el-button></template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Refresh, Search, View, Edit } from '@element-plus/icons-vue'

export default {
  name: 'CaseLibrary',
  components: { Plus, Refresh, Search, View, Edit },
  setup() {
    const loading = ref(false)
    const caseDialogVisible = ref(false)
    const detailDialogVisible = ref(false)
    const caseDialogTitle = ref('新增案例')
    const currentCase = ref(null)
    
    // 搜索和分页
    const searchForm = reactive({ caseId: '', caseName: '', riskType: '', riskLevel: '' })
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(100)
    
    // 案例列表
    const caseList = ref([
      { caseId: 'CASE001', caseName: '芯片供应中断风险案例', riskType: 'supply_chain', riskLevel: 'high', industry: '电子制造', status: 'published', createTime: '2026-04-09 10:00:00' },
      { caseId: 'CASE002', caseName: '原材料价格上涨风险案例', riskType: 'market', riskLevel: 'medium', industry: '制造业', status: 'published', createTime: '2026-04-08 14:00:00' },
      { caseId: 'CASE003', caseName: '地缘政治冲突风险案例', riskType: 'geopolitical', riskLevel: 'high', industry: '国际贸易', status: 'draft', createTime: '2026-04-07 09:00:00' },
      { caseId: 'CASE004', caseName: '政策法规变更风险案例', riskType: 'policy', riskLevel: 'medium', industry: '医药行业', status: 'published', createTime: '2026-04-06 16:00:00' },
      { caseId: 'CASE005', caseName: '供应商财务风险案例', riskType: 'financial', riskLevel: 'high', industry: '汽车制造', status: 'published', createTime: '2026-04-05 11:00:00' }
    ])
    
    // 案例表单
    const caseForm = reactive({
      caseName: '',
      riskType: '',
      riskLevel: '',
      industry: '',
      occurTime: null,
      description: '',
      measures: '',
      lessons: '',
      status: 'draft'
    })
    
    const handleCreateCase = () => {
      caseDialogTitle.value = '新增案例'
      Object.keys(caseForm).forEach(key => {
        caseForm[key] = key === 'status' ? 'draft' : ''
      })
      caseForm.occurTime = null
      caseDialogVisible.value = true
    }
    
    const handleEditCase = (caseItem) => {
      caseDialogTitle.value = '编辑案例'
      currentCase.value = caseItem
      Object.assign(caseForm, caseItem)
      caseDialogVisible.value = true
    }
    
    const handleSaveCase = () => {
      if (!caseForm.caseName) {
        ElMessage.warning('请输入案例名称')
        return
      }
      if (!caseForm.riskType) {
        ElMessage.warning('请选择风险类型')
        return
      }
      if (!caseForm.riskLevel) {
        ElMessage.warning('请选择风险等级')
        return
      }
      if (!caseForm.industry) {
        ElMessage.warning('请输入所属行业')
        return
      }
      if (!caseForm.occurTime) {
        ElMessage.warning('请选择发生时间')
        return
      }
      ElMessage.success('案例保存成功')
      caseDialogVisible.value = false
      // 模拟添加或更新案例
      if (currentCase.value) {
        // 更新现有案例
        const index = caseList.value.findIndex(item => item.caseId === currentCase.value.caseId)
        if (index !== -1) {
          caseList.value[index] = { ...caseForm, caseId: currentCase.value.caseId, createTime: currentCase.value.createTime }
        }
      } else {
        // 添加新案例
        const newCase = {
          caseId: 'CASE' + new Date().getTime(),
          ...caseForm,
          createTime: new Date().toLocaleString()
        }
        caseList.value.unshift(newCase)
      }
      currentCase.value = null
    }
    
    const handleViewCase = (caseItem) => {
      currentCase.value = caseItem
      detailDialogVisible.value = true
    }
    
    const handleRefresh = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('刷新成功')
        loading.value = false
      }, 1000)
    }
    
    const handleSearch = () => {
      ElMessage.info('搜索功能开发中')
    }
    
    const resetForm = () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
    }
    
    const handleSizeChange = (size) => {
      pagination.pageSize = size
    }
    
    const handleCurrentChange = (current) => {
      pagination.currentPage = current
    }
    
    const getRiskTypeName = (type) => {
      const typeMap = {
        supply_chain: '供应链风险',
        market: '市场风险',
        policy: '政策风险',
        geopolitical: '地缘政治风险',
        financial: '财务风险',
        quality: '质量风险'
      }
      return typeMap[type] || type
    }
    
    const getRiskLevelName = (level) => {
      switch (level) {
        case 'high': return '高风险'
        case 'medium': return '中风险'
        case 'low': return '低风险'
        default: return level
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
    
    const getStatusName = (status) => {
      switch (status) {
        case 'draft': return '草稿'
        case 'published': return '已发布'
        default: return status
      }
    }
    
    onMounted(() => {
      console.log('案例库管理页面加载')
    })
    
    return {
      loading, caseDialogVisible, detailDialogVisible, caseDialogTitle, currentCase,
      searchForm, pagination, total, caseList, caseForm,
      handleCreateCase, handleEditCase, handleSaveCase, handleViewCase,
      handleRefresh, handleSearch, resetForm, handleSizeChange, handleCurrentChange,
      getRiskTypeName, getRiskLevelName, getRiskLevelColor, getStatusName
    }
  }
}
</script>

<style scoped>
.case-library {
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
.search-container {
  margin-bottom: 20px;
}
.search-form {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
}
.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
.case-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.detail-dialog {
  padding: 10px;
}
</style>