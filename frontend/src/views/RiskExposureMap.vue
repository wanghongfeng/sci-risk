<template>
  <div class="risk-exposure-map">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>风险暴露地图</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleRefresh">
              <el-icon><Refresh /></el-icon>
              刷新数据
            </el-button>
            <el-button type="success" size="small" @click="handleExport">
              <el-icon><Download /></el-icon>
              导出报告
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
                  <el-icon><MapLocation /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.totalRegions }}</div>
                  <div class="stat-label">监测区域</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: #f56c6c;">
                  <el-icon><Warning /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.highRiskRegions }}</div>
                  <div class="stat-label">高风险区域</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: #e6a23c;">
                  <el-icon><Clock /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.pendingDeal }}</div>
                  <div class="stat-label">待处理暴露点</div>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: #67c23a;">
                  <el-icon><SuccessFilled /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ stats.coveredSuppliers }}</div>
                  <div class="stat-label">覆盖供应商</div>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>

        <el-row :gutter="20" class="content-row">
          <el-col :span="16">
            <el-card class="region-card">
              <template #header>
                <span>区域风险分布</span>
              </template>
              <div class="region-grid">
                <div
                  v-for="region in regionList"
                  :key="region.code"
                  class="region-item"
                  :class="'risk-level-' + region.riskLevel"
                  @click="handleRegionClick(region)"
                >
                  <div class="region-name">{{ region.name }}</div>
                  <div class="region-code">{{ region.code }}</div>
                  <div class="region-risk">
                    <el-tag :type="getRiskType(region.riskLevel)" size="small">
                      {{ getRiskName(region.riskLevel) }}
                    </el-tag>
                  </div>
                  <div class="region-stats">
                    <span>供应商: {{ region.supplierCount }}</span>
                    <span>物料: {{ region.materialCount }}</span>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="breakdown-card">
              <template #header>
                <span>风险等级分布</span>
              </template>
              <div class="breakdown-list">
                <div v-for="item in riskBreakdown" :key="item.level" class="breakdown-item">
                  <div class="breakdown-label">
                    <span class="breakdown-dot" :class="'dot-' + item.level"></span>
                    <span>{{ item.name }}</span>
                  </div>
                  <div class="breakdown-value">
                    <el-progress :percentage="item.percentage" :color="getProgressColor(item.level)" />
                    <span class="breakdown-count">{{ item.count }}个区域</span>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <el-card class="detail-card">
          <template #header>
            <div class="detail-header">
              <span>暴露点详情</span>
              <div class="detail-actions">
                <el-select v-model="filterForm.riskLevel" placeholder="风险等级" clearable size="small" style="width: 120px; margin-right: 10px;">
                  <el-option label="重大风险" value="critical" />
                  <el-option label="高风险" value="high" />
                  <el-option label="中风险" value="medium" />
                  <el-option label="低风险" value="low" />
                </el-select>
                <el-select v-model="filterForm.region" placeholder="区域" clearable size="small" style="width: 120px; margin-right: 10px;">
                  <el-option v-for="region in regionList" :key="region.code" :label="region.name" :value="region.code" />
                </el-select>
                <el-button type="primary" size="small" @click="handleFilter"><el-icon><Search /></el-icon>搜索</el-button>
              </div>
            </div>
          </template>
          <el-table :data="exposureList" style="width: 100%" border stripe>
            <el-table-column prop="exposureId" label="暴露点ID" width="150" />
            <el-table-column prop="region" label="区域" width="100">
              <template #default="scope">
                {{ getRegionName(scope.row.regionCode) }}
              </template>
            </el-table-column>
            <el-table-column prop="supplierName" label="供应商名称" min-width="180" show-overflow-tooltip />
            <el-table-column prop="materialName" label="物料名称" min-width="150" show-overflow-tooltip />
            <el-table-column prop="riskFactor" label="风险因素" min-width="200" show-overflow-tooltip />
            <el-table-column prop="riskLevel" label="风险等级" width="100">
              <template #default="scope">
                <el-tag :type="getRiskType(scope.row.riskLevel)" size="small">
                  {{ getRiskName(scope.row.riskLevel) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="exposureValue" label="暴露值" width="120" align="right">
              <template #default="scope">
                {{ formatNumber(scope.row.exposureValue) }}
              </template>
            </el-table-column>
            <el-table-column prop="updateTime" label="更新时间" width="160" />
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="scope">
                <el-button type="primary" size="small" @click="handleView(scope.row)"><el-icon><View /></el-icon>查看</el-button>
                <el-button type="warning" size="small" @click="handleAnalyze(scope.row)"><el-icon><DataAnalysis /></el-icon>分析</el-button>
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
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="900px">
      <el-descriptions v-if="currentExposure" :column="2" border>
        <el-descriptions-item label="暴露点ID">{{ currentExposure.exposureId }}</el-descriptions-item>
        <el-descriptions-item label="风险等级">
          <el-tag :type="getRiskType(currentExposure.riskLevel)">{{ getRiskName(currentExposure.riskLevel) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="区域">{{ getRegionName(currentExposure.regionCode) }}</el-descriptions-item>
        <el-descriptions-item label="暴露值">{{ formatNumber(currentExposure.exposureValue) }}</el-descriptions-item>
        <el-descriptions-item label="供应商名称" :span="2">{{ currentExposure.supplierName }}</el-descriptions-item>
        <el-descriptions-item label="物料名称" :span="2">{{ currentExposure.materialName }}</el-descriptions-item>
        <el-descriptions-item label="风险因素" :span="2">{{ currentExposure.riskFactor }}</el-descriptions-item>
        <el-descriptions-item label="详细描述" :span="2">{{ currentExposure.description }}</el-descriptions-item>
        <el-descriptions-item label="影响范围" :span="2">{{ currentExposure.impactScope }}</el-descriptions-item>
        <el-descriptions-item label="建议措施" :span="2">{{ currentExposure.suggestedAction }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentExposure.updateTime }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleAnalyzeFromDialog">发起分析</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, Download, MapLocation, Warning, Clock, SuccessFilled, Search, View, DataAnalysis } from '@element-plus/icons-vue'

export default {
  name: 'RiskExposureMap',
  components: {
    Refresh, Download, MapLocation, Warning, Clock, SuccessFilled, Search, View, DataAnalysis
  },
  setup() {
    const loading = ref(false)
    const dialogVisible = ref(false)
    const dialogTitle = ref('暴露点详情')
    const currentExposure = ref(null)

    const stats = reactive({
      totalRegions: 15,
      highRiskRegions: 4,
      pendingDeal: 28,
      coveredSuppliers: 1256
    })

    const regionList = ref([
      { code: 'CN', name: '中国大陆', riskLevel: 'medium', supplierCount: 520, materialCount: 3820 },
      { code: 'US', name: '北美', riskLevel: 'high', supplierCount: 180, materialCount: 1250 },
      { code: 'EU', name: '欧洲', riskLevel: 'low', supplierCount: 156, materialCount: 980 },
      { code: 'SEA', name: '东南亚', riskLevel: 'high', supplierCount: 245, materialCount: 1560 },
      { code: 'ME', name: '中东', riskLevel: 'critical', supplierCount: 32, materialCount: 180 },
      { code: 'AF', name: '非洲', riskLevel: 'high', supplierCount: 28, materialCount: 145 },
      { code: 'SA', name: '南美', riskLevel: 'medium', supplierCount: 45, materialCount: 320 },
      { code: 'EA', name: '东亚', riskLevel: 'medium', supplierCount: 38, materialCount: 280 },
      { code: 'OC', name: '大洋洲', riskLevel: 'low', supplierCount: 12, materialCount: 85 },
      { code: 'SEA2', name: '南亚', riskLevel: 'high', supplierCount: 68, materialCount: 520 },
      { code: 'RU', name: '俄罗斯', riskLevel: 'critical', supplierCount: 25, materialCount: 165 },
      { code: 'CA', name: '中亚', riskLevel: 'medium', supplierCount: 15, materialCount: 95 },
      { code: 'NA', name: '北欧', riskLevel: 'low', supplierCount: 22, materialCount: 145 },
      { code: 'SA2', name: '南非', riskLevel: 'medium', supplierCount: 18, materialCount: 110 },
      { code: 'WA', name: '西非', riskLevel: 'high', supplierCount: 8, materialCount: 45 }
    ])

    const riskBreakdown = ref([
      { level: 'critical', name: '重大风险', count: 2, percentage: 13 },
      { level: 'high', name: '高风险', count: 6, percentage: 40 },
      { level: 'medium', name: '中风险', count: 4, percentage: 27 },
      { level: 'low', name: '低风险', count: 3, percentage: 20 }
    ])

    const filterForm = reactive({
      riskLevel: '',
      region: ''
    })

    const pagination = reactive({
      currentPage: 1,
      pageSize: 10
    })

    const total = ref(0)

    const exposureList = ref([
      { exposureId: 'EXP20260409001', regionCode: 'US', region: '北美', supplierName: 'ABC Electronics Corp', materialName: '电子元器件-A001', riskFactor: '贸易政策风险', riskLevel: 'high', exposureValue: 2580000, updateTime: '2026-04-09 10:30:00', description: '美国可能对部分电子产品加征关税', impactScope: '影响12家供应商，45种物料', suggestedAction: '建议寻找替代供应商或调整采购策略' },
      { exposureId: 'EXP20260409002', regionCode: 'ME', region: '中东', supplierName: 'XYZ Logistics LLC', materialName: '国际物流服务', riskFactor: '地缘政治风险', riskLevel: 'critical', exposureValue: 5200000, updateTime: '2026-04-09 09:15:00', description: '红海航运风险持续，可能影响货物交付', impactScope: '影响8条物流线路', suggestedAction: '建议启用备选物流通道' },
      { exposureId: 'EXP20260409003', regionCode: 'SEA', region: '东南亚', supplierName: 'Delta Manufacturing', materialName: '纺织品-布料类', riskFactor: '汇率波动风险', riskLevel: 'high', exposureValue: 1850000, updateTime: '2026-04-09 08:00:00', description: '东南亚货币贬值压力增大', impactScope: '影响5家供应商，28种物料', suggestedAction: '建议锁定汇率合约' },
      { exposureId: 'EXP20260409004', regionCode: 'CN', region: '中国大陆', supplierName: '华东制材料', materialName: '塑料粒子-PR001', riskFactor: '环保政策风险', riskLevel: 'medium', exposureValue: 980000, updateTime: '2026-04-08 16:45:00', description: '部分地区环保限产可能影响供应', impactScope: '影响3家供应商，15种物料', suggestedAction: '建议增加安全库存' },
      { exposureId: 'EXP20260409005', regionCode: 'RU', region: '俄罗斯', supplierName: 'Russian Steel Inc', materialName: '钢材-冷轧板', riskFactor: '制裁风险', riskLevel: 'critical', exposureValue: 3200000, updateTime: '2026-04-08 14:20:00', description: '制裁升级可能影响正常贸易', impactScope: '影响6家供应商，32种物料', suggestedAction: '建议转移采购渠道' }
    ])

    const riskMap = {
      critical: '重大风险',
      high: '高风险',
      medium: '中风险',
      low: '低风险'
    }

    const riskTypeMap = {
      critical: 'danger',
      high: 'warning',
      medium: '',
      low: 'success'
    }

    const progressColorMap = {
      critical: '#f56c6c',
      high: '#e6a23c',
      medium: '#409eff',
      low: '#67c23a'
    }

    const getRiskName = (level) => riskMap[level] || level
    const getRiskType = (level) => riskTypeMap[level] || ''
    const getProgressColor = (level) => progressColorMap[level] || '#409eff'

    const getRegionName = (code) => {
      const region = regionList.value.find(r => r.code === code)
      return region ? region.name : code
    }

    const formatNumber = (num) => {
      return num.toLocaleString('zh-CN')
    }

    const loadData = async () => {
      loading.value = true
      try {
        await new Promise(resolve => setTimeout(resolve, 500))
        total.value = exposureList.value.length
      } finally {
        loading.value = false
      }
    }

    const handleRefresh = () => {
      ElMessage.success('正在刷新数据...')
      setTimeout(() => {
        ElMessage.success('数据刷新完成')
        loadData()
      }, 1000)
    }

    const handleExport = () => {
      ElMessage.success('正在生成导出报告...')
    }

    const handleRegionClick = (region) => {
      ElMessage.info(`查看区域: ${region.name}`)
      filterForm.region = region.code
      loadData()
    }

    const handleFilter = () => {
      ElMessage.success('筛选条件已应用')
      loadData()
    }

    const handleView = (row) => {
      currentExposure.value = row
      dialogTitle.value = '暴露点详情'
      dialogVisible.value = true
    }

    const handleAnalyze = (row) => {
      currentExposure.value = row
      ElMessage.success('正在分析暴露点: ' + row.exposureId)
    }

    const handleAnalyzeFromDialog = () => {
      if (currentExposure.value) {
        ElMessage.success('正在分析暴露点: ' + currentExposure.value.exposureId)
        dialogVisible.value = false
      }
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
      dialogTitle,
      currentExposure,
      stats,
      regionList,
      riskBreakdown,
      filterForm,
      pagination,
      total,
      exposureList,
      getRiskName,
      getRiskType,
      getProgressColor,
      getRegionName,
      formatNumber,
      handleRefresh,
      handleExport,
      handleRegionClick,
      handleFilter,
      handleView,
      handleAnalyze,
      handleAnalyzeFromDialog,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.risk-exposure-map {
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

.content-row {
  margin-bottom: 20px;
}

.region-card {
  height: 100%;
}

.region-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 15px;
}

.region-item {
  padding: 15px;
  border-radius: 8px;
  background: #f5f7fa;
  cursor: pointer;
  transition: all 0.3s;
  border-left: 4px solid #409eff;
}

.region-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.region-item.risk-level-critical {
  border-left-color: #f56c6c;
  background: #fef0f0;
}

.region-item.risk-level-high {
  border-left-color: #e6a23c;
  background: #fdf6ec;
}

.region-item.risk-level-medium {
  border-left-color: #409eff;
  background: #ecf5ff;
}

.region-item.risk-level-low {
  border-left-color: #67c23a;
  background: #f0f9eb;
}

.region-name {
  font-size: 14px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.region-code {
  font-size: 12px;
  color: #909399;
  margin-bottom: 8px;
}

.region-risk {
  margin-bottom: 8px;
}

.region-stats {
  font-size: 11px;
  color: #606266;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.breakdown-card {
  height: 100%;
}

.breakdown-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.breakdown-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.breakdown-label {
  display: flex;
  align-items: center;
  min-width: 100px;
}

.breakdown-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 8px;
}

.breakdown-dot.dot-critical {
  background: #f56c6c;
}

.breakdown-dot.dot-high {
  background: #e6a23c;
}

.breakdown-dot.dot-medium {
  background: #409eff;
}

.breakdown-dot.dot-low {
  background: #67c23a;
}

.breakdown-value {
  flex: 1;
  margin-left: 15px;
  display: flex;
  align-items: center;
}

.breakdown-count {
  margin-left: 10px;
  font-size: 12px;
  color: #909399;
  min-width: 70px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-actions {
  display: flex;
  align-items: center;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
