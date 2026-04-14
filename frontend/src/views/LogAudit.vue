<template>
  <div class="log-audit">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>日志审计</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleExport"><el-icon><Download /></el-icon>导出日志</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 搜索和筛选 -->
        <div class="search-container">
          <el-form :inline="true" :model="searchForm" class="search-form">
            <el-form-item label="操作人"><el-input v-model="searchForm.username" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="操作类型"><el-select v-model="searchForm.operationType" placeholder="请选择" clearable style="width: 150px;"><el-option label="登录" value="login" /><el-option label="登出" value="logout" /><el-option label="新增" value="create" /><el-option label="编辑" value="update" /><el-option label="删除" value="delete" /><el-option label="查询" value="query" /></el-select></el-form-item>
            <el-form-item label="操作模块"><el-input v-model="searchForm.module" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
            <el-form-item label="操作时间"><el-date-picker v-model="searchForm.timeRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="width: 300px;" /></el-form-item>
            <el-form-item><el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
          </el-form>
        </div>
        
        <!-- 日志列表 -->
        <el-table :data="logList" style="width: 100%" border stripe>
          <el-table-column prop="logId" label="日志ID" width="120" />
          <el-table-column prop="username" label="操作人" width="120" />
          <el-table-column prop="ipAddress" label="IP地址" width="150" />
          <el-table-column prop="operationType" label="操作类型" width="120"><template #default="scope">{{ getOperationTypeName(scope.row.operationType) }}</template></el-table-column>
          <el-table-column prop="module" label="操作模块" width="150" />
          <el-table-column prop="operationContent" label="操作内容" min-width="300" show-overflow-tooltip />
          <el-table-column prop="operationTime" label="操作时间" width="180" />
          <el-table-column prop="status" label="操作状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'"> {{ getStatusName(scope.row.status) }}</el-tag></template></el-table-column>
          <el-table-column label="操作" width="120" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleViewLog(scope.row)"><el-icon><View /></el-icon>查看</el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination-wrapper"><el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" /></div>
      </div>
    </el-card>
    
    <!-- 日志详情对话框 -->
    <el-dialog v-model="detailDialogVisible" :title="'日志详情 - ' + (currentLog?.logId || '')" width="800px">
      <div v-if="currentLog" class="detail-dialog">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="日志ID">{{ currentLog.logId }}</el-descriptions-item>
          <el-descriptions-item label="操作人">{{ currentLog.username }}</el-descriptions-item>
          <el-descriptions-item label="IP地址">{{ currentLog.ipAddress }}</el-descriptions-item>
          <el-descriptions-item label="用户代理">{{ currentLog.userAgent || '-' }}</el-descriptions-item>
          <el-descriptions-item label="操作类型">{{ getOperationTypeName(currentLog.operationType) }}</el-descriptions-item>
          <el-descriptions-item label="操作模块">{{ currentLog.module }}</el-descriptions-item>
          <el-descriptions-item label="操作内容">{{ currentLog.operationContent }}</el-descriptions-item>
          <el-descriptions-item label="操作时间">{{ currentLog.operationTime }}</el-descriptions-item>
          <el-descriptions-item label="操作状态">{{ getStatusName(currentLog.status) }}</el-descriptions-item>
          <el-descriptions-item label="错误信息" v-if="currentLog.errorMessage">{{ currentLog.errorMessage }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer><el-button @click="detailDialogVisible = false">关闭</el-button></template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Download, Refresh, Search, View } from '@element-plus/icons-vue'

export default {
  name: 'LogAudit',
  components: { Download, Refresh, Search, View },
  setup() {
    const loading = ref(false)
    const detailDialogVisible = ref(false)
    const currentLog = ref(null)
    
    // 搜索和分页
    const searchForm = reactive({ username: '', operationType: '', module: '', timeRange: [] })
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(100)
    
    // 日志列表
    const logList = ref([
      { logId: 'LOG001', username: 'admin', ipAddress: '192.168.1.100', operationType: 'login', module: '系统登录', operationContent: '用户登录系统', operationTime: '2026-04-09 10:00:00', status: 'success' },
      { logId: 'LOG002', username: 'analyst1', ipAddress: '192.168.1.101', operationType: 'create', module: '风险事件库', operationContent: '新增风险事件', operationTime: '2026-04-09 09:30:00', status: 'success' },
      { logId: 'LOG003', username: 'user1', ipAddress: '192.168.1.102', operationType: 'update', module: '任务工单', operationContent: '更新任务状态', operationTime: '2026-04-09 09:00:00', status: 'success' },
      { logId: 'LOG004', username: 'admin', ipAddress: '192.168.1.100', operationType: 'delete', module: '用户管理', operationContent: '删除用户', operationTime: '2026-04-08 16:00:00', status: 'success' },
      { logId: 'LOG005', username: 'user2', ipAddress: '192.168.1.103', operationType: 'login', module: '系统登录', operationContent: '用户登录系统', operationTime: '2026-04-08 14:30:00', status: 'failed', errorMessage: '密码错误' },
      { logId: 'LOG006', username: 'analyst1', ipAddress: '192.168.1.101', operationType: 'query', module: '风险分析', operationContent: '查询风险数据', operationTime: '2026-04-08 11:00:00', status: 'success' },
      { logId: 'LOG007', username: 'admin', ipAddress: '192.168.1.100', operationType: 'logout', module: '系统登出', operationContent: '用户登出系统', operationTime: '2026-04-08 10:30:00', status: 'success' }
    ])
    
    const handleViewLog = (log) => {
      currentLog.value = {
        ...log,
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      }
      detailDialogVisible.value = true
    }
    
    const handleExport = () => {
      ElMessage.success('日志导出成功')
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
        searchForm[key] = key === 'timeRange' ? [] : ''
      })
    }
    
    const handleSizeChange = (size) => {
      pagination.pageSize = size
    }
    
    const handleCurrentChange = (current) => {
      pagination.currentPage = current
    }
    
    const getOperationTypeName = (type) => {
      switch (type) {
        case 'login': return '登录'
        case 'logout': return '登出'
        case 'create': return '新增'
        case 'update': return '编辑'
        case 'delete': return '删除'
        case 'query': return '查询'
        default: return type
      }
    }
    
    const getStatusName = (status) => {
      switch (status) {
        case 'success': return '成功'
        case 'failed': return '失败'
        default: return status
      }
    }
    
    onMounted(() => {
      console.log('日志审计页面加载')
    })
    
    return {
      loading, detailDialogVisible, currentLog,
      searchForm, pagination, total, logList,
      handleViewLog, handleExport, handleRefresh, handleSearch, resetForm,
      handleSizeChange, handleCurrentChange, getOperationTypeName, getStatusName
    }
  }
}
</script>

<style scoped>
.log-audit {
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
.detail-dialog {
  padding: 10px;
}
</style>
