<template>
  <div class="supply-chain-impact">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>供应链影响量化测算</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleCalculate"><el-icon><Calculator /></el-icon>开始测算</el-button>
            <el-button type="success" size="small" @click="handleExport"><el-icon><Download /></el-icon>导出报告</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <div class="calculation-section">
          <el-card class="calculation-card">
            <template #header><span>测算配置</span></template>
            <el-form :model="calculationForm" label-width="120px">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="风险类型">
                    <el-select v-model="calculationForm.riskType" placeholder="请选择" style="width: 100%;">
                      <el-option label="供应商风险" value="supplier" />
                      <el-option label="原材料风险" value="material" />
                      <el-option label="物流风险" value="logistics" />
                      <el-option label="市场风险" value="market" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="影响范围">
                    <el-select v-model="calculationForm.impactScope" placeholder="请选择" style="width: 100%;">
                      <el-option label="单供应商" value="single_supplier" />
                      <el-option label="多供应商" value="multiple_suppliers" />
                      <el-option label="全供应链" value="full_supply_chain" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="时间范围">
                    <el-date-picker v-model="calculationForm.timeRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="width: 100%;" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="置信度">
                    <el-slider v-model="calculationForm.confidence" :min="0" :max="100" :step="5" show-input />
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </el-card>
        </div>
        <div class="results-section">
          <el-card class="results-card">
            <template #header><span>测算结果</span></template>
            <div class="impact-analysis">
              <div class="impact-stats">
                <el-row :gutter="20">
                  <el-col :span="6"><div class="stat-card"><div class="stat-icon" style="background: #f56c6c;"><el-icon><Warning /></el-icon></div><div class="stat-info"><div class="stat-value">¥{{ impactStats.financialLoss }}</div><div class="stat-label">财务损失</div></div></div></el-col>
                  <el-col :span="6"><div class="stat-card"><div class="stat-icon" style="background: #e6a23c;"><el-icon><Clock /></el-icon></div><div class="stat-info"><div class="stat-value">{{ impactStats.deliveryDelay }}天</div><div class="stat-label">交付延迟</div></div></div></el-col>
                  <el-col :span="6"><div class="stat-card"><div class="stat-icon" style="background: #409eff;"><el-icon><Cpu /></el-icon></div><div class="stat-info"><div class="stat-value">{{ impactStats.capacityImpact }}%</div><div class="stat-label">产能影响</div></div></div></el-col>
                  <el-col :span="6"><div class="stat-card"><div class="stat-icon" style="background: #67c23a;"><el-icon><TrendCharts /></el-icon></div><div class="stat-info"><div class="stat-value">{{ impactStats.customerImpact }}%</div><div class="stat-label">客户影响</div></div></div></el-col>
                </el-row>
              </div>
              <div class="impact-breakdown">
                <h4>影响因素分解</h4>
                <div class="breakdown-chart">
                  <div v-for="factor in impactFactors" :key="factor.name" class="factor-item">
                    <div class="factor-name">{{ factor.name }}</div>
                    <div class="factor-bar"><div class="factor-fill" :style="{ width: factor.percentage + '%', backgroundColor: factor.color }"></div></div>
                    <div class="factor-value">{{ factor.value }} ({{ factor.percentage }}%)</div>
                  </div>
                </div>
              </div>
              <div class="impact-details">
                <h4>详细影响分析</h4>
                <el-table :data="impactDetails" style="width: 100%" border stripe>
                  <el-table-column prop="category" label="影响类别" width="120" />
                  <el-table-column prop="item" label="具体项目" min-width="150" show-overflow-tooltip />
                  <el-table-column prop="impactValue" label="影响值" width="120" align="right" />
                  <el-table-column prop="unit" label="单位" width="80" />
                  <el-table-column prop="percentage" label="占比" width="100" align="right"><template #default="scope">{{ scope.row.percentage }}%</template></el-table-column>
                  <el-table-column prop="description" label="说明" min-width="200" show-overflow-tooltip />
                </el-table>
              </div>
              <div class="risk-mitigation">
                <h4>风险缓解建议</h4>
                <div class="suggestions-list">
                  <div v-for="suggestion in mitigationSuggestions" :key="suggestion.id" class="suggestion-item">
                    <el-icon :color="suggestion.priority === 'high' ? '#f56c6c' : suggestion.priority === 'medium' ? '#e6a23c' : '#67c23a'"><Tip /></el-icon>
                    <div class="suggestion-content">
                      <div class="suggestion-title">{{ suggestion.title }}</div>
                      <div class="suggestion-desc">{{ suggestion.description }}</div>
                      <div class="suggestion-impact">预期缓解效果: {{ suggestion.impact }}%</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </el-card>
  </div>
</template>
<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Calculator, Download, Warning, Clock, Cpu, TrendCharts, Tip } from '@element-plus/icons-vue'
export default {
  name: 'SupplyChainImpact',
  components: { Calculator, Download, Warning, Clock, Cpu, TrendCharts, Tip },
  setup() {
    const loading = ref(false)
    const calculationForm = reactive({
      riskType: 'supplier',
      impactScope: 'multiple_suppliers',
      timeRange: null,
      confidence: 80
    })
    const impactStats = reactive({
      financialLoss: 1250000,
      deliveryDelay: 15,
      capacityImpact: 35,
      customerImpact: 25
    })
    const impactFactors = ref([
      { name: '原材料短缺', value: 450000, percentage: 36, color: '#f56c6c' },
      { name: '生产中断', value: 320000, percentage: 26, color: '#e6a23c' },
      { name: '物流延迟', value: 280000, percentage: 22, color: '#409eff' },
      { name: '客户流失', value: 200000, percentage: 16, color: '#67c23a' }
    ])
    const impactDetails = ref([
      { category: '财务影响', item: '直接损失', impactValue: 850000, unit: '元', percentage: 68, description: '原材料价格上涨和生产中断导致的直接损失' },
      { category: '财务影响', item: '间接损失', impactValue: 400000, unit: '元', percentage: 32, description: '客户流失和声誉损失' },
      { category: '运营影响', item: '生产延迟', impactValue: 15, unit: '天', percentage: 60, description: '生产线停工期' },
      { category: '运营影响', item: '交付延迟', impactValue: 10, unit: '天', percentage: 40, description: '产品交付给客户的延迟' },
      { category: '市场影响', item: '市场份额', impactValue: 5, unit: '%', percentage: 60, description: '市场份额下降' },
      { category: '市场影响', item: '客户满意度', impactValue: 15, unit: '%', percentage: 40, description: '客户满意度下降' }
    ])
    const mitigationSuggestions = ref([
      { id: 1, title: '寻找替代供应商', priority: 'high', description: '在不同地区寻找2-3家备用供应商', impact: 65 },
      { id: 2, title: '建立安全库存', priority: 'high', description: '针对关键原材料建立30天安全库存', impact: 50 },
      { id: 3, title: '优化生产计划', priority: 'medium', description: '调整生产计划，优先生产高利润产品', impact: 35 },
      { id: 4, title: '加强供应链监控', priority: 'medium', description: '实施实时供应链监控系统', impact: 40 },
      { id: 5, title: '客户沟通策略', priority: 'low', description: '制定客户沟通计划，减少客户流失', impact: 25 }
    ])
    const handleCalculate = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('测算完成')
        loading.value = false
      }, 2000)
    }
    const handleExport = () => {
      ElMessage.info('导出功能开发中')
    }
    onMounted(() => {
      console.log('供应链影响量化测算页面加载')
    })
    return {
      loading, calculationForm, impactStats, impactFactors, impactDetails, mitigationSuggestions, handleCalculate, handleExport
    }
  }
}
</script>
<style scoped>
.supply-chain-impact {
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
.calculation-section {
  margin-bottom: 20px;
}
.calculation-card {
  margin-bottom: 20px;
}
.results-section {
  margin-top: 20px;
}
.results-card {
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
.impact-breakdown,
.impact-details,
.risk-mitigation {
  margin: 30px 0;
}
.impact-breakdown h4,
.impact-details h4,
.risk-mitigation h4 {
  margin-bottom: 15px;
  font-size: 16px;
  font-weight: 500;
}
.breakdown-chart {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.factor-item {
  margin-bottom: 15px;
}
.factor-name {
  margin-bottom: 5px;
  font-size: 14px;
}
.factor-bar {
  height: 20px;
  background: #e4e7ed;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 5px;
}
.factor-fill {
  height: 100%;
  border-radius: 10px;
  transition: width 0.3s ease;
}
.factor-value {
  font-size: 12px;
  color: #909399;
  text-align: right;
}
.suggestions-list {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.suggestion-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 15px 0;
  border-bottom: 1px solid #e4e7ed;
}
.suggestion-item:last-child {
  border-bottom: none;
}
.suggestion-content {
  flex: 1;
}
.suggestion-title {
  font-weight: 500;
  margin-bottom: 5px;
}
.suggestion-desc {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
  line-height: 1.4;
}
.suggestion-impact {
  font-size: 12px;
  color: #909399;
}
</style>