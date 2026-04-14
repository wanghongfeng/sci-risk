<template>
  <div class="user-management">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>用户与权限管理</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleCreateUser"><el-icon><Plus /></el-icon>新增用户</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 搜索和筛选 -->
        <div class="search-container">
          <el-form :inline="true" :model="searchForm" class="search-form">
            <el-form-item label="用户ID"><el-input v-model="searchForm.userId" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="用户名"><el-input v-model="searchForm.username" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="角色"><el-select v-model="searchForm.role" placeholder="请选择" clearable style="width: 150px;"><el-option label="管理员" value="admin" /><el-option label="风险分析师" value="analyst" /><el-option label="普通用户" value="user" /></el-select></el-form-item>
            <el-form-item label="状态"><el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 120px;"><el-option label="启用" value="enabled" /><el-option label="禁用" value="disabled" /></el-select></el-form-item>
            <el-form-item><el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
          </el-form>
        </div>
        
        <!-- 用户列表 -->
        <el-table :data="userList" style="width: 100%" border stripe>
          <el-table-column prop="userId" label="用户ID" width="120" />
          <el-table-column prop="username" label="用户名" min-width="150" show-overflow-tooltip />
          <el-table-column prop="name" label="姓名" width="120" />
          <el-table-column prop="email" label="邮箱" min-width="200" show-overflow-tooltip />
          <el-table-column prop="role" label="角色" width="120"><template #default="scope">{{ getRoleName(scope.row.role) }}</template></el-table-column>
          <el-table-column prop="department" label="部门" width="150" />
          <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'enabled' ? 'success' : 'info'"> {{ getStatusName(scope.row.status) }}</el-tag></template></el-table-column>
          <el-table-column prop="createTime" label="创建时间" width="180" />
          <el-table-column label="操作" width="250" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleViewUser(scope.row)" style="margin-right: 5px;">
                <el-icon><View /></el-icon>查看
              </el-button>
              <el-button type="warning" size="small" @click="handleEditUser(scope.row)" style="margin-right: 5px;">
                <el-icon><Edit /></el-icon>编辑
              </el-button>
              <el-button type="danger" size="small" @click="handleDeleteUser(scope.row)">
                <el-icon><Delete /></el-icon>删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination-wrapper"><el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" /></div>
      </div>
    </el-card>
    
    <!-- 用户对话框 -->
    <el-dialog v-model="userDialogVisible" :title="userDialogTitle" width="800px">
      <el-form :model="userForm" label-width="120px" class="user-form">
        <el-form-item label="用户名" required><el-input v-model="userForm.username" placeholder="请输入用户名" style="width: 100%;" /></el-form-item>
        <el-form-item label="密码" :required="!currentUser"><el-input v-model="userForm.password" type="password" placeholder="请输入密码" style="width: 100%;" /></el-form-item>
        <el-form-item label="姓名" required><el-input v-model="userForm.name" placeholder="请输入姓名" style="width: 100%;" /></el-form-item>
        <el-form-item label="邮箱" required><el-input v-model="userForm.email" type="email" placeholder="请输入邮箱" style="width: 100%;" /></el-form-item>
        <el-form-item label="部门" required><el-input v-model="userForm.department" placeholder="请输入部门" style="width: 100%;" /></el-form-item>
        <el-form-item label="角色" required><el-select v-model="userForm.role" placeholder="请选择角色" style="width: 100%;"><el-option label="管理员" value="admin" /><el-option label="风险分析师" value="analyst" /><el-option label="普通用户" value="user" /></el-select></el-form-item>
        <el-form-item label="状态"><el-select v-model="userForm.status" placeholder="请选择状态" style="width: 100%;"><el-option label="启用" value="enabled" /><el-option label="禁用" value="disabled" /></el-select></el-form-item>
      </el-form>
      <template #footer><el-button @click="userDialogVisible = false">取消</el-button><el-button type="primary" @click="handleSaveUser">保存</el-button></template>
    </el-dialog>
    
    <!-- 用户详情对话框 -->
    <el-dialog v-model="detailDialogVisible" :title="'用户详情 - ' + (currentUser?.username || '')" width="800px">
      <div v-if="currentUser" class="detail-dialog">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="用户ID">{{ currentUser.userId }}</el-descriptions-item>
          <el-descriptions-item label="用户名">{{ currentUser.username }}</el-descriptions-item>
          <el-descriptions-item label="姓名">{{ currentUser.name }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ currentUser.email }}</el-descriptions-item>
          <el-descriptions-item label="部门">{{ currentUser.department }}</el-descriptions-item>
          <el-descriptions-item label="角色">{{ getRoleName(currentUser.role) }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ getStatusName(currentUser.status) }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ currentUser.createTime }}</el-descriptions-item>
          <el-descriptions-item label="最后登录时间">{{ currentUser.lastLoginTime || '-' }}</el-descriptions-item>
        </el-descriptions>
        
        <!-- 权限配置 -->
        <div class="permissions-section" style="margin-top: 20px;">
          <h4>权限配置</h4>
          <el-tree
            :data="permissionTree"
            node-key="id"
            show-checkbox
            default-expand-all
            :default-checked-keys="currentUser.permissions || []"
            @check-change="handlePermissionChange"
          />
        </div>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleUpdatePermissions">更新权限</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh, Search, View, Edit, Delete } from '@element-plus/icons-vue'

export default {
  name: 'UserManagement',
  components: { Plus, Refresh, Search, View, Edit, Delete },
  setup() {
    const loading = ref(false)
    const userDialogVisible = ref(false)
    const detailDialogVisible = ref(false)
    const userDialogTitle = ref('新增用户')
    const currentUser = ref(null)
    
    // 搜索和分页
    const searchForm = reactive({ userId: '', username: '', role: '', status: '' })
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(50)
    
    // 用户列表
    const userList = ref([
      { userId: 'USER001', username: 'admin', name: '管理员', email: 'admin@example.com', role: 'admin', department: 'IT部门', status: 'enabled', createTime: '2026-04-01 09:00:00', lastLoginTime: '2026-04-09 10:00:00' },
      { userId: 'USER002', username: 'analyst1', name: '分析师1', email: 'analyst1@example.com', role: 'analyst', department: '风险部门', status: 'enabled', createTime: '2026-04-02 10:00:00', lastLoginTime: '2026-04-08 14:00:00' },
      { userId: 'USER003', username: 'user1', name: '普通用户1', email: 'user1@example.com', role: 'user', department: '业务部门', status: 'enabled', createTime: '2026-04-03 11:00:00', lastLoginTime: '2026-04-07 09:00:00' },
      { userId: 'USER004', username: 'user2', name: '普通用户2', email: 'user2@example.com', role: 'user', department: '业务部门', status: 'disabled', createTime: '2026-04-04 14:00:00', lastLoginTime: '2026-04-05 16:00:00' }
    ])
    
    // 用户表单
    const userForm = reactive({
      username: '',
      password: '',
      name: '',
      email: '',
      department: '',
      role: '',
      status: 'enabled'
    })
    
    // 权限树
    const permissionTree = ref([
      {
        id: 'risk_perception',
        label: '风险感知',
        children: [
          { id: 'risk_data_collection', label: '全球风险数据采集' },
          { id: 'risk_event_management', label: '风险事件库管理' },
          { id: 'supply_chain_master_data', label: '供应链网络主数据' },
          { id: 'risk_exposure_map', label: '风险暴露地图' },
          { id: 'manual_risk_report', label: '人工风险上报' },
          { id: 'data_monitor', label: '数据监控与日志' }
        ]
      },
      {
        id: 'conduction_analysis',
        label: '传导分析',
        children: [
          { id: 'risk_classification', label: '风险自动分类分级' },
          { id: 'risk_path_analysis', label: '风险传导路径推演' },
          { id: 'supply_chain_impact', label: '供应链影响量化测算' },
          { id: 'risk_profile', label: '风险画像' },
          { id: 'risk_analysis', label: '风险分析报告' }
        ]
      },
      {
        id: 'collaborative_disposal',
        label: '协同处置',
        children: [
          { id: 'risk_warning', label: '风险预警管理' },
          { id: 'response_measures', label: '应对措施库' },
          { id: 'smart_plan', label: '智能方案推荐与审批' },
          { id: 'task_orders', label: '任务工单管理' },
          { id: 'cross_department', label: '跨部门协同跟踪' },
          { id: 'disposal_progress', label: '处置进度大屏' }
        ]
      },
      {
        id: 'closed_loop_learning',
        label: '闭环学习',
        children: [
          { id: 'risk_review', label: '风险事件复盘' },
          { id: 'case_library', label: '案例库管理' },
          { id: 'rule_optimization', label: '预警规则优化' },
          { id: 'risk_model_optimization', label: '风险模型参数优化' },
          { id: 'measure_iteration', label: '应对措施迭代' },
          { id: 'knowledge_base', label: '知识沉淀与经验库' }
        ]
      },
      {
        id: 'system_management',
        label: '系统管理',
        children: [
          { id: 'user_management', label: '用户与权限' },
          { id: 'system_config', label: '系统参数配置' },
          { id: 'interface_management', label: '接口对接管理' },
          { id: 'log_audit', label: '日志审计' },
          { id: 'data_backup', label: '数据备份与恢复' },
          { id: 'announcement', label: '公告与帮助中心' }
        ]
      }
    ])
    
    const handleCreateUser = () => {
      userDialogTitle.value = '新增用户'
      Object.keys(userForm).forEach(key => {
        userForm[key] = key === 'status' ? 'enabled' : ''
      })
      currentUser.value = null
      userDialogVisible.value = true
    }
    
    const handleEditUser = (user) => {
      userDialogTitle.value = '编辑用户'
      currentUser.value = user
      Object.assign(userForm, user)
      // 清空密码字段，编辑时可选择是否修改密码
      userForm.password = ''
      userDialogVisible.value = true
    }
    
    const handleSaveUser = () => {
      if (!userForm.username) {
        ElMessage.warning('请输入用户名')
        return
      }
      if (!currentUser.value && !userForm.password) {
        ElMessage.warning('请输入密码')
        return
      }
      if (!userForm.name) {
        ElMessage.warning('请输入姓名')
        return
      }
      if (!userForm.email) {
        ElMessage.warning('请输入邮箱')
        return
      }
      if (!userForm.department) {
        ElMessage.warning('请输入部门')
        return
      }
      if (!userForm.role) {
        ElMessage.warning('请选择角色')
        return
      }
      ElMessage.success('用户保存成功')
      userDialogVisible.value = false
      // 模拟添加或更新用户
      if (currentUser.value) {
        // 更新现有用户
        const index = userList.value.findIndex(item => item.userId === currentUser.value.userId)
        if (index !== -1) {
          userList.value[index] = { ...userForm, userId: currentUser.value.userId, createTime: currentUser.value.createTime, lastLoginTime: currentUser.value.lastLoginTime }
        }
      } else {
        // 添加新用户
        const newUser = {
          userId: 'USER' + new Date().getTime(),
          ...userForm,
          createTime: new Date().toLocaleString(),
          lastLoginTime: null
        }
        userList.value.unshift(newUser)
      }
      currentUser.value = null
    }
    
    const handleViewUser = (user) => {
      currentUser.value = {
        ...user,
        permissions: ['risk_perception', 'conduction_analysis', 'risk_warning'] // 模拟权限数据
      }
      detailDialogVisible.value = true
    }
    
    const handleDeleteUser = (user) => {
      ElMessageBox.confirm('确定要删除此用户吗？', '删除用户', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = userList.value.findIndex(item => item.userId === user.userId)
        if (index !== -1) {
          userList.value.splice(index, 1)
        }
        ElMessage.success('用户删除成功')
      })
    }
    
    const handlePermissionChange = (data, checked, indeterminate) => {
      console.log('权限变更:', data, checked, indeterminate)
    }
    
    const handleUpdatePermissions = () => {
      ElMessage.success('权限更新成功')
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
    
    const getRoleName = (role) => {
      switch (role) {
        case 'admin': return '管理员'
        case 'analyst': return '风险分析师'
        case 'user': return '普通用户'
        default: return role
      }
    }
    
    const getStatusName = (status) => {
      switch (status) {
        case 'enabled': return '启用'
        case 'disabled': return '禁用'
        default: return status
      }
    }
    
    onMounted(() => {
      console.log('用户与权限管理页面加载')
    })
    
    return {
      loading, userDialogVisible, detailDialogVisible, userDialogTitle, currentUser,
      searchForm, pagination, total, userList, userForm, permissionTree,
      handleCreateUser, handleEditUser, handleSaveUser, handleViewUser, handleDeleteUser,
      handlePermissionChange, handleUpdatePermissions, handleRefresh, handleSearch, resetForm,
      handleSizeChange, handleCurrentChange, getRoleName, getStatusName
    }
  }
}
</script>

<style scoped>
.user-management {
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
.user-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.detail-dialog {
  padding: 10px;
}
.permissions-section {
  margin-top: 20px;
}
</style>