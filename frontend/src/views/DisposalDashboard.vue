<template>
  <div class="page-container">
    <h2 class="page-title">处置进度大屏</h2>
    
    <!-- 统计卡片 -->
    <div class="stats-container">
      <el-card shadow="hover" class="stats-card">
        <div class="stats-item">
          <div class="stats-value">{{ totalTasks }}</div>
          <div class="stats-label">总任务数</div>
        </div>
      </el-card>
      <el-card shadow="hover" class="stats-card">
        <div class="stats-item">
          <div class="stats-value">{{ pendingTasks }}</div>
          <div class="stats-label">待处理</div>
        </div>
      </el-card>
      <el-card shadow="hover" class="stats-card">
        <div class="stats-item">
          <div class="stats-value">{{ inProgressTasks }}</div>
          <div class="stats-label">处理中</div>
        </div>
      </el-card>
      <el-card shadow="hover" class="stats-card">
        <div class="stats-item">
          <div class="stats-value">{{ completedTasks }}</div>
          <div class="stats-label">已完成</div>
        </div>
      </el-card>
      <el-card shadow="hover" class="stats-card">
        <div class="stats-item">
          <div class="stats-value">{{ completionRate }}%</div>
          <div class="stats-label">完成率</div>
        </div>
      </el-card>
    </div>
    
    <!-- 图表区域 -->
    <div class="charts-container">
      <!-- 任务状态分布 -->
      <el-card shadow="hover" class="chart-card">
        <template #header>
          <div class="card-header">
            <span>任务状态分布</span>
          </div>
        </template>
        <div class="chart-wrapper">
          <div ref="statusChart" class="chart"></div>
        </div>
      </el-card>
      
      <!-- 任务趋势 -->
      <el-card shadow="hover" class="chart-card">
        <template #header>
          <div class="card-header">
            <span>任务趋势</span>
          </div>
        </template>
        <div class="chart-wrapper">
          <div ref="trendChart" class="chart"></div>
        </div>
      </el-card>
      
      <!-- 部门任务完成情况 -->
      <el-card shadow="hover" class="chart-card">
        <template #header>
          <div class="card-header">
            <span>部门任务完成情况</span>
          </div>
        </template>
        <div class="chart-wrapper">
          <div ref="departmentChart" class="chart"></div>
        </div>
      </el-card>
      
      <!-- 高优先级任务 -->
      <el-card shadow="hover" class="chart-card">
        <template #header>
          <div class="card-header">
            <span>高优先级任务</span>
          </div>
        </template>
        <div class="priority-tasks">
          <el-table :data="priorityTasks" style="width: 100%" border stripe>
            <el-table-column prop="taskId" label="任务ID" width="120" />
            <el-table-column prop="taskName" label="任务名称" min-width="200" show-overflow-tooltip />
            <el-table-column prop="department" label="负责部门" width="150" />
            <el-table-column prop="assignee" label="负责人" width="120" />
            <el-table-column prop="deadline" label="截止时间" width="180" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)">{{ getStatusName(scope.row.status) }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import * as echarts from 'echarts'

// 统计数据
const totalTasks = ref(128)
const pendingTasks = ref(42)
const inProgressTasks = ref(56)
const completedTasks = ref(30)
const completionRate = computed(() => Math.round((completedTasks.value / totalTasks.value) * 100))

// 高优先级任务
const priorityTasks = ref([
  { taskId: 'T001', taskName: '供应商财务风险处置', department: '采购部', assignee: '张三', deadline: '2026-04-15', status: 'pending' },
  { taskId: 'T002', taskName: '地缘政治风险应对', department: '国际业务部', assignee: '李四', deadline: '2026-04-18', status: 'in_progress' },
  { taskId: 'T003', taskName: '供应链中断风险评估', department: '供应链管理部', assignee: '王五', deadline: '2026-04-20', status: 'pending' },
  { taskId: 'T004', taskName: '市场波动风险分析', department: '市场部', assignee: '赵六', deadline: '2026-04-22', status: 'in_progress' },
  { taskId: 'T005', taskName: '技术风险评估', department: '技术部', assignee: '钱七', deadline: '2026-04-25', status: 'pending' }
])

// 图表引用
const statusChart = ref(null)
const trendChart = ref(null)
const departmentChart = ref(null)

// 状态类型和名称
const getStatusType = (status) => {
  const typeMap = {
    pending: 'info',
    in_progress: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return typeMap[status] || 'info'
}

const getStatusName = (status) => {
  const nameMap = {
    pending: '待处理',
    in_progress: '处理中',
    completed: '已完成',
    failed: '失败'
  }
  return nameMap[status] || status
}

// 初始化状态分布图表
const initStatusChart = () => {
  const chart = echarts.init(statusChart.value)
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      data: ['待处理', '处理中', '已完成', '失败']
    },
    series: [
      {
        name: '任务状态',
        type: 'pie',
        radius: '60%',
        center: ['50%', '50%'],
        data: [
          { value: pendingTasks.value, name: '待处理' },
          { value: inProgressTasks.value, name: '处理中' },
          { value: completedTasks.value, name: '已完成' },
          { value: 10, name: '失败' }
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

// 初始化任务趋势图表
const initTrendChart = () => {
  const chart = echarts.init(trendChart.value)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['新增任务', '完成任务']
    },
    xAxis: {
      type: 'category',
      data: ['1日', '2日', '3日', '4日', '5日', '6日', '7日']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '新增任务',
        type: 'line',
        data: [15, 20, 18, 25, 22, 30, 28],
        smooth: true,
        lineStyle: {
          color: '#409EFF'
        }
      },
      {
        name: '完成任务',
        type: 'line',
        data: [10, 15, 12, 20, 18, 25, 22],
        smooth: true,
        lineStyle: {
          color: '#67C23A'
        }
      }
    ]
  }
  chart.setOption(option)
  window.addEventListener('resize', () => chart.resize())
}

// 初始化部门任务完成情况图表
const initDepartmentChart = () => {
  const chart = echarts.init(departmentChart.value)
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['已完成', '未完成']
    },
    xAxis: {
      type: 'category',
      data: ['采购部', '供应链管理部', '国际业务部', '市场部', '技术部', '财务部']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '已完成',
        type: 'bar',
        data: [8, 6, 5, 4, 3, 4],
        itemStyle: {
          color: '#67C23A'
        }
      },
      {
        name: '未完成',
        type: 'bar',
        data: [12, 8, 7, 6, 5, 6],
        itemStyle: {
          color: '#E6A23C'
        }
      }
    ]
  }
  chart.setOption(option)
  window.addEventListener('resize', () => chart.resize())
}

// 组件挂载后初始化图表
onMounted(() => {
  initStatusChart()
  initTrendChart()
  initDepartmentChart()
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

.stats-container {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.stats-card {
  flex: 1;
  min-width: 150px;
}

.stats-item {
  text-align: center;
  padding: 20px 0;
}

.stats-value {
  font-size: 24px;
  font-weight: bold;
  color: #1890ff;
  margin-bottom: 8px;
}

.stats-label {
  font-size: 14px;
  color: #666;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.chart-card {
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

.priority-tasks {
  height: calc(100% - 40px);
  overflow: auto;
}

@media (max-width: 1200px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-container {
    flex-direction: column;
  }
  
  .stats-card {
    min-width: 100%;
  }
}
</style>
