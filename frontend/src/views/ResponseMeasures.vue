<template>
  <div class="response-measures">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>应对措施库</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleAddMeasure"><el-icon><Plus /></el-icon>新增措施</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 搜索和筛选 -->
        <div class="search-container">
          <el-form :inline="true" :model="searchForm" class="search-form">
            <el-form-item label="措施名称"><el-input v-model="searchForm.name" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="措施类型"><el-select v-model="searchForm.type" placeholder="请选择" clearable style="width: 120px;"><el-option v-for="type in measureTypes" :key="type.value" :label="type.label" :value="type.value" /></el-select></el-form-item>
            <el-form-item label="风险等级"><el-select v-model="searchForm.riskLevel" placeholder="请选择" clearable style="width: 120px;"><el-option label="高风险" value="high" /><el-option label="中风险" value="medium" /><el-option label="低风险" value="low" /></el-select></el-form-item>
            <el-form-item><el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
          </el-form>
        </div>
        
        <!-- 措施列表 -->
        <el-table :data="measureList" style="width: 100%" border stripe>
          <el-table-column prop="measureId" label="措施ID" width="120" />
          <el-table-column prop="measureName" label="措施名称" min-width="200" show-overflow-tooltip />
          <el-table-column prop="type" label="措施类型" width="120"><template #default="scope">{{ getTypeName(scope.row.type) }}</template></el-table-column>
          <el-table-column prop="riskLevel" label="适用风险等级" width="120"><template #default="scope">{{ getRiskLevelName(scope.row.riskLevel) }}</template></el-table-column>
          <el-table-column prop="description" label="措施描述" min-width="250" show-overflow-tooltip />
          <el-table-column prop="effectiveness" label="预计效果" width="100" align="right"><template #default="scope"><el-progress :percentage="scope.row.effectiveness" :color="getEffectivenessColor(scope.row.effectiveness)" :stroke-width="10" /></template></el-table-column>
          <el-table-column prop="createTime" label="创建时间" width="180" />
          <el-table-column label="操作" width="220" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleEditMeasure(scope.row)"><el-icon><Edit /></el-icon>编辑</el-button>
              <el-button type="danger" size="small" @click="handleDeleteMeasure(scope.row)"><el-icon><Delete /></el-icon>删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination-wrapper"><el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" /></div>
      </div>
    </el-card>
    
    <!-- 措施编辑对话框 -->
    <el-dialog v-model="measureDialogVisible" :title="measureDialogTitle" width="600px">
      <el-form :model="measureForm" label-width="120px" class="measure-form">
        <el-form-item label="措施名称" required><el-input v-model="measureForm.measureName" placeholder="请输入措施名称" style="width: 100%;" /></el-form-item>
        <el-form-item label="措施类型" required><el-select v-model="measureForm.type" placeholder="请选择措施类型" style="width: 100%;"><el-option v-for="type in measureTypes" :key="type.value" :label="type.label" :value="type.value" /></el-select></el-form-item>
        <el-form-item label="适用风险等级" required><el-select v-model="measureForm.riskLevel" placeholder="请选择适用风险等级" style="width: 100%;"><el-option label="高风险" value="high" /><el-option label="中风险" value="medium" /><el-option label="低风险" value="low" /></el-select></el-form-item>
        <el-form-item label="措施描述"><el-input v-model="measureForm.description" type="textarea" :rows="4" placeholder="请输入措施描述" style="width: 100%;" /></el-form-item>
        <el-form-item label="预计效果" required><el-slider v-model="measureForm.effectiveness" :min="0" :max="100" :step="5" show-input /></el-form-item>
        <el-form-item label="实施成本"><el-select v-model="measureForm.cost" placeholder="请选择实施成本" style="width: 100%;"><el-option label="低" value="low" /><el-option label="中" value="medium" /><el-option label="高" value="high" /></el-select></el-form-item>
        <el-form-item label="实施周期"><el-select v-model="measureForm.period" placeholder="请选择实施周期" style="width: 100%;"><el-option label="短期" value="short" /><el-option label="中期" value="medium" /><el-option label="长期" value="long" /></el-select></el-form-item>
      </el-form>
      <template #footer><el-button @click="measureDialogVisible = false">取消</el-button><el-button type="primary" @click="handleSaveMeasure">保存</el-button></template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Refresh, Search, Edit, Delete } from '@element-plus/icons-vue'

export default {
  name: 'ResponseMeasures',
  components: { Plus, Refresh, Search, Edit, Delete },
  setup() {
    const loading = ref(false)
    const measureDialogVisible = ref(false)
    const measureDialogTitle = ref('新增措施')
    
    // 措施类型
    const measureTypes = [
      { label: '供应链调整', value: 'supply_chain' },
      { label: '库存管理', value: 'inventory' },
      { label: '供应商管理', value: 'supplier' },
      { label: '价格策略', value: 'price' },
      { label: '物流优化', value: 'logistics' },
      { label: '风险管理', value: 'risk_management' }
    ]
    
    // 搜索和分页
    const searchForm = reactive({ name: '', type: '', riskLevel: '' })
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(80)
    
    // 措施列表
    const measureList = ref([
      { measureId: 'MEAS001', measureName: '增加安全库存', type: 'inventory', riskLevel: 'high', description: '针对核心芯片等关键物料，增加30%的安全库存', effectiveness: 85, cost: 'medium', period: 'short', createTime: '2026-04-01 10:00:00' },
      { measureId: 'MEAS002', measureName: '寻找替代供应商', type: 'supplier', riskLevel: 'high', description: '积极寻找芯片和原材料的替代供应商，降低单一供应商依赖', effectiveness: 90, cost: 'high', period: 'medium', createTime: '2026-03-15 14:00:00' },
      { measureId: 'MEAS003', measureName: '优化供应链网络', type: 'supply_chain', riskLevel: 'medium', description: '重新评估供应链网络，考虑区域化采购策略', effectiveness: 75, cost: 'high', period: 'long', createTime: '2026-03-01 09:00:00' },
      { measureId: 'MEAS004', measureName: '建立价格波动预警机制', type: 'price', riskLevel: 'medium', description: '建立原材料价格波动预警机制，及时调整采购策略', effectiveness: 70, cost: 'low', period: 'short', createTime: '2026-02-20 16:00:00' },
      { measureId: 'MEAS005', measureName: '优化物流路线', type: 'logistics', riskLevel: 'low', description: '优化物流路线，减少运输时间和成本', effectiveness: 65, cost: 'medium', period: 'medium', createTime: '2026-02-10 11:00:00' },
      { measureId: 'MEAS006', measureName: '与供应商签订长期合同', type: 'supplier', riskLevel: 'medium', description: '与关键供应商签订长期合同，锁定价格和供应量', effectiveness: 80, cost: 'medium', period: 'long', createTime: '2026-01-20 10:00:00' },
      { measureId: 'MEAS007', measureName: '实施供应商评估体系', type: 'supplier', riskLevel: 'low', description: '建立供应商评估体系，定期评估供应商表现', effectiveness: 60, cost: 'low', period: 'medium', createTime: '2026-01-10 09:00:00' },
      { measureId: 'MEAS008', measureName: '增加多元化采购渠道', type: 'supply_chain', riskLevel: 'high', description: '拓展采购渠道，减少对单一市场的依赖', effectiveness: 85, cost: 'medium', period: 'medium', createTime: '2025-12-20 14:00:00' }
    ])
    
    // 措施表单
    const measureForm = reactive({
      measureName: '',
      type: '',
      riskLevel: '',
      description: '',
      effectiveness: 0,
      cost: 'medium',
      period: 'medium'
    })
    
    const handleAddMeasure = () => {
      measureDialogTitle.value = '新增措施'
      Object.keys(measureForm).forEach(key => {
        measureForm[key] = key === 'cost' || key === 'period' ? 'medium' : ''
      })
      measureForm.effectiveness = 0
      measureDialogVisible.value = true
    }
    
    const handleEditMeasure = (measure) => {
      measureDialogTitle.value = '编辑措施'
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
      ElMessage.success('保存成功')
      measureDialogVisible.value = false
    }
    
    const handleDeleteMeasure = (measure) => {
      ElMessage.confirm('确定要删除此措施吗？', '删除措施', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'danger'
      }).then(() => {
        const index = measureList.value.findIndex(item => item.measureId === measure.measureId)
        if (index !== -1) {
          measureList.value.splice(index, 1)
          ElMessage.success('删除成功')
        }
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
      const typeObj = measureTypes.find(t => t.value === type)
      return typeObj ? typeObj.label : type
    }
    
    const getRiskLevelName = (level) => {
      switch (level) {
        case 'high': return '高风险'
        case 'medium': return '中风险'
        case 'low': return '低风险'
        default: return level
      }
    }
    
    const getEffectivenessColor = (value) => {
      if (value >= 80) return '#67c23a'
      if (value >= 60) return '#e6a23c'
      return '#f56c6c'
    }
    
    onMounted(() => {
      console.log('应对措施库页面加载')
    })
    
    return {
      loading, measureDialogVisible, measureDialogTitle, measureTypes,
      searchForm, pagination, total, measureList, measureForm,
      handleAddMeasure, handleEditMeasure, handleSaveMeasure, handleDeleteMeasure,
      handleRefresh, handleSearch, resetForm, handleSizeChange, handleCurrentChange,
      getTypeName, getRiskLevelName, getEffectivenessColor
    }
  }
}
</script>

<style scoped>
.response-measures {
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
</style>
