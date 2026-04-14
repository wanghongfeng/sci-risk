<template>
  <div class="supply-chain-master">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>供应链网络主数据</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon>
              新增
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

      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <el-tab-pane label="供应商管理" name="supplier">
          <div class="stats-container">
            <el-row :gutter="20">
              <el-col :span="6">
                <div class="stat-card">
                  <div class="stat-icon" style="background-color: #409eff;">
                    <el-icon :size="24"><OfficeBuilding /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">{{ supplierStats.totalCount }}</div>
                    <div class="stat-label">供应商总数</div>
                  </div>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="stat-card">
                  <div class="stat-icon" style="background-color: #f56c6c;">
                    <el-icon :size="24"><Warning /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">{{ supplierStats.highRiskCount }}</div>
                    <div class="stat-label">高风险供应商</div>
                  </div>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="stat-card">
                  <div class="stat-icon" style="background-color: #e6a23c;">
                    <el-icon :size="24"><Clock /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">{{ supplierStats.mediumRiskCount }}</div>
                    <div class="stat-label">中风险供应商</div>
                  </div>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="stat-card">
                  <div class="stat-icon" style="background-color: #67c23a;">
                    <el-icon :size="24"><CircleCheck /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">{{ supplierStats.lowRiskCount }}</div>
                    <div class="stat-label">低风险供应商</div>
                  </div>
                </div>
              </el-col>
            </el-row>
          </div>

          <div class="search-container">
            <el-form :inline="true" :model="searchForm">
              <el-form-item label="供应商名称">
                <el-input v-model="searchForm.supplierName" placeholder="请输入供应商名称" clearable style="width: 150px;" />
              </el-form-item>
              <el-form-item label="地区">
                <el-select v-model="searchForm.region" placeholder="请选择" clearable style="width: 120px;">
                  <el-option label="北美" value="north_america" />
                  <el-option label="欧洲" value="europe" />
                  <el-option label="东南亚" value="southeast_asia" />
                  <el-option label="日韩" value="japan_korea" />
                  <el-option label="中国" value="china" />
                </el-select>
              </el-form-item>
              <el-form-item label="风险等级">
                <el-select v-model="searchForm.riskLevel" placeholder="请选择" clearable style="width: 120px;">
                  <el-option label="高" value="high" />
                  <el-option label="中" value="medium" />
                  <el-option label="低" value="low" />
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button>
                <el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button>
              </el-form-item>
            </el-form>
          </div>

          <el-table :data="supplierList" style="width: 100%" border stripe>
            <el-table-column prop="supplierCode" label="供应商编码" width="120" />
            <el-table-column prop="supplierName" label="供应商名称" min-width="200" show-overflow-tooltip />
            <el-table-column prop="region" label="地区" width="100">
              <template #default="scope">
                <el-tag>{{ getRegionName(scope.row.region) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="riskLevel" label="风险等级" width="100">
              <template #default="scope">
                <el-tag :type="getRiskType(scope.row.riskLevel)">{{ getRiskName(scope.row.riskLevel) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="contactPerson" label="联系人" width="120" />
            <el-table-column prop="contactPhone" label="联系电话" width="130" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.status === 'active' ? 'success' : 'info'">
                  {{ scope.row.status === 'active' ? '正常' : '停用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="scope">
                <el-button type="primary" size="small" @click="handleView(scope.row)"><el-icon><View /></el-icon>查看</el-button>
                <el-button type="warning" size="small" @click="handleEdit(scope.row)"><el-icon><Edit /></el-icon>编辑</el-button>
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
        </el-tab-pane>

        <el-tab-pane label="物料管理" name="material">
          <div class="search-container">
            <el-form :inline="true" :model="materialSearchForm">
              <el-form-item label="物料编码">
                <el-input v-model="materialSearchForm.materialCode" placeholder="请输入物料编码" clearable style="width: 150px;" />
              </el-form-item>
              <el-form-item label="物料名称">
                <el-input v-model="materialSearchForm.materialName" placeholder="请输入物料名称" clearable style="width: 150px;" />
              </el-form-item>
              <el-form-item label="物料分类">
                <el-select v-model="materialSearchForm.category" placeholder="请选择" clearable style="width: 120px;">
                  <el-option label="原材料" value="raw_material" />
                  <el-option label="电子元器件" value="electronic" />
                  <el-option label="包装材料" value="packaging" />
                  <el-option label="成品" value="finished" />
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleMaterialSearch"><el-icon><Search /></el-icon>搜索</el-button>
                <el-button @click="resetMaterialForm"><el-icon><Refresh /></el-icon>重置</el-button>
              </el-form-item>
            </el-form>
          </div>

          <el-table :data="materialList" style="width: 100%" border stripe>
            <el-table-column prop="materialCode" label="物料编码" width="120" />
            <el-table-column prop="materialName" label="物料名称" min-width="200" show-overflow-tooltip />
            <el-table-column prop="category" label="物料分类" width="120">
              <template #default="scope">
                <el-tag>{{ getCategoryName(scope.row.category) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="unit" label="单位" width="80" />
            <el-table-column prop="supplierCount" label="供应商数量" width="100" />
            <el-table-column prop="stockLevel" label="库存水平" width="100">
              <template #default="scope">
                <el-tag :type="getStockType(scope.row.stockLevel)">{{ scope.row.stockLevel }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="scope">
                <el-button type="primary" size="small" @click="handleMaterialView(scope.row)"><el-icon><View /></el-icon>查看</el-button>
                <el-button type="warning" size="small" @click="handleMaterialEdit(scope.row)"><el-icon><Edit /></el-icon>编辑</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="900px">
      <el-descriptions v-if="currentSupplier" :column="2" border>
        <el-descriptions-item label="供应商编码">{{ currentSupplier.supplierCode }}</el-descriptions-item>
        <el-descriptions-item label="供应商名称">{{ currentSupplier.supplierName }}</el-descriptions-item>
        <el-descriptions-item label="地区">{{ getRegionName(currentSupplier.region) }}</el-descriptions-item>
        <el-descriptions-item label="风险等级">
          <el-tag :type="getRiskType(currentSupplier.riskLevel)">{{ getRiskName(currentSupplier.riskLevel) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="联系人">{{ currentSupplier.contactPerson }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentSupplier.contactPhone }}</el-descriptions-item>
        <el-descriptions-item label="地址" :span="2">{{ currentSupplier.address }}</el-descriptions-item>
        <el-descriptions-item label="主营产品" :span="2">{{ currentSupplier.mainProducts }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentSupplier.remark }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Upload, Download, Search, Refresh, View, Edit, OfficeBuilding, Warning, Clock, CircleCheck } from '@element-plus/icons-vue'

export default {
  name: 'SupplyChainMaster',
  components: {
    Plus, Upload, Download, Search, Refresh, View, Edit, OfficeBuilding, Warning, Clock, CircleCheck
  },
  setup() {
    const activeTab = ref('supplier')
    const dialogVisible = ref(false)
    const dialogTitle = ref('详情')
    const currentSupplier = ref(null)

    const supplierStats = reactive({
      totalCount: 89,
      highRiskCount: 12,
      mediumRiskCount: 31,
      lowRiskCount: 46
    })

    const searchForm = reactive({
      supplierName: '',
      region: '',
      riskLevel: ''
    })

    const materialSearchForm = reactive({
      materialCode: '',
      materialName: '',
      category: ''
    })

    const pagination = reactive({
      currentPage: 1,
      pageSize: 10
    })

    const total = ref(0)

    const supplierList = ref([
      { supplierCode: 'SUP001', supplierName: '深圳华星电子有限公司', region: 'china', riskLevel: 'low', contactPerson: '张经理', contactPhone: '0755-12345678', status: 'active', address: '深圳市南山区科技园', mainProducts: '电子元器件、显示屏', remark: '长期合作伙伴' },
      { supplierCode: 'SUP002', supplierName: '日本村田制作所', region: 'japan_korea', riskLevel: 'low', contactPerson: '田中先生', contactPhone: '+81-3-1234-5678', status: 'active', address: '日本东京都', mainProducts: 'MLCC、电容', remark: '高端供应商' },
      { supplierCode: 'SUP003', supplierName: '德国BASF化工', region: 'europe', riskLevel: 'medium', contactPerson: 'Hans Mueller', contactPhone: '+49-621-123456', status: 'active', address: '德国路德维希港', mainProducts: '化工原材料', remark: '环保合规企业' },
      { supplierCode: 'SUP004', supplierName: '越南福盛塑料制品厂', region: 'southeast_asia', riskLevel: 'high', contactPerson: '阮氏明月', contactPhone: '+84-24-9876543', status: 'active', address: '越南河内工业园', mainProducts: '塑料粒子、包装材料', remark: '需关注环保政策风险' },
      { supplierCode: 'SUP005', supplierName: '墨西哥北美电器公司', region: 'north_america', riskLevel: 'medium', contactPerson: 'John Smith', contactPhone: '+1-512-555-1234', status: 'active', address: '美国德克萨斯州', mainProducts: '家电配件', remark: '贸易摩擦风险' }
    ])

    const materialList = ref([
      { materialCode: 'MAT001', materialName: '铜线', category: 'raw_material', unit: '吨', supplierCount: 5, stockLevel: '正常' },
      { materialCode: 'MAT002', materialName: '塑料粒子PP', category: 'raw_material', unit: '吨', supplierCount: 8, stockLevel: '偏低' },
      { materialCode: 'MAT003', materialName: 'MLCC电容', category: 'electronic', unit: '万个', supplierCount: 3, stockLevel: '正常' },
      { materialCode: 'MAT004', materialName: '纸箱包装', category: 'packaging', unit: '万个', supplierCount: 6, stockLevel: '充足' },
      { materialCode: 'MAT005', materialName: '压缩机', category: 'finished', unit: '台', supplierCount: 2, stockLevel: '偏低' }
    ])

    const regionMap = {
      north_america: '北美',
      europe: '欧洲',
      southeast_asia: '东南亚',
      japan_korea: '日韩',
      china: '中国'
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

    const categoryMap = {
      raw_material: '原材料',
      electronic: '电子元器件',
      packaging: '包装材料',
      finished: '成品'
    }

    const getRegionName = (region) => regionMap[region] || region
    const getRiskName = (level) => riskMap[level] || level
    const getRiskType = (level) => riskTypeMap[level] || ''
    const getCategoryName = (category) => categoryMap[category] || category
    const getStockType = (level) => level === '偏低' ? 'warning' : level === '充足' ? 'success' : ''

    const loadData = async () => {
      try {
        await new Promise(resolve => setTimeout(resolve, 300))
        total.value = supplierList.value.length
      } catch (error) {
        ElMessage.error('加载数据失败')
      }
    }

    const handleTabChange = () => {
      if (activeTab.value === 'supplier') {
        loadData()
      }
    }

    const handleAdd = () => {
      ElMessage.info('新增功能开发中')
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
      searchForm.supplierName = ''
      searchForm.region = ''
      searchForm.riskLevel = ''
      ElMessage.info('已重置筛选条件')
      loadData()
    }

    const handleView = (row) => {
      currentSupplier.value = row
      dialogTitle.value = '供应商详情'
      dialogVisible.value = true
    }

    const handleEdit = (row) => {
      ElMessage.info('编辑功能开发中: ' + row.supplierCode)
    }

    const handleSizeChange = (val) => {
      pagination.pageSize = val
      loadData()
    }

    const handleCurrentChange = (val) => {
      pagination.currentPage = val
      loadData()
    }

    const handleMaterialSearch = () => {
      ElMessage.success('搜索功能开发中')
    }

    const resetMaterialForm = () => {
      materialSearchForm.materialCode = ''
      materialSearchForm.materialName = ''
      materialSearchForm.category = ''
      ElMessage.info('已重置筛选条件')
    }

    const handleMaterialView = (row) => {
      ElMessage.info('查看物料详情: ' + row.materialCode)
    }

    const handleMaterialEdit = (row) => {
      ElMessage.info('编辑物料: ' + row.materialCode)
    }

    onMounted(() => {
      loadData()
    })

    return {
      activeTab,
      dialogVisible,
      dialogTitle,
      currentSupplier,
      supplierStats,
      searchForm,
      materialSearchForm,
      pagination,
      total,
      supplierList,
      materialList,
      getRegionName,
      getRiskName,
      getRiskType,
      getCategoryName,
      getStockType,
      handleTabChange,
      handleAdd,
      handleImport,
      handleExport,
      handleSearch,
      resetForm,
      handleView,
      handleEdit,
      handleSizeChange,
      handleCurrentChange,
      handleMaterialSearch,
      resetMaterialForm,
      handleMaterialView,
      handleMaterialEdit
    }
  }
}
</script>

<style scoped>
.supply-chain-master {
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
