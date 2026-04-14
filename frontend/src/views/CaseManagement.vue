<template>
  <div class="page-container">
    <h2 class="page-title">案例库管理</h2>
    
    <!-- 搜索和筛选 -->
    <div class="search-container">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="案例名称">
          <el-input v-model="searchForm.caseName" placeholder="请输入" clearable style="width: 250px;" />
        </el-form-item>
        <el-form-item label="风险类型">
          <el-select v-model="searchForm.riskType" placeholder="请选择" clearable style="width: 200px;">
            <el-option label="供应链风险" value="supply_chain" />
            <el-option label="市场风险" value="market" />
            <el-option label="地缘政治风险" value="geopolitical" />
            <el-option label="财务风险" value="financial" />
            <el-option label="技术风险" value="technical" />
          </el-select>
        </el-form-item>
        <el-form-item label="风险等级">
          <el-select v-model="searchForm.riskLevel" placeholder="请选择" clearable style="width: 150px;">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
            <el-option label="极高" value="critical" />
          </el-select>
        </el-form-item>
        <el-form-item label="创建时间">
          <el-date-picker v-model="searchForm.timeRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="width: 300px;" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button>
          <el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button>
          <el-button type="success" @click="handleCreateCase"><el-icon><Plus /></el-icon>创建案例</el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <!-- 案例列表 -->
    <el-card shadow="hover" class="case-list-card">
      <template #header>
        <div class="card-header">
          <span>案例列表</span>
        </div>
      </template>
      <el-table :data="caseList" style="width: 100%" border stripe>
        <el-table-column prop="caseId" label="案例ID" width="120" />
        <el-table-column prop="caseName" label="案例名称" min-width="250" show-overflow-tooltip />
        <el-table-column prop="riskType" label="风险类型" width="150">
          <template #default="scope">
            {{ getRiskTypeName(scope.row.riskType) }}
          </template>
        </el-table-column>
        <el-table-column prop="riskLevel" label="风险等级" width="100">
          <template #default="scope">
            <el-tag :type="getRiskLevelType(scope.row.riskLevel)">{{ scope.row.riskLevel }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="industry" label="所属行业" width="150" />
        <el-table-column prop="creator" label="创建人" width="120" />
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleViewCase(scope.row)" style="margin-right: 5px;">
              <el-icon><View /></el-icon>查看
            </el-button>
            <el-button type="warning" size="small" @click="handleEditCase(scope.row)" style="margin-right: 5px;">
              <el-icon><Edit /></el-icon>编辑
            </el-button>
            <el-button type="danger" size="small" @click="handleDeleteCase(scope.row)">
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
    
    <!-- 创建/编辑案例对话框 -->
    <el-dialog
      v-model="caseDialogVisible"
      :title="isEdit ? '编辑案例' : '创建案例'"
      width="800px"
    >
      <el-form :model="caseForm" label-width="120px">
        <el-form-item label="案例名称" required>
          <el-input v-model="caseForm.caseName" placeholder="请输入案例名称" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="风险类型" required>
          <el-select v-model="caseForm.riskType" placeholder="请选择" style="width: 100%;">
            <el-option label="供应链风险" value="supply_chain" />
            <el-option label="市场风险" value="market" />
            <el-option label="地缘政治风险" value="geopolitical" />
            <el-option label="财务风险" value="financial" />
            <el-option label="技术风险" value="technical" />
          </el-select>
        </el-form-item>
        <el-form-item label="风险等级" required>
          <el-select v-model="caseForm.riskLevel" placeholder="请选择" style="width: 100%;">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
            <el-option label="极高" value="critical" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属行业">
          <el-input v-model="caseForm.industry" placeholder="请输入所属行业" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="案例描述" required>
          <el-input v-model="caseForm.description" type="textarea" :rows="3" placeholder="请输入案例描述" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="风险事件">
          <el-input v-model="caseForm.riskEvent" type="textarea" :rows="3" placeholder="请输入风险事件详情" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="应对措施">
          <el-input v-model="caseForm.responseMeasures" type="textarea" :rows="3" placeholder="请输入应对措施" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="经验教训">
          <el-input v-model="caseForm.lessonsLearned" type="textarea" :rows="3" placeholder="请输入经验教训" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="参考价值">
          <el-select v-model="caseForm.referenceValue" placeholder="请选择" style="width: 100%;">
            <el-option label="高" value="high" />
            <el-option label="中" value="medium" />
            <el-option label="低" value="low" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="caseDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitCase">保存</el-button>
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
  caseName: '',
  riskType: '',
  riskLevel: '',
  timeRange: []
})

// 案例列表
const caseList = ref([
  { caseId: 'C001', caseName: '某供应商财务风险案例', riskType: 'financial', riskLevel: '高', industry: '制造业', creator: '张三', createTime: '2026-03-01 10:00:00' },
  { caseId: 'C002', caseName: '地缘政治冲突导致供应链中断', riskType: 'geopolitical', riskLevel: '极高', industry: '电子行业', creator: '李四', createTime: '2026-03-10 14:30:00' },
  { caseId: 'C003', caseName: '原材料价格大幅波动风险', riskType: 'market', riskLevel: '中', industry: '化工行业', creator: '王五', createTime: '2026-03-15 09:15:00' },
  { caseId: 'C004', caseName: '技术创新失败导致产品滞销', riskType: 'technical', riskLevel: '高', industry: '科技行业', creator: '赵六', createTime: '2026-03-20 16:45:00' },
  { caseId: 'C005', caseName: '物流运输中断风险案例', riskType: 'supply_chain', riskLevel: '中', industry: '零售行业', creator: '张三', createTime: '2026-03-25 11:20:00' }
])

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(caseList.value.length)

// 创建/编辑案例对话框
const caseDialogVisible = ref(false)
const isEdit = ref(false)
const caseForm = ref({
  caseId: '',
  caseName: '',
  riskType: '',
  riskLevel: '',
  industry: '',
  description: '',
  riskEvent: '',
  responseMeasures: '',
  lessonsLearned: '',
  referenceValue: ''
})

// 处理搜索
const handleSearch = () => {
  console.log('搜索条件:', searchForm.value)
  // 这里可以添加搜索逻辑
}

// 重置表单
const resetForm = () => {
  searchForm.value = {
    caseName: '',
    riskType: '',
    riskLevel: '',
    timeRange: []
  }
}

// 创建案例
const handleCreateCase = () => {
  isEdit.value = false
  caseForm.value = {
    caseId: '',
    caseName: '',
    riskType: '',
    riskLevel: '',
    industry: '',
    description: '',
    riskEvent: '',
    responseMeasures: '',
    lessonsLearned: '',
    referenceValue: ''
  }
  caseDialogVisible.value = true
}

// 编辑案例
const handleEditCase = (caseItem) => {
  isEdit.value = true
  caseForm.value = { ...caseItem }
  caseDialogVisible.value = true
}

// 提交案例
const handleSubmitCase = () => {
  if (!caseForm.value.caseName) {
    ElMessageBox.warning('请输入案例名称')
    return
  }
  if (!caseForm.value.riskType) {
    ElMessageBox.warning('请选择风险类型')
    return
  }
  if (!caseForm.value.riskLevel) {
    ElMessageBox.warning('请选择风险等级')
    return
  }
  if (!caseForm.value.industry) {
    ElMessageBox.warning('请输入所属行业')
    return
  }
  
  console.log(isEdit.value ? '编辑案例:' : '创建案例:', caseForm.value)
  
  // 模拟提交案例的逻辑
  setTimeout(() => {
    if (isEdit.value) {
      // 更新案例列表中的数据
      const index = caseList.value.findIndex(item => item.caseId === caseForm.value.caseId)
      if (index !== -1) {
        caseList.value[index] = { ...caseForm.value }
      }
    } else {
      // 添加新案例
      const newCase = {
        ...caseForm.value,
        caseId: 'C' + String(caseList.value.length + 1).padStart(3, '0'),
        creator: '当前用户',
        createTime: new Date().toLocaleString()
      }
      caseList.value.unshift(newCase)
    }
    
    caseDialogVisible.value = false
    ElMessageBox.success(isEdit.value ? '案例编辑成功' : '案例创建成功')
  }, 500)
}

// 查看案例
const handleViewCase = (caseItem) => {
  console.log('查看案例:', caseItem)
  // 这里可以添加查看案例的逻辑
  ElMessageBox.alert(`查看案例: ${caseItem.caseName}`, '案例详情', {
    confirmButtonText: '确定'
  })
}

// 删除案例
const handleDeleteCase = (caseItem) => {
  ElMessageBox.confirm(`确定要删除案例 ${caseItem.caseName} 吗？`, '删除案例', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    console.log('删除案例:', caseItem)
    
    // 模拟删除案例的逻辑
    setTimeout(() => {
      // 从案例列表中移除数据
      const index = caseList.value.findIndex(item => item.caseId === caseItem.caseId)
      if (index !== -1) {
        caseList.value.splice(index, 1)
      }
      ElMessageBox.success('案例删除成功')
    }, 500)
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

// 获取风险类型名称
const getRiskTypeName = (type) => {
  const typeMap = {
    supply_chain: '供应链风险',
    market: '市场风险',
    geopolitical: '地缘政治风险',
    financial: '财务风险',
    technical: '技术风险'
  }
  return typeMap[type] || type
}

// 获取风险等级类型
const getRiskLevelType = (level) => {
  const typeMap = {
    'low': 'info',
    'medium': 'warning',
    'high': 'danger',
    'critical': 'danger'
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

.case-list-card {
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
