<template>
  <div class="data-monitor">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>数据监控与日志</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
            <el-button type="success" size="small" @click="handleExport"><el-icon><Download /></el-icon>导出日志</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="系统状态" name="status">
            <div class="stats-container">
              <el-row :gutter="20">
                <el-col :span="6"><div class="stat-card"><div class="stat-icon" style="background: #409eff;"><el-icon><Monitor /></el-icon></div><div class="stat-info"><div class="stat-value">{{ stats.cpuUsage }}%</div><div class="stat-label">CPU使用率</div></div></div></el-col>
                <el-col :span="6"><div class="stat-card"><div class="stat-icon" style="background: #67c23a;"><el-icon><Coin /></el-icon></div><div class="stat-info"><div class="stat-value">{{ stats.memoryUsage }}%</div><div class="stat-label">内存使用率</div></div></div></el-col>
                <el-col :span="6"><div class="stat-card"><div class="stat-icon" style="background: #e6a23c;"><el-icon><Calendar /></el-icon></div><div class="stat-info"><div class="stat-value">{{ stats.diskUsage }}%</div><div class="stat-label">磁盘使用率</div></div></div></el-col>
                <el-col :span="6"><div class="stat-card"><div class="stat-icon" style="background: #f56c6c;"><el-icon><Connection /></el-icon></div><div class="stat-info"><div class="stat-value">{{ stats.networkTraffic }}</div><div class="stat-label">网络流量</div></div></div></el-col>
              </el-row>
            </div>
            <el-row :gutter="20">
              <el-col :span="12"><el-card class="service-card"><template #header><span>服务状态</span></template><el-table :data="serviceList" style="width: 100%"><el-table-column prop="serviceName" label="服务名称" /><el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'running' ? 'success' : 'danger'" size="small">{{ scope.row.status === 'running' ? '运行中' : '已停止' }}</el-tag></template></el-table-column><el-table-column prop="uptime" label="运行时长" width="120" /><el-table-column prop="requests" label="请求数" width="100" align="right" /></el-table></el-card></el-col>
              <el-col :span="12"><el-card class="alert-card"><template #header><span>最近告警</span></template><div class="alert-list"><div v-for="alert in recentAlerts" :key="alert.id" class="alert-item"><el-icon :color="getAlertColor(alert.level)"><Warning /></el-icon><div class="alert-content"><div class="alert-title">{{ alert.title }}</div><div class="alert-time">{{ alert.time }}</div></div></div></div></el-card></el-col>
            </el-row>
          </el-tab-pane>
          <el-tab-pane label="操作日志" name="operation">
            <div class="search-container">
              <el-form :inline="true" :model="searchForm" class="search-form">
                <el-form-item label="操作人"><el-input v-model="searchForm.operator" placeholder="请输入" clearable style="width: 120px;" /></el-form-item>
                <el-form-item label="操作类型"><el-select v-model="searchForm.operationType" placeholder="请选择" clearable style="width: 120px;"><el-option label="登录" value="login" /><el-option label="新增" value="create" /><el-option label="修改" value="update" /><el-option label="删除" value="delete" /></el-select></el-form-item>
                <el-form-item label="操作模块"><el-select v-model="searchForm.module" placeholder="请选择" clearable style="width: 140px;"><el-option label="用户管理" value="user" /><el-option label="菜单管理" value="menu" /><el-option label="风险数据" value="risk" /></el-select></el-form-item>
                <el-form-item><el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
              </el-form>
            </div>
            <el-table :data="operationLogList" style="width: 100%" border stripe>
              <el-table-column prop="logId" label="日志ID" width="130" /><el-table-column prop="operator" label="操作人" width="100" /><el-table-column prop="operationType" label="操作类型" width="100"><template #default="scope"><el-tag :type="getOperationTypeColor(scope.row.operationType)" size="small">{{ getOperationTypeName(scope.row.operationType) }}</el-tag></template></el-table-column><el-table-column prop="module" label="操作模块" width="120"><template #default="scope">{{ getModuleName(scope.row.module) }}</template></el-table-column><el-table-column prop="operationDesc" label="操作描述" min-width="200" show-overflow-tooltip /><el-table-column prop="ipAddress" label="IP地址" width="130" /><el-table-column prop="operationTime" label="操作时间" width="160" /><el-table-column label="操作" width="100" fixed="right"><template #default="scope"><el-button type="primary" size="small" @click="handleViewLog(scope.row)"><el-icon><View /></el-icon>详情</el-button></template></el-table-column>
            </el-table>
            <div class="pagination-wrapper"><el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" /></div>
          </el-tab-pane>
          <el-tab-pane label="数据采集日志" name="collection">
            <div class="search-container">
              <el-form :inline="true" :model="collectionSearchForm" class="search-form">
                <el-form-item label="数据源"><el-select v-model="collectionSearchForm.source" placeholder="请选择" clearable style="width: 120px;"><el-option label="海关数据" value="customs" /><el-option label="物流数据" value="logistics" /><el-option label="舆情数据" value="public_opinion" /></el-select></el-form-item>
                <el-form-item label="采集状态"><el-select v-model="collectionSearchForm.status" placeholder="请选择" clearable style="width: 120px;"><el-option label="成功" value="success" /><el-option label="失败" value="failed" /><el-option label="进行中" value="running" /></el-select></el-form-item>
                <el-form-item><el-button type="primary" @click="handleCollectionSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetCollectionForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
              </el-form>
            </div>
            <el-table :data="collectionLogList" style="width: 100%" border stripe>
              <el-table-column prop="logId" label="日志ID" width="140" /><el-table-column prop="source" label="数据源" width="120"><template #default="scope"><el-tag>{{ getSourceName(scope.row.source) }}</el-tag></template></el-table-column><el-table-column prop="dataType" label="数据类型" width="120" /><el-table-column prop="recordsCount" label="记录数" width="100" align="right" /><el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="getCollectionStatusType(scope.row.status)" size="small">{{ getCollectionStatusName(scope.row.status) }}</el-tag></template></el-table-column><el-table-column prop="startTime" label="开始时间" width="160" /><el-table-column prop="endTime" label="结束时间" width="160" /><el-table-column label="操作" width="100" fixed="right"><template #default="scope"><el-button type="primary" size="small" @click="handleViewCollectionLog(scope.row)"><el-icon><View /></el-icon>详情</el-button></template></el-table-column>
            </el-table>
            <div class="pagination-wrapper"><el-pagination v-model:current-page="collectionPagination.currentPage" v-model:page-size="collectionPagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="collectionTotal" @size-change="handleCollectionSizeChange" @current-change="handleCollectionCurrentChange" /></div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>
    <el-dialog v-model="logDialogVisible" title="日志详情" width="800px">
      <el-descriptions v-if="currentLog" :column="1" border>
        <el-descriptions-item label="日志ID">{{ currentLog.logId }}</el-descriptions-item>
        <el-descriptions-item label="操作人">{{ currentLog.operator }}</el-descriptions-item>
        <el-descriptions-item label="操作类型">{{ getOperationTypeName(currentLog.operationType) }}</el-descriptions-item>
        <el-descriptions-item label="操作模块">{{ getModuleName(currentLog.module) }}</el-descriptions-item>
        <el-descriptions-item label="IP地址">{{ currentLog.ipAddress }}</el-descriptions-item>
        <el-descriptions-item label="操作时间">{{ currentLog.operationTime }}</el-descriptions-item>
        <el-descriptions-item label="操作描述">{{ currentLog.operationDesc }}</el-descriptions-item>
        <el-descriptions-item label="请求参数">{{ currentLog.requestParams || '-' }}</el-descriptions-item>
        <el-descriptions-item label="响应结果">{{ currentLog.responseResult || '-' }}</el-descriptions-item>
      </el-descriptions>
      <template #footer><el-button @click="logDialogVisible = false">关闭</el-button></template>
    </el-dialog>
  </div>
</template>
<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, Download, Monitor, Coin, Calendar, Connection, Warning, Search, View } from '@element-plus/icons-vue'
export default {
  name: 'DataMonitor',
  components: { Refresh, Download, Monitor, Coin, Calendar, Connection, Warning, Search, View },
  setup() {
    const loading = ref(false)
    const activeTab = ref('status')
    const logDialogVisible = ref(false)
    const currentLog = ref(null)
    const stats = reactive({ cpuUsage: 45, memoryUsage: 62, diskUsage: 38, networkTraffic: '125MB/s' })
    const serviceList = ref([
      { serviceName: '前端服务', status: 'running', uptime: '15天3小时', requests: 125680 },
      { serviceName: '后端服务', status: 'running', uptime: '15天3小时', requests: 98650 },
      { serviceName: '算法服务', status: 'running', uptime: '10天5小时', requests: 45230 },
      { serviceName: 'AI Agent', status: 'running', uptime: '5天2小时', requests: 12450 }
    ])
    const recentAlerts = ref([
      { id: 1, level: 'warning', title: 'CPU使用率超过80%', time: '2026-04-09 11:30:00' },
      { id: 2, level: 'danger', title: '磁盘空间不足', time: '2026-04-08 16:45:00' },
      { id: 3, level: 'info', title: '服务重启成功', time: '2026-04-07 08:15:00' }
    ])
    const searchForm = reactive({ operator: '', operationType: '', module: '' })
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(100)
    const operationLogList = ref([
      { logId: 'LOG20260409001', operator: 'admin', operationType: 'login', module: 'user', operationDesc: '用户登录', ipAddress: '192.168.1.100', operationTime: '2026-04-09 10:00:00' },
      { logId: 'LOG20260409002', operator: 'admin', operationType: 'create', module: 'risk', operationDesc: '新增风险数据', ipAddress: '192.168.1.100', operationTime: '2026-04-09 10:05:00' },
      { logId: 'LOG20260409003', operator: 'user1', operationType: 'update', module: 'menu', operationDesc: '修改菜单配置', ipAddress: '192.168.1.101', operationTime: '2026-04-09 10:10:00' },
      { logId: 'LOG20260409004', operator: 'user2', operationType: 'delete', module: 'risk', operationDesc: '删除风险数据', ipAddress: '192.168.1.102', operationTime: '2026-04-09 10:15:00' }
    ])
    const collectionSearchForm = reactive({ source: '', status: '' })
    const collectionPagination = reactive({ currentPage: 1, pageSize: 10 })
    const collectionTotal = ref(80)
    const collectionLogList = ref([
      { logId: 'CL20260409001', source: 'customs', dataType: '进出口数据', recordsCount: 1250, status: 'success', startTime: '2026-04-09 09:00:00', endTime: '2026-04-09 09:15:00' },
      { logId: 'CL20260409002', source: 'logistics', dataType: '运输数据', recordsCount: 890, status: 'success', startTime: '2026-04-09 09:30:00', endTime: '2026-04-09 09:40:00' },
      { logId: 'CL20260409003', source: 'public_opinion', dataType: '舆情数据', recordsCount: 2300, status: 'success', startTime: '2026-04-09 10:00:00', endTime: '2026-04-09 10:20:00' },
      { logId: 'CL20260409004', source: 'customs', dataType: '关税数据', recordsCount: 0, status: 'failed', startTime: '2026-04-09 10:30:00', endTime: '2026-04-09 10:35:00' }
    ])
    const handleRefresh = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('刷新成功')
        loading.value = false
      }, 1000)
    }
    const handleExport = () => {
      ElMessage.info('导出功能开发中')
    }
    const handleTabChange = (tab) => {
      console.log('切换到标签页:', tab)
    }
    const getAlertColor = (level) => {
      switch (level) {
        case 'danger': return '#f56c6c'
        case 'warning': return '#e6a23c'
        case 'info': return '#409eff'
        default: return '#67c23a'
      }
    }
    const getOperationTypeColor = (type) => {
      switch (type) {
        case 'login': return 'info'
        case 'create': return 'success'
        case 'update': return 'warning'
        case 'delete': return 'danger'
        default: return 'info'
      }
    }
    const getOperationTypeName = (type) => {
      switch (type) {
        case 'login': return '登录'
        case 'create': return '新增'
        case 'update': return '修改'
        case 'delete': return '删除'
        default: return type
      }
    }
    const getModuleName = (module) => {
      switch (module) {
        case 'user': return '用户管理'
        case 'menu': return '菜单管理'
        case 'risk': return '风险数据'
        default: return module
      }
    }
    const getSourceName = (source) => {
      switch (source) {
        case 'customs': return '海关数据'
        case 'logistics': return '物流数据'
        case 'public_opinion': return '舆情数据'
        default: return source
      }
    }
    const getCollectionStatusType = (status) => {
      switch (status) {
        case 'success': return 'success'
        case 'failed': return 'danger'
        case 'running': return 'warning'
        default: return 'info'
      }
    }
    const getCollectionStatusName = (status) => {
      switch (status) {
        case 'success': return '成功'
        case 'failed': return '失败'
        case 'running': return '进行中'
        default: return status
      }
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
    const handleViewLog = (log) => {
      currentLog.value = log
      logDialogVisible.value = true
    }
    const handleCollectionSearch = () => {
      ElMessage.info('搜索功能开发中')
    }
    const resetCollectionForm = () => {
      Object.keys(collectionSearchForm).forEach(key => {
        collectionSearchForm[key] = ''
      })
    }
    const handleCollectionSizeChange = (size) => {
      collectionPagination.pageSize = size
    }
    const handleCollectionCurrentChange = (current) => {
      collectionPagination.currentPage = current
    }
    const handleViewCollectionLog = (log) => {
      currentLog.value = log
      logDialogVisible.value = true
    }
    onMounted(() => {
      console.log('数据监控与日志页面加载')
    })
    return {
      loading, activeTab, logDialogVisible, currentLog, stats, serviceList, recentAlerts, searchForm, pagination, total, operationLogList, collectionSearchForm, collectionPagination, collectionTotal, collectionLogList, handleRefresh, handleExport, handleTabChange, getAlertColor, getOperationTypeColor, getOperationTypeName, getModuleName, getSourceName, getCollectionStatusType, getCollectionStatusName, handleSearch, resetForm, handleSizeChange, handleCurrentChange, handleViewLog, handleCollectionSearch, resetCollectionForm, handleCollectionSizeChange, handleCollectionCurrentChange, handleViewCollectionLog
    }
  }
}
</script>
<style scoped>
.data-monitor {
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
.stats-container {
  margin-bottom: 20px;
}
.stat-card {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}
.stat-info {
  flex: 1;
}
.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 4px;
}
.stat-label {
  font-size: 14px;
  color: #606266;
}
.service-card,
.alert-card {
  margin-top: 20px;
}
.alert-list {
  padding: 10px 0;
}
.alert-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}
.alert-content {
  flex: 1;
}
.alert-title {
  font-weight: 500;
  margin-bottom: 4px;
}
.alert-time {
  font-size: 12px;
  color: #909399;
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
</style>