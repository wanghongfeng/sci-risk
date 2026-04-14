<template>
  <div class="risk-review">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>风险事件复盘</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleCreateReview"><el-icon><Plus /></el-icon>创建复盘</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 搜索和筛选 -->
        <div class="search-container">
          <el-form :inline="true" :model="searchForm" class="search-form">
            <el-form-item label="复盘ID"><el-input v-model="searchForm.reviewId" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="风险事件"><el-input v-model="searchForm.eventName" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="状态"><el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 120px;"><el-option label="待复盘" value="pending" /><el-option label="进行中" value="in_progress" /><el-option label="已完成" value="completed" /></el-select></el-form-item>
            <el-form-item><el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
          </el-form>
        </div>
        
        <!-- 复盘列表 -->
        <el-table :data="reviewList" style="width: 100%" border stripe>
          <el-table-column prop="reviewId" label="复盘ID" width="120" />
          <el-table-column prop="eventName" label="风险事件" min-width="200" show-overflow-tooltip />
          <el-table-column prop="riskId" label="风险ID" width="120" />
          <el-table-column prop="reviewer" label="复盘人" width="120" />
          <el-table-column prop="startTime" label="开始时间" width="180" />
          <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="getStatusColor(scope.row.status)">{{ getStatusName(scope.row.status) }}</el-tag></template></el-table-column>
          <el-table-column prop="completionRate" label="完成率" width="120"><template #default="scope"><el-progress :percentage="scope.row.completionRate" :stroke-width="10" /></template></el-table-column>
          <el-table-column label="操作" width="150" fixed="right"><template #default="scope"><el-button type="primary" size="small" @click="handleViewReview(scope.row)"><el-icon><View /></el-icon>查看</el-button></template></el-table-column>
        </el-table>
        <div class="pagination-wrapper"><el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" /></div>
      </div>
    </el-card>
    
    <!-- 创建复盘对话框 -->
    <el-dialog v-model="reviewDialogVisible" :title="reviewDialogTitle" width="600px">
      <el-form :model="reviewForm" label-width="120px" class="review-form">
        <el-form-item label="风险事件" required><el-input v-model="reviewForm.eventName" placeholder="请输入风险事件名称" style="width: 100%;" /></el-form-item>
        <el-form-item label="风险ID" required><el-input v-model="reviewForm.riskId" placeholder="请输入风险ID" style="width: 100%;" /></el-form-item>
        <el-form-item label="复盘人" required><el-input v-model="reviewForm.reviewer" placeholder="请输入复盘人" style="width: 100%;" /></el-form-item>
        <el-form-item label="复盘目标"><el-input v-model="reviewForm.objective" type="textarea" :rows="3" placeholder="请输入复盘目标" style="width: 100%;" /></el-form-item>
        <el-form-item label="预计完成时间"><el-date-picker v-model="reviewForm.expectedEndTime" type="datetime" placeholder="选择预计完成时间" style="width: 100%;" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="reviewDialogVisible = false">取消</el-button><el-button type="primary" @click="handleSaveReview">保存</el-button></template>
    </el-dialog>
    
    <!-- 复盘详情对话框 -->
    <el-dialog v-model="detailDialogVisible" :title="'复盘详情 - ' + (currentReview?.reviewId || '')" width="800px">
      <div v-if="currentReview" class="detail-dialog">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="复盘ID">{{ currentReview.reviewId }}</el-descriptions-item>
          <el-descriptions-item label="风险事件">{{ currentReview.eventName }}</el-descriptions-item>
          <el-descriptions-item label="风险ID">{{ currentReview.riskId }}</el-descriptions-item>
          <el-descriptions-item label="复盘人">{{ currentReview.reviewer }}</el-descriptions-item>
          <el-descriptions-item label="开始时间">{{ currentReview.startTime }}</el-descriptions-item>
          <el-descriptions-item label="完成时间">{{ currentReview.completeTime || '-' }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ getStatusName(currentReview.status) }}</el-descriptions-item>
          <el-descriptions-item label="复盘目标">{{ currentReview.objective }}</el-descriptions-item>
        </el-descriptions>
        
        <!-- 复盘内容 -->
        <div class="review-content" style="margin-top: 20px;">
          <h4>复盘内容</h4>
          <el-steps :active="currentStep" finish-status="success" align-center>
            <el-step title="事件回顾" description="回顾风险事件的发生过程" />
            <el-step title="原因分析" description="分析风险事件的根本原因" />
            <el-step title="应对措施评估" description="评估已采取的应对措施" />
            <el-step title="改进建议" description="提出改进建议" />
            <el-step title="总结" description="总结复盘结果" />
          </el-steps>
          
          <div class="step-content" style="margin-top: 20px;">
            <div v-if="currentStep === 0" class="step-item">
              <el-form :model="reviewSteps.eventReview" label-width="120px">
                <el-form-item label="事件描述"><el-input type="textarea" v-model="reviewSteps.eventReview.description" :rows="4" style="width: 100%;" /></el-form-item>
                <el-form-item label="发生时间"><el-date-picker type="datetime" v-model="reviewSteps.eventReview.occurTime" style="width: 100%;" /></el-form-item>
                <el-form-item label="影响范围"><el-input v-model="reviewSteps.eventReview.impactScope" style="width: 100%;" /></el-form-item>
              </el-form>
            </div>
            <div v-else-if="currentStep === 1" class="step-item">
              <el-form :model="reviewSteps.rootCause" label-width="120px">
                <el-form-item label="根本原因"><el-input type="textarea" v-model="reviewSteps.rootCause.analysis" :rows="4" style="width: 100%;" /></el-form-item>
                <el-form-item label="原因类型"><el-select v-model="reviewSteps.rootCause.type" style="width: 100%;"><el-option label="内部原因" value="internal" /><el-option label="外部原因" value="external" /><el-option label="系统性原因" value="systematic" /></el-select></el-form-item>
              </el-form>
            </div>
            <div v-else-if="currentStep === 2" class="step-item">
              <el-form :model="reviewSteps.measureEvaluation" label-width="120px">
                <el-form-item label="采取的措施"><el-input type="textarea" v-model="reviewSteps.measureEvaluation.measures" :rows="4" style="width: 100%;" /></el-form-item>
                <el-form-item label="措施效果"><el-input type="textarea" v-model="reviewSteps.measureEvaluation.effectiveness" :rows="4" style="width: 100%;" /></el-form-item>
                <el-form-item label="改进空间"><el-input type="textarea" v-model="reviewSteps.measureEvaluation.improvement" :rows="4" style="width: 100%;" /></el-form-item>
              </el-form>
            </div>
            <div v-else-if="currentStep === 3" class="step-item">
              <el-form :model="reviewSteps.improvementSuggestions" label-width="120px">
                <el-form-item label="改进建议"><el-input type="textarea" v-model="reviewSteps.improvementSuggestions.suggestions" :rows="4" style="width: 100%;" /></el-form-item>
                <el-form-item label="责任部门"><el-select v-model="reviewSteps.improvementSuggestions.department" style="width: 100%;"><el-option label="采购部" value="procurement" /><el-option label="生产部" value="production" /><el-option label="物流部" value="logistics" /><el-option label="质量部" value="quality" /></el-select></el-form-item>
                <el-form-item label="建议完成时间"><el-date-picker type="datetime" v-model="reviewSteps.improvementSuggestions.deadline" style="width: 100%;" /></el-form-item>
              </el-form>
            </div>
            <div v-else-if="currentStep === 4" class="step-item">
              <el-form :model="reviewSteps.summary" label-width="120px">
                <el-form-item label="复盘总结"><el-input type="textarea" v-model="reviewSteps.summary.content" :rows="4" style="width: 100%;" /></el-form-item>
                <el-form-item label="经验教训"><el-input type="textarea" v-model="reviewSteps.summary.lessons" :rows="4" style="width: 100%;" /></el-form-item>
                <el-form-item label="后续行动计划"><el-input type="textarea" v-model="reviewSteps.summary.actionPlan" :rows="4" style="width: 100%;" /></el-form-item>
              </el-form>
            </div>
          </div>
          
          <div class="step-actions" style="margin-top: 20px; display: flex; justify-content: space-between;">
            <el-button v-if="currentStep > 0" @click="currentStep--">上一步</el-button>
            <div>
              <el-button v-if="currentStep < 4" @click="currentStep++">下一步</el-button>
              <el-button v-else type="primary" @click="handleCompleteReview">完成复盘</el-button>
            </div>
          </div>
        </div>
      </div>
      <template #footer><el-button @click="detailDialogVisible = false">关闭</el-button></template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Refresh, Search, View } from '@element-plus/icons-vue'

export default {
  name: 'RiskReview',
  components: { Plus, Refresh, Search, View },
  setup() {
    const loading = ref(false)
    const reviewDialogVisible = ref(false)
    const detailDialogVisible = ref(false)
    const reviewDialogTitle = ref('创建复盘')
    const currentReview = ref(null)
    const currentStep = ref(0)
    
    // 搜索和分页
    const searchForm = reactive({ reviewId: '', eventName: '', status: '' })
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(60)
    
    // 复盘列表
    const reviewList = ref([
      { reviewId: 'REVIEW001', eventName: '核心芯片供应中断', riskId: 'RISK001', reviewer: '张三', startTime: '2026-04-09 10:00:00', status: 'in_progress', completionRate: 60 },
      { reviewId: 'REVIEW002', eventName: '原材料价格大幅上涨', riskId: 'RISK002', reviewer: '李四', startTime: '2026-04-08 14:00:00', status: 'completed', completionRate: 100 },
      { reviewId: 'REVIEW003', eventName: '地缘政治冲突影响', riskId: 'RISK003', reviewer: '王五', startTime: '2026-04-07 09:00:00', status: 'pending', completionRate: 0 },
      { reviewId: 'REVIEW004', eventName: '物流运输延迟', riskId: 'RISK004', reviewer: '赵六', startTime: '2026-04-06 16:00:00', status: 'in_progress', completionRate: 40 }
    ])
    
    // 复盘表单
    const reviewForm = reactive({
      eventName: '',
      riskId: '',
      reviewer: '',
      objective: '',
      expectedEndTime: null
    })
    
    // 复盘步骤
    const reviewSteps = reactive({
      eventReview: {
        description: '',
        occurTime: null,
        impactScope: ''
      },
      rootCause: {
        analysis: '',
        type: ''
      },
      measureEvaluation: {
        measures: '',
        effectiveness: '',
        improvement: ''
      },
      improvementSuggestions: {
        suggestions: '',
        department: '',
        deadline: null
      },
      summary: {
        content: '',
        lessons: '',
        actionPlan: ''
      }
    })
    
    const handleCreateReview = () => {
      reviewDialogTitle.value = '创建复盘'
      Object.keys(reviewForm).forEach(key => {
        reviewForm[key] = ''
      })
      reviewForm.expectedEndTime = null
      reviewDialogVisible.value = true
    }
    
    const handleSaveReview = () => {
      if (!reviewForm.eventName) {
        ElMessage.warning('请输入风险事件名称')
        return
      }
      if (!reviewForm.riskId) {
        ElMessage.warning('请输入风险ID')
        return
      }
      if (!reviewForm.reviewer) {
        ElMessage.warning('请输入复盘人')
        return
      }
      ElMessage.success('复盘创建成功')
      reviewDialogVisible.value = false
      // 模拟添加新复盘
      const newReview = {
        reviewId: 'REVIEW' + new Date().getTime(),
        eventName: reviewForm.eventName,
        riskId: reviewForm.riskId,
        reviewer: reviewForm.reviewer,
        startTime: new Date().toLocaleString(),
        status: 'pending',
        completionRate: 0
      }
      reviewList.value.unshift(newReview)
    }
    
    const handleViewReview = (review) => {
      currentReview.value = review
      currentStep.value = 0
      // 重置复盘步骤
      Object.keys(reviewSteps).forEach(key => {
        Object.keys(reviewSteps[key]).forEach(subKey => {
          reviewSteps[key][subKey] = ''
        })
      })
      detailDialogVisible.value = true
    }
    
    const handleCompleteReview = () => {
      ElMessage.success('复盘完成')
      currentReview.value.status = 'completed'
      currentReview.value.completionRate = 100
      currentReview.value.completeTime = new Date().toLocaleString()
      detailDialogVisible.value = false
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
    
    const getStatusName = (status) => {
      switch (status) {
        case 'pending': return '待复盘'
        case 'in_progress': return '进行中'
        case 'completed': return '已完成'
        default: return status
      }
    }
    
    const getStatusColor = (status) => {
      switch (status) {
        case 'pending': return 'warning'
        case 'in_progress': return 'primary'
        case 'completed': return 'success'
        default: return 'info'
      }
    }
    
    onMounted(() => {
      console.log('风险事件复盘页面加载')
    })
    
    return {
      loading, reviewDialogVisible, detailDialogVisible, reviewDialogTitle, currentReview, currentStep,
      searchForm, pagination, total, reviewList, reviewForm, reviewSteps,
      handleCreateReview, handleSaveReview, handleViewReview, handleCompleteReview,
      handleRefresh, handleSearch, resetForm, handleSizeChange, handleCurrentChange,
      getStatusName, getStatusColor
    }
  }
}
</script>

<style scoped>
.risk-review {
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
.review-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.detail-dialog {
  padding: 10px;
}
.review-content {
  margin-top: 20px;
}
.step-content {
  margin-top: 20px;
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.step-item {
  min-height: 300px;
}
.step-actions {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}
</style>