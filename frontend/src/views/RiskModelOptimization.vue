<template>
  <div class="risk-model-optimization">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>风险模型参数优化</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="handleOptimizeModel"><el-icon><Refresh /></el-icon>优化模型</el-button>
            <el-button type="success" size="small" @click="handleRefresh"><el-icon><Refresh /></el-icon>刷新</el-button>
          </div>
        </div>
      </template>
      <div v-loading="loading">
        <!-- 模型选择和配置 -->
        <div class="model-config">
          <el-form :inline="true" :model="modelConfig" class="config-form">
            <el-form-item label="模型类型"><el-select v-model="modelConfig.modelType" placeholder="请选择" style="width: 180px;"><el-option label="供应链风险模型" value="supply_chain" /><el-option label="市场风险模型" value="market" /><el-option label="政策风险模型" value="policy" /></el-select></el-form-item>
            <el-form-item label="模型版本"><el-select v-model="modelConfig.modelVersion" placeholder="请选择" style="width: 150px;"><el-option label="V1.0" value="v1.0" /><el-option label="V1.1" value="v1.1" /><el-option label="V2.0" value="v2.0" /></el-select></el-form-item>
            <el-form-item><el-button type="primary" @click="handleLoadModel">加载模型</el-button></el-form-item>
          </el-form>
        </div>
        
        <!-- 模型参数配置 -->
        <div class="parameters-section" style="margin-top: 20px;">
          <h3>模型参数配置</h3>
          <el-card shadow="hover" style="margin-bottom: 20px;">
            <div class="params-grid">
              <div v-for="param in modelParams" :key="param.id" class="param-item">
                <el-form-item :label="param.name" style="margin-bottom: 15px;">
                  <el-slider v-model="param.value" :min="param.min" :max="param.max" :step="param.step" :marks="param.marks" show-input />
                  <div class="param-description">{{ param.description }}</div>
                </el-form-item>
              </div>
            </div>
          </el-card>
        </div>
        
        <!-- 模型性能分析 -->
        <div class="performance-section" style="margin-top: 20px;">
          <h3>模型性能分析</h3>
          <el-card shadow="hover">
            <div class="performance-grid">
              <div class="performance-item">
                <div class="performance-label">准确率</div>
                <div class="performance-value">{{ modelPerformance.accuracy }}%</div>
                <el-progress :percentage="modelPerformance.accuracy" :stroke-width="15" :color="getPerformanceColor(modelPerformance.accuracy)" />
              </div>
              <div class="performance-item">
                <div class="performance-label">召回率</div>
                <div class="performance-value">{{ modelPerformance.recall }}%</div>
                <el-progress :percentage="modelPerformance.recall" :stroke-width="15" :color="getPerformanceColor(modelPerformance.recall)" />
              </div>
              <div class="performance-item">
                <div class="performance-label">F1分数</div>
                <div class="performance-value">{{ modelPerformance.f1Score }}%</div>
                <el-progress :percentage="modelPerformance.f1Score" :stroke-width="15" :color="getPerformanceColor(modelPerformance.f1Score)" />
              </div>
              <div class="performance-item">
                <div class="performance-label">精确率</div>
                <div class="performance-value">{{ modelPerformance.precision }}%</div>
                <el-progress :percentage="modelPerformance.precision" :stroke-width="15" :color="getPerformanceColor(modelPerformance.precision)" />
              </div>
            </div>
            
            <!-- 性能趋势 -->
            <div class="performance-trend" style="margin-top: 20px;">
              <h4>性能趋势</h4>
              <div class="trend-placeholder">
                <el-empty description="性能趋势图表" />
              </div>
            </div>
          </el-card>
        </div>
        
        <!-- 优化建议 -->
        <div class="suggestions-section" style="margin-top: 20px;">
          <h3>优化建议</h3>
          <el-card shadow="hover">
            <div class="suggestions-list">
              <div v-for="(suggestion, index) in optimizationSuggestions" :key="index" class="suggestion-item">
                <div class="suggestion-header">
                  <span class="suggestion-title">{{ suggestion.title }}</span>
                  <el-tag :type="suggestion.priority === 'high' ? 'danger' : suggestion.priority === 'medium' ? 'warning' : 'info'">
                    {{ suggestion.priority === 'high' ? '高优先级' : suggestion.priority === 'medium' ? '中优先级' : '低优先级' }}
                  </el-tag>
                </div>
                <div class="suggestion-content">{{ suggestion.content }}</div>
                <div class="suggestion-impact">预期影响: {{ suggestion.impact }}</div>
              </div>
            </div>
          </el-card>
        </div>
        
        <!-- 操作按钮 -->
        <div class="action-buttons" style="margin-top: 20px; display: flex; gap: 10px;">
          <el-button type="primary" @click="handleSaveParameters">保存参数</el-button>
          <el-button type="warning" @click="handleResetParameters">重置参数</el-button>
          <el-button type="info" @click="handleExportModel">导出模型</el-button>
          <el-button type="danger" @click="handleDeleteModel">删除模型</el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'

export default {
  name: 'RiskModelOptimization',
  components: { Refresh },
  setup() {
    const loading = ref(false)
    
    // 模型配置
    const modelConfig = reactive({
      modelType: 'supply_chain',
      modelVersion: 'v2.0'
    })
    
    // 模型参数
    const modelParams = reactive([
      {
        id: 1,
        name: '风险概率权重',
        value: 0.7,
        min: 0,
        max: 1,
        step: 0.01,
        marks: { 0: '0', 0.5: '0.5', 1: '1' },
        description: '风险发生概率的权重系数'
      },
      {
        id: 2,
        name: '影响程度权重',
        value: 0.8,
        min: 0,
        max: 1,
        step: 0.01,
        marks: { 0: '0', 0.5: '0.5', 1: '1' },
        description: '风险影响程度的权重系数'
      },
      {
        id: 3,
        name: '风险传导系数',
        value: 0.6,
        min: 0,
        max: 1,
        step: 0.01,
        marks: { 0: '0', 0.5: '0.5', 1: '1' },
        description: '风险传导的强度系数'
      },
      {
        id: 4,
        name: '预警阈值',
        value: 75,
        min: 0,
        max: 100,
        step: 1,
        marks: { 0: '0', 50: '50', 100: '100' },
        description: '触发预警的风险值阈值'
      },
      {
        id: 5,
        name: '时间衰减因子',
        value: 0.9,
        min: 0.5,
        max: 1,
        step: 0.01,
        marks: { 0.5: '0.5', 0.75: '0.75', 1: '1' },
        description: '历史数据的时间衰减因子'
      },
      {
        id: 6,
        name: '行业调整系数',
        value: 1.2,
        min: 0.5,
        max: 2,
        step: 0.1,
        marks: { 0.5: '0.5', 1: '1', 2: '2' },
        description: '不同行业的风险调整系数'
      }
    ])
    
    // 模型性能
    const modelPerformance = reactive({
      accuracy: 89,
      recall: 85,
      f1Score: 87,
      precision: 91
    })
    
    // 优化建议
    const optimizationSuggestions = reactive([
      {
        title: '调整风险概率权重',
        content: '建议将风险概率权重调整为0.75，以提高模型对高概率风险的识别能力',
        priority: 'high',
        impact: '准确率提升约3%'
      },
      {
        title: '优化时间衰减因子',
        content: '建议将时间衰减因子调整为0.85，使模型更关注近期数据',
        priority: 'medium',
        impact: '召回率提升约2%'
      },
      {
        title: '调整行业调整系数',
        content: '建议根据不同行业设置差异化的调整系数，提高模型的行业适应性',
        priority: 'low',
        impact: '整体性能提升约1%'
      }
    ])
    
    const handleLoadModel = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('模型加载成功')
        loading.value = false
      }, 1000)
    }
    
    const handleOptimizeModel = () => {
      loading.value = true
      setTimeout(() => {
        // 模拟优化结果
        modelPerformance.accuracy = 92
        modelPerformance.recall = 88
        modelPerformance.f1Score = 90
        modelPerformance.precision = 94
        ElMessage.success('模型优化成功')
        loading.value = false
      }, 2000)
    }
    
    const handleSaveParameters = () => {
      ElMessage.success('参数保存成功')
    }
    
    const handleResetParameters = () => {
      // 重置参数到默认值
      modelParams.forEach(param => {
        switch (param.id) {
          case 1: param.value = 0.7; break
          case 2: param.value = 0.8; break
          case 3: param.value = 0.6; break
          case 4: param.value = 75; break
          case 5: param.value = 0.9; break
          case 6: param.value = 1.2; break
        }
      })
      ElMessage.info('参数已重置')
    }
    
    const handleExportModel = () => {
      ElMessage.success('模型导出成功')
    }
    
    const handleDeleteModel = () => {
      ElMessageBox.confirm('确定要删除当前模型吗？', '删除模型', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        ElMessage.success('模型删除成功')
      })
    }
    
    const handleRefresh = () => {
      loading.value = true
      setTimeout(() => {
        ElMessage.success('刷新成功')
        loading.value = false
      }, 1000)
    }
    
    const getPerformanceColor = (value) => {
      if (value >= 90) return '#67c23a'
      if (value >= 80) return '#e6a23c'
      return '#f56c6c'
    }
    
    onMounted(() => {
      console.log('风险模型参数优化页面加载')
    })
    
    return {
      loading, modelConfig, modelParams, modelPerformance, optimizationSuggestions,
      handleLoadModel, handleOptimizeModel, handleSaveParameters, handleResetParameters,
      handleExportModel, handleDeleteModel, handleRefresh, getPerformanceColor
    }
  }
}
</script>

<style scoped>
.risk-model-optimization {
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
.model-config {
  margin-bottom: 20px;
}
.config-form {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
}
.parameters-section {
  margin-top: 20px;
}
.params-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}
.param-item {
  padding: 10px;
  background: #f5f7fa;
  border-radius: 8px;
}
.param-description {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}
.performance-section {
  margin-top: 20px;
}
.performance-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}
.performance-item {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}
.performance-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 10px;
}
.performance-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}
.performance-trend {
  margin-top: 20px;
}
.suggestions-section {
  margin-top: 20px;
}
.suggestions-list {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
}
.suggestion-item {
  margin-bottom: 15px;
  padding: 15px;
  background: #fff;
  border-radius: 8px;
  border-left: 4px solid #409eff;
}
.suggestion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.suggestion-title {
  font-weight: bold;
  font-size: 14px;
}
.suggestion-content {
  margin-bottom: 10px;
  font-size: 14px;
  line-height: 1.5;
}
.suggestion-impact {
  font-size: 12px;
  color: #909399;
}
.action-buttons {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}
</style>