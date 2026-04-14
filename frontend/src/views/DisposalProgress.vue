<template>
  <div class="disposal-progress">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>处置进度大屏</span>
          <div class="header-actions">
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
            <el-select v-model="timeRange" size="small" style="margin-left: 10px;"><el-option label="今日" value="today" /><el-option label="本周" value="week" /><el-option label="本月" value="month" /><el-option label="全部" value="all" /></el-select>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 统计卡片 -->
        <div class="stats-container">
          <el-row :gutter="20">
            <el-col :span="6"><el-card class="stat-card primary"><div class="stat-icon"><el-icon><InfoFilled /></el-icon></div><div class="stat-info"><div class="stat-value">{{ stats.totalTasks }}</div><div class="stat-label">总任务数</div></div></el-card></el-col>
            <el-col :span="6"><el-card class="stat-card success"><div class="stat-icon"><el-icon><Check /></el-icon></div><div class="stat-info"><div class="stat-value">{{ stats.completedTasks }}</div><div class="stat-label">已完成</div></div></el-card></el-col>
            <el-col :span="6"><el-card class="stat-card warning"><div class="stat-icon"><el-icon><Clock /></el-icon></div><div class="stat-info"><div class="stat-value">{{ stats.inProgressTasks }}</div><div class="stat-label">进行中</div></div></el-card></el-col>
            <el-col :span="6"><el-card class="stat-card danger"><div class="stat-icon"><el-icon><Warning /></el-icon></div><div class="stat-info"><div class="stat-value">{{ stats.overdueTasks }}</div><div class="stat-label">逾期</div></div></el-card></el-col>
          </el-row>
        </div>
        
        <!-- 图表区域 -->
        <div class="charts-container">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card class="chart-card">
                <template #header><span>任务状态分布</span></template>
                <div class="chart-content">
                  <div class="chart-placeholder">
                    <el-empty description="任务状态分布图表" />
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card class="chart-card">
                <template #header><span>部门任务完成率</span></template>
                <div class="chart-content">
                  <div class="chart-placeholder">
                    <el-empty description="部门任务完成率图表" />
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
        
        <!-- 任务列表 -->
        <div class="tasks-container">
          <el-card class="tasks-card">
            <template #header><span>任务进度明细</span></template>
            <el-table :data="taskList" style="width: 100%" border stripe>
              <el-table-column prop="taskId" label="任务ID" width="120" />
              <el-table-column prop="taskName" label="任务名称" min-width="200" show-overflow-tooltip />
              <el-table-column prop="riskId" label="关联风险ID" width="120" />
              <el-table-column prop="assignee" label="负责人" width="120" />
              <el-table-column prop="department" label="部门" width="120" />
              <el-table-column prop="deadline" label="截止时间" width="180" />
              <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="getStatusColor(scope.row.status)">{{ getStatusName(scope.row.status) }}</el-tag></template></el-table-column>
              <el-table-column prop="progress" label="进度" width="120"><template #default="scope"><el-progress :percentage="scope.row.progress" :stroke-width="10" /></template></el-table-column>
            </el-table>
          </el-card>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, InfoFilled, Check, Clock, Warning } from '@element-plus/icons-vue'

export default {
  name: 'DisposalProgress',
  components: { Refresh, InfoFilled, Check, Clock, Warning },
  setup() {
    const loading = ref(false)
    const timeRange = ref('today')
    
    // 统计数据
    const stats = reactive({
      totalTasks: 120,
      completedTasks: 85,
      inProgressTasks: 25,
      overdueTasks: 10
    })
    
    // 任务列表
    const taskList = ref([
      { taskId: 'TASK001', taskName: '核心芯片供应风险应对', riskId: 'RISK001', assignee: '张三', department: '采购部', deadline: '2026-04-15 18:00:00', status: 'executing', progress: 75 },
      { taskId: 'TASK002', taskName: '原材料价格上涨应对', riskId: 'RISK002', assignee: '李四', department: '采购部', deadline: '2026-04-12 18:00:00', status: 'assigned', progress: 0 },
      { taskId: 'TASK003', taskName: '地缘政治风险应对', riskId: 'RISK003', assignee: '王五', department: '物流部', deadline: '2026-04-10 18:00:00', status: 'executing', progress: 60 },
      { taskId: 'TASK004', taskName: '物流延迟风险应对', riskId: 'RISK004', assignee: '赵六', department: '物流部', deadline: '2026-04-08 18:00:00', status: 'completed', progress: 100 },
      { taskId: 'TASK005', taskName: '供应商财务风险应对', riskId: 'RISK005', assignee: '钱七', department: '财务部', deadline: '2026-04-09 18:00:00', status: 'accepted', progress: 100 },
      { taskId: 'TASK006', taskName: '市场需求波动应对', riskId: 'RISK006', assignee: '孙八', department: '市场部', deadline: '2026-04-11 18:00:00', status: 'executing', progress: 40 },
      { taskId: 'TASK007', taskName: '质量风险应对', riskId: 'RISK007', assignee: '周九', department: '质量部', deadline: '2026-04-13 18:00:00', status: 'pending', progress: 0 },
      { taskId: 'TASK008', taskName: '生产计划调整', riskId: 'RISK008', assignee: '吴十', department: '生产部', deadline: '2026-04-07 18:00:00', status: 'overdue', progress: 30 }
    ])
    
    const handleRefresh = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('刷新成功')
        loading.value = false
      }, 1000)
    }
    
    const getStatusName = (status) => {
      switch (status) {
        case 'pending': return '待分配'
        case 'assigned': return '已分配'
        case 'executing': return '执行中'
        case 'completed': return '已完成'
        case 'accepted': return '已验收'
        case 'overdue': return '逾期'
        default: return status
      }
    }
    
    const getStatusColor = (status) => {
      switch (status) {
        case 'pending': return 'warning'
        case 'assigned': return 'info'
        case 'executing': return 'primary'
        case 'completed': return 'success'
        case 'accepted': return 'success'
        case 'overdue': return 'danger'
        default: return 'info'
      }
    }
    
    onMounted(() => {
      console.log('处置进度大屏页面加载')
    })
    
    return {
      loading, timeRange, stats, taskList,
      handleRefresh, getStatusName, getStatusColor
    }
  }
}
</script>

<style scoped>
.disposal-progress {
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
  align-items: center;
  gap: 10px;
}
.stats-container {
  margin-bottom: 20px;
}
.stat-card {
  height: 120px;
  display: flex;
  align-items: center;
  padding: 20px;
}
.stat-icon {
  font-size: 32px;
  margin-right: 20px;
  color: white;
}
.stat-info {
  flex: 1;
}
.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: white;
}
.stat-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 5px;
}
.stat-card.primary {
  background: linear-gradient(135deg, #409EFF, #66B1FF);
}
.stat-card.success {
  background: linear-gradient(135deg, #67C23A, #85CE61);
}
.stat-card.warning {
  background: linear-gradient(135deg, #E6A23C, #F56C6C);
}
.stat-card.danger {
  background: linear-gradient(135deg, #F56C6C, #F78989);
}
.charts-container {
  margin-bottom: 20px;
}
.chart-card {
  height: 300px;
}
.chart-content {
  height: calc(100% - 40px);
  display: flex;
  align-items: center;
  justify-content: center;
}
.chart-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.tasks-container {
  margin-bottom: 20px;
}
.tasks-card {
  min-height: 400px;
}
</style>