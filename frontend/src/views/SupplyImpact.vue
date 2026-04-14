<template>
  <div class="page-container">
    <h2 class="page-title">供应链影响量化测算</h2>
    
    <!-- 搜索和筛选 -->
    <div class="search-container">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="风险事件">
          <el-select v-model="searchForm.riskEvent" placeholder="请选择" style="width: 250px;">
            <el-option label="原材料价格上涨" value="material_price_increase" />
            <el-option label="供应商工厂停产" value="supplier_closure" />
            <el-option label="物流运输中断" value="logistics_disruption" />
            <el-option label="地缘政治冲突" value="geopolitical_conflict" />
            <el-option label="自然灾害" value="natural_disaster" />
          </el-select>
        </el-form-item>
        <el-form-item label="影响范围">
          <el-select v-model="searchForm.impactScope" placeholder="请选择" style="width: 150px;">
            <el-option label="局部" value="local" />
            <el-option label="区域" value="regional" />
            <el-option label="全球" value="global" />
          </el-select>
        </el-form-item>
        <el-form-item label="时间范围">
          <el-date-picker v-model="searchForm.timeRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="width: 300px;" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button>
          <el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <!-- 影响量化指标 -->
    <div class="metrics-container">
      <el-card shadow="hover" class="metric-card">
        <div class="metric-item">
          <div class="metric-value">{{ financialImpact }}</div>
          <div class="metric-label">财务影响 (万元)</div>
        </div>
      </el-card>
      <el-card shadow="hover" class="metric-card">
        <div class="metric-item">
          <div class="metric-value">{{ productionImpact }}%</div>
          <div class="metric-label">生产影响</div>
        </div>
      </el-card>
      <el-card shadow="hover" class="metric-card">
        <div class="metric-item">
          <div class="metric-value">{{ deliveryImpact }}%</div>
          <div class="metric-label">交付影响</div>
        </div>
      </el-card>
      <el-card shadow="hover" class="metric-card">
        <div class="metric-item">
          <div class="metric-value">{{ supplierImpact }}</div>
          <div class="metric-label">受影响供应商</div>
        </div>
      </el-card>
      <el-card shadow="hover" class="metric-card">
        <div class="metric-item">
          <div class="metric-value">{{ materialImpact }}</div>
          <div class="metric-label">受影响物料</div>
        </div>
      </el-card>
    </div>
    
    <!-- 影响趋势图表 -->
    <el-card shadow="hover" class="chart-card">
      <template #header>
        <div class="card-header">
          <span>影响趋势分析</span>
        </div>
      </template>
      <div class="chart-wrapper">
        <div ref="trendChart" class="chart"></div>
      </div>
    </el-card>
    
    <!-- 影响分布图表 -->
    <div class="charts-row">
      <el-card shadow="hover" class="chart-card">
        <template #header>
          <div class="card-header">
            <span>影响类型分布</span>
          </div>
        </template>
        <div class="chart-wrapper">
          <div ref="typeChart" class="chart"></div>
        </div>
      </el-card>
      <el-card shadow="hover" class="chart-card">
        <template #header>
          <div class="card-header">
            <span>影响区域分布</span>
          </div>
        </template>
        <div class="chart-wrapper">
          <div ref="regionChart" class="chart"></div>
        </div>
      </el-card>
    </div>
    
    <!-- 影响详情 -->
    <el-card shadow="hover" class="detail-card">
      <template #header>
        <div class="card-header">
          <span>影响详情</span>
        </div>
      </template>
      <div class="detail-content">
        <h3>受影响供应商列表</h3>
        <el-table :data="affectedSuppliers" style="width: 100%" border stripe>
          <el-table-column prop="supplierId" label="供应商ID" width="120" />
          <el-table-column prop="supplierName" label="供应商名称" min-width="200" show-overflow-tooltip />
          <el-table-column prop="region" label="地区" width="120" />
          <el-table-column prop="impactLevel" label="影响等级" width="100">
            <template #default="scope">
              <el-tag :type="getImpactLevelType(scope.row.impactLevel)">{{ scope.row.impactLevel }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="affectedMaterials" label="受影响物料" min-width="150" show-overflow-tooltip />
          <el-table-column prop="recoveryTime" label="预计恢复时间" width="150" />
        </el-table>
        
        <h3>受影响物料列表</h3>
        <el-table :data="affectedMaterials" style="width: 100%" border stripe>
          <el-table-column prop="materialId" label="物料ID" width="120" />
          <el-table-column prop="materialName" label="物料名称" min-width="200" show-overflow-tooltip />
          <el-table-column prop="category" label="物料类别" width="120" />
          <el-table-column prop="impactLevel" label="影响等级" width="100">
            <template #default="scope">
              <el-tag :type="getImpactLevelType(scope.row.impactLevel)">{{ scope.row.impactLevel }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="stockLevel" label="库存水平" width="100" />
          <el-table-column prop="alternativeSources" label="替代来源" width="120">
            <template #default="scope">
              <el-tag :type="scope.row.alternativeSources ? 'success' : 'danger'">
                {{ scope.row.alternativeSources ? '有' : '无' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

// 搜索表单
const searchForm = ref({
  riskEvent: '',
  impactScope: '',
  timeRange: []
})

// 影响量化指标
const financialImpact = ref(1250)
const productionImpact = ref(35)
const deliveryImpact = ref(42)
const supplierImpact = ref(28)
const materialImpact = ref(45)

// 受影响供应商列表
const affectedSuppliers = ref([
  { supplierId: 'S001', supplierName: '青岛海尔供应链有限公司', region: '中国', impactLevel: '高', affectedMaterials: '芯片、电子元件', recoveryTime: '2026-04-20' },
  { supplierId: 'S002', supplierName: '上海海立集团股份有限公司', region: '中国', impactLevel: '中', affectedMaterials: '压缩机', recoveryTime: '2026-04-15' },
  { supplierId: 'S003', supplierName: '美的集团股份有限公司', region: '中国', impactLevel: '低', affectedMaterials: '电机', recoveryTime: '2026-04-10' },
  { supplierId: 'S004', supplierName: 'LG Electronics Inc.', region: '韩国', impactLevel: '高', affectedMaterials: '显示屏、芯片', recoveryTime: '2026-04-25' },
  { supplierId: 'S005', supplierName: 'Samsung Electronics Co., Ltd.', region: '韩国', impactLevel: '中', affectedMaterials: '芯片、存储设备', recoveryTime: '2026-04-18' }
])

// 受影响物料列表
const affectedMaterials = ref([
  { materialId: 'M001', materialName: 'CPU芯片', category: '电子元件', impactLevel: '高', stockLevel: '低', alternativeSources: false },
  { materialId: 'M002', materialName: '压缩机', category: '机械部件', impactLevel: '中', stockLevel: '中', alternativeSources: true },
  { materialId: 'M003', materialName: '显示屏', category: '电子元件', impactLevel: '高', stockLevel: '低', alternativeSources: false },
  { materialId: 'M004', materialName: '电机', category: '机械部件', impactLevel: '低', stockLevel: '高', alternativeSources: true },
  { materialId: 'M005', materialName: '存储芯片', category: '电子元件', impactLevel: '中', stockLevel: '中', alternativeSources: true }
])

// 图表引用
const trendChart = ref(null)
const typeChart = ref(null)
const regionChart = ref(null)

// 处理搜索
const handleSearch = () => {
  console.log('搜索条件:', searchForm.value)
  // 这里可以添加搜索逻辑
}

// 重置表单
const resetForm = () => {
  searchForm.value = {
    riskEvent: '',
    impactScope: '',
    timeRange: []
  }
}

// 获取影响等级类型
const getImpactLevelType = (level) => {
  const typeMap = {
    '高': 'danger',
    '中': 'warning',
    '低': 'info'
  }
  return typeMap[level] || 'info'
}

// 初始化影响趋势图表
const initTrendChart = () => {
  const chart = echarts.init(trendChart.value)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['财务影响', '生产影响', '交付影响']
    },
    xAxis: {
      type: 'category',
      data: ['1周', '2周', '3周', '4周', '5周', '6周', '7周', '8周']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '财务影响',
        type: 'line',
        data: [1250, 1180, 1100, 950, 820, 700, 600, 500],
        smooth: true,
        lineStyle: {
          color: '#F56C6C'
        }
      },
      {
        name: '生产影响',
        type: 'line',
        data: [35, 32, 28, 25, 20, 15, 10, 5],
        smooth: true,
        lineStyle: {
          color: '#E6A23C'
        }
      },
      {
        name: '交付影响',
        type: 'line',
        data: [42, 38, 35, 30, 25, 20, 15, 10],
        smooth: true,
        lineStyle: {
          color: '#409EFF'
        }
      }
    ]
  }
  chart.setOption(option)
  window.addEventListener('resize', () => chart.resize())
}

// 初始化影响类型分布图表
const initTypeChart = () => {
  const chart = echarts.init(typeChart.value)
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: ['财务影响', '生产影响', '交付影响', '声誉影响', '合规影响']
    },
    series: [
      {
        name: '影响类型',
        type: 'pie',
        radius: '60%',
        center: ['50%', '50%'],
        data: [
          { value: 40, name: '财务影响' },
          { value: 25, name: '生产影响' },
          { value: 20, name: '交付影响' },
          { value: 10, name: '声誉影响' },
          { value: 5, name: '合规影响' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  chart.setOption(option)
  window.addEventListener('resize', () => chart.resize())
}

// 初始化影响区域分布图表
const initRegionChart = () => {
  const chart = echarts.init(regionChart.value)
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: ['中国', '韩国', '日本', '美国', '欧洲', '其他']
    },
    series: [
      {
        name: '影响区域',
        type: 'pie',
        radius: '60%',
        center: ['50%', '50%'],
        data: [
          { value: 45, name: '中国' },
          { value: 25, name: '韩国' },
          { value: 15, name: '日本' },
          { value: 10, name: '美国' },
          { value: 3, name: '欧洲' },
          { value: 2, name: '其他' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  chart.setOption(option)
  window.addEventListener('resize', () => chart.resize())
}

// 组件挂载后初始化图表
onMounted(() => {
  initTrendChart()
  initTypeChart()
  initRegionChart()
})
</script>

<style scoped>
.page-container {
  padding: 20px;
}

.page-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.search-container {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.search-form {
  display: flex;
  align-items: center;
  gap: 10px;
}

.metrics-container {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.metric-card {
  flex: 1;
  min-width: 150px;
}

.metric-item {
  text-align: center;
  padding: 20px 0;
}

.metric-value {
  font-size: 24px;
  font-weight: bold;
  color: #1890ff;
  margin-bottom: 8px;
}

.metric-label {
  font-size: 14px;
  color: #666;
}

.chart-card {
  margin-bottom: 20px;
  height: 400px;
}

.card-header {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.chart-wrapper {
  height: calc(100% - 40px);
}

.chart {
  width: 100%;
  height: 100%;
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.detail-card {
  margin-bottom: 20px;
}

.detail-content {
  padding: 10px;
}

.detail-content h3 {
  font-size: 18px;
  font-weight: bold;
  margin: 20px 0 10px 0;
  color: #333;
}

@media (max-width: 1200px) {
  .charts-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .search-form {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .metrics-container {
    flex-direction: column;
  }
  
  .metric-card {
    min-width: 100%;
  }
  
  .chart-card {
    height: 300px;
  }
}
</style>
