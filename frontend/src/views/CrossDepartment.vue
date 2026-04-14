<template>
  <div class="cross-department">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>跨部门协同跟踪</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleCreateCollaboration"><el-icon><Plus /></el-icon>创建协同</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 搜索和筛选 -->
        <div class="search-container">
          <el-form :inline="true" :model="searchForm" class="search-form">
            <el-form-item label="协同ID"><el-input v-model="searchForm.collabId" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="协同主题"><el-input v-model="searchForm.title" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="状态"><el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 120px;"><el-option label="待启动" value="pending" /><el-option label="进行中" value="in_progress" /><el-option label="已完成" value="completed" /><el-option label="已关闭" value="closed" /></el-select></el-form-item>
            <el-form-item label="责任部门"><el-select v-model="searchForm.department" placeholder="请选择" clearable style="width: 150px;"><el-option v-for="dept in departments" :key="dept.id" :label="dept.name" :value="dept.id" /></el-select></el-form-item>
            <el-form-item><el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
          </el-form>
        </div>
        
        <!-- 协同列表 -->
        <el-table :data="collabList" style="width: 100%" border stripe>
          <el-table-column prop="collabId" label="协同ID" width="120" />
          <el-table-column prop="title" label="协同主题" min-width="200" show-overflow-tooltip />
          <el-table-column prop="riskId" label="关联风险ID" width="120" />
          <el-table-column prop="departments" label="参与部门" min-width="200"><template #default="scope">{{ scope.row.departments.join('、') }}</template></el-table-column>
          <el-table-column prop="leadDepartment" label="责任部门" width="120" />
          <el-table-column prop="deadline" label="截止时间" width="180" />
          <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="getStatusColor(scope.row.status)">{{ getStatusName(scope.row.status) }}</el-tag></template></el-table-column>
          <el-table-column prop="createTime" label="创建时间" width="180" />
          <el-table-column label="操作" width="150" fixed="right"><template #default="scope"><el-button type="primary" size="small" @click="handleViewCollab(scope.row)"><el-icon><View /></el-icon>查看</el-button></template></el-table-column>
        </el-table>
        <div class="pagination-wrapper"><el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" /></div>
      </div>
    </el-card>
    
    <!-- 创建协同对话框 -->
    <el-dialog v-model="collabDialogVisible" :title="collabDialogTitle" width="800px">
      <el-form :model="collabForm" label-width="120px" class="collab-form">
        <el-form-item label="协同主题" required><el-input v-model="collabForm.title" placeholder="请输入协同主题" style="width: 100%;" /></el-form-item>
        <el-form-item label="关联风险ID" required><el-input v-model="collabForm.riskId" placeholder="请输入关联风险ID" style="width: 100%;" /></el-form-item>
        <el-form-item label="参与部门" required><el-checkbox-group v-model="collabForm.departments"><el-checkbox v-for="dept in departments" :key="dept.id" :label="dept.name" /></el-checkbox-group></el-form-item>
        <el-form-item label="责任部门" required><el-select v-model="collabForm.leadDepartment" placeholder="请选择责任部门" style="width: 100%;"><el-option v-for="dept in departments" :key="dept.id" :label="dept.name" :value="dept.name" /></el-select></el-form-item>
        <el-form-item label="截止时间" required><el-date-picker v-model="collabForm.deadline" type="datetime" placeholder="选择截止时间" style="width: 100%;" /></el-form-item>
        <el-form-item label="协同描述"><el-input v-model="collabForm.description" type="textarea" :rows="4" placeholder="请输入协同描述" style="width: 100%;" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="collabDialogVisible = false">取消</el-button><el-button type="primary" @click="handleSaveCollab">保存</el-button></template>
    </el-dialog>
    
    <!-- 协同详情对话框 -->
    <el-dialog v-model="detailDialogVisible" :title="'协同详情 - ' + (currentCollab?.collabId || '')" width="800px">
      <div v-if="currentCollab" class="detail-dialog">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="协同ID">{{ currentCollab.collabId }}</el-descriptions-item>
          <el-descriptions-item label="协同主题">{{ currentCollab.title }}</el-descriptions-item>
          <el-descriptions-item label="关联风险ID">{{ currentCollab.riskId }}</el-descriptions-item>
          <el-descriptions-item label="参与部门">{{ currentCollab.departments.join('、') }}</el-descriptions-item>
          <el-descriptions-item label="责任部门">{{ currentCollab.leadDepartment }}</el-descriptions-item>
          <el-descriptions-item label="截止时间">{{ currentCollab.deadline }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ getStatusName(currentCollab.status) }}</el-descriptions-item>
          <el-descriptions-item label="协同描述">{{ currentCollab.description }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentCollab.createTime }}</el-descriptions-item>
          <el-descriptions-item label="完成时间">{{ currentCollab.completeTime || '-' }}</el-descriptions-item>
        </el-descriptions>
        
        <!-- 部门任务分配 -->
        <div class="dept-tasks" style="margin-top: 20px;">
          <h4>部门任务分配</h4>
          <el-table :data="currentCollab.deptTasks" style="width: 100%" border>
            <el-table-column prop="department" label="部门" width="120" />
            <el-table-column prop="task" label="任务内容" min-width="200" show-overflow-tooltip />
            <el-table-column prop="assignee" label="负责人" width="120" />
            <el-table-column prop="deadline" label="截止时间" width="180" />
            <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="getStatusColor(scope.row.status)">{{ getStatusName(scope.row.status) }}</el-tag></template></el-table-column>
          </el-table>
        </div>
        
        <!-- 协同进度 -->
        <div class="collab-progress" style="margin-top: 20px;">
          <h4>协同进度</h4>
          <el-timeline>
            <el-timeline-item v-for="(item, index) in currentCollab.progress" :key="index" :timestamp="item.time" :type="item.type">
              {{ item.content }}
            </el-timeline-item>
          </el-timeline>
        </div>
        
        <!-- 协同讨论 -->
        <div class="collab-discussion" style="margin-top: 20px;">
          <h4>协同讨论</h4>
          <div class="discussion-list" style="max-height: 300px; overflow-y: auto; border: 1px solid #e4e7ed; border-radius: 4px; padding: 10px;">
            <div v-for="(comment, index) in currentCollab.comments" :key="index" class="comment-item">
              <div class="comment-header"><span class="comment-user">{{ comment.user }}</span><span class="comment-time">{{ comment.time }}</span></div>
              <div class="comment-content">{{ comment.content }}</div>
            </div>
          </div>
          <div class="comment-input" style="margin-top: 10px;"><el-input v-model="commentContent" type="textarea" :rows="3" placeholder="输入讨论内容" style="width: 100%;" /><el-button type="primary" style="margin-top: 10px;" @click="handleAddComment">发表评论</el-button></div>
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
  name: 'CrossDepartment',
  components: { Plus, Refresh, Search, View },
  setup() {
    const loading = ref(false)
    const collabDialogVisible = ref(false)
    const detailDialogVisible = ref(false)
    const collabDialogTitle = ref('创建协同')
    const currentCollab = ref(null)
    const commentContent = ref('')
    
    // 模拟部门数据
    const departments = [
      { id: 'dept001', name: '采购部' },
      { id: 'dept002', name: '生产部' },
      { id: 'dept003', name: '物流部' },
      { id: 'dept004', name: '质量部' },
      { id: 'dept005', name: '财务部' },
      { id: 'dept006', name: '市场部' }
    ]
    
    // 搜索和分页
    const searchForm = reactive({ collabId: '', title: '', status: '', department: '' })
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(80)
    
    // 协同列表
    const collabList = ref([
      { collabId: 'COLLAB001', title: '芯片供应风险跨部门协同', riskId: 'RISK001', departments: ['采购部', '生产部', '物流部'], leadDepartment: '采购部', deadline: '2026-04-15 18:00:00', status: 'in_progress', createTime: '2026-04-09 10:00:00' },
      { collabId: 'COLLAB002', title: '原材料价格上涨应对协同', riskId: 'RISK002', departments: ['采购部', '财务部', '市场部'], leadDepartment: '采购部', deadline: '2026-04-12 18:00:00', status: 'pending', createTime: '2026-04-08 14:00:00' },
      { collabId: 'COLLAB003', title: '地缘政治风险应对协同', riskId: 'RISK003', departments: ['采购部', '物流部', '市场部'], leadDepartment: '物流部', deadline: '2026-04-10 18:00:00', status: 'completed', createTime: '2026-04-07 09:00:00' },
      { collabId: 'COLLAB004', title: '物流延迟风险应对协同', riskId: 'RISK004', departments: ['物流部', '生产部'], leadDepartment: '物流部', deadline: '2026-04-08 18:00:00', status: 'closed', createTime: '2026-04-06 16:00:00' }
    ])
    
    // 协同表单
    const collabForm = reactive({
      title: '',
      riskId: '',
      departments: [],
      leadDepartment: '',
      deadline: null,
      description: ''
    })
    
    // 模拟部门任务数据
    const mockDeptTasks = [
      { department: '采购部', task: '寻找替代芯片供应商', assignee: '张三', deadline: '2026-04-12 18:00:00', status: 'in_progress' },
      { department: '生产部', task: '调整生产计划', assignee: '李四', deadline: '2026-04-10 18:00:00', status: 'completed' },
      { department: '物流部', task: '优化物流路线', assignee: '王五', deadline: '2026-04-11 18:00:00', status: 'in_progress' }
    ]
    
    // 模拟协同进度数据
    const mockCollabProgress = [
      { time: '2026-04-09 10:00:00', content: '协同创建', type: 'primary' },
      { time: '2026-04-09 11:00:00', content: '分配部门任务', type: 'success' },
      { time: '2026-04-10 09:00:00', content: '生产部完成任务', type: 'info' },
      { time: '2026-04-10 14:00:00', content: '采购部正在寻找替代供应商', type: 'warning' }
    ]
    
    // 模拟评论数据
    const mockComments = [
      { user: '张三', time: '2026-04-09 10:30:00', content: '已开始寻找替代供应商' },
      { user: '李四', time: '2026-04-10 09:30:00', content: '生产计划已调整完成' },
      { user: '王五', time: '2026-04-10 10:00:00', content: '物流路线优化方案正在制定' }
    ]
    
    const handleCreateCollaboration = () => {
      collabDialogTitle.value = '创建协同'
      Object.keys(collabForm).forEach(key => {
        collabForm[key] = key === 'departments' ? [] : ''
      })
      collabForm.deadline = null
      collabDialogVisible.value = true
    }
    
    const handleSaveCollab = () => {
      if (!collabForm.title) {
        ElMessage.warning('请输入协同主题')
        return
      }
      if (!collabForm.riskId) {
        ElMessage.warning('请输入关联风险ID')
        return
      }
      if (collabForm.departments.length === 0) {
        ElMessage.warning('请选择参与部门')
        return
      }
      if (!collabForm.leadDepartment) {
        ElMessage.warning('请选择责任部门')
        return
      }
      if (!collabForm.deadline) {
        ElMessage.warning('请选择截止时间')
        return
      }
      ElMessage.success('协同创建成功')
      collabDialogVisible.value = false
      // 模拟添加新协同
      const newCollab = {
        collabId: 'COLLAB' + new Date().getTime(),
        title: collabForm.title,
        riskId: collabForm.riskId,
        departments: collabForm.departments,
        leadDepartment: collabForm.leadDepartment,
        deadline: collabForm.deadline,
        status: 'pending',
        description: collabForm.description,
        createTime: new Date().toLocaleString()
      }
      collabList.value.unshift(newCollab)
    }
    
    const handleViewCollab = (collab) => {
      currentCollab.value = {
        ...collab,
        deptTasks: mockDeptTasks,
        progress: mockCollabProgress,
        comments: mockComments
      }
      commentContent.value = ''
      detailDialogVisible.value = true
    }
    
    const handleAddComment = () => {
      if (!commentContent.value) {
        ElMessage.warning('请输入评论内容')
        return
      }
      currentCollab.value.comments.push({
        user: '当前用户',
        time: new Date().toLocaleString(),
        content: commentContent.value
      })
      ElMessage.success('评论发表成功')
      commentContent.value = ''
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
        case 'pending': return '待启动'
        case 'in_progress': return '进行中'
        case 'completed': return '已完成'
        case 'closed': return '已关闭'
        default: return status
      }
    }
    
    const getStatusColor = (status) => {
      switch (status) {
        case 'pending': return 'warning'
        case 'in_progress': return 'primary'
        case 'completed': return 'success'
        case 'closed': return 'info'
        default: return 'info'
      }
    }
    
    onMounted(() => {
      console.log('跨部门协同跟踪页面加载')
    })
    
    return {
      loading, collabDialogVisible, detailDialogVisible, collabDialogTitle, currentCollab, commentContent,
      departments, searchForm, pagination, total, collabList, collabForm,
      handleCreateCollaboration, handleSaveCollab, handleViewCollab, handleAddComment,
      handleRefresh, handleSearch, resetForm, handleSizeChange, handleCurrentChange,
      getStatusName, getStatusColor
    }
  }
}
</script>

<style scoped>
.cross-department {
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
.collab-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.detail-dialog {
  padding: 10px;
}
.dept-tasks {
  margin-top: 20px;
}
.collab-progress {
  margin-top: 20px;
}
.collab-discussion {
  margin-top: 20px;
}
.discussion-list {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 10px;
}
.comment-item {
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}
.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}
.comment-user {
  font-weight: bold;
}
.comment-time {
  font-size: 12px;
  color: #999;
}
.comment-content {
  line-height: 1.4;
}
.comment-input {
  margin-top: 10px;
}
</style>