<template>
  <div class="system-user-container">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" size="small" @click="handleAddUser">
            <el-icon><Plus /></el-icon>
            新增用户
          </el-button>
        </div>
      </template>

      <!-- 搜索和筛选 -->
      <div class="search-container">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="用户名">
            <el-input v-model="searchForm.username" placeholder="请输入用户名" style="width: 200px" />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" style="width: 120px">
              <el-option label="全部" value="" />
              <el-option label="启用" value="1" />
              <el-option label="禁用" value="0" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 用户表格 -->
      <el-table v-loading="loading" :data="userList" style="width: 100%" border>
        <el-table-column prop="userId" label="用户ID" width="100" />
        <el-table-column prop="username" label="用户名" width="180" />
        <el-table-column prop="name" label="姓名" width="150" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="phone" label="电话" width="150" />
        <el-table-column prop="roleName" label="角色" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
              {{ scope.row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEditUser(scope.row)" style="margin-right: 5px">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="handleDeleteUser(scope.row.userId)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 新增/编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
    >
      <el-form ref="userForm" :model="formData" :rules="rules" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="formData.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="formData.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="密码" v-if="!formData.userId">
          <el-input v-model="formData.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formData.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="formData.phone" placeholder="请输入电话" />
        </el-form-item>
        <el-form-item label="角色" prop="roleId">
          <el-select v-model="formData.roleId" placeholder="请选择角色">
            <el-option
              v-for="role in roleList"
              :key="role.roleId"
              :label="role.roleName"
              :value="role.roleId"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-switch v-model="formData.status" active-value="1" inactive-value="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { Plus, Search, Edit, Delete } from '@element-plus/icons-vue'
import { ElMessageBox, ElMessage } from 'element-plus'

export default {
  name: 'SystemUser',
  components: {
    Plus,
    Search,
    Edit,
    Delete
  },
  setup() {
    // 响应式数据
    const userList = ref([])
    const loading = ref(false)
    const total = ref(0)
    const searchForm = ref({
      username: '',
      status: ''
    })
    const pagination = ref({
      currentPage: 1,
      pageSize: 10
    })
    const dialogVisible = ref(false)
    const dialogTitle = ref('新增用户')
    const formData = ref({
      userId: '',
      username: '',
      name: '',
      password: '',
      email: '',
      phone: '',
      roleId: '',
      status: 1
    })
    const roleList = ref([
      { roleId: 1, roleName: '管理员' },
      { roleId: 2, roleName: '普通用户' },
      { roleId: 3, roleName: '查看权限' }
    ])
    const rules = ref({
      username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
      name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
      ],
      phone: [{ required: true, message: '请输入电话', trigger: 'blur' }],
      roleId: [{ required: true, message: '请选择角色', trigger: 'blur' }]
    })

    // 模拟用户数据
    const mockUsers = [
      { userId: 1, username: 'admin', name: '管理员', email: 'admin@example.com', phone: '13800138000', roleName: '管理员', status: 1, createTime: '2024-01-01 00:00:00' },
      { userId: 2, username: 'user1', name: '用户1', email: 'user1@example.com', phone: '13800138001', roleName: '普通用户', status: 1, createTime: '2024-01-02 00:00:00' },
      { userId: 3, username: 'user2', name: '用户2', email: 'user2@example.com', phone: '13800138002', roleName: '查看权限', status: 0, createTime: '2024-01-03 00:00:00' }
    ]

    // 加载用户数据
    const loadUsers = () => {
      loading.value = true
      // 模拟API调用
      setTimeout(() => {
        let filteredUsers = [...mockUsers]
        
        // 搜索筛选
        if (searchForm.value.username) {
          filteredUsers = filteredUsers.filter(user => 
            user.username.includes(searchForm.value.username)
          )
        }
        
        if (searchForm.value.status) {
          filteredUsers = filteredUsers.filter(user => 
            user.status === parseInt(searchForm.value.status)
          )
        }
        
        total.value = filteredUsers.length
        
        // 分页
        const start = (pagination.value.currentPage - 1) * pagination.value.pageSize
        const end = start + pagination.value.pageSize
        userList.value = filteredUsers.slice(start, end)
        
        loading.value = false
      }, 500)
    }

    // 搜索
    const handleSearch = () => {
      pagination.value.currentPage = 1
      loadUsers()
    }

    // 重置
    const resetForm = () => {
      searchForm.value = {
        username: '',
        status: ''
      }
      pagination.value.currentPage = 1
      loadUsers()
    }

    // 分页处理
    const handleSizeChange = (size) => {
      pagination.value.pageSize = size
      loadUsers()
    }

    const handleCurrentChange = (current) => {
      pagination.value.currentPage = current
      loadUsers()
    }

    // 新增用户
    const handleAddUser = () => {
      dialogTitle.value = '新增用户'
      formData.value = {
        userId: '',
        username: '',
        name: '',
        password: '',
        email: '',
        phone: '',
        roleId: '',
        status: 1
      }
      dialogVisible.value = true
    }

    // 编辑用户
    const handleEditUser = (user) => {
      dialogTitle.value = '编辑用户'
      formData.value = {
        userId: user.userId,
        username: user.username,
        name: user.name,
        email: user.email,
        phone: user.phone,
        roleId: user.roleId || 2,
        status: user.status
      }
      dialogVisible.value = true
    }

    // 删除用户
    const handleDeleteUser = (userId) => {
      ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 模拟删除操作
        setTimeout(() => {
          ElMessage.success('删除成功')
          loadUsers()
        }, 500)
      }).catch(() => {
        // 取消删除
      })
    }

    // 提交表单
    const handleSubmit = () => {
      // 模拟表单验证
      if (!formData.value.username || !formData.value.name || !formData.value.email || !formData.value.phone || !formData.value.roleId) {
        ElMessage.error('请填写完整信息')
        return
      }

      // 模拟提交操作
      setTimeout(() => {
        ElMessage.success(formData.value.userId ? '编辑成功' : '新增成功')
        dialogVisible.value = false
        loadUsers()
      }, 500)
    }

    // 生命周期
    onMounted(() => {
      loadUsers()
    })

    return {
      userList,
      loading,
      total,
      searchForm,
      pagination,
      dialogVisible,
      dialogTitle,
      formData,
      roleList,
      rules,
      handleSearch,
      resetForm,
      handleSizeChange,
      handleCurrentChange,
      handleAddUser,
      handleEditUser,
      handleDeleteUser,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.system-user-container {
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

.search-container {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  text-align: right;
}
</style>