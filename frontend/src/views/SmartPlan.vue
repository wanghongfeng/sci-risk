<template>
  <div class="smart-plan">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>智能方案推荐与审批</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleGeneratePlan"><el-icon><MagicStick /></el-icon>生成方案</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 标签页 -->
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="方案推荐" name="recommend" />
          <el-tab-pane label="方案审批" name="approval" />
          <el-tab-pane label="方案管理" name="manage" />
        </el-tabs>
        
        <!-- 方案推荐 -->
        <div v-if="activeTab === 'recommend'" class="tab-content">
          <el-card class="recommend-card">
            <template #header>
              <div class="card-header">
                <span>智能方案推荐</span>
              </div>
            </template>
            <el-form :model="recommendForm" label-width="120px" class="recommend-form">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="风险ID" required><el-input v-model="recommendForm.riskId" placeholder="请输入风险ID" style="width: 100%;" /></el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="风险等级" required><el-select v-model="recommendForm.riskLevel" placeholder="请选择风险等级" style="width: 100%;"><el-option label="高风险" value="high" /><el-option label="中风险" value="medium" /><el-option label="低风险" value="low" /></el-select></el-form-item>
                </el-col>
                <el-col :span="24">
                  <el-form-item label="风险描述"><el-input v-model="recommendForm.description" type="textarea" :rows="3" placeholder="请输入风险描述" style="width: 100%;" /></el-form-item>
                </el-col>
                <el-col :span="24">
                  <el-form-item label="推荐策略"><el-checkbox-group v-model="recommendForm.strategies"><el-checkbox label="成本优先" /><el-checkbox label="效果优先" /><el-checkbox label="时间优先" /><el-checkbox label="综合平衡" /></el-checkbox-group></el-form-item>
                </el-col>
              </el-row>
              <div class="form-actions" style="margin-top: 20px;"><el-button type="primary" @click="handleRecommend">生成推荐方案</el-button></div>
            </el-form>
          </el-card>
          
          <!-- 推荐结果 -->
          <div v-if="recommendResult" class="recommend-result" style="margin-top: 20px;">
            <el-card class="result-card">
              <template #header>
                <div class="card-header">
                  <span>推荐方案</span>
                </div>
              </template>
              <div class="result-content">
                <el-descriptions :column="1" border>
                  <el-descriptions-item label="方案名称">{{ recommendResult.planName }}</el-descriptions-item>
                  <el-descriptions-item label="推荐理由">{{ recommendResult.reason }}</el-descriptions-item>
                  <el-descriptions-item label="预计效果">{{ recommendResult.effectiveness }}%</el-descriptions-item>
                  <el-descriptions-item label="实施成本">{{ getCostName(recommendResult.cost) }}</el-descriptions-item>
                  <el-descriptions-item label="实施周期">{{ getPeriodName(recommendResult.period) }}</el-descriptions-item>
                </el-descriptions>
                <div class="measures-list" style="margin-top: 20px;">
                  <h4>包含措施</h4>
                  <el-table :data="recommendResult.measures" style="width: 100%" border>
                    <el-table-column prop="measureName" label="措施名称" min-width="200" />
                    <el-table-column prop="effectiveness" label="预计效果" width="100" align="right" />
                    <el-table-column prop="cost" label="实施成本" width="100"><template #default="scope">{{ getCostName(scope.row.cost) }}</template></el-table-column>
                  </el-table>
                </div>
                <div class="result-actions" style="margin-top: 20px;"><el-button type="primary" @click="handleSubmitApproval">提交审批</el-button></div>
              </div>
            </el-card>
          </div>
        </div>
        
        <!-- 方案审批 -->
        <div v-if="activeTab === 'approval'" class="tab-content">
          <div class="search-container">
            <el-form :inline="true" :model="approvalSearch" class="search-form">
              <el-form-item label="方案ID"><el-input v-model="approvalSearch.planId" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
              <el-form-item label="审批状态"><el-select v-model="approvalSearch.status" placeholder="请选择" clearable style="width: 120px;"><el-option label="待审批" value="pending" /><el-option label="审批中" value="processing" /><el-option label="已通过" value="approved" /><el-option label="已拒绝" value="rejected" /></el-select></el-form-item>
              <el-form-item><el-button type="primary" @click="handleApprovalSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetApprovalForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
            </el-form>
          </div>
          <el-table :data="approvalList" style="width: 100%" border stripe>
            <el-table-column prop="planId" label="方案ID" width="120" />
            <el-table-column prop="planName" label="方案名称" min-width="200" show-overflow-tooltip />
            <el-table-column prop="riskId" label="关联风险ID" width="120" />
            <el-table-column prop="submitter" label="提交人" width="120" />
            <el-table-column prop="submitTime" label="提交时间" width="180" />
            <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'pending' ? 'warning' : scope.row.status === 'processing' ? 'info' : scope.row.status === 'approved' ? 'success' : 'danger'"> {{ getApprovalStatusName(scope.row.status) }}</el-tag></template></el-table-column>
            <el-table-column label="操作" width="150" fixed="right"><template #default="scope"><el-button type="primary" size="small" @click="handleViewApproval(scope.row)"><el-icon><View /></el-icon>审批</el-button></template></el-table-column>
          </el-table>
          <div class="pagination-wrapper"><el-pagination v-model:current-page="approvalPagination.currentPage" v-model:page-size="approvalPagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="approvalTotal" @size-change="handleApprovalSizeChange" @current-change="handleApprovalCurrentChange" /></div>
        </div>
        
        <!-- 方案管理 -->
        <div v-if="activeTab === 'manage'" class="tab-content">
          <div class="search-container">
            <el-form :inline="true" :model="manageSearch" class="search-form">
              <el-form-item label="方案ID"><el-input v-model="manageSearch.planId" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
              <el-form-item label="方案名称"><el-input v-model="manageSearch.planName" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
              <el-form-item label="状态"><el-select v-model="manageSearch.status" placeholder="请选择" clearable style="width: 120px;"><el-option label="已通过" value="approved" /><el-option label="已拒绝" value="rejected" /><el-option label="已实施" value="implemented" /></el-select></el-form-item>
              <el-form-item><el-button type="primary" @click="handleManageSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetManageForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
            </el-form>
          </div>
          <el-table :data="manageList" style="width: 100%" border stripe>
            <el-table-column prop="planId" label="方案ID" width="120" />
            <el-table-column prop="planName" label="方案名称" min-width="200" show-overflow-tooltip />
            <el-table-column prop="riskId" label="关联风险ID" width="120" />
            <el-table-column prop="effectiveness" label="预计效果" width="100" align="right" />
            <el-table-column prop="cost" label="实施成本" width="100"><template #default="scope">{{ getCostName(scope.row.cost) }}</template></el-table-column>
            <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'approved' ? 'success' : scope.row.status === 'rejected' ? 'danger' : 'info'"> {{ getManageStatusName(scope.row.status) }}</el-tag></template></el-table-column>
            <el-table-column prop="createTime" label="创建时间" width="180" />
            <el-table-column label="操作" width="150" fixed="right"><template #default="scope"><el-button type="primary" size="small" @click="handleViewPlan(scope.row)"><el-icon><View /></el-icon>查看</el-button></template></el-table-column>
          </el-table>
          <div class="pagination-wrapper"><el-pagination v-model:current-page="managePagination.currentPage" v-model:page-size="managePagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="manageTotal" @size-change="handleManageSizeChange" @current-change="handleManageCurrentChange" /></div>
        </div>
      </div>
    </el-card>
    
    <!-- 审批对话框 -->
    <el-dialog v-model="approvalDialogVisible" :title="'审批方案 - ' + (currentApproval?.planId || '')" width="800px">
      <div v-if="currentApproval" class="approval-dialog">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="方案ID">{{ currentApproval.planId }}</el-descriptions-item>
          <el-descriptions-item label="方案名称">{{ currentApproval.planName }}</el-descriptions-item>
          <el-descriptions-item label="关联风险ID">{{ currentApproval.riskId }}</el-descriptions-item>
          <el-descriptions-item label="提交人">{{ currentApproval.submitter }}</el-descriptions-item>
          <el-descriptions-item label="提交时间">{{ currentApproval.submitTime }}</el-descriptions-item>
          <el-descriptions-item label="当前状态">{{ getApprovalStatusName(currentApproval.status) }}</el-descriptions-item>
        </el-descriptions>
        <el-form :model="approvalForm" label-width="120px" class="approval-form" style="margin-top: 20px;">
          <el-form-item label="审批意见" required><el-input v-model="approvalForm.remark" type="textarea" :rows="4" placeholder="请输入审批意见" style="width: 100%;" /></el-form-item>
          <el-form-item label="审批结果" required><el-select v-model="approvalForm.result" placeholder="请选择审批结果" style="width: 100%;"><el-option label="通过" value="approved" /><el-option label="拒绝" value="rejected" /></el-select></el-form-item>
        </el-form>
      </div>
      <template #footer><el-button @click="approvalDialogVisible = false">取消</el-button><el-button type="primary" @click="handleSubmitApprovalResult">提交审批</el-button></template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { MagicStick, Refresh, Search, View } from '@element-plus/icons-vue'

export default {
  name: 'SmartPlan',
  components: { MagicStick, Refresh, Search, View },
  setup() {
    const loading = ref(false)
    const activeTab = ref('recommend')
    const approvalDialogVisible = ref(false)
    const currentApproval = ref(null)
    
    // 推荐相关
    const recommendForm = reactive({
      riskId: '',
      riskLevel: '',
      description: '',
      strategies: ['综合平衡']
    })
    const recommendResult = ref(null)
    
    // 审批相关
    const approvalSearch = reactive({ planId: '', status: '' })
    const approvalPagination = reactive({ currentPage: 1, pageSize: 10 })
    const approvalTotal = ref(50)
    const approvalList = ref([
      { planId: 'PLAN001', planName: '核心芯片供应风险应对方案', riskId: 'RISK001', submitter: '张三', submitTime: '2026-04-09 10:00:00', status: 'pending' },
      { planId: 'PLAN002', planName: '原材料价格上涨应对方案', riskId: 'RISK002', submitter: '李四', submitTime: '2026-04-08 14:00:00', status: 'processing' },
      { planId: 'PLAN003', planName: '地缘政治风险应对方案', riskId: 'RISK003', submitter: '王五', submitTime: '2026-04-07 09:00:00', status: 'approved' },
      { planId: 'PLAN004', planName: '物流延迟风险应对方案', riskId: 'RISK004', submitter: '赵六', submitTime: '2026-04-06 16:00:00', status: 'rejected' }
    ])
    const approvalForm = reactive({ remark: '', result: 'approved' })
    
    // 管理相关
    const manageSearch = reactive({ planId: '', planName: '', status: '' })
    const managePagination = reactive({ currentPage: 1, pageSize: 10 })
    const manageTotal = ref(80)
    const manageList = ref([
      { planId: 'PLAN003', planName: '地缘政治风险应对方案', riskId: 'RISK003', effectiveness: 85, cost: 'medium', status: 'approved', createTime: '2026-04-07 09:00:00' },
      { planId: 'PLAN004', planName: '物流延迟风险应对方案', riskId: 'RISK004', effectiveness: 70, cost: 'low', status: 'rejected', createTime: '2026-04-06 16:00:00' },
      { planId: 'PLAN005', planName: '供应商财务风险应对方案', riskId: 'RISK005', effectiveness: 80, cost: 'medium', status: 'implemented', createTime: '2026-04-05 11:00:00' },
      { planId: 'PLAN006', planName: '市场需求波动应对方案', riskId: 'RISK006', effectiveness: 75, cost: 'low', status: 'approved', createTime: '2026-04-04 10:00:00' }
    ])
    
    const handleGeneratePlan = () => {
      ElMessage.info('生成方案功能开发中')
    }
    
    const handleRecommend = () => {
      if (!recommendForm.riskId) {
        ElMessage.warning('请输入风险ID')
        return
      }
      if (!recommendForm.riskLevel) {
        ElMessage.warning('请选择风险等级')
        return
      }
      loading.value = true
      setTimeout(() => {
        recommendResult.value = {
          planName: '核心芯片供应风险应对方案',
          reason: '基于风险等级和推荐策略，为您推荐以下方案',
          effectiveness: 85,
          cost: 'medium',
          period: 'medium',
          measures: [
            { measureName: '增加安全库存', effectiveness: 85, cost: 'medium' },
            { measureName: '寻找替代供应商', effectiveness: 90, cost: 'high' },
            { measureName: '与供应商签订长期合同', effectiveness: 80, cost: 'medium' }
          ]
        }
        ElMessage.success('推荐方案生成成功')
        loading.value = false
      }, 2000)
    }
    
    const handleSubmitApproval = () => {
      ElMessage.success('方案已提交审批')
      recommendResult.value = null
    }
    
    const handleViewApproval = (approval) => {
      currentApproval.value = approval
      approvalForm.remark = ''
      approvalForm.result = 'approved'
      approvalDialogVisible.value = true
    }
    
    const handleSubmitApprovalResult = () => {
      if (!approvalForm.remark) {
        ElMessage.warning('请输入审批意见')
        return
      }
      ElMessage.success('审批提交成功')
      approvalDialogVisible.value = false
    }
    
    const handleViewPlan = (plan) => {
      ElMessage.info('查看方案详情功能开发中')
    }
    
    const handleRefresh = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('刷新成功')
        loading.value = false
      }, 1000)
    }
    
    const handleTabChange = (tab) => {
      activeTab.value = tab
    }
    
    const getCostName = (cost) => {
      switch (cost) {
        case 'low': return '低'
        case 'medium': return '中'
        case 'high': return '高'
        default: return cost
      }
    }
    
    const getPeriodName = (period) => {
      switch (period) {
        case 'short': return '短期'
        case 'medium': return '中期'
        case 'long': return '长期'
        default: return period
      }
    }
    
    const getApprovalStatusName = (status) => {
      switch (status) {
        case 'pending': return '待审批'
        case 'processing': return '审批中'
        case 'approved': return '已通过'
        case 'rejected': return '已拒绝'
        default: return status
      }
    }
    
    const getManageStatusName = (status) => {
      switch (status) {
        case 'approved': return '已通过'
        case 'rejected': return '已拒绝'
        case 'implemented': return '已实施'
        default: return status
      }
    }
    
    const handleApprovalSearch = () => {
      ElMessage.info('搜索功能开发中')
    }
    
    const resetApprovalForm = () => {
      Object.keys(approvalSearch).forEach(key => {
        approvalSearch[key] = ''
      })
    }
    
    const handleApprovalSizeChange = (size) => {
      approvalPagination.pageSize = size
    }
    
    const handleApprovalCurrentChange = (current) => {
      approvalPagination.currentPage = current
    }
    
    const handleManageSearch = () => {
      ElMessage.info('搜索功能开发中')
    }
    
    const resetManageForm = () => {
      Object.keys(manageSearch).forEach(key => {
        manageSearch[key] = ''
      })
    }
    
    const handleManageSizeChange = (size) => {
      managePagination.pageSize = size
    }
    
    const handleManageCurrentChange = (current) => {
      managePagination.currentPage = current
    }
    
    onMounted(() => {
      console.log('智能方案推荐与审批页面加载')
    })
    
    return {
      loading, activeTab, approvalDialogVisible, currentApproval,
      recommendForm, recommendResult,
      approvalSearch, approvalPagination, approvalTotal, approvalList, approvalForm,
      manageSearch, managePagination, manageTotal, manageList,
      handleGeneratePlan, handleRecommend, handleSubmitApproval,
      handleViewApproval, handleSubmitApprovalResult, handleViewPlan,
      handleRefresh, handleTabChange, getCostName, getPeriodName,
      getApprovalStatusName, getManageStatusName,
      handleApprovalSearch, resetApprovalForm, handleApprovalSizeChange, handleApprovalCurrentChange,
      handleManageSearch, resetManageForm, handleManageSizeChange, handleManageCurrentChange
    }
  }
}
</script>

<style scoped>
.smart-plan {
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
.tab-content {
  margin-top: 20px;
}
.recommend-card {
  margin-bottom: 20px;
}
.recommend-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.form-actions {
  display: flex;
  justify-content: center;
}
.result-card {
  margin-top: 20px;
}
.result-content {
  padding: 10px;
}
.measures-list {
  margin-top: 20px;
}
.result-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
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
.approval-dialog {
  padding: 10px;
}
.approval-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
</style>
