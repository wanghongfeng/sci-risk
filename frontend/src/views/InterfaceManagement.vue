<template>
  <div class="interface-management">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>接口对接管理</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleCreateInterface"><el-icon><Plus /></el-icon>新增接口</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 搜索和筛选 -->
        <div class="search-container">
          <el-form :inline="true" :model="searchForm" class="search-form">
            <el-form-item label="接口名称"><el-input v-model="searchForm.interfaceName" placeholder="请输入" clearable style="width: 200px;" /></el-form-item>
            <el-form-item label="接口类型"><el-select v-model="searchForm.interfaceType" placeholder="请选择" clearable style="width: 150px;"><el-option label="REST API" value="rest" /><el-option label="SOAP" value="soap" /><el-option label="WebSocket" value="websocket" /><el-option label="其他" value="other" /></el-select></el-form-item>
            <el-form-item label="状态"><el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 120px;"><el-option label="启用" value="enabled" /><el-option label="禁用" value="disabled" /></el-select></el-form-item>
            <el-form-item><el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
          </el-form>
        </div>
        
        <!-- 接口列表 -->
        <el-table :data="interfaceList" style="width: 100%" border stripe>
          <el-table-column prop="interfaceId" label="接口ID" width="120" />
          <el-table-column prop="interfaceName" label="接口名称" min-width="200" show-overflow-tooltip />
          <el-table-column prop="interfaceType" label="接口类型" width="120"><template #default="scope">{{ getInterfaceTypeName(scope.row.interfaceType) }}</template></el-table-column>
          <el-table-column prop="url" label="接口地址" min-width="300" show-overflow-tooltip />
          <el-table-column prop="method" label="请求方法" width="100" />
          <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'enabled' ? 'success' : 'info'"> {{ getStatusName(scope.row.status) }}</el-tag></template></el-table-column>
          <el-table-column prop="lastTestTime" label="最后测试时间" width="180" />
          <el-table-column prop="testResult" label="测试结果" width="100"><template #default="scope"><el-tag :type="scope.row.testResult === 'success' ? 'success' : scope.row.testResult === 'failed' ? 'danger' : 'info'"> {{ getTestResultName(scope.row.testResult) }}</el-tag></template></el-table-column>
          <el-table-column label="操作" width="240" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleViewInterface(scope.row)"><el-icon><View /></el-icon>查看</el-button>
              <el-button type="warning" size="small" @click="handleEditInterface(scope.row)"><el-icon><Edit /></el-icon>编辑</el-button>
              <el-button type="danger" size="small" @click="handleDeleteInterface(scope.row)"><el-icon><Delete /></el-icon>删除</el-button>
              <el-button type="info" size="small" @click="handleTestInterface(scope.row)"><el-icon><Connection /></el-icon>测试</el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination-wrapper"><el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" /></div>
      </div>
    </el-card>
    
    <!-- 接口对话框 -->
    <el-dialog v-model="interfaceDialogVisible" :title="interfaceDialogTitle" width="800px">
      <el-form :model="interfaceForm" label-width="120px" class="interface-form">
        <el-form-item label="接口名称" required><el-input v-model="interfaceForm.interfaceName" placeholder="请输入接口名称" style="width: 100%;" /></el-form-item>
        <el-form-item label="接口类型" required><el-select v-model="interfaceForm.interfaceType" placeholder="请选择接口类型" style="width: 100%;"><el-option label="REST API" value="rest" /><el-option label="SOAP" value="soap" /><el-option label="WebSocket" value="websocket" /><el-option label="其他" value="other" /></el-select></el-form-item>
        <el-form-item label="接口地址" required><el-input v-model="interfaceForm.url" placeholder="请输入接口地址" style="width: 100%;" /></el-form-item>
        <el-form-item label="请求方法"><el-select v-model="interfaceForm.method" placeholder="请选择请求方法" style="width: 100%;"><el-option label="GET" value="GET" /><el-option label="POST" value="POST" /><el-option label="PUT" value="PUT" /><el-option label="DELETE" value="DELETE" /></el-select></el-form-item>
        <el-form-item label="请求头"><el-input v-model="interfaceForm.headers" type="textarea" :rows="3" placeholder="请输入请求头（JSON格式）" style="width: 100%;" /></el-form-item>
        <el-form-item label="请求体"><el-input v-model="interfaceForm.body" type="textarea" :rows="4" placeholder="请输入请求体" style="width: 100%;" /></el-form-item>
        <el-form-item label="认证方式"><el-select v-model="interfaceForm.authType" placeholder="请选择认证方式" style="width: 100%;"><el-option label="无认证" value="none" /><el-option label="Basic Auth" value="basic" /><el-option label="Bearer Token" value="bearer" /><el-option label="API Key" value="api_key" /></el-select></el-form-item>
        <el-form-item label="认证信息" v-if="interfaceForm.authType !== 'none'" required><el-input v-model="interfaceForm.authInfo" type="password" placeholder="请输入认证信息" style="width: 100%;" /></el-form-item>
        <el-form-item label="状态"><el-select v-model="interfaceForm.status" placeholder="请选择状态" style="width: 100%;"><el-option label="启用" value="enabled" /><el-option label="禁用" value="disabled" /></el-select></el-form-item>
        <el-form-item label="描述"><el-input v-model="interfaceForm.description" type="textarea" :rows="2" placeholder="请输入接口描述" style="width: 100%;" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="interfaceDialogVisible = false">取消</el-button><el-button type="primary" @click="handleSaveInterface">保存</el-button></template>
    </el-dialog>
    
    <!-- 接口详情对话框 -->
    <el-dialog v-model="detailDialogVisible" :title="'接口详情 - ' + (currentInterface?.interfaceName || '')" width="800px">
      <div v-if="currentInterface" class="detail-dialog">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="接口ID">{{ currentInterface.interfaceId }}</el-descriptions-item>
          <el-descriptions-item label="接口名称">{{ currentInterface.interfaceName }}</el-descriptions-item>
          <el-descriptions-item label="接口类型">{{ getInterfaceTypeName(currentInterface.interfaceType) }}</el-descriptions-item>
          <el-descriptions-item label="接口地址">{{ currentInterface.url }}</el-descriptions-item>
          <el-descriptions-item label="请求方法">{{ currentInterface.method }}</el-descriptions-item>
          <el-descriptions-item label="请求头">{{ currentInterface.headers || '-' }}</el-descriptions-item>
          <el-descriptions-item label="请求体">{{ currentInterface.body || '-' }}</el-descriptions-item>
          <el-descriptions-item label="认证方式">{{ getAuthTypeName(currentInterface.authType) }}</el-descriptions-item>
          <el-descriptions-item label="状态">{{ getStatusName(currentInterface.status) }}</el-descriptions-item>
          <el-descriptions-item label="最后测试时间">{{ currentInterface.lastTestTime || '-' }}</el-descriptions-item>
          <el-descriptions-item label="测试结果">{{ getTestResultName(currentInterface.testResult) }}</el-descriptions-item>
          <el-descriptions-item label="描述">{{ currentInterface.description || '-' }}</el-descriptions-item>
        </el-descriptions>
        
        <!-- 测试结果 -->
        <div class="test-result-section" style="margin-top: 20px;">
          <h4>测试结果</h4>
          <div v-if="currentInterface.testResult" class="test-result">
            <el-alert :title="getTestResultName(currentInterface.testResult)" :type="currentInterface.testResult === 'success' ? 'success' : 'error'" show-icon />
            <div v-if="currentInterface.testResponse" class="test-response" style="margin-top: 10px; padding: 10px; background: #f9f9f9; border-radius: 4px;">
              <h5>响应内容：</h5>
              <pre>{{ currentInterface.testResponse }}</pre>
            </div>
          </div>
          <div v-else class="no-test-result">
            <el-empty description="暂无测试记录" />
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleTestInterface(currentInterface)">测试接口</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh, Search, View, Edit, Delete, Connection } from '@element-plus/icons-vue'

export default {
  name: 'InterfaceManagement',
  components: { Plus, Refresh, Search, View, Edit, Delete, Connection },
  setup() {
    const loading = ref(false)
    const interfaceDialogVisible = ref(false)
    const detailDialogVisible = ref(false)
    const interfaceDialogTitle = ref('新增接口')
    const currentInterface = ref(null)
    
    // 搜索和分页
    const searchForm = reactive({ interfaceName: '', interfaceType: '', status: '' })
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(20)
    
    // 接口列表
    const interfaceList = ref([
      { interfaceId: 'IF001', interfaceName: '风险数据采集接口', interfaceType: 'rest', url: 'http://api.example.com/risk/data', method: 'GET', status: 'enabled', lastTestTime: '2026-04-09 10:00:00', testResult: 'success' },
      { interfaceId: 'IF002', interfaceName: '预警推送接口', interfaceType: 'rest', url: 'http://api.example.com/alert/push', method: 'POST', status: 'enabled', lastTestTime: '2026-04-08 14:00:00', testResult: 'success' },
      { interfaceId: 'IF003', interfaceName: '供应商数据接口', interfaceType: 'rest', url: 'http://api.example.com/supplier/data', method: 'GET', status: 'disabled', lastTestTime: '2026-04-07 09:00:00', testResult: 'failed' },
      { interfaceId: 'IF004', interfaceName: '风险分析接口', interfaceType: 'rest', url: 'http://api.example.com/risk/analysis', method: 'POST', status: 'enabled', lastTestTime: '2026-04-06 16:00:00', testResult: 'success' }
    ])
    
    // 接口表单
    const interfaceForm = reactive({
      interfaceName: '',
      interfaceType: 'rest',
      url: '',
      method: 'GET',
      headers: '',
      body: '',
      authType: 'none',
      authInfo: '',
      status: 'enabled',
      description: ''
    })
    
    const handleCreateInterface = () => {
      interfaceDialogTitle.value = '新增接口'
      Object.keys(interfaceForm).forEach(key => {
        interfaceForm[key] = key === 'interfaceType' ? 'rest' : key === 'method' ? 'GET' : key === 'authType' ? 'none' : key === 'status' ? 'enabled' : ''
      })
      currentInterface.value = null
      interfaceDialogVisible.value = true
    }
    
    const handleEditInterface = (interf) => {
      interfaceDialogTitle.value = '编辑接口'
      currentInterface.value = interf
      Object.assign(interfaceForm, interf)
      interfaceDialogVisible.value = true
    }
    
    const handleSaveInterface = () => {
      if (!interfaceForm.interfaceName) {
        ElMessage.warning('请输入接口名称')
        return
      }
      if (!interfaceForm.url) {
        ElMessage.warning('请输入接口地址')
        return
      }
      if (interfaceForm.authType !== 'none' && !interfaceForm.authInfo) {
        ElMessage.warning('请输入认证信息')
        return
      }
      ElMessage.success('接口保存成功')
      interfaceDialogVisible.value = false
      // 模拟添加或更新接口
      if (currentInterface.value) {
        // 更新现有接口
        const index = interfaceList.value.findIndex(item => item.interfaceId === currentInterface.value.interfaceId)
        if (index !== -1) {
          interfaceList.value[index] = { ...interfaceForm, interfaceId: currentInterface.value.interfaceId, lastTestTime: currentInterface.value.lastTestTime, testResult: currentInterface.value.testResult }
        }
      } else {
        // 添加新接口
        const newInterface = {
          interfaceId: 'IF' + new Date().getTime(),
          ...interfaceForm,
          lastTestTime: null,
          testResult: null
        }
        interfaceList.value.unshift(newInterface)
      }
      currentInterface.value = null
    }
    
    const handleViewInterface = (interf) => {
      currentInterface.value = {
        ...interf,
        testResponse: '{"code": 200, "message": "success", "data": {"riskLevel": "high", "riskScore": 85, "riskFactors": ["供应商财务风险", "地缘政治风险"]}}'
      }
      detailDialogVisible.value = true
    }
    
    const handleDeleteInterface = (interf) => {
      ElMessageBox.confirm('确定要删除此接口吗？', '删除接口', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = interfaceList.value.findIndex(item => item.interfaceId === interf.interfaceId)
        if (index !== -1) {
          interfaceList.value.splice(index, 1)
        }
        ElMessage.success('接口删除成功')
      })
    }
    
    const handleTestInterface = (interf) => {
      ElMessage.info('接口测试功能开发中')
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
    
    const getInterfaceTypeName = (type) => {
      switch (type) {
        case 'rest': return 'REST API'
        case 'soap': return 'SOAP'
        case 'websocket': return 'WebSocket'
        case 'other': return '其他'
        default: return type
      }
    }
    
    const getAuthTypeName = (type) => {
      switch (type) {
        case 'none': return '无认证'
        case 'basic': return 'Basic Auth'
        case 'bearer': return 'Bearer Token'
        case 'api_key': return 'API Key'
        default: return type
      }
    }
    
    const getStatusName = (status) => {
      switch (status) {
        case 'enabled': return '启用'
        case 'disabled': return '禁用'
        default: return status
      }
    }
    
    const getTestResultName = (result) => {
      switch (result) {
        case 'success': return '成功'
        case 'failed': return '失败'
        default: return '未测试'
      }
    }
    
    onMounted(() => {
      console.log('接口对接管理页面加载')
    })
    
    return {
      loading, interfaceDialogVisible, detailDialogVisible, interfaceDialogTitle, currentInterface,
      searchForm, pagination, total, interfaceList, interfaceForm,
      handleCreateInterface, handleEditInterface, handleSaveInterface, handleViewInterface, handleDeleteInterface,
      handleTestInterface, handleRefresh, handleSearch, resetForm,
      handleSizeChange, handleCurrentChange, getInterfaceTypeName, getAuthTypeName, getStatusName, getTestResultName
    }
  }
}
</script>

<style scoped>
.interface-management {
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
.interface-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.detail-dialog {
  padding: 10px;
}
.test-result-section {
  margin-top: 20px;
}
.test-result {
  padding: 10px;
  background: #f9f9f9;
  border-radius: 4px;
}
.test-response {
  margin-top: 10px;
}
.test-response pre {
  margin: 0;
  white-space: pre-wrap;
  font-family: monospace;
}
</style>
