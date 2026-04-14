<template>
  <div class="risk-event-management">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>风险事件库管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>
              新增事件
            </el-button>
            <el-button type="success" @click="handleImport">
              <el-icon><Upload /></el-icon>
              导入
            </el-button>
            <el-button type="warning" @click="handleExport">
              <el-icon><Download /></el-icon>
              导出
            </el-button>
          </div>
        </div>
      </template>

      <div class="stats-container">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon" style="background-color: #409eff;">
                <el-icon :size="24"><Document /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.totalCount }}</div>
                <div class="stat-label">事件总数</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon" style="background-color: #f56c6c;">
                <el-icon :size="24"><CircleClose /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.highRiskCount }}</div>
                <div class="stat-label">高风险事件</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon" style="background-color: #e6a23c;">
                <el-icon :size="24"><Warning /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.mediumRiskCount }}</div>
                <div class="stat-label">中风险事件</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon" style="background-color: #67c23a;">
                <el-icon :size="24"><CircleCheck /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.lowRiskCount }}</div>
                <div class="stat-label">低风险事件</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <div class="search-container">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="事件类型">
            <el-select v-model="searchForm.eventType" placeholder="请选择" clearable style="width: 150px;">
              <el-option label="关税风险" value="tariff" />
              <el-option label="物流风险" value="logistics" />
              <el-option label="供应风险" value="supply" />
              <el-option label="市场风险" value="market" />
              <el-option label="政策风险" value="policy" />
            </el-select>
          </el-form-item>
          <el-form-item label="风险等级">
            <el-select v-model="searchForm.riskLevel" placeholder="请选择" clearable style="width: 120px;">
              <el-option label="高" value="high" />
              <el-option label="中" value="medium" />
              <el-option label="低" value="low" />
            </el-select>
          </el-form-item>
          <el-form-item label="发生时间">
            <el-date-picker v-model="searchForm.dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="width: 240px;" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button>
            <el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table :data="eventList" style="width: 100%" border stripe>
        <el-table-column prop="eventId" label="事件ID" width="180" />
        <el-table-column prop="eventType" label="事件类型" width="120">
          <template #default="scope">
            <el-tag>{{ getEventTypeName(scope.row.eventType) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="eventTitle" label="事件标题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="riskLevel" label="风险等级" width="100">
          <template #default="scope">
            <el-tag :type="getRiskType(scope.row.riskLevel)">{{ getRiskName(scope.row.riskLevel) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="occurrenceTime" label="发生时间" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'closed' ? 'info' : 'success'">
              {{ scope.row.status === 'closed' ? '已关闭' : '处理中' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleView(scope.row)"><el-icon><View /></el-icon>查看</el-button>
            <el-button type="warning" size="small" @click="handleEdit(scope.row)"><el-icon><Edit /></el-icon>编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row)"><el-icon><Delete /></el-icon>删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
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

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="900px">
      <el-form v-if="currentEvent" :model="editForm" label-width="120px" ref="editFormRef">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="事件ID">{{ currentEvent.eventId }}</el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="事件类型" required>
              <el-select v-model="editForm.eventType" placeholder="请选择" style="width: 100%;">
                <el-option label="关税风险" value="tariff" />
                <el-option label="物流风险" value="logistics" />
                <el-option label="供应风险" value="supply" />
                <el-option label="市场风险" value="market" />
                <el-option label="政策风险" value="policy" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="事件标题" required>
          <el-input v-model="editForm.eventTitle" placeholder="请输入事件标题" style="width: 100%;" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="风险等级" required>
              <el-select v-model="editForm.riskLevel" placeholder="请选择" style="width: 100%;">
                <el-option label="高" value="high" />
                <el-option label="中" value="medium" />
                <el-option label="低" value="low" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="发生时间" required>
              <el-date-picker v-model="editForm.occurrenceTime" type="date" placeholder="选择日期" style="width: 100%;" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="影响区域" required>
          <el-input v-model="editForm.affectedRegion" placeholder="请输入影响区域" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="影响物料" required>
          <el-input v-model="editForm.affectedMaterials" placeholder="请输入影响物料" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="详细描述" required>
          <el-input v-model="editForm.description" type="textarea" :rows="3" placeholder="请输入详细描述" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="处置建议" required>
          <el-input v-model="editForm.suggestion" type="textarea" :rows="3" placeholder="请输入处置建议" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="状态" required>
          <el-select v-model="editForm.status" placeholder="请选择" style="width: 100%;">
            <el-option label="处理中" value="processing" />
            <el-option label="已关闭" value="closed" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
        <el-button type="primary" v-if="isEdit" @click="handleSaveEdit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Upload, Download, Search, Refresh, View, Edit, Delete, Document, CircleClose, Warning, CircleCheck } from '@element-plus/icons-vue'

export default {
  name: 'RiskEventManagement',
  components: {
    Plus, Upload, Download, Search, Refresh, View, Edit, Delete, Document, CircleClose, Warning, CircleCheck
  },
  setup() {
    const dialogVisible = ref(false)
    const dialogTitle = ref('事件详情')
    const currentEvent = ref(null)
    const isEdit = ref(false)
    const editForm = ref({})
    const editFormRef = ref(null)

    const stats = reactive({
      totalCount: 156,
      highRiskCount: 23,
      mediumRiskCount: 67,
      lowRiskCount: 66
    })

    const searchForm = reactive({
      eventType: '',
      riskLevel: '',
      dateRange: []
    })

    const pagination = reactive({
      currentPage: 1,
      pageSize: 10
    })

    const total = ref(0)

    const eventList = ref([
      { eventId: 'EVT20260409001', eventType: 'tariff', eventTitle: '美国对华电子类产品加征25%关税', riskLevel: 'high', occurrenceTime: '2026-04-01', status: 'processing', affectedRegion: '北美', affectedMaterials: '电子元器件', description: '美国宣布对价值2000亿美元的中国商品加征25%关税，涉及电子类产品。', suggestion: '建议寻找替代供应商或调整定价策略。' },
      { eventId: 'EVT20260409002', eventType: 'logistics', eventTitle: '红海航线运输延误', riskLevel: 'medium', occurrenceTime: '2026-03-28', status: 'processing', affectedRegion: '欧洲/中东', affectedMaterials: '家电成品', description: '红海安全形势紧张，多家船公司绕行好望角，导致运输时间延长2-3周。', suggestion: '建议提前备货或选择替代航线。' },
      { eventId: 'EVT20260409003', eventType: 'supply', eventTitle: '东南亚原材料供应商停产', riskLevel: 'medium', occurrenceTime: '2026-03-25', status: 'closed', affectedRegion: '东南亚', affectedMaterials: '塑料粒子', description: '越南供应商因环保检查停产，预计影响一个月供货。', suggestion: '已启动备选供应商。' },
      { eventId: 'EVT20260409004', eventType: 'market', eventTitle: '原材料价格大幅上涨', riskLevel: 'high', occurrenceTime: '2026-03-20', status: 'processing', affectedRegion: '全球', affectedMaterials: '铜/铝', description: '国际铜价上涨15%，铝价上涨10%。', suggestion: '密切监控价格走势，适时锁定价格。' },
      { eventId: 'EVT20260409005', eventType: 'policy', eventTitle: '欧盟环保新法规实施', riskLevel: 'low', occurrenceTime: '2026-03-15', status: 'closed', affectedRegion: '欧洲', affectedMaterials: '家电产品', description: '欧盟发布新的能效标准要求。', suggestion: '已完成产品合规性调整。' }
    ])

    const eventTypeMap = {
      tariff: '关税风险',
      logistics: '物流风险',
      supply: '供应风险',
      market: '市场风险',
      policy: '政策风险'
    }

    const riskMap = {
      high: '高',
      medium: '中',
      low: '低'
    }

    const riskTypeMap = {
      high: 'danger',
      medium: 'warning',
      low: 'success'
    }

    const getEventTypeName = (type) => eventTypeMap[type] || type
    const getRiskName = (level) => riskMap[level] || level
    const getRiskType = (level) => riskTypeMap[level] || ''

    const loadData = async () => {
      try {
        await new Promise(resolve => setTimeout(resolve, 300))
        total.value = eventList.value.length
      } catch (error) {
        ElMessage.error('加载数据失败')
      }
    }

    const handleAdd = () => {
      ElMessage.info('新增事件功能开发中')
    }

    const handleImport = () => {
      ElMessage.info('导入功能开发中')
    }

    const handleExport = () => {
      ElMessage.success('导出成功')
    }

    const handleSearch = () => {
      ElMessage.success('搜索功能开发中')
      loadData()
    }

    const resetForm = () => {
      searchForm.eventType = ''
      searchForm.riskLevel = ''
      searchForm.dateRange = []
      ElMessage.info('已重置筛选条件')
      loadData()
    }

    const handleView = (row) => {
      currentEvent.value = row
      dialogTitle.value = '事件详情'
      isEdit.value = false
      dialogVisible.value = true
    }

    const handleEdit = (row) => {
      currentEvent.value = row
      editForm.value = { ...row }
      dialogTitle.value = '编辑事件'
      isEdit.value = true
      dialogVisible.value = true
    }

    const handleSaveEdit = () => {
      if (editFormRef.value) {
        editFormRef.value.validate((valid) => {
          if (valid) {
            // 模拟保存操作
            setTimeout(() => {
              // 更新事件列表中的数据
              const index = eventList.value.findIndex(item => item.eventId === editForm.value.eventId)
              if (index !== -1) {
                eventList.value[index] = { ...editForm.value }
              }
              ElMessage.success('保存成功')
              dialogVisible.value = false
              loadData()
            }, 500)
          } else {
            ElMessage.error('请填写完整信息')
          }
        })
      }
    }

    const handleDelete = (row) => {
      ElMessageBox.confirm('确定要删除该事件吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 模拟删除操作
        setTimeout(() => {
          // 从事件列表中移除数据
          const index = eventList.value.findIndex(item => item.eventId === row.eventId)
          if (index !== -1) {
            eventList.value.splice(index, 1)
          }
          ElMessage.success('删除成功')
          loadData()
        }, 500)
      }).catch(() => {})
    }

    const handleSizeChange = (val) => {
      pagination.pageSize = val
      loadData()
    }

    const handleCurrentChange = (val) => {
      pagination.currentPage = val
      loadData()
    }

    onMounted(() => {
      loadData()
    })

    return {
      dialogVisible,
      dialogTitle,
      currentEvent,
      isEdit,
      editForm,
      editFormRef,
      stats,
      searchForm,
      pagination,
      total,
      eventList,
      getEventTypeName,
      getRiskName,
      getRiskType,
      handleAdd,
      handleImport,
      handleExport,
      handleSearch,
      resetForm,
      handleView,
      handleEdit,
      handleSaveEdit,
      handleDelete,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.risk-event-management {
  padding: 20px;
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
  display: flex;
  align-items: center;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  margin-right: 15px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.search-container {
  margin-bottom: 20px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
