<template>
  <div class="rule-optimization">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>预警规则优化</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleCreateRule"><el-icon><Plus /></el-icon>新增规则</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 搜索和筛选 -->
        <div class="search-container">
          <el-form :inline="true" :model="searchForm" class="search-form">
            <el-form-item label="规则ID"><el-input v-model="searchForm.ruleId" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="规则名称"><el-input v-model="searchForm.ruleName" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="规则类型"><el-select v-model="searchForm.ruleType" placeholder="请选择" clearable style="width: 150px;"><el-option label="阈值规则" value="threshold" /><el-option label="趋势规则" value="trend" /><el-option label="异常规则" value="anomaly" /></el-select></el-form-item>
            <el-form-item label="状态"><el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 120px;"><el-option label="启用" value="enabled" /><el-option label="禁用" value="disabled" /></el-select></el-form-item>
            <el-form-item><el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
          </el-form>
        </div>
        
        <!-- 规则列表 -->
        <el-table :data="ruleList" style="width: 100%" border stripe>
          <el-table-column prop="ruleId" label="规则ID" width="120" />
          <el-table-column prop="ruleName" label="规则名称" min-width="200" show-overflow-tooltip />
          <el-table-column prop="ruleType" label="规则类型" width="120"><template #default="scope">{{ getRuleTypeName(scope.row.ruleType) }}</template></el-table-column>
          <el-table-column prop="riskType" label="风险类型" width="120"><template #default="scope">{{ getRiskTypeName(scope.row.riskType) }}</template></el-table-column>
          <el-table-column prop="threshold" label="阈值" width="100" />
          <el-table-column prop="accuracy" label="准确率" width="120"><template #default="scope"><el-progress :percentage="scope.row.accuracy" :stroke-width="10" /></template></el-table-column>
          <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'enabled' ? 'success' : 'info'"> {{ getStatusName(scope.row.status) }}</el-tag></template></el-table-column>
          <el-table-column prop="createTime" label="创建时间" width="180" />
          <el-table-column label="操作" width="220" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleViewRule(scope.row)"><el-icon><View /></el-icon>查看</el-button>
              <el-button type="warning" size="small" @click="handleEditRule(scope.row)"><el-icon><Edit /></el-icon>编辑</el-button>
              <el-button type="danger" size="small" @click="handleDeleteRule(scope.row)"><el-icon><Delete /></el-icon>删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination-wrapper"><el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" /></div>
      </div>
    </el-card>
    
    <!-- 规则对话框 -->
    <el-dialog v-model="ruleDialogVisible" :title="ruleDialogTitle" width="800px">
      <el-form :model="ruleForm" label-width="120px" class="rule-form">
        <el-form-item label="规则名称" required><el-input v-model="ruleForm.ruleName" placeholder="请输入规则名称" style="width: 100%;" /></el-form-item>
        <el-form-item label="规则类型" required><el-select v-model="ruleForm.ruleType" placeholder="请选择规则类型" style="width: 100%;"><el-option label="阈值规则" value="threshold" /><el-option label="趋势规则" value="trend" /><el-option label="异常规则" value="anomaly" /></el-select></el-form-item>
        <el-form-item label="风险类型" required><el-select v-model="ruleForm.riskType" placeholder="请选择风险类型" style="width: 100%;"><el-option label="供应链风险" value="supply_chain" /><el-option label="市场风险" value="market" /><el-option label="政策风险" value="policy" /><el-option label="地缘政治风险" value="geopolitical" /></el-select></el-form-item>
        <el-form-item label="阈值" required><el-input v-model="ruleForm.threshold" type="number" placeholder="请输入阈值" style="width: 100%;" /></el-form-item>
        <el-form-item label="规则描述"><el-input v-model="ruleForm.description" type="textarea" :rows="3" placeholder="请输入规则描述" style="width: 100%;" /></el-form-item>
        <el-form-item label="状态"><el-select v-model="ruleForm.status" placeholder="请选择状态" style="width: 100%;"><el-option label="启用" value="enabled" /><el-option label="禁用" value="disabled" /></el-select></el-form-item>
      </el-form>
      <template #footer><el-button @click="ruleDialogVisible = false">取消</el-button><el-button type="primary" @click="handleSaveRule">保存</el-button></template>
    </el-dialog>
    
    <!-- 规则详情对话框 -->
    <el-dialog v-model="detailDialogVisible" :title="'规则详情 - ' + (currentRule?.ruleId || '')" width="800px">
      <div v-if="currentRule" class="detail-dialog">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="规则ID">{{ currentRule.ruleId }}</el-descriptions-item>
          <el-descriptions-item label="规则名称">{{ currentRule.ruleName }}</el-descriptions-item>
          <el-descriptions-item label="规则类型">{{ getRuleTypeName(currentRule.ruleType) }}</el-descriptions-item>
          <el-descriptions-item label="风险类型">{{ getRiskTypeName(currentRule.riskType) }}</el-descriptions-item>
          <el-descriptions-item label="阈值">{{ currentRule.threshold }}</el-descriptions-item>
          <el-descriptions-item label="准确率">{{ currentRule.accuracy }}%</el-descriptions-item>
          <el-descriptions-item label="状态">{{ getStatusName(currentRule.status) }}</el-descriptions-item>
          <el-descriptions-item label="规则描述">{{ currentRule.description }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentRule.createTime }}</el-descriptions-item>
          <el-descriptions-item label="上次优化时间">{{ currentRule.lastOptimizeTime || '-' }}</el-descriptions-item>
        </el-descriptions>
        
        <!-- 规则性能分析 -->
        <div class="rule-analysis" style="margin-top: 20px;">
          <h4>规则性能分析</h4>
          <el-table :data="currentRule.performanceData" style="width: 100%" border>
            <el-table-column prop="metric" label="指标" width="120" />
            <el-table-column prop="value" label="值" width="100" />
            <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'good' ? 'success' : scope.row.status === 'warning' ? 'warning' : 'danger'"> {{ scope.row.status === 'good' ? '良好' : scope.row.status === 'warning' ? '警告' : '异常' }}</el-tag></template></el-table-column>
          </el-table>
        </div>
        
        <!-- 优化建议 -->
        <div class="optimization-suggestions" style="margin-top: 20px;">
          <h4>优化建议</h4>
          <div class="suggestions-list">
            <div v-for="(suggestion, index) in currentRule.suggestions" :key="index" class="suggestion-item">
              <div class="suggestion-content">{{ suggestion.content }}</div>
              <div class="suggestion-priority"><el-tag :type="suggestion.priority === 'high' ? 'danger' : suggestion.priority === 'medium' ? 'warning' : 'info'"> {{ suggestion.priority === 'high' ? '高' : suggestion.priority === 'medium' ? '中' : '低' }}</el-tag></div>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleOptimizeRule">优化规则</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh, Search, View, Edit, Delete } from '@element-plus/icons-vue'

export default {
  name: 'RuleOptimization',
  components: { Plus, Refresh, Search, View, Edit, Delete },
  setup() {
    const loading = ref(false)
    const ruleDialogVisible = ref(false)
    const detailDialogVisible = ref(false)
    const ruleDialogTitle = ref('新增规则')
    const currentRule = ref(null)
    
    // 搜索和分页
    const searchForm = reactive({ ruleId: '', ruleName: '', ruleType: '', status: '' })
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(80)
    
    // 规则列表
    const ruleList = ref([
      { ruleId: 'RULE001', ruleName: '芯片供应中断预警规则', ruleType: 'threshold', riskType: 'supply_chain', threshold: 80, accuracy: 92, status: 'enabled', createTime: '2026-04-09 10:00:00' },
      { ruleId: 'RULE002', ruleName: '原材料价格上涨预警规则', ruleType: 'trend', riskType: 'market', threshold: 10, accuracy: 85, status: 'enabled', createTime: '2026-04-08 14:00:00' },
      { ruleId: 'RULE003', ruleName: '地缘政治风险预警规则', ruleType: 'anomaly', riskType: 'geopolitical', threshold: 70, accuracy: 78, status: 'disabled', createTime: '2026-04-07 09:00:00' },
      { ruleId: 'RULE004', ruleName: '政策法规变更预警规则', ruleType: 'threshold', riskType: 'policy', threshold: 60, accuracy: 88, status: 'enabled', createTime: '2026-04-06 16:00:00' }
    ])
    
    // 规则表单
    const ruleForm = reactive({
      ruleName: '',
      ruleType: '',
      riskType: '',
      threshold: '',
      description: '',
      status: 'enabled'
    })
    
    // 模拟规则性能数据
    const mockPerformanceData = [
      { metric: '准确率', value: '92%', status: 'good' },
      { metric: '召回率', value: '85%', status: 'good' },
      { metric: '误报率', value: '5%', status: 'good' },
      { metric: '漏报率', value: '3%', status: 'good' },
      { metric: '响应时间', value: '0.5s', status: 'good' }
    ]
    
    // 模拟优化建议
    const mockSuggestions = [
      { content: '建议调整阈值为75，以提高准确率', priority: 'high' },
      { content: '建议增加趋势分析维度，提高预警精度', priority: 'medium' },
      { content: '建议定期更新规则参数，适应市场变化', priority: 'low' }
    ]
    
    const handleCreateRule = () => {
      ruleDialogTitle.value = '新增规则'
      Object.keys(ruleForm).forEach(key => {
        ruleForm[key] = key === 'status' ? 'enabled' : ''
      })
      ruleDialogVisible.value = true
    }
    
    const handleEditRule = (rule) => {
      ruleDialogTitle.value = '编辑规则'
      currentRule.value = rule
      Object.assign(ruleForm, rule)
      ruleDialogVisible.value = true
    }
    
    const handleSaveRule = () => {
      if (!ruleForm.ruleName) {
        ElMessage.warning('请输入规则名称')
        return
      }
      if (!ruleForm.ruleType) {
        ElMessage.warning('请选择规则类型')
        return
      }
      if (!ruleForm.riskType) {
        ElMessage.warning('请选择风险类型')
        return
      }
      if (!ruleForm.threshold) {
        ElMessage.warning('请输入阈值')
        return
      }
      ElMessage.success('规则保存成功')
      ruleDialogVisible.value = false
      // 模拟添加或更新规则
      if (currentRule.value) {
        // 更新现有规则
        const index = ruleList.value.findIndex(item => item.ruleId === currentRule.value.ruleId)
        if (index !== -1) {
          ruleList.value[index] = { ...ruleForm, ruleId: currentRule.value.ruleId, createTime: currentRule.value.createTime, accuracy: currentRule.value.accuracy }
        }
      } else {
        // 添加新规则
        const newRule = {
          ruleId: 'RULE' + new Date().getTime(),
          ...ruleForm,
          accuracy: 80,
          createTime: new Date().toLocaleString()
        }
        ruleList.value.unshift(newRule)
      }
      currentRule.value = null
    }
    
    const handleViewRule = (rule) => {
      currentRule.value = {
        ...rule,
        performanceData: mockPerformanceData,
        suggestions: mockSuggestions,
        lastOptimizeTime: '2026-04-08 10:00:00'
      }
      detailDialogVisible.value = true
    }
    
    const handleDeleteRule = (rule) => {
      ElMessageBox.confirm('确定要删除此规则吗？', '删除规则', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = ruleList.value.findIndex(item => item.ruleId === rule.ruleId)
        if (index !== -1) {
          ruleList.value.splice(index, 1)
        }
        ElMessage.success('规则删除成功')
      })
    }
    
    const handleOptimizeRule = () => {
      ElMessage.success('规则优化成功')
      currentRule.value.accuracy = 95
      currentRule.value.lastOptimizeTime = new Date().toLocaleString()
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
    
    const getRuleTypeName = (type) => {
      switch (type) {
        case 'threshold': return '阈值规则'
        case 'trend': return '趋势规则'
        case 'anomaly': return '异常规则'
        default: return type
      }
    }
    
    const getRiskTypeName = (type) => {
      const typeMap = {
        supply_chain: '供应链风险',
        market: '市场风险',
        policy: '政策风险',
        geopolitical: '地缘政治风险'
      }
      return typeMap[type] || type
    }
    
    const getStatusName = (status) => {
      switch (status) {
        case 'enabled': return '启用'
        case 'disabled': return '禁用'
        default: return status
      }
    }
    
    onMounted(() => {
      console.log('预警规则优化页面加载')
    })
    
    return {
      loading, ruleDialogVisible, detailDialogVisible, ruleDialogTitle, currentRule,
      searchForm, pagination, total, ruleList, ruleForm,
      handleCreateRule, handleEditRule, handleSaveRule, handleViewRule, handleDeleteRule, handleOptimizeRule,
      handleRefresh, handleSearch, resetForm, handleSizeChange, handleCurrentChange,
      getRuleTypeName, getRiskTypeName, getStatusName
    }
  }
}
</script>

<style scoped>
.rule-optimization {
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
.rule-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.detail-dialog {
  padding: 10px;
}
.rule-analysis {
  margin-top: 20px;
}
.optimization-suggestions {
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