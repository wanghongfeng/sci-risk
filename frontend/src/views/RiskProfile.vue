<template>
  <div class="risk-profile">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>供应商 / 物料 / 区域风险画像</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
            <el-button type="success" size="small" @click="handleExport"><el-icon><Download /></el-icon>导出报告</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <div class="profile-tabs">
          <el-tabs v-model="activeTab" @tab-change="handleTabChange">
            <el-tab-pane label="供应商风险画像" name="supplier" />
            <el-tab-pane label="物料风险画像" name="material" />
            <el-tab-pane label="区域风险画像" name="region" />
          </el-tabs>
        </div>
        <div class="profile-content">
          <!-- 供应商风险画像 -->
          <div v-if="activeTab === 'supplier'" class="supplier-profile">
            <div class="search-container">
              <el-form :inline="true" :model="supplierSearch" class="search-form">
                <el-form-item label="供应商名称"><el-input v-model="supplierSearch.name" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
                <el-form-item label="供应商等级"><el-select v-model="supplierSearch.level" placeholder="请选择" clearable style="width: 120px;"><el-option label="战略级" value="strategic" /><el-option label="核心级" value="core" /><el-option label="一般级" value="general" /></el-select></el-form-item>
                <el-form-item label="风险等级"><el-select v-model="supplierSearch.riskLevel" placeholder="请选择" clearable style="width: 120px;"><el-option label="高风险" value="high" /><el-option label="中风险" value="medium" /><el-option label="低风险" value="low" /></el-select></el-form-item>
                <el-form-item><el-button type="primary" @click="handleSupplierSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetSupplierForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
              </el-form>
            </div>
            <el-table :data="supplierList" style="width: 100%" border stripe>
              <el-table-column prop="supplierId" label="供应商ID" width="120" />
              <el-table-column prop="supplierName" label="供应商名称" min-width="180" show-overflow-tooltip />
              <el-table-column prop="level" label="供应商等级" width="100"><template #default="scope"><el-tag :type="scope.row.level === 'strategic' ? 'primary' : scope.row.level === 'core' ? 'success' : 'info'"> {{ getLevelName(scope.row.level) }}</el-tag></template></el-table-column>
              <el-table-column prop="riskScore" label="风险得分" width="100" align="right" />
              <el-table-column prop="riskLevel" label="风险等级" width="100"><template #default="scope"><el-tag :type="getRiskLevelColor(scope.row.riskLevel)">{{ getRiskLevelName(scope.row.riskLevel) }}</el-tag></template></el-table-column>
              <el-table-column prop="mainRisk" label="主要风险" min-width="150" show-overflow-tooltip />
              <el-table-column prop="lastUpdated" label="更新时间" width="160" />
              <el-table-column label="操作" width="120" fixed="right"><template #default="scope"><el-button type="primary" size="small" @click="handleViewSupplier(scope.row)"><el-icon><View /></el-icon>详情</el-button></template></el-table-column>
            </el-table>
            <div class="pagination-wrapper"><el-pagination v-model:current-page="supplierPagination.currentPage" v-model:page-size="supplierPagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="supplierTotal" @size-change="handleSupplierSizeChange" @current-change="handleSupplierCurrentChange" /></div>
          </div>
          <!-- 物料风险画像 -->
          <div v-if="activeTab === 'material'" class="material-profile">
            <div class="search-container">
              <el-form :inline="true" :model="materialSearch" class="search-form">
                <el-form-item label="物料编码"><el-input v-model="materialSearch.code" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
                <el-form-item label="物料名称"><el-input v-model="materialSearch.name" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
                <el-form-item label="风险等级"><el-select v-model="materialSearch.riskLevel" placeholder="请选择" clearable style="width: 120px;"><el-option label="高风险" value="high" /><el-option label="中风险" value="medium" /><el-option label="低风险" value="low" /></el-select></el-form-item>
                <el-form-item><el-button type="primary" @click="handleMaterialSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetMaterialForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
              </el-form>
            </div>
            <el-table :data="materialList" style="width: 100%" border stripe>
              <el-table-column prop="materialId" label="物料ID" width="120" />
              <el-table-column prop="materialCode" label="物料编码" width="150" />
              <el-table-column prop="materialName" label="物料名称" min-width="180" show-overflow-tooltip />
              <el-table-column prop="category" label="物料类别" width="120" />
              <el-table-column prop="riskScore" label="风险得分" width="100" align="right" />
              <el-table-column prop="riskLevel" label="风险等级" width="100"><template #default="scope"><el-tag :type="getRiskLevelColor(scope.row.riskLevel)">{{ getRiskLevelName(scope.row.riskLevel) }}</el-tag></template></el-table-column>
              <el-table-column prop="supplyChain" label="供应链状态" width="120"><template #default="scope"><el-tag :type="scope.row.supplyChain === 'normal' ? 'success' : 'warning'"> {{ scope.row.supplyChain === 'normal' ? '正常' : '紧张' }}</el-tag></template></el-table-column>
              <el-table-column label="操作" width="120" fixed="right"><template #default="scope"><el-button type="primary" size="small" @click="handleViewMaterial(scope.row)"><el-icon><View /></el-icon>详情</el-button></template></el-table-column>
            </el-table>
            <div class="pagination-wrapper"><el-pagination v-model:current-page="materialPagination.currentPage" v-model:page-size="materialPagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="materialTotal" @size-change="handleMaterialSizeChange" @current-change="handleMaterialCurrentChange" /></div>
          </div>
          <!-- 区域风险画像 -->
          <div v-if="activeTab === 'region'" class="region-profile">
            <div class="search-container">
              <el-form :inline="true" :model="regionSearch" class="search-form">
                <el-form-item label="区域名称"><el-input v-model="regionSearch.name" placeholder="请输入" clearable style="width: 180px;" /></el-form-item>
                <el-form-item label="区域类型"><el-select v-model="regionSearch.type" placeholder="请选择" clearable style="width: 120px;"><el-option label="国家" value="country" /><el-option label="地区" value="region" /><el-option label="城市" value="city" /></el-select></el-form-item>
                <el-form-item label="风险等级"><el-select v-model="regionSearch.riskLevel" placeholder="请选择" clearable style="width: 120px;"><el-option label="高风险" value="high" /><el-option label="中风险" value="medium" /><el-option label="低风险" value="low" /></el-select></el-form-item>
                <el-form-item><el-button type="primary" @click="handleRegionSearch"><el-icon><Search /></el-icon>搜索</el-button><el-button @click="resetRegionForm"><el-icon><Refresh /></el-icon>重置</el-button></el-form-item>
              </el-form>
            </div>
            <el-table :data="regionList" style="width: 100%" border stripe>
              <el-table-column prop="regionId" label="区域ID" width="120" />
              <el-table-column prop="regionName" label="区域名称" min-width="180" show-overflow-tooltip />
              <el-table-column prop="regionType" label="区域类型" width="100"><template #default="scope">{{ getRegionTypeName(scope.row.regionType) }}</template></el-table-column>
              <el-table-column prop="riskScore" label="风险得分" width="100" align="right" />
              <el-table-column prop="riskLevel" label="风险等级" width="100"><template #default="scope"><el-tag :type="getRiskLevelColor(scope.row.riskLevel)">{{ getRiskLevelName(scope.row.riskLevel) }}</el-tag></template></el-table-column>
              <el-table-column prop="riskFactors" label="风险因素" min-width="150" show-overflow-tooltip />
              <el-table-column prop="supplierCount" label="供应商数" width="100" align="right" />
              <el-table-column label="操作" width="120" fixed="right"><template #default="scope"><el-button type="primary" size="small" @click="handleViewRegion(scope.row)"><el-icon><View /></el-icon>详情</el-button></template></el-table-column>
            </el-table>
            <div class="pagination-wrapper"><el-pagination v-model:current-page="regionPagination.currentPage" v-model:page-size="regionPagination.pageSize" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" :total="regionTotal" @size-change="handleRegionSizeChange" @current-change="handleRegionCurrentChange" /></div>
          </div>
        </div>
      </div>
    </el-card>
    <el-dialog v-model="detailDialogVisible" :title="detailTitle" width="800px">
      <el-descriptions v-if="currentItem" :column="1" border>
        <el-descriptions-item v-if="activeTab === 'supplier'" label="供应商ID">{{ currentItem.supplierId }}</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'supplier'" label="供应商名称">{{ currentItem.supplierName }}</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'supplier'" label="供应商等级">{{ getLevelName(currentItem.level) }}</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'material'" label="物料ID">{{ currentItem.materialId }}</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'material'" label="物料编码">{{ currentItem.materialCode }}</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'material'" label="物料名称">{{ currentItem.materialName }}</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'material'" label="物料类别">{{ currentItem.category }}</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'region'" label="区域ID">{{ currentItem.regionId }}</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'region'" label="区域名称">{{ currentItem.regionName }}</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'region'" label="区域类型">{{ getRegionTypeName(currentItem.regionType) }}</el-descriptions-item>
        <el-descriptions-item label="风险得分">{{ currentItem.riskScore }}</el-descriptions-item>
        <el-descriptions-item label="风险等级">{{ getRiskLevelName(currentItem.riskLevel) }}</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'supplier'" label="主要风险">{{ currentItem.mainRisk }}</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'supplier'" label="供应能力">{{ currentItem.supplyCapacity }}%</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'supplier'" label="交付及时率">{{ currentItem.deliveryRate }}%</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'material'" label="供应链状态">{{ currentItem.supplyChain === 'normal' ? '正常' : '紧张' }}</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'material'" label="替代物料">{{ currentItem.alternativeMaterial || '-' }}</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'region'" label="风险因素">{{ currentItem.riskFactors }}</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'region'" label="供应商数">{{ currentItem.supplierCount }}</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'region'" label="影响范围">{{ currentItem.impactScope }}</el-descriptions-item>
        <el-descriptions-item label="风险描述">{{ currentItem.description }}</el-descriptions-item>
        <el-descriptions-item label="建议措施">{{ currentItem.suggestions }}</el-descriptions-item>
        <el-descriptions-item v-if="activeTab === 'supplier'" label="更新时间">{{ currentItem.lastUpdated }}</el-descriptions-item>
      </el-descriptions>
      <template #footer><el-button @click="detailDialogVisible = false">关闭</el-button></template>
    </el-dialog>
  </div>
</template>
<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, Download, Search, View } from '@element-plus/icons-vue'
export default {
  name: 'RiskProfile',
  components: { Refresh, Download, Search, View },
  setup() {
    const loading = ref(false)
    const activeTab = ref('supplier')
    const detailDialogVisible = ref(false)
    const detailTitle = ref('')
    const currentItem = ref(null)
    const supplierSearch = reactive({ name: '', level: '', riskLevel: '' })
    const supplierPagination = reactive({ currentPage: 1, pageSize: 10 })
    const supplierTotal = ref(120)
    const supplierList = ref([
      { supplierId: 'SUP001', supplierName: '青岛海尔供应商有限公司', level: 'strategic', riskScore: 85, riskLevel: 'high', mainRisk: '生产能力不足', supplyCapacity: 75, deliveryRate: 80, lastUpdated: '2026-04-09 10:00:00', description: '主要供应商，生产能力接近饱和', suggestions: '增加产能，寻找备用供应商' },
      { supplierId: 'SUP002', supplierName: '上海物流运输有限公司', level: 'core', riskScore: 65, riskLevel: 'medium', mainRisk: '物流延迟', supplyCapacity: 90, deliveryRate: 75, lastUpdated: '2026-04-09 09:30:00', description: '核心物流供应商，近期出现延迟', suggestions: '优化物流路线，增加运输能力' },
      { supplierId: 'SUP003', supplierName: '深圳电子元件有限公司', level: 'core', riskScore: 45, riskLevel: 'low', mainRisk: '质量波动', supplyCapacity: 85, deliveryRate: 90, lastUpdated: '2026-04-08 16:00:00', description: '核心电子元件供应商，质量稳定', suggestions: '继续保持合作，定期质量检查' },
      { supplierId: 'SUP004', supplierName: '江苏原材料有限公司', level: 'general', riskScore: 75, riskLevel: 'medium', mainRisk: '价格波动', supplyCapacity: 80, deliveryRate: 85, lastUpdated: '2026-04-08 14:00:00', description: '一般原材料供应商，价格波动较大', suggestions: '签订长期合同，锁定价格' },
      { supplierId: 'SUP005', supplierName: '北京科技有限公司', level: 'strategic', riskScore: 90, riskLevel: 'high', mainRisk: '技术风险', supplyCapacity: 95, deliveryRate: 95, lastUpdated: '2026-04-07 10:00:00', description: '战略技术供应商，技术迭代风险', suggestions: '加强技术合作，共同研发' }
    ])
    const materialSearch = reactive({ code: '', name: '', riskLevel: '' })
    const materialPagination = reactive({ currentPage: 1, pageSize: 10 })
    const materialTotal = ref(250)
    const materialList = ref([
      { materialId: 'MAT001', materialCode: 'M-2026-001', materialName: '核心芯片', category: '电子元件', riskScore: 88, riskLevel: 'high', supplyChain: '紧张', alternativeMaterial: '替代芯片A', description: '关键电子元件，供应紧张', suggestions: '增加安全库存，寻找替代供应商' },
      { materialId: 'MAT002', materialCode: 'M-2026-002', materialName: '塑料外壳', category: '包装材料', riskScore: 35, riskLevel: 'low', supplyChain: '正常', alternativeMaterial: '多种替代', description: '通用包装材料，供应稳定', suggestions: '保持现有供应商' },
      { materialId: 'MAT003', materialCode: 'M-2026-003', materialName: '电路板', category: '电子元件', riskScore: 65, riskLevel: 'medium', supplyChain: '正常', alternativeMaterial: '替代电路板B', description: '重要电子元件，供应正常', suggestions: '定期评估供应商' },
      { materialId: 'MAT004', materialCode: 'M-2026-004', materialName: '显示屏', category: '电子元件', riskScore: 75, riskLevel: 'medium', supplyChain: '紧张', alternativeMaterial: '无', description: '显示屏供应紧张', suggestions: '长期合同锁定供应' },
      { materialId: 'MAT005', materialCode: 'M-2026-005', materialName: '螺丝', category: '五金配件', riskScore: 25, riskLevel: 'low', supplyChain: '正常', alternativeMaterial: '多种替代', description: '通用五金配件，供应充足', suggestions: '保持现有供应商' }
    ])
    const regionSearch = reactive({ name: '', type: '', riskLevel: '' })
    const regionPagination = reactive({ currentPage: 1, pageSize: 10 })
    const regionTotal = ref(80)
    const regionList = ref([
      { regionId: 'REG001', regionName: '中国', regionType: 'country', riskScore: 45, riskLevel: 'low', riskFactors: '政策稳定，供应链成熟', supplierCount: 150, impactScope: '全球', description: '中国地区供应链稳定', suggestions: '加强本地化采购' },
      { regionId: 'REG002', regionName: '美国', regionType: 'country', riskScore: 65, riskLevel: 'medium', riskFactors: '贸易政策变化', supplierCount: 80, impactScope: '北美', description: '美国地区贸易政策不稳定', suggestions: '分散采购，减少依赖' },
      { regionId: 'REG003', regionName: '东南亚', regionType: 'region', riskScore: 55, riskLevel: 'medium', riskFactors: '物流基础设施', supplierCount: 120, impactScope: '亚太', description: '东南亚地区物流设施待完善', suggestions: '加强物流网络建设' },
      { regionId: 'REG004', regionName: '欧洲', regionType: 'region', riskScore: 60, riskLevel: 'medium', riskFactors: '环保法规严格', supplierCount: 100, impactScope: '欧洲', description: '欧洲地区环保法规严格', suggestions: '提前合规准备' },
      { regionId: 'REG005', regionName: '中东', regionType: 'region', riskScore: 85, riskLevel: 'high', riskFactors: '地缘政治风险', supplierCount: 40, impactScope: '中东', description: '中东地区地缘政治不稳定', suggestions: '减少高风险地区依赖' }
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
      activeTab.value = tab
    }
    const getLevelName = (level) => {
      switch (level) {
        case 'strategic': return '战略级'
        case 'core': return '核心级'
        case 'general': return '一般级'
        default: return level
      }
    }
    const getRiskLevelColor = (level) => {
      switch (level) {
        case 'high': return 'danger'
        case 'medium': return 'warning'
        case 'low': return 'success'
        default: return 'info'
      }
    }
    const getRiskLevelName = (level) => {
      switch (level) {
        case 'high': return '高风险'
        case 'medium': return '中风险'
        case 'low': return '低风险'
        default: return level
      }
    }
    const getRegionTypeName = (type) => {
      switch (type) {
        case 'country': return '国家'
        case 'region': return '地区'
        case 'city': return '城市'
        default: return type
      }
    }
    const handleSupplierSearch = () => {
      ElMessage.info('搜索功能开发中')
    }
    const resetSupplierForm = () => {
      Object.keys(supplierSearch).forEach(key => {
        supplierSearch[key] = ''
      })
    }
    const handleSupplierSizeChange = (size) => {
      supplierPagination.pageSize = size
    }
    const handleSupplierCurrentChange = (current) => {
      supplierPagination.currentPage = current
    }
    const handleViewSupplier = (supplier) => {
      currentItem.value = supplier
      detailTitle.value = '供应商详情'
      detailDialogVisible.value = true
    }
    const handleMaterialSearch = () => {
      ElMessage.info('搜索功能开发中')
    }
    const resetMaterialForm = () => {
      Object.keys(materialSearch).forEach(key => {
        materialSearch[key] = ''
      })
    }
    const handleMaterialSizeChange = (size) => {
      materialPagination.pageSize = size
    }
    const handleMaterialCurrentChange = (current) => {
      materialPagination.currentPage = current
    }
    const handleViewMaterial = (material) => {
      currentItem.value = material
      detailTitle.value = '物料详情'
      detailDialogVisible.value = true
    }
    const handleRegionSearch = () => {
      ElMessage.info('搜索功能开发中')
    }
    const resetRegionForm = () => {
      Object.keys(regionSearch).forEach(key => {
        regionSearch[key] = ''
      })
    }
    const handleRegionSizeChange = (size) => {
      regionPagination.pageSize = size
    }
    const handleRegionCurrentChange = (current) => {
      regionPagination.currentPage = current
    }
    const handleViewRegion = (region) => {
      currentItem.value = region
      detailTitle.value = '区域详情'
      detailDialogVisible.value = true
    }
    onMounted(() => {
      console.log('风险画像页面加载')
    })
    return {
      loading, activeTab, detailDialogVisible, detailTitle, currentItem, supplierSearch, supplierPagination, supplierTotal, supplierList, materialSearch, materialPagination, materialTotal, materialList, regionSearch, regionPagination, regionTotal, regionList, handleRefresh, handleExport, handleTabChange, getLevelName, getRiskLevelColor, getRiskLevelName, getRegionTypeName, handleSupplierSearch, resetSupplierForm, handleSupplierSizeChange, handleSupplierCurrentChange, handleViewSupplier, handleMaterialSearch, resetMaterialForm, handleMaterialSizeChange, handleMaterialCurrentChange, handleViewMaterial, handleRegionSearch, resetRegionForm, handleRegionSizeChange, handleRegionCurrentChange, handleViewRegion
    }
  }
}
</script>
<style scoped>
.risk-profile {
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
.profile-tabs {
  margin-bottom: 20px;
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