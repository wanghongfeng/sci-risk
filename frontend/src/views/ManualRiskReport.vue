<template>
  <div class="manual-risk-report">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>人工风险上报</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleNewReport">
              <el-icon><Plus /></el-icon>
              新增上报
            </el-button>
            <el-button type="success" size="small" @click="handleExport">
              <el-icon><Download /></el-icon>
              导出记录
            </el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <div class="stats-container">
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: #409eff;">
                  <el-icon><Document /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.totalReports }}</div>
                  <div class="stat-label">上报总数</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: #e6a23c;">
                  <el-icon><Clock /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.pendingReports }}</div>
                  <div class="stat-label">待处理</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: #67c23a;">
                  <el-icon><SuccessFilled /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.processedReports }}</div>
                  <div class="stat-label">已处理</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: #f56c6c;">
                  <el-icon><Warning /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.highRiskReports }}</div>
                  <div class="stat-label">高风险上报</div>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="search-container">
          <el-form :inline="true" :model="searchForm" class="search-form">
            <el-form-item label="上报编号">
              <el-input v-model="searchForm.reportNo" placeholder="请输入" clearable style="width: 150px;" />
            </el-form-item>
            <el-form-item label="风险类型">
              <el-select v-model="searchForm.riskType" placeholder="请选择" clearable style="width: 140px;">
                <el-option label="贸易风险" value="trade" />
                <el-option label="物流风险" value="logistics" />
                <el-option label="供应风险" value="supply" />
                <el-option label="市场风险" value="market" />
                <el-option label="汇率风险" value="exchange" />
                <el-option label="政策风险" value="policy" />
              </el-select>
            </el-form-item>
            <el-form-item label="风险等级">
              <el-select v-model="searchForm.riskLevel" placeholder="请选择" clearable style="width: 120px;">
                <el-option label="重大风险" value="critical" />
                <el-option label="高风险" value="high" />
                <el-option label="中风险" value="medium" />
                <el-option label="低风险" value="low" />
              </el-select>
            </el-form-item>
            <el-form-item label="处理状态">
              <el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 120px;">
                <el-option label="待处理" value="pending" />
                <el-option label="处理中" value="processing" />
                <el-option label="已处理" value="processed" />
                <el-option label="已关闭" value="closed" />
              </el-select>
            </el-form-item>
            <el-form-item label="上报时间">
              <el-date-picker v-model="searchForm.dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="width: 240px;" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button>
              <el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button>
            </el-form-item>
          </el-form>
        </div>

        <el-table :data="reportList" style="width: 100%" border stripe class="data-table">
          <el-table-column prop="reportNo" label="上报编号" width="150" />
          <el-table-column prop="riskType" label="风险类型" width="100">
            <template #default="scope">
              <el-tag>{{ getRiskTypeName(scope.row.riskType) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="riskTitle" label="风险标题" min-width="200" show-overflow-tooltip />
          <el-table-column prop="riskLevel" label="风险等级" width="100">
            <template #default="scope">
              <el-tag :type="getRiskType(scope.row.riskLevel)">
                {{ getRiskName(scope.row.riskLevel) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="region" label="涉及区域" width="100" />
          <el-table-column prop="reporterName" label="上报人" width="100" />
          <el-table-column prop="reportTime" label="上报时间" width="160" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ getStatusName(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="280" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleView(scope.row)"><el-icon><View /></el-icon>查看</el-button>
              <el-button type="warning" size="small" @click="handleEdit(scope.row)"><el-icon><Edit /></el-icon>编辑</el-button>
              <el-button v-if="scope.row.status === 'pending'" type="danger" size="small" @click="handleDelete(scope.row)"><el-icon><Delete /></el-icon>删除</el-button>
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
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="900px" @closed="handleDialogClosed">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="风险类型" prop="riskType">
              <el-select v-model="form.riskType" placeholder="请选择风险类型" style="width: 100%;">
                <el-option label="贸易风险" value="trade" />
                <el-option label="物流风险" value="logistics" />
                <el-option label="供应风险" value="supply" />
                <el-option label="市场风险" value="market" />
                <el-option label="汇率风险" value="exchange" />
                <el-option label="政策风险" value="policy" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="风险等级" prop="riskLevel">
              <el-select v-model="form.riskLevel" placeholder="请选择风险等级" style="width: 100%;">
                <el-option label="重大风险" value="critical" />
                <el-option label="高风险" value="high" />
                <el-option label="中风险" value="medium" />
                <el-option label="低风险" value="low" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="风险标题" prop="riskTitle">
          <el-input v-model="form.riskTitle" placeholder="请输入风险标题" maxlength="100" show-word-limit />
        </el-form-item>
        <el-form-item label="涉及区域" prop="region">
          <el-input v-model="form.region" placeholder="请输入涉及区域" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="涉及供应商">
              <el-input v-model="form.supplierName" placeholder="请输入供应商名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="涉及物料">
              <el-input v-model="form.materialName" placeholder="请输入物料名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="风险描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="4" placeholder="请详细描述风险情况" maxlength="500" show-word-limit />
        </el-form-item>
        <el-form-item label="影响范围">
          <el-input v-model="form.impactScope" type="textarea" :rows="2" placeholder="请描述风险可能造成的影响范围" maxlength="300" show-word-limit />
        </el-form-item>
        <el-form-item label="建议措施">
          <el-input v-model="form.suggestedAction" type="textarea" :rows="2" placeholder="请输入建议的处理措施" maxlength="300" show-word-limit />
        </el-form-item>
        <el-form-item label="附件上传">
          <el-upload
            ref="uploadRef"
            class="upload-demo"
            action="#"
            :auto-upload="false"
            :limit="5"
            :on-change="handleFileChange"
            :file-list="fileList"
          >
            <el-button type="primary" size="small"><el-icon><Upload /></el-icon>选择文件</el-button>
            <template #tip>
              <div class="el-upload__tip">支持上传图片、文档等文件，单个文件不超过10MB，最多上传5个文件</div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">提交</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="viewDialogVisible" title="上报详情" width="900px">
      <el-descriptions v-if="currentReport" :column="2" border>
        <el-descriptions-item label="上报编号">{{ currentReport.reportNo }}</el-descriptions-item>
        <el-descriptions-item label="风险类型">
          <el-tag>{{ getRiskTypeName(currentReport.riskType) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="风险等级">
          <el-tag :type="getRiskType(currentReport.riskLevel)">
            {{ getRiskName(currentReport.riskLevel) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(currentReport.status)">
            {{ getStatusName(currentReport.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="风险标题" :span="2">{{ currentReport.riskTitle }}</el-descriptions-item>
        <el-descriptions-item label="涉及区域">{{ currentReport.region }}</el-descriptions-item>
        <el-descriptions-item label="涉及供应商">{{ currentReport.supplierName || '-' }}</el-descriptions-item>
        <el-descriptions-item label="涉及物料">{{ currentReport.materialName || '-' }}</el-descriptions-item>
        <el-descriptions-item label="上报人">{{ currentReport.reporterName }}</el-descriptions-item>
        <el-descriptions-item label="上报时间">{{ currentReport.reportTime }}</el-descriptions-item>
        <el-descriptions-item label="风险描述" :span="2">{{ currentReport.description }}</el-descriptions-item>
        <el-descriptions-item label="影响范围" :span="2">{{ currentReport.impactScope || '-' }}</el-descriptions-item>
        <el-descriptions-item label="建议措施" :span="2">{{ currentReport.suggestedAction || '-' }}</el-descriptions-item>
        <el-descriptions-item v-if="currentReport.processingComment" label="处理意见" :span="2">{{ currentReport.processingComment }}</el-descriptions-item>
        <el-descriptions-item v-if="currentReport.processingTime" label="处理时间" :span="2">{{ currentReport.processingTime }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="viewDialogVisible = false">关闭</el-button>
        <el-button v-if="currentReport && currentReport.status !== 'closed'" type="primary" @click="handleProcess(currentReport)">处理</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Download, Document, Clock, SuccessFilled, Warning, Search, Refresh, View, Edit, Delete, Upload } from '@element-plus/icons-vue'

export default {
  name: 'ManualRiskReport',
  components: {
    Plus, Download, Document, Clock, SuccessFilled, Warning, Search, Refresh, View, Edit, Delete, Upload
  },
  setup() {
    const loading = ref(false)
    const dialogVisible = ref(false)
    const viewDialogVisible = ref(false)
    const dialogTitle = ref('新增上报')
    const formRef = ref(null)
    const uploadRef = ref(null)
    const currentReport = ref(null)
    const fileList = ref([])
    const isEdit = ref(false)

    const stats = reactive({
      totalReports: 156,
      pendingReports: 23,
      processedReports: 118,
      highRiskReports: 15
    })

    const searchForm = reactive({
      reportNo: '',
      riskType: '',
      riskLevel: '',
      status: '',
      dateRange: []
    })

    const pagination = reactive({
      currentPage: 1,
      pageSize: 10
    })

    const total = ref(0)

    const form = reactive({
      riskType: '',
      riskLevel: '',
      riskTitle: '',
      region: '',
      supplierName: '',
      materialName: '',
      description: '',
      impactScope: '',
      suggestedAction: ''
    })

    const formRules = {
      riskType: [{ required: true, message: '请选择风险类型', trigger: 'change' }],
      riskLevel: [{ required: true, message: '请选择风险等级', trigger: 'change' }],
      riskTitle: [{ required: true, message: '请输入风险标题', trigger: 'blur' }],
      region: [{ required: true, message: '请输入涉及区域', trigger: 'blur' }],
      description: [{ required: true, message: '请输入风险描述', trigger: 'blur' }]
    }

    const reportList = ref([
      { reportNo: 'MRR20260409001', riskType: 'trade', riskTitle: '美国对华电子元器件加征关税风险', riskLevel: 'high', region: '北美', supplierName: 'ABC Electronics', materialName: '电子元器件', reporterName: '张明', reportTime: '2026-04-09 10:30:00', status: 'pending', description: '美国可能对从中国进口的电子元器件加征更高关税', impactScope: '影响12家供应商，45种物料采购成本', suggestedAction: '建议寻找替代供应商或提前备货' },
      { reportNo: 'MRR20260409002', riskType: 'logistics', riskTitle: '红海航运风险持续影响', riskLevel: 'critical', region: '中东', supplierName: 'XYZ Logistics', materialName: '国际物流服务', reporterName: '李华', reportTime: '2026-04-09 09:15:00', status: 'processing', description: '红海地区安全形势紧张，导致物流成本大幅上升', impactScope: '影响8条物流线路，交付周期延长2-3周', suggestedAction: '建议启用备选物流通道', processingComment: '已启动备选方案评估', processingTime: '2026-04-09 11:00:00' },
      { reportNo: 'MRR20260408001', riskType: 'supply', riskTitle: '东南亚供应商产能波动', riskLevel: 'medium', region: '东南亚', supplierName: 'Delta Manufacturing', materialName: '纺织品', reporterName: '王芳', reportTime: '2026-04-08 14:20:00', status: 'processed', description: '东南亚部分国家政局变动可能影响供应商产能', impactScope: '影响5家供应商，28种物料', suggestedAction: '建议增加安全库存' },
      { reportNo: 'MRR20260407003', riskType: 'exchange', riskTitle: '汇率波动风险预警', riskLevel: 'high', region: '全球', supplierName: '-', materialName: '多币种结算', reporterName: '赵强', reportTime: '2026-04-07 16:45:00', status: 'closed', description: '主要货币汇率出现大幅波动', impactScope: '影响进出口业务成本核算', suggestedAction: '建议锁定汇率合约' }
    ])

    const riskTypeMap = {
      trade: '贸易风险',
      logistics: '物流风险',
      supply: '供应风险',
      market: '市场风险',
      exchange: '汇率风险',
      policy: '政策风险'
    }

    const riskMap = {
      critical: '重大风险',
      high: '高风险',
      medium: '中风险',
      low: '低风险'
    }

    const riskTypeLevelMap = {
      critical: 'danger',
      high: 'warning',
      medium: '',
      low: 'success'
    }

    const statusMap = {
      pending: '待处理',
      processing: '处理中',
      processed: '已处理',
      closed: '已关闭'
    }

    const statusTypeMap = {
      pending: 'warning',
      processing: 'primary',
      processed: 'success',
      closed: 'info'
    }

    const getRiskTypeName = (type) => riskTypeMap[type] || type
    const getRiskName = (level) => riskMap[level] || level
    const getRiskType = (level) => riskTypeLevelMap[level] || ''
    const getStatusName = (status) => statusMap[status] || status
    const getStatusType = (status) => statusTypeMap[status] || ''

    const loadData = async () => {
      loading.value = true
      try {
        await new Promise(resolve => setTimeout(resolve, 500))
        total.value = reportList.value.length
      } finally {
        loading.value = false
      }
    }

    const handleSearch = () => {
      ElMessage.success('搜索功能开发中')
      loadData()
    }

    const resetForm = () => {
      searchForm.reportNo = ''
      searchForm.riskType = ''
      searchForm.riskLevel = ''
      searchForm.status = ''
      searchForm.dateRange = []
      ElMessage.info('已重置筛选条件')
      loadData()
    }

    const handleNewReport = () => {
      isEdit.value = false
      dialogTitle.value = '新增上报'
      resetFormData()
      dialogVisible.value = true
    }

    const handleExport = () => {
      ElMessage.success('正在导出记录...')
    }

    const handleView = (row) => {
      currentReport.value = row
      viewDialogVisible.value = true
    }

    const handleEdit = (row) => {
      isEdit.value = true
      dialogTitle.value = '编辑上报'
      Object.assign(form, row)
      dialogVisible.value = true
    }

    const handleDelete = (row) => {
      ElMessageBox.confirm('确定要删除这条上报记录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        ElMessage.success('删除成功')
        loadData()
      }).catch(() => {})
    }

    const handleProcess = (row) => {
      currentReport.value = row
      viewDialogVisible.value = false
      setTimeout(() => {
        handleEdit(row)
      }, 300)
    }

    const handleFileChange = (file, files) => {
      fileList.value = files
    }

    const handleSubmit = async () => {
      if (!formRef.value) return
      await formRef.value.validate((valid) => {
        if (valid) {
          if (isEdit.value) {
            ElMessage.success('修改成功')
          } else {
            ElMessage.success('提交成功')
          }
          dialogVisible.value = false
          loadData()
        }
      })
    }

    const handleDialogClosed = () => {
      resetFormData()
      fileList.value = []
    }

    const resetFormData = () => {
      form.riskType = ''
      form.riskLevel = ''
      form.riskTitle = ''
      form.region = ''
      form.supplierName = ''
      form.materialName = ''
      form.description = ''
      form.impactScope = ''
      form.suggestedAction = ''
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
      loading,
      dialogVisible,
      viewDialogVisible,
      dialogTitle,
      formRef,
      uploadRef,
      currentReport,
      fileList,
      stats,
      searchForm,
      pagination,
      total,
      reportList,
      form,
      formRules,
      riskTypeMap,
      riskMap,
      riskTypeLevelMap,
      statusMap,
      statusTypeMap,
      getRiskTypeName,
      getRiskName,
      getRiskType,
      getStatusName,
      getStatusType,
      handleSearch,
      resetForm,
      handleNewReport,
      handleExport,
      handleView,
      handleEdit,
      handleDelete,
      handleProcess,
      handleFileChange,
      handleSubmit,
      handleDialogClosed,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.manual-risk-report {
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

.data-table {
  margin-bottom: 20px;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
}
</style>
