<template>
  <div class="page-container">
    <h2 class="page-title">风险传导路径推演</h2>
    
    <!-- 搜索和筛选 -->
    <div class="search-container">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="风险类型">
          <el-select v-model="searchForm.riskType" placeholder="请选择" style="width: 200px;">
            <el-option label="供应链风险" value="supply_chain" />
            <el-option label="市场风险" value="market" />
            <el-option label="地缘政治风险" value="geopolitical" />
            <el-option label="财务风险" value="financial" />
            <el-option label="技术风险" value="technical" />
          </el-select>
        </el-form-item>
        <el-form-item label="风险等级">
          <el-select v-model="searchForm.riskLevel" placeholder="请选择" style="width: 150px;">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
            <el-option label="极高" value="critical" />
          </el-select>
        </el-form-item>
        <el-form-item label="影响范围">
          <el-select v-model="searchForm.impactScope" placeholder="请选择" style="width: 200px;">
            <el-option label="局部" value="local" />
            <el-option label="区域" value="regional" />
            <el-option label="全球" value="global" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>搜索</el-button>
          <el-button @click="resetForm"><el-icon><Refresh /></el-icon>重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <!-- 风险传导路径图 -->
    <el-card shadow="hover" class="chart-card">
      <template #header>
        <div class="card-header">
          <span>风险传导路径图</span>
          <div class="header-actions">
            <el-button size="small" @click="zoomIn"><el-icon><ZoomIn /></el-icon>放大</el-button>
            <el-button size="small" @click="zoomOut"><el-icon><ZoomOut /></el-icon>缩小</el-button>
            <el-button size="small" @click="resetZoom"><el-icon><Refresh /></el-icon>重置</el-button>
          </div>
        </div>
      </template>
      <div class="chart-wrapper">
        <div ref="propagationChart" class="chart"></div>
      </div>
    </el-card>
    
    <!-- 风险传导分析 -->
    <div class="analysis-container">
      <el-card shadow="hover" class="analysis-card">
        <template #header>
          <div class="card-header">
            <span>风险传导分析</span>
          </div>
        </template>
        <div class="analysis-content">
          <h3>传导路径分析</h3>
          <p>基于当前风险事件，系统分析了可能的传导路径，从源头风险开始，经过中间环节，最终影响到目标节点。</p>
          
          <h4>主要传导路径</h4>
          <el-timeline>
            <el-timeline-item timestamp="2026-04-01" placement="top">
              <el-card>
                <h5>源头风险：原材料价格上涨</h5>
                <p>影响程度：高</p>
                <p>发生概率：75%</p>
              </el-card>
            </el-timeline-item>
            <el-timeline-item timestamp="2026-04-05" placement="top">
              <el-card>
                <h5>中间环节：生产成本增加</h5>
                <p>影响程度：中</p>
                <p>发生概率：80%</p>
              </el-card>
            </el-timeline-item>
            <el-timeline-item timestamp="2026-04-10" placement="top">
              <el-card>
                <h5>中间环节：产品价格上涨</h5>
                <p>影响程度：中</p>
                <p>发生概率：70%</p>
              </el-card>
            </el-timeline-item>
            <el-timeline-item timestamp="2026-04-15" placement="top">
              <el-card>
                <h5>目标节点：市场份额下降</h5>
                <p>影响程度：高</p>
                <p>发生概率：65%</p>
              </el-card>
            </el-timeline-item>
          </el-timeline>
          
          <h3>影响评估</h3>
          <div class="impact-assessment">
            <el-progress :percentage="85" status="warning" label="财务影响" />
            <el-progress :percentage="65" status="warning" label="运营影响" />
            <el-progress :percentage="50" status="info" label="声誉影响" />
            <el-progress :percentage="40" status="info" label="合规影响" />
          </div>
          
          <h3>应对建议</h3>
          <div class="suggestion-list">
            <div class="suggestion-item">
              <el-icon class="suggestion-icon"><Check /></el-icon>
              <span>建立原材料价格预警机制，提前锁定价格</span>
            </div>
            <div class="suggestion-item">
              <el-icon class="suggestion-icon"><Check /></el-icon>
              <span>优化供应链结构，增加供应商多样性</span>
            </div>
            <div class="suggestion-item">
              <el-icon class="suggestion-icon"><Check /></el-icon>
              <span>制定产品价格调整策略，平衡成本与市场竞争力</span>
            </div>
            <div class="suggestion-item">
              <el-icon class="suggestion-icon"><Check /></el-icon>
              <span>加强与客户沟通，提高价格调整的接受度</span>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

// 搜索表单
const searchForm = ref({
  riskType: '',
  riskLevel: '',
  impactScope: ''
})

// 图表引用
const propagationChart = ref(null)
let chartInstance = null

// 处理搜索
const handleSearch = () => {
  console.log('搜索条件:', searchForm.value)
  // 这里可以添加搜索逻辑
}

// 重置表单
const resetForm = () => {
  searchForm.value = {
    riskType: '',
    riskLevel: '',
    impactScope: ''
  }
}

// 放大图表
const zoomIn = () => {
  if (chartInstance) {
    chartInstance.dispatchAction({
      type: 'dataZoom',
      start: 0,
      end: 80
    })
  }
}

// 缩小图表
const zoomOut = () => {
  if (chartInstance) {
    chartInstance.dispatchAction({
      type: 'dataZoom',
      start: 0,
      end: 100
    })
  }
}

// 重置图表
const resetZoom = () => {
  if (chartInstance) {
    chartInstance.dispatchAction({
      type: 'dataZoom',
      start: 0,
      end: 100
    })
  }
}

// 初始化风险传导路径图
const initPropagationChart = () => {
  chartInstance = echarts.init(propagationChart.value)
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}'
    },
    legend: {
      top: '5%',
      left: 'center'
    },
    series: [
      {
        name: '风险传导',
        type: 'graph',
        layout: 'force',
        data: [
          { name: '原材料价格上涨', value: 100, symbolSize: 50, itemStyle: { color: '#F56C6C' } },
          { name: '生产成本增加', value: 80, symbolSize: 40, itemStyle: { color: '#E6A23C' } },
          { name: '产品价格上涨', value: 60, symbolSize: 35, itemStyle: { color: '#E6A23C' } },
          { name: '市场份额下降', value: 90, symbolSize: 45, itemStyle: { color: '#F56C6C' } },
          { name: '利润减少', value: 85, symbolSize: 42, itemStyle: { color: '#F56C6C' } },
          { name: '现金流压力', value: 75, symbolSize: 38, itemStyle: { color: '#E6A23C' } },
          { name: '供应商关系紧张', value: 65, symbolSize: 36, itemStyle: { color: '#E6A23C' } },
          { name: '客户满意度下降', value: 70, symbolSize: 37, itemStyle: { color: '#E6A23C' } }
        ],
        links: [
          { source: '原材料价格上涨', target: '生产成本增加' },
          { source: '生产成本增加', target: '产品价格上涨' },
          { source: '产品价格上涨', target: '市场份额下降' },
          { source: '市场份额下降', target: '利润减少' },
          { source: '利润减少', target: '现金流压力' },
          { source: '原材料价格上涨', target: '供应商关系紧张' },
          { source: '产品价格上涨', target: '客户满意度下降' },
          { source: '客户满意度下降', target: '市场份额下降' }
        ],
        lineStyle: {
          color: 'source',
          curveness: 0.3
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: {
            width: 4
          }
        },
        force: {
          repulsion: 1000,
          edgeLength: 120
        }
      }
    ]
  }
  chartInstance.setOption(option)
  window.addEventListener('resize', () => chartInstance.resize())
}

// 组件挂载后初始化图表
onMounted(() => {
  initPropagationChart()
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

.chart-card {
  margin-bottom: 20px;
  height: 500px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.chart-wrapper {
  height: calc(100% - 40px);
}

.chart {
  width: 100%;
  height: 100%;
}

.analysis-container {
  margin-top: 20px;
}

.analysis-card {
  margin-bottom: 20px;
}

.analysis-content {
  padding: 10px;
}

.analysis-content h3 {
  font-size: 18px;
  font-weight: bold;
  margin: 20px 0 10px 0;
  color: #333;
}

.analysis-content h4 {
  font-size: 16px;
  font-weight: bold;
  margin: 15px 0 10px 0;
  color: #666;
}

.analysis-content p {
  margin: 10px 0;
  line-height: 1.6;
  color: #666;
}

.impact-assessment {
  margin: 20px 0;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.impact-assessment .el-progress {
  margin-bottom: 10px;
}

.suggestion-list {
  margin-top: 15px;
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 10px;
}

.suggestion-icon {
  color: #67C23A;
  font-size: 18px;
}

@media (max-width: 768px) {
  .search-form {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .chart-card {
    height: 400px;
  }
}
</style>
