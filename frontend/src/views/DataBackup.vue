<template>
  <div class="data-backup">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>数据备份与恢复</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleCreateBackup"><el-icon><Plus /></el-icon>创建备份</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 备份配置 -->
        <el-card shadow="hover" style="margin-bottom: 20px;">
          <template #header>
            <div class="sub-card-header">
              <span>备份配置</span>
            </div>
          </template>
          <el-form :model="backupConfig" label-width="150px" class="config-form">
            <el-form-item label="自动备份">
              <el-switch v-model="backupConfig.autoBackup" />
            </el-form-item>
            <el-form-item label="备份频率" v-if="backupConfig.autoBackup">
              <el-select v-model="backupConfig.frequency" placeholder="请选择" style="width: 200px;">
                <el-option label="每天" value="daily" />
                <el-option label="每周" value="weekly" />
                <el-option label="每月" value="monthly" />
              </el-select>
            </el-form-item>
            <el-form-item label="备份时间" v-if="backupConfig.autoBackup">
              <el-time-picker v-model="backupConfig.backupTime" placeholder="选择时间" style="width: 200px;" />
            </el-form-item>
            <el-form-item label="备份保留天数">
              <el-input v-model="backupConfig.retentionDays" type="number" placeholder="请输入保留天数" style="width: 200px;" />
            </el-form-item>
            <el-form-item label="备份路径">
              <el-input v-model="backupConfig.backupPath" placeholder="请输入备份路径" style="width: 100%;" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSaveConfig">保存配置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
        
        <!-- 备份列表 -->
        <el-card shadow="hover">
          <template #header>
            <div class="sub-card-header">
              <span>备份记录</span>
            </div>
          </template>
          <div class="backup-list">
            <el-table :data="backupList" style="width: 100%" border stripe>
              <el-table-column prop="backupId" label="备份ID" width="150" />
              <el-table-column prop="backupTime" label="备份时间" width="180" />
              <el-table-column prop="backupType" label="备份类型" width="120"><template #default="scope">{{ getBackupTypeName(scope.row.backupType) }}</template></el-table-column>
              <el-table-column prop="size" label="备份大小" width="120" />
              <el-table-column prop="status" label="状态" width="100"><template #default="scope"><el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'"> {{ getStatusName(scope.row.status) }}</el-tag></template></el-table-column>
              <el-table-column prop="operator" label="操作人" width="120" />
              <el-table-column label="操作" width="240" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click="handleRestoreBackup(scope.row)"><el-icon><RefreshLeft /></el-icon>恢复</el-button>
                  <el-button type="warning" size="small" @click="handleDownloadBackup(scope.row)"><el-icon><Download /></el-icon>下载</el-button>
                  <el-button type="danger" size="small" @click="handleDeleteBackup(scope.row)"><el-icon><Delete /></el-icon>删除</el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="pagination-wrapper"><el-pagination v-model:current-page="pagination.currentPage" v-model:page-size="pagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="total" @size-change="handleSizeChange" @current-change="handleCurrentChange" /></div>
          </div>
        </el-card>
      </div>
    </el-card>
    
    <!-- 恢复确认对话框 -->
    <el-dialog v-model="restoreDialogVisible" title="恢复数据" width="500px">
      <div class="restore-dialog">
        <p>确定要从备份中恢复数据吗？</p>
        <p class="warning-text">恢复操作会覆盖当前系统数据，请谨慎操作！</p>
        <div class="backup-info" v-if="selectedBackup">
          <p>备份ID: {{ selectedBackup.backupId }}</p>
          <p>备份时间: {{ selectedBackup.backupTime }}</p>
          <p>备份类型: {{ getBackupTypeName(selectedBackup.backupType) }}</p>
        </div>
      </div>
      <template #footer>
        <el-button @click="restoreDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="handleConfirmRestore">确认恢复</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh, RefreshLeft, Download, Delete } from '@element-plus/icons-vue'

export default {
  name: 'DataBackup',
  components: { Plus, Refresh, RefreshLeft, Download, Delete },
  setup() {
    const loading = ref(false)
    const restoreDialogVisible = ref(false)
    const selectedBackup = ref(null)
    
    // 分页
    const pagination = reactive({ currentPage: 1, pageSize: 10 })
    const total = ref(20)
    
    // 备份配置
    const backupConfig = reactive({
      autoBackup: true,
      frequency: 'daily',
      backupTime: new Date('2026-04-01 02:00:00'),
      retentionDays: 30,
      backupPath: '/backup/data'
    })
    
    // 备份列表
    const backupList = ref([
      { backupId: 'BACKUP001', backupTime: '2026-04-09 02:00:00', backupType: 'full', size: '1.2 GB', status: 'success', operator: '系统' },
      { backupId: 'BACKUP002', backupTime: '2026-04-08 02:00:00', backupType: 'full', size: '1.1 GB', status: 'success', operator: '系统' },
      { backupId: 'BACKUP003', backupTime: '2026-04-07 02:00:00', backupType: 'full', size: '1.1 GB', status: 'success', operator: '系统' },
      { backupId: 'BACKUP004', backupTime: '2026-04-06 10:30:00', backupType: 'manual', size: '1.0 GB', status: 'success', operator: 'admin' },
      { backupId: 'BACKUP005', backupTime: '2026-04-06 02:00:00', backupType: 'full', size: '1.0 GB', status: 'success', operator: '系统' },
      { backupId: 'BACKUP006', backupTime: '2026-04-05 02:00:00', backupType: 'full', size: '0.9 GB', status: 'success', operator: '系统' }
    ])
    
    const handleCreateBackup = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('备份创建成功')
        // 模拟添加新备份
        const newBackup = {
          backupId: 'BACKUP' + new Date().getTime(),
          backupTime: new Date().toLocaleString(),
          backupType: 'manual',
          size: '1.2 GB',
          status: 'success',
          operator: 'admin'
        }
        backupList.value.unshift(newBackup)
        loading.value = false
      }, 2000)
    }
    
    const handleRestoreBackup = (backup) => {
      selectedBackup.value = backup
      restoreDialogVisible.value = true
    }
    
    const handleConfirmRestore = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('数据恢复成功')
        restoreDialogVisible.value = false
        selectedBackup.value = null
        loading.value = false
      }, 2000)
    }
    
    const handleDownloadBackup = (backup) => {
      ElMessage.success('备份下载成功')
    }
    
    const handleDeleteBackup = (backup) => {
      ElMessageBox.confirm('确定要删除此备份吗？', '删除备份', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = backupList.value.findIndex(item => item.backupId === backup.backupId)
        if (index !== -1) {
          backupList.value.splice(index, 1)
        }
        ElMessage.success('备份删除成功')
      })
    }
    
    const handleSaveConfig = () => {
      ElMessage.success('配置保存成功')
    }
    
    const handleRefresh = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('刷新成功')
        loading.value = false
      }, 1000)
    }
    
    const handleSizeChange = (size) => {
      pagination.pageSize = size
    }
    
    const handleCurrentChange = (current) => {
      pagination.currentPage = current
    }
    
    const getBackupTypeName = (type) => {
      switch (type) {
        case 'full': return '完整备份'
        case 'incremental': return '增量备份'
        case 'manual': return '手动备份'
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
      console.log('数据备份与恢复页面加载')
    })
    
    return {
      loading, restoreDialogVisible, selectedBackup,
      pagination, total, backupConfig, backupList,
      handleCreateBackup, handleRestoreBackup, handleConfirmRestore,
      handleDownloadBackup, handleDeleteBackup, handleSaveConfig, handleRefresh,
      handleSizeChange, handleCurrentChange, getBackupTypeName, getStatusName
    }
  }
}
</script>

<style scoped>
.data-backup {
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
.sub-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.config-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.backup-list {
  margin-top: 20px;
}
.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
.restore-dialog {
  padding: 20px;
}
.warning-text {
  color: #f56c6c;
  margin-top: 10px;
}
.backup-info {
  margin-top: 20px;
  padding: 10px;
  background: #f9f9f9;
  border-radius: 4px;
}
</style>
