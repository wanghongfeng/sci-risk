<template>
  <div class="dashboard" :style="dashboardStyle">
    <el-row :gutter="gutter" class="stat-row">
      <el-col v-for="item in statCards" :key="item.title" :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-info">
              <div class="stat-title">{{ item.title }}</div>
              <div class="stat-value">{{ item.value }}</div>
              <div class="stat-change" :class="item.changeType">
                <span>{{ item.change }}</span>
                <el-icon v-if="item.changeType === 'up'"><Top /></el-icon>
                <el-icon v-else><Bottom /></el-icon>
              </div>
            </div>
            <div class="stat-icon" :style="{ background: item.bgColor }">
              <el-icon :size="iconSize" :color="item.color"><component :is="item.icon" /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="gutter" class="chart-row">
      <el-col :xs="24" :lg="14">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">风险趋势分析</div>
          </template>
          <div ref="riskTrendChart" class="chart" :style="{ height: chartHeight }"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :lg="10">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">全球风险分布</div>
          </template>
          <div ref="globeContainer" class="globe" :style="{ height: chartHeight }"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="gutter" class="chart-row">
      <el-col :xs="24" :lg="8">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">风险类型分布</div>
          </template>
          <div ref="riskTypeChart" class="chart" :style="{ height: smallChartHeight }"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :lg="8">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">地区风险排名</div>
          </template>
          <div ref="regionRankChart" class="chart" :style="{ height: smallChartHeight }"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :lg="8">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">风险预警</div>
          </template>
          <el-table :data="warningList" :size="tableSize">
            <el-table-column prop="region" label="地区" />
            <el-table-column prop="level" label="级别" width="80">
              <template #default="{ row }">
                <el-tag :type="row.levelType" :size="tableSize">{{ row.level }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import * as d3 from 'd3'
import * as topojson from 'topojson-client'
import { Top, Bottom, Warning, TrendCharts, Money, DataLine } from '@element-plus/icons-vue'

const riskTrendChart = ref(null)
const riskTypeChart = ref(null)
const regionRankChart = ref(null)
const globeContainer = ref(null)

let trendChart = null
let typeChart = null
let rankChart = null
let globeInterval = null

const windowWidth = ref(window.innerWidth)
const windowHeight = ref(window.innerHeight)

const gutter = computed(() => 10)

const iconSize = computed(() => {
  if (windowWidth.value < 768) return 24
  if (windowWidth.value < 1200) return 28
  return 32
})

const chartHeight = computed(() => {
  if (windowWidth.value < 768) return '240px'
  if (windowWidth.value < 1200) return '280px'
  return '320px'
})

const smallChartHeight = computed(() => {
  if (windowWidth.value < 768) return '200px'
  if (windowWidth.value < 1200) return '240px'
  return '280px'
})

const tableSize = computed(() => windowWidth.value < 768 ? 'small' : 'default')

const dashboardStyle = computed(() => ({
  padding: '5px',
  fontSize: windowWidth.value < 768 ? '12px' : '14px',
  height: '100%',
  boxSizing: 'border-box'
}))

const statCards = [
  { title: '风险事件', value: '1,234', change: '+12.5%', changeType: 'up', icon: Warning, color: '#ff4d4f', bgColor: '#fff1f0' },
  { title: '受影响区域', value: '56', change: '+3', changeType: 'up', icon: DataLine, color: '#1890ff', bgColor: '#e6f7ff' },
  { title: '高风险企业', value: '89', change: '-5.2%', changeType: 'down', icon: TrendCharts, color: '#faad14', bgColor: '#fffbe6' },
  { title: '涉及金额(亿)', value: '12.8', change: '+8.1%', changeType: 'up', icon: Money, color: '#52c41a', bgColor: '#f6ffed' }
]

const warningList = ref([
  { region: '北美地区', level: '高', levelType: 'danger' },
  { region: '欧洲地区', level: '中', levelType: 'warning' },
  { region: '亚太地区', level: '低', levelType: 'success' },
  { region: '中东地区', level: '高', levelType: 'danger' },
  { region: '非洲地区', level: '中', levelType: 'warning' }
])

const getFontSize = (base) => {
  const scale = Math.min(windowWidth.value / 1920, windowHeight.value / 1080)
  return Math.round(base * scale)
}

const initRiskTrendChart = () => {
  if (!riskTrendChart.value) return
  trendChart = echarts.init(riskTrendChart.value)

  const fontSize = getFontSize(14)

  const option = {
    tooltip: { trigger: 'axis', textStyle: { fontSize } },
    legend: { data: ['关税风险', '供应链风险', '物流风险'], textStyle: { fontSize } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: ['1月', '2月', '3月', '4月', '5月', '6月'],
      axisLabel: { fontSize }
    },
    yAxis: { type: 'value', axisLabel: { fontSize } },
    series: [
      {
        name: '关税风险',
        type: 'line',
        smooth: true,
        data: [120, 132, 101, 134, 90, 230],
        areaStyle: { opacity: 0.3 },
        lineStyle: { color: '#1890ff' },
        itemStyle: { color: '#1890ff' }
      },
      {
        name: '供应链风险',
        type: 'line',
        smooth: true,
        data: [220, 182, 191, 234, 290, 330],
        areaStyle: { opacity: 0.3 },
        lineStyle: { color: '#faad14' },
        itemStyle: { color: '#faad14' }
      },
      {
        name: '物流风险',
        type: 'line',
        smooth: true,
        data: [150, 232, 201, 154, 190, 330],
        areaStyle: { opacity: 0.3 },
        lineStyle: { color: '#ff4d4f' },
        itemStyle: { color: '#ff4d4f' }
      }
    ]
  }

  trendChart.setOption(option)
}

const initRiskTypeChart = () => {
  if (!riskTypeChart.value) return
  typeChart = echarts.init(riskTypeChart.value)

  const fontSize = getFontSize(14)

  const option = {
    tooltip: { trigger: 'item', textStyle: { fontSize } },
    legend: { bottom: '5%', left: 'center', textStyle: { fontSize } },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
      label: { show: false },
      emphasis: { label: { show: true, fontSize: fontSize + 2, fontWeight: 'bold' } },
      data: [
        { value: 40, name: '关税风险', itemStyle: { color: '#1890ff' } },
        { value: 25, name: '供应中断', itemStyle: { color: '#faad14' } },
        { value: 20, name: '物流延迟', itemStyle: { color: '#ff4d4f' } },
        { value: 15, name: '需求波动', itemStyle: { color: '#52c41a' } }
      ]
    }]
  }

  typeChart.setOption(option)
}

const initRegionRankChart = () => {
  if (!regionRankChart.value) return
  rankChart = echarts.init(regionRankChart.value)

  const fontSize = getFontSize(14)

  const option = {
    tooltip: { trigger: 'axis', textStyle: { fontSize } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'value', axisLabel: { fontSize } },
    yAxis: {
      type: 'category',
      data: ['非洲', '中东', '亚太', '欧洲', '北美'],
      axisLabel: { fontSize }
    },
    series: [{
      type: 'bar',
      data: [35, 45, 60, 75, 90],
      itemStyle: {
        color: (params) => ['#52c41a', '#faad14', '#1890ff', '#ff4d4f', '#ff4d4f'][params.dataIndex],
        borderRadius: [0, 4, 4, 0]
      },
      barWidth: '50%'
    }]
  }

  rankChart.setOption(option)
}

const initGlobe = async () => {
  if (!globeContainer.value) return

  d3.select(globeContainer.value).select('svg').remove()
  if (globeInterval) { clearInterval(globeInterval); globeInterval = null }

  const container = globeContainer.value
  const width = container.clientWidth
  const height = parseInt(chartHeight.value)
  if (!width || !height) return

  const R = Math.min(width, height) * 0.44
  const cx = width / 2, cy = height / 2

  // ── Fetch world topojson ──────────────────────────────────────
  let world
  try {
    world = await d3.json('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json')
  } catch {
    // fallback: just draw plain sphere if offline
    world = null
  }

  const svg = d3.select(container)
    .append('svg')
    .attr('width', width).attr('height', height)
    .style('background', '#f0f2f5')
    .style('border-radius', '8px')

  const defs = svg.append('defs')

  // Globe gradient
  const grad = defs.append('radialGradient').attr('id', 'gGrad').attr('cx', '35%').attr('cy', '28%')
  grad.append('stop').attr('offset', '0%').attr('stop-color', '#5aade0')
  grad.append('stop').attr('offset', '100%').attr('stop-color', '#1a6ab5')

  // Outer glow ring
  const glowG = defs.append('radialGradient').attr('id', 'glowRing').attr('cx', '50%').attr('cy', '50%').attr('r', '50%')
  glowG.append('stop').attr('offset', '70%').attr('stop-color', 'transparent')
  glowG.append('stop').attr('offset', '100%').attr('stop-color', 'rgba(24,144,255,0.22)')

  // Point glow filter
  const filt = defs.append('filter').attr('id', 'ptGlow').attr('x', '-80%').attr('y', '-80%').attr('width', '260%').attr('height', '260%')
  filt.append('feGaussianBlur').attr('stdDeviation', '2.5').attr('result', 'blur')
  const fm = filt.append('feMerge')
  fm.append('feMergeNode').attr('in', 'blur')
  fm.append('feMergeNode').attr('in', 'SourceGraphic')

  const projection = d3.geoOrthographic()
    .scale(R).translate([cx, cy]).clipAngle(90).precision(0.3)

  const pathGen = d3.geoPath().projection(projection)
  const graticule = d3.geoGraticule()

  // ── Drawing layers (order matters) ──────────────────────────
  // 1. Ocean base circle
  svg.append('circle').attr('cx', cx).attr('cy', cy).attr('r', R)
    .attr('fill', 'url(#gGrad)')

  // 2. Graticule grid
  const gridPath = svg.append('path')
    .datum(graticule())
    .attr('fill', 'none')
    .attr('stroke', 'rgba(90,160,220,0.25)')
    .attr('stroke-width', 0.5)

  // 3. Land
  const landGroup = svg.append('g')
  if (world) {
    const countries = topojson.feature(world, world.objects.countries)
    landGroup.selectAll('path')
      .data(countries.features)
      .join('path')
      .attr('fill', '#3a9e6a')
      .attr('fill-opacity', 0.88)
      .attr('stroke', 'rgba(30,130,60,0.7)')
      .attr('stroke-width', 0.4)
  }

  // 4. Country borders (mesh, no coastline duplication)
  const borderPath = world ? svg.append('path')
    .datum(topojson.mesh(world, world.objects.countries, (a, b) => a !== b))
    .attr('fill', 'none')
    .attr('stroke', 'rgba(30,110,50,0.45)')
    .attr('stroke-width', 0.5)
    : null

  // 5. Outer glow ring on top of sphere
  svg.append('circle').attr('cx', cx).attr('cy', cy).attr('r', R)
    .attr('fill', 'url(#glowRing)')
    .attr('pointer-events', 'none')

  // ── Risk hotspots [lng, lat, dotR, color, label] ─────────────
  const riskData = [
    [-74.0,  40.7, 9,  '#ff4d4f', '纽约'],
    [116.4,  39.9, 11, '#ff4d4f', '北京'],
    [121.5,  31.2, 8,  '#faad14', '上海'],
    [  2.4,  48.9, 7,  '#faad14', '巴黎'],
    [ 37.6,  55.8, 8,  '#faad14', '莫斯科'],
    [ 31.2,  30.1, 9,  '#ff4d4f', '开罗'],
    [ 55.3,  25.2, 8,  '#ff4d4f', '迪拜'],
    [103.8,   1.4, 6,  '#1890ff', '新加坡'],
    [ 28.0, -26.2, 7,  '#faad14', '约翰内斯堡'],
    [-43.2, -22.9, 7,  '#faad14', '里约'],
    [139.7,  35.7, 7,  '#1890ff', '东京'],
    [ 72.9,  19.1, 8,  '#faad14', '孟买'],
    [-87.6,  41.9, 6,  '#1890ff', '芝加哥'],
    [151.2, -33.9, 5,  '#1890ff', '悉尼'],
    [ -3.7,  40.4, 6,  '#faad14', '马德里'],
    [ 18.1,  59.3, 5,  '#1890ff', '斯德哥尔摩'],
    [126.9,  37.6, 6,  '#1890ff', '首尔'],
    [-99.1,  19.4, 7,  '#faad14', '墨西哥城'],
    [ 77.1,  28.6, 8,  '#ff4d4f', '新德里'],
  ]

  const pointGs = riskData.map(([lng, lat, r, color, label], i) => {
    const g = svg.append('g').attr('opacity', 0).style('cursor', 'default')

    // Pulse ring (SVG SMIL animation)
    const ring = g.append('circle').attr('r', r).attr('fill', 'none')
      .attr('stroke', color).attr('stroke-width', 1.4).attr('opacity', 0)
    ring.append('animate').attr('attributeName', 'r')
      .attr('from', r).attr('to', r * 3.8)
      .attr('dur', '2.2s').attr('begin', `${(i * 0.15) % 2.2}s`).attr('repeatCount', 'indefinite')
    ring.append('animate').attr('attributeName', 'opacity')
      .attr('values', '0.9;0').attr('dur', '2.2s')
      .attr('begin', `${(i * 0.15) % 2.2}s`).attr('repeatCount', 'indefinite')

    // Halo
    g.append('circle').attr('r', r * 1.7).attr('fill', color).attr('fill-opacity', 0.15)
      .attr('filter', 'url(#ptGlow)')

    // Center dot
    g.append('circle').attr('r', r * 0.48).attr('fill', color).attr('filter', 'url(#ptGlow)')

    // Label (shown when near facing center)
    const txt = g.append('text')
      .attr('y', -(r * 1.5 + 3))
      .attr('text-anchor', 'middle')
      .attr('fill', color)
      .attr('font-size', Math.max(9, r * 1.1))
      .attr('font-family', 'sans-serif')
      .attr('paint-order', 'stroke')
      .attr('stroke', '#f0f2f5')
      .attr('stroke-width', 3)
      .text(label)

    return { g, lng, lat, txt, r }
  })

  // ── Animation loop ───────────────────────────────────────────
  let angle = 0
  const update = () => {
    angle += 0.22
    projection.rotate([angle, -20])

    gridPath.attr('d', pathGen)
    if (world) {
      landGroup.selectAll('path').attr('d', pathGen)
      if (borderPath) borderPath.attr('d', pathGen)
    }

    const centerCoord = [-(angle % 360), 20]

    pointGs.forEach(({ g, lng, lat, txt, r }) => {
      const dist = d3.geoDistance([lng, lat], centerCoord)
      if (dist > Math.PI / 2) { g.attr('opacity', 0); return }
      const p = projection([lng, lat])
      if (!p) { g.attr('opacity', 0); return }
      const fade = 1 - (dist / (Math.PI / 2)) * 0.4
      g.attr('opacity', fade).attr('transform', `translate(${p[0]},${p[1]})`)
      // Only show label when facing front 60%
      txt.attr('display', dist < Math.PI / 3 ? null : 'none')
    })
  }

  update()
  globeInterval = setInterval(update, 40)
}

const handleResize = () => {
  windowWidth.value = window.innerWidth
  windowHeight.value = window.innerHeight

  trendChart?.resize()
  typeChart?.resize()
  rankChart?.resize()

  initGlobe()
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  initRiskTrendChart()
  initRiskTypeChart()
  initRegionRankChart()
  initGlobe()
})

onUnmounted(() => {
  trendChart?.dispose()
  typeChart?.dispose()
  rankChart?.dispose()
  if (globeInterval) clearInterval(globeInterval)
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.dashboard {
  background: #f0f2f5;
  min-height: calc(100vh - 60px);
}

.stat-row {
  margin-bottom: 5px;
}

.stat-card {
  margin-bottom: 5px;
  border-radius: 8px;
}

.stat-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-info {
  flex: 1;
}

.stat-title {
  font-size: 0.9em;
  color: #666;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 1.8em;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.stat-change {
  font-size: 0.85em;
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-change.up { color: #52c41a; }
.stat-change.down { color: #ff4d4f; }

.stat-icon {
  width: 3.5em;
  height: 3.5em;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.chart-row {
  margin-bottom: 5px;
}

.chart-card {
  border-radius: 8px;
  height: 100%;
}

.card-header {
  font-weight: 600;
  font-size: 1em;
}

.chart {
  width: 100%;
}

.globe {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 768px) {
  .stat-value {
    font-size: 1.4em;
  }

  .stat-icon {
    width: 3em;
    height: 3em;
  }
}
</style>