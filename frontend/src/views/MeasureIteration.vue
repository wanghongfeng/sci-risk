<template>
  <div class="measure-iteration">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>应对措施迭代</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleCreateMeasure"><el-icon><Plus /></el-icon>新增措施</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 搜索和筛选 -->
        <div class="search-container">
          <el-form :inline="true" :model="searchForm" class="search-form">
            <el-form-item label="措施ID"><el-input v-model="searchForm.measureId" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="措施名称"><el-input v-model="searchForm.measureName" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="措施类型"><el-select v-model="searchForm.type" placeholder="请选择" clearable style="width: 150px;"><el-option label="技术措施" value="technical" /><el-option label="管理措施" value="management" /><el-option label="应急措施" value="emergency" /></el-select></el-form-item>
            <el-form-item label="状态"><el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 120px;"><el-option label="生效" value="active" /><el-option label="失效" value="inactive" /></el-select></el-form-item>
            <el-form-item><el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
          </el-form>
        </div>
        
        <!-- 措施列表 -->
        <el-table :data="measureList" style="width: 100%" border stripe>
          <el-table-column prop="measureId" label="措施ID" width="120" />
          <el-table-column prop="measureName" label="措施名称" min-width="200" show-overflow-tooltip />
          <el-table-column prop="type" label="措施类型" width="120"><template #default="scope">{{ getTypeName(scope.row.type) }}</template></el-table-column>
          <el-table-column prop="riskLevel" label="适用风险等级" width="120"><template #default="scope">{{ getRiskLevelName(scope.row.riskLevel) }}</template></el-table-column>
          <el-table-column prop="effectiveness" label="预计效果" width="100" align="right"><template #default="scope"><el-progress :percentage="scope.row.effectiveness" :color="getEffectivenessColor(scope.row.effectiveness)" :stroke-width="10" /></template></el-table-column>
          <el-table-column prop="actualEffectiveness" label="实际效果" width="100" align="right"><template #default="scope"><el-progress :percentage="scope.row.actualEffectiveness" :color="getEffectivenessColor(scope.row.actualEffectiveness)" :stroke-width="10" /></template></el-table-column>
          <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'active' ? 'success' : 'info'"> {{ getStatusName(scope.row.status) }}</el-tag></template></el-table-column>
          <el-table-column prop="lastIterationTime" label="上次迭代时间" width="180" />
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleViewMeasure(scope.row)"><el-icon><View /></el-icon>查看</el-button>
              <el-button type="warning" size="small" @click="handleEditMeasure(scope.row)"><el-icon><Edit /></el-icon>编辑</el-button>
              <el-button type="danger" size="small" @click="handleDeleteMeasure(scope.row)"><el-icon><Delete /></el-icon>删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination-wrapper"><el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" /></div>
      </div>
    </el-card>
    
    <!-- 措施对话框 -->
    <el-dialog v-model="measureDialogVisible" :title="measureDialogTitle" width="800px">
      <el-form :model="measureForm" label-width="120px" class="measure-form">
        <el-form-item label="措施名称" required><el-input v-model="measureForm.measureName" placeholder="请输入措施名称" style="width: 100%;" /></el-form-item>
        <el-form-item label="措施类型" required><el-select v-model="measureForm.type" placeholder="请选择措施类型" style="width: 100%;"><el-option label="技术措施" value="technical" /><el-option label="管理措施" value="management" /><el-option label="应急措施" value="emergency" /><el-option label="其他措施" value="other" /></el-select></el-form-item>
        <el-form-item label="适用风险等级" required><el-select v-model="measureForm.riskLevel" placeholder="请选择适用风险等级" style="width: 100%;"><el-option label="高风险" value="high" /><el-option label="中风险" value="medium" /><el-option label="低风险" value="low" /></el-select></el-form-item>
        <el-form-item label="预计效果" required><el-slider v-model="measureForm.effectiveness" :min="0" :max="100" :step="1" show-input /></el-form-item>
        <el-form-item label="实际效果"><el-slider v-model="measureForm.actualEffectiveness" :min="0" :max="100" :step="1" show-input /></el-form-item>
        <el-form-item label="措施描述"><el-input v-model="measureForm.description" type="textarea" :rows="4" placeholder="请输入措施描述" style="width: 100%;" /></el-form-item>
        <el-form-item label="实施步骤"><el-input v-model="measureForm.steps" type="textarea" :rows="4" placeholder="请输入实施步骤" style="width: 100%;" /></el-form-item>
        <el-form-item label="状态"><el-select v-model="measureForm.status" placeholder="请选择状态" style="width: 100%;"><el-option label="生效" value="active" /><el-option label="失效" value="inactive" /></el-select></el-form-item>
      </el-form>
      <template #footer><el-button @click="measureDialogVisible = false">取消</el-button><el-button type="primary" @click="handleSaveMeasure">保存</el-button></template>
    </el-dialog>
    
    <!-- 措施详情对话框 -->
    <el-dialog v-model="detailDialogVisible" :title="'措施详情 - ' + (currentMeasure?.measureId || '')" width="800px">
      <div v-if="currentMeasure" class="detail-dialog">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="措施ID">{{ currentMeasure.measureId }}</el-descriptions-item>
          <el-descriptions-item label="措施名称">{{ currentMeasure.measureName }}</el-descriptions-item>
          <el-descriptions-item label="措施类型">{{ getTypeName(currentMeasure.type) }}</el-descriptions-item>
          <el-descriptions-item label="适用风险等级">{{ getRiskLevelName(currentMeasure.riskLevel) }}</el-descriptions-item>
          <el-descriptions-item label="预计效果">{{ currentMeasure.effectiveness }}%</el-descriptions-item>
          <el-descriptions-item label="实际效果">{{ currentMeasure.actualEffectiveness }}%</el-descriptions-item>
          <el-descriptions-item label="状态">{{ getStatusName(currentMeasure.status) }}</el-descriptions-item>
          <el-descriptions-item label="措施描述">{{ currentMeasure.description }}</el-descriptions-item>
          <el-descriptions-item label="实施步骤">{{ currentMeasure.steps }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentMeasure.createTime }}</el-descriptions-item>
          <el-descriptions-item label="上次迭代时间">{{ currentMeasure.lastIterationTime || '-' }}</el-descriptions-item>
        </el-descriptions>
        
        <!-- 迭代历史 -->
        <div class="iteration-history" style="margin-top: 20px;">
          <h4>迭代历史</h4>
          <el-timeline>
            <el-timeline-item v-for="(record, index) in currentMeasure.iterationHistory" :key="index" :timestamp="record.time" :type="record.type">
              <el-card shadow="hover" style="width: 100%;">
                <div class="timeline-content">
                  <div class="timeline-title">{{ record.title }}</div>
                  <div class="timeline-description">{{ record.description }}</div>
                  <div class="timeline-changes" v-if="record.changes.length > 0">
                    <h5>变更内容：</h5>
                    <ul>
                      <li v-for="(change, i) in record.changes" :key="i">{{ change }}</li>
                    </ul>
                  </div>
                </div>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>
        
        <!-- 迭代建议 -->
        <div class="iteration-suggestions" style="margin-top: 20px;">
          <h4>迭代建议</h4>
          <div class="suggestions-list">
            <div v-for="(suggestion, index) in currentMeasure.suggestions" :key="index" class="suggestion-item">
              <div class="suggestion-content">{{ suggestion.content }}</div>
              <div class="suggestion-priority"><el-tag :type="suggestion.priority === 'high' ? 'danger' : suggestion.priority === 'medium' ? 'warning' : 'info'"> {{ suggestion.priority === 'high' ? '高' : suggestion.priority === 'medium' ? '中' : '低' }}</el-tag></div>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleIterateMeasure">执行迭代</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh, Search, View, Edit, Delete } from '@element-plus/icons-vue'

export default {
  name: 'MeasureIteration',
  components: { Plus, Refresh, Search, View, Edit, Delete },
  setup() {
    const loading = ref(false)
    const measureDialogVisible = ref(false)
    const detailDialogVisible = ref(false)
    const measureDialogTitle = ref('新增措施')
    const currentMeasure = ref(null)
    
    // 搜索和分页
    const searchForm = reactive({ measureId: '', measureName: '', type: '', status: '' })
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(120)
    
    // 措施列表
    const measureList = ref([
      { measureId: 'MEASURE001', measureName: '供应商多元化策略', type: 'management', riskLevel: 'high', effectiveness: 90, actualEffectiveness: 85, status: 'active', lastIterationTime: '2026-04-08 10:00:00', createTime: '2026-04-01 09:00:00' },
      { measureId: 'MEASURE002', measureName: '库存缓冲策略', type: 'technical', riskLevel: 'medium', effectiveness: 80, actualEffectiveness: 75, status: 'active', lastIterationTime: '2026-04-07 14:00:00', createTime: '2026-04-02 10:00:00' },
      { measureId: 'MEASURE003', measureName: '应急响应预案', type: 'emergency', riskLevel: 'high', effectiveness: 85, actualEffectiveness: 80, status: 'active', lastIterationTime: '2026-04-06 16:00:00', createTime: '2026-04-03 11:00:00' },
      { measureId: 'MEASURE004', measureName: '风险监控系统', type: 'technical', riskLevel: 'medium', effectiveness: 75, actualEffectiveness: 70, status: 'active', lastIterationTime: '2026-04-05 09:00:00', createTime: '2026-04-04 14:00:00' }
    ])
    
    // 措施表单
    const measureForm = reactive({
      measureName: '',
      type: '',
      riskLevel: '',
      effectiveness: 80,
      actualEffectiveness: 0,
      description: '',
      steps: '',
      status: 'active'
    })
    
    // 模拟迭代历史
    const mockIterationHistory = [
      {
        time: '2026-04-08 10:00:00',
        type: 'primary',
        title: '优化供应商选择标准',
        description: '根据最新市场情况，优化供应商评估标准',
        changes: ['增加供应商财务稳定性评估', '优化供应商地理位置分布']
      },
      {
        time: '2026-04-01 09:00:00',
        type: 'success',
        title: '初始创建',
        description: '创建供应商多元化策略',
        changes: ['制定初始供应商多元化方案', '设置实施时间表']
      }
    ]
    
    // 模拟迭代建议
    const mockSuggestions = [
      { content: '建议增加供应商绩效评估机制，定期评估供应商表现', priority: 'high' },
      { content: '建议优化库存缓冲策略，根据不同物料设置差异化缓冲水平', priority: 'medium' },
      { content: '建议建立供应商风险预警机制，提前识别潜在风险', priority: 'low' }
    ]
    
    const handleCreateMeasure = () => {
      measureDialogTitle.value = '新增措施'
      Object.keys(measureForm).forEach(key => {
        measureForm[key] = key === 'effectiveness' ? 80 : key === 'actualEffectiveness' ? 0 : key === 'status' ? 'active' : ''
      })
      measureDialogVisible.value = true
    }
    
    const handleEditMeasure = (measure) => {
      measureDialogTitle.value = '编辑措施'
      currentMeasure.value = measure
      Object.assign(measureForm, measure)
      measureDialogVisible.value = true
    }
    
    const handleSaveMeasure = () => {
      if (!measureForm.measureName) {
        ElMessage.warning('请输入措施名称')
        return
      }
      if (!measureForm.type) {
        ElMessage.warning('请选择措施类型')
        return
      }
      if (!measureForm.riskLevel) {
        ElMessage.warning('请选择适用风险等级')
        return
      }
      ElMessage.success('措施保存成功')
      measureDialogVisible.value = false
      // 模拟添加或更新措施
      if (currentMeasure.value) {
        // 更新现有措施
        const index = measureList.value.findIndex(item => item.measureId === currentMeasure.value.measureId)
        if (index !== -1) {
          measureList.value[index] = { ...measureForm, measureId: currentMeasure.value.measureId, createTime: currentMeasure.value.createTime, lastIterationTime: new Date().toLocaleString() }
        }
      } else {
        // 添加新措施
        const newMeasure = {
          measureId: 'MEASURE' + new Date().getTime(),
          ...measureForm,
          createTime: new Date().toLocaleString(),
          lastIterationTime: null
        }
        measureList.value.unshift(newMeasure)
      }
      currentMeasure.value = null
    }
    
    const handleViewMeasure = (measure) => {
      currentMeasure.value = {
        ...measure,
        iterationHistory: mockIterationHistory,
        suggestions: mockSuggestions
      }
      detailDialogVisible.value = true
    }
    
    const handleDeleteMeasure = (measure) => {
      ElMessageBox.confirm('确定要删除此措施吗？', '删除措施', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = measureList.value.findIndex(item => item.measureId === measure.measureId)
        if (index !== -1) {
          measureList.value.splice(index, 1)
        }
        ElMessage.success('措施删除成功')
      })
    }
    
    const handleIterateMeasure = () => {
      ElMessage.success('措施迭代成功')
      currentMeasure.value.lastIterationTime = new Date().toLocaleString()
      // 模拟添加新的迭代记录
      currentMeasure.value.iterationHistory.unshift({
        time: new Date().toLocaleString(),
        type: 'warning',
        title: '执行迭代优化',
        description: '根据最新数据和建议进行措施优化',
        changes: ['优化实施步骤', '调整效果预期']
      })
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
    
    const getTypeName = (type) => {
      const typeMap = {
        technical: '技术措施',
        management: '管理措施',
        emergency: '应急措施',
        other: '其他措施'
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
    
    const getStatusName = (status) => {
      switch (status) {
        case 'active': return '生效'
        case 'inactive': return '失效'
        default: return status
      }
    }
    
    const getEffectivenessColor = (value) => {
      if (value >= 80) return '#67c23a'
      if (value >= 60) return '#e6a23c'
      return '#f56c6c'
    }
    
    onMounted(() => {
      console.log('应对措施迭代页面加载')
    })
    
    return {
      loading, measureDialogVisible, detailDialogVisible, measureDialogTitle, currentMeasure,
      searchForm, pagination, total, measureList, measureForm,
      handleCreateMeasure, handleEditMeasure, handleSaveMeasure, handleViewMeasure, handleDeleteMeasure, handleIterateMeasure,
      handleRefresh, handleSearch, resetForm, handleSizeChange, handleCurrentChange,
      getTypeName, getRiskLevelName, getStatusName, getEffectivenessColor
    }
  }
}
</script>

<style scoped>
.measure-iteration {
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
.measure-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.detail-dialog {
  padding: 10px;
}
.iteration-history {
  margin-top: 20px;
}
.timeline-content {
  padding: 10px;
}
.timeline-title {
  font-weight: bold;
  margin-bottom: 5px;
}
.timeline-description {
  margin-bottom: 10px;
  font-size: 14px;
}
.timeline-changes {
  margin-top: 10px;
  font-size: 14px;
}
.timeline-changes h5 {
  margin-bottom: 5px;
  font-size: 14px;
}
.timeline-changes ul {
  margin: 0;
  padding-left: 20px;
}
.timeline-changes li {
  margin-bottom: 3px;
}
.iteration-suggestions {
  margin-top: 20px;
}
.suggestions-list {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
}
.suggestion-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}
.suggestion-content {
  flex: 1;
}
.suggestion-priority {
  margin-left: 20px;
}
</style>