<template>
  <div class="task-orders">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>任务工单管理</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleCreateTask"><el-icon><Plus /></el-icon>创建任务</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 搜索和筛选 -->
        <div class="search-container">
          <el-form :inline="true" :model="searchForm" class="search-form">
            <el-form-item label="任务ID"><el-input v-model="searchForm.taskId" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="任务名称"><el-input v-model="searchForm.taskName" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="状态"><el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 120px;"><el-option label="待分配" value="pending" /><el-option label="已分配" value="assigned" /><el-option label="执行中" value="executing" /><el-option label="已完成" value="completed" /><el-option label="已验收" value="accepted" /></el-select></el-form-item>
            <el-form-item><el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
          </el-form>
        </div>
        
        <!-- 任务列表 -->
        <el-table :data="taskList" style="width: 100%" border stripe>
          <el-table-column prop="taskId" label="任务ID" width="120" />
          <el-table-column prop="taskName" label="任务名称" min-width="200" show-overflow-tooltip />
          <el-table-column prop="riskId" label="关联风险ID" width="120" />
          <el-table-column prop="assignee" label="负责人" width="120" />
          <el-table-column prop="deadline" label="截止时间" width="180" />
          <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="getStatusColor(scope.row.status)">{{ getStatusName(scope.row.status) }}</el-tag></template></el-table-column>
          <el-table-column prop="createTime" label="创建时间" width="180" />
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="scope">
              <el-button v-if="scope.row.status === 'pending'" type="primary" size="small" @click="handleAssignTask(scope.row)"><el-icon><UserFilled /></el-icon>分配</el-button>
              <el-button v-else-if="scope.row.status === 'assigned'" type="success" size="small" @click="handleStartTask(scope.row)"><el-icon><VideoPlay /></el-icon>开始</el-button>
              <el-button v-else-if="scope.row.status === 'executing'" type="warning" size="small" @click="handleCompleteTask(scope.row)"><el-icon><Check /></el-icon>完成</el-button>
              <el-button v-else-if="scope.row.status === 'completed'" type="info" size="small" @click="handleAcceptTask(scope.row)"><el-icon><Check /></el-icon>验收</el-button>
              <el-button type="primary" size="small" @click="handleViewTask(scope.row)"><el-icon><View /></el-icon>查看</el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination-wrapper"><el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" /></div>
      </div>
    </el-card>
    
    <!-- 创建任务对话框 -->
    <el-dialog v-model="taskDialogVisible" :title="taskDialogTitle" width="600px">
      <el-form :model="taskForm" label-width="120px" class="task-form">
        <el-form-item label="任务名称" required><el-input v-model="taskForm.taskName" placeholder="请输入任务名称" style="width: 100%;" /></el-form-item>
        <el-form-item label="关联风险ID" required><el-input v-model="taskForm.riskId" placeholder="请输入关联风险ID" style="width: 100%;" /></el-form-item>
        <el-form-item label="任务描述"><el-input v-model="taskForm.description" type="textarea" :rows="4" placeholder="请输入任务描述" style="width: 100%;" /></el-form-item>
        <el-form-item label="截止时间" required><el-date-picker v-model="taskForm.deadline" type="datetime" placeholder="选择截止时间" style="width: 100%;" /></el-form-item>
        <el-form-item label="优先级"><el-select v-model="taskForm.priority" placeholder="请选择优先级" style="width: 100%;"><el-option label="高" value="high" /><el-option label="中" value="medium" /><el-option label="低" value="low" /></el-select></el-form-item>
      </el-form>
      <template #footer><el-button @click="taskDialogVisible = false">取消</el-button><el-button type="primary" @click="handleSaveTask">保存</el-button></template>
    </el-dialog>
    
    <!-- 分配任务对话框 -->
    <el-dialog v-model="assignDialogVisible" :title="'分配任务 - ' + (currentTask?.taskId || '')" width="600px">
      <div v-if="currentTask" class="assign-dialog">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="任务ID">{{ currentTask.taskId }}</el-descriptions-item>
          <el-descriptions-item label="任务名称">{{ currentTask.taskName }}</el-descriptions-item>
          <el-descriptions-item label="关联风险ID">{{ currentTask.riskId }}</el-descriptions-item>
          <el-descriptions-item label="任务描述">{{ currentTask.description }}</el-descriptions-item>
          <el-descriptions-item label="截止时间">{{ currentTask.deadline }}</el-descriptions-item>
        </el-descriptions>
        <el-form :model="assignForm" label-width="120px" class="assign-form" style="margin-top: 20px;">
          <el-form-item label="负责人" required><el-select v-model="assignForm.assignee" placeholder="请选择负责人" style="width: 100%;"><el-option v-for="user in users" :key="user.id" :label="user.name" :value="user.id" /></el-select></el-form-item>
          <el-form-item label="分配说明"><el-input v-model="assignForm.remark" type="textarea" :rows="3" placeholder="请输入分配说明" style="width: 100%;" /></el-form-item>
        </el-form>
      </div>
      <template #footer><el-button @click="assignDialogVisible = false">取消</el-button><el-button type="primary" @click="handleSubmitAssign">提交分配</el-button></template>
    </el-dialog>
    
    <!-- 任务详情对话框 -->
    <el-dialog v-model="detailDialogVisible" :title="'任务详情 - ' + (currentTask?.taskId || '')" width="800px">
      <div v-if="currentTask" class="detail-dialog">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="任务ID">{{ currentTask.taskId }}</el-descriptions-item>
          <el-descriptions-item label="任务名称">{{ currentTask.taskName }}</el-descriptions-item>
          <el-descriptions-item label="关联风险ID">{{ currentTask.riskId }}</el-descriptions-item>
          <el-descriptions-item label="负责人">{{ currentTask.assignee }}</el-descriptions-item>
          <el-descriptions-item label="截止时间">{{ currentTask.deadline }}</el-descriptions-item>
          <el-descriptions-item label="优先级">{{ getPriorityName(currentTask.priority) }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ getStatusName(currentTask.status) }}</el-descriptions-item>
          <el-descriptions-item label="任务描述">{{ currentTask.description }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentTask.createTime }}</el-descriptions-item>
          <el-descriptions-item label="完成时间">{{ currentTask.completeTime || '-' }}</el-descriptions-item>
          <el-descriptions-item label="验收时间">{{ currentTask.acceptTime || '-' }}</el-descriptions-item>
        </el-descriptions>
        <div class="task-progress" style="margin-top: 20px;">
          <h4>任务进度</h4>
          <el-timeline>
            <el-timeline-item v-for="(item, index) in currentTask.progress" :key="index" :timestamp="item.time" :type="item.type">
              {{ item.content }}
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>
      <template #footer><el-button @click="detailDialogVisible = false">关闭</el-button></template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Refresh, Search, UserFilled, VideoPlay, Check, View } from '@element-plus/icons-vue'

export default {
  name: 'TaskOrders',
  components: { Plus, Refresh, Search, UserFilled, VideoPlay, Check, View },
  setup() {
    const loading = ref(false)
    const taskDialogVisible = ref(false)
    const assignDialogVisible = ref(false)
    const detailDialogVisible = ref(false)
    const taskDialogTitle = ref('创建任务')
    const currentTask = ref(null)
    
    // 模拟用户数据
    const users = [
      { id: 'user001', name: '张三' },
      { id: 'user002', name: '李四' },
      { id: 'user003', name: '王五' },
      { id: 'user004', name: '赵六' },
      { id: 'user005', name: '钱七' }
    ]
    
    // 搜索和分页
    const searchForm = reactive({ taskId: '', taskName: '', status: '' })
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(100)
    
    // 任务列表
    const taskList = ref([
      { taskId: 'TASK001', taskName: '核心芯片供应风险应对', riskId: 'RISK001', assignee: '', deadline: '2026-04-15 18:00:00', status: 'pending', priority: 'high', createTime: '2026-04-09 10:00:00' },
      { taskId: 'TASK002', taskName: '原材料价格上涨应对', riskId: 'RISK002', assignee: '张三', deadline: '2026-04-12 18:00:00', status: 'assigned', priority: 'medium', createTime: '2026-04-08 14:00:00' },
      { taskId: 'TASK003', taskName: '地缘政治风险应对', riskId: 'RISK003', assignee: '李四', deadline: '2026-04-10 18:00:00', status: 'executing', priority: 'high', createTime: '2026-04-07 09:00:00' },
      { taskId: 'TASK004', taskName: '物流延迟风险应对', riskId: 'RISK004', assignee: '王五', deadline: '2026-04-08 18:00:00', status: 'completed', priority: 'medium', createTime: '2026-04-06 16:00:00' },
      { taskId: 'TASK005', taskName: '供应商财务风险应对', riskId: 'RISK005', assignee: '赵六', deadline: '2026-04-09 18:00:00', status: 'accepted', priority: 'high', createTime: '2026-04-05 11:00:00' }
    ])
    
    // 任务表单
    const taskForm = reactive({
      taskName: '',
      riskId: '',
      description: '',
      deadline: null,
      priority: 'medium'
    })
    
    // 分配表单
    const assignForm = reactive({
      assignee: '',
      remark: ''
    })
    
    // 模拟任务进度数据
    const mockTaskProgress = [
      { time: '2026-04-07 09:00:00', content: '任务创建', type: 'primary' },
      { time: '2026-04-07 10:00:00', content: '任务分配给李四', type: 'success' },
      { time: '2026-04-08 09:00:00', content: '任务开始执行', type: 'info' },
      { time: '2026-04-09 14:00:00', content: '任务执行中', type: 'warning' }
    ]
    
    const handleCreateTask = () => {
      taskDialogTitle.value = '创建任务'
      Object.keys(taskForm).forEach(key => {
        taskForm[key] = key === 'priority' ? 'medium' : ''
      })
      taskForm.deadline = null
      taskDialogVisible.value = true
    }
    
    const handleSaveTask = () => {
      if (!taskForm.taskName) {
        ElMessage.warning('请输入任务名称')
        return
      }
      if (!taskForm.riskId) {
        ElMessage.warning('请输入关联风险ID')
        return
      }
      if (!taskForm.deadline) {
        ElMessage.warning('请选择截止时间')
        return
      }
      ElMessage.success('任务创建成功')
      taskDialogVisible.value = false
      // 模拟添加新任务
      const newTask = {
        taskId: 'TASK' + new Date().getTime(),
        taskName: taskForm.taskName,
        riskId: taskForm.riskId,
        assignee: '',
        deadline: taskForm.deadline,
        status: 'pending',
        priority: taskForm.priority,
        createTime: new Date().toLocaleString()
      }
      taskList.value.unshift(newTask)
    }
    
    const handleAssignTask = (task) => {
      currentTask.value = task
      assignForm.assignee = ''
      assignForm.remark = ''
      assignDialogVisible.value = true
    }
    
    const handleSubmitAssign = () => {
      if (!assignForm.assignee) {
        ElMessage.warning('请选择负责人')
        return
      }
      currentTask.value.assignee = assignForm.assignee
      currentTask.value.status = 'assigned'
      ElMessage.success('任务分配成功')
      assignDialogVisible.value = false
    }
    
    const handleStartTask = (task) => {
      ElMessage.confirm('确定要开始执行此任务吗？', '开始任务', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        task.status = 'executing'
        ElMessage.success('任务已开始执行')
      })
    }
    
    const handleCompleteTask = (task) => {
      ElMessage.confirm('确定要标记此任务为完成吗？', '完成任务', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'success'
      }).then(() => {
        task.status = 'completed'
        task.completeTime = new Date().toLocaleString()
        ElMessage.success('任务已完成')
      })
    }
    
    const handleAcceptTask = (task) => {
      ElMessage.confirm('确定要验收此任务吗？', '验收任务', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }).then(() => {
        task.status = 'accepted'
        task.acceptTime = new Date().toLocaleString()
        ElMessage.success('任务已验收')
      })
    }
    
    const handleViewTask = (task) => {
      currentTask.value = { ...task, progress: mockTaskProgress }
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
    
    const getStatusName = (status) => {
      switch (status) {
        case 'pending': return '待分配'
        case 'assigned': return '已分配'
        case 'executing': return '执行中'
        case 'completed': return '已完成'
        case 'accepted': return '已验收'
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
        default: return 'info'
      }
    }
    
    const getPriorityName = (priority) => {
      switch (priority) {
        case 'high': return '高'
        case 'medium': return '中'
        case 'low': return '低'
        default: return priority
      }
    }
    
    onMounted(() => {
      console.log('任务工单管理页面加载')
    })
    
    return {
      loading, taskDialogVisible, assignDialogVisible, detailDialogVisible, taskDialogTitle, currentTask,
      users, searchForm, pagination, total, taskList, taskForm, assignForm,
      handleCreateTask, handleSaveTask, handleAssignTask, handleSubmitAssign,
      handleStartTask, handleCompleteTask, handleAcceptTask, handleViewTask,
      handleRefresh, handleSearch, resetForm, handleSizeChange, handleCurrentChange,
      getStatusName, getStatusColor, getPriorityName
    }
  }
}
</script>

<style scoped>
.task-orders {
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
.task-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.assign-dialog {
  padding: 10px;
}
.assign-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.detail-dialog {
  padding: 10px;
}
.task-progress {
  margin-top: 20px;
}
</style>
