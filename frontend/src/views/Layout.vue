<template>
  <el-container class="layout-container">
    <el-aside :width="asideWidth" class="aside" :class="{ 'collapsed': isCollapsed }">
      <div class="logo">
        <el-icon :size="20"><Warning /></el-icon>
        <span v-if="!isCollapsed" class="logo-text">风险控制塔</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="menu"
        :collapse="isCollapsed"
        :collapse-transition="false"
        :router="false"
        @select="handleMenuSelect"
      >
        <template v-for="menu in menuList" :key="menu.menuId">
          <el-menu-item v-if="!menu.children || menu.children.length === 0" :index="menu.routePath || '/'">
            <el-icon v-if="menu.icon"><component :is="menu.icon" /></el-icon>
            <span>{{ menu.menuName }}</span>
          </el-menu-item>
          <el-sub-menu v-else :index="menu.routePath || menu.menuId">
            <template #title>
              <el-icon v-if="menu.icon"><component :is="menu.icon" /></el-icon>
              <span v-if="!isCollapsed">{{ menu.menuName }}</span>
            </template>
            <el-menu-item
              v-for="child in menu.children"
              :key="child.menuId"
              :index="child.routePath || '/'"
            >
              <el-icon v-if="child.icon"><component :is="child.icon" /></el-icon>
              <span>{{ child.menuName }}</span>
            </el-menu-item>
          </el-sub-menu>
        </template>
      </el-menu>
    </el-aside>

    <el-container class="main-container">
      <el-header class="header">
        <div class="header-left">
          <el-button text @click="toggleCollapse" class="collapse-btn">
            <el-icon :size="20"><Fold v-if="!isCollapsed" /><Expand v-else /></el-icon>
          </el-button>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="currentRoute">{{ currentRoute }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-avatar :size="28" icon="UserFilled" />
              <span class="username" v-if="!isMobile">管理员</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, markRaw } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Warning, Fold, Expand, DataBoard, Money, Setting, Tools, User, Share, List, House, TrendCharts, Document, DataAnalysis, Histogram, Menu, Avatar, Files, Compass } from '@element-plus/icons-vue'
import axios from 'axios'
import config from '../config'

const iconMap = {
  'Dashboard': markRaw(House),
  'DataBoard': markRaw(DataBoard),
  'Money': markRaw(Money),
  'Setting': markRaw(Setting),
  'Tools': markRaw(Tools),
  'User': markRaw(Avatar),
  'Share': markRaw(Files),
  'List': markRaw(Menu),
  'Warning': markRaw(Warning),
  'Home': markRaw(House),
  'TrendCharts': markRaw(TrendCharts),
  'Document': markRaw(Document),
  'DataAnalysis': markRaw(DataAnalysis),
  'Histogram': markRaw(Histogram),
  'Menu': markRaw(Menu),
  'Avatar': markRaw(Avatar),
  'Files': markRaw(Files),
  'Compass': markRaw(Compass)
}

const getIcon = (iconName) => {
  if (!iconName) return markRaw(DataBoard)
  return iconMap[iconName] || markRaw(DataBoard)
}

const router = useRouter()
const route = useRoute()
const menuList = ref([])
const activeMenu = ref('/dashboard')
const currentRoute = computed(() => route.name)
const isCollapsed = ref(false)
const windowWidth = ref(window.innerWidth)
const isMobile = computed(() => windowWidth.value < 768)

const asideWidth = computed(() => {
  if (windowWidth.value < 768) return '64px'
  return isCollapsed.value ? '64px' : '200px'
})

const buildMenuTree = (list) => {
  const map = {}
  const roots = []

  list.forEach(item => {
    map[item.menuId] = { ...item, children: [] }
  })

  list.forEach(item => {
    if (item.parentId && item.parentId !== '0' && map[item.parentId]) {
      map[item.parentId].children.push(map[item.menuId])
    } else if (!item.parentId || item.parentId === '0') {
      roots.push(map[item.menuId])
    }
  })

  return roots
}

const loadMenus = async () => {
  try {
    console.log('Trying to load menus from backend')
    const response = await axios.get(`${config.apiBaseUrl}/menu/list`)
    console.log('Backend menu response:', response.data)
    const rawMenuList = response.data || []

    const mappedMenuList = rawMenuList.map(menu => ({
      ...menu,
      icon: getIcon(menu.icon)
    }))

    console.log('Mapped menu list:', mappedMenuList)
    menuList.value = buildMenuTree(mappedMenuList)
    console.log('Built menu tree:', menuList.value)
  } catch (error) {
    console.error('Failed to load menus from backend, using default menus:', error)
    const defaultMenus = [
      {
        menuId: '1',
        menuName: '仪表盘',
        routePath: '/dashboard',
        icon: 'Dashboard',
        parentId: '0'
      },
      {
        menuId: '2',
        menuName: '风险感知',
        icon: 'Compass',
        parentId: '0'
      },
      {
        menuId: '2-1',
        menuName: '全球风险数据采集',
        routePath: '/risk/global-collection',
        icon: 'DataAnalysis',
        parentId: '2'
      },
      {
        menuId: '2-2',
        menuName: '风险事件库管理',
        routePath: '/risk/event-management',
        icon: 'Document',
        parentId: '2'
      },
      {
        menuId: '2-3',
        menuName: '供应链网络主数据',
        routePath: '/risk/supply-chain',
        icon: 'Histogram',
        parentId: '2'
      },
      {
        menuId: '2-4',
        menuName: '风险暴露地图',
        routePath: '/risk/exposure-map',
        icon: 'Compass',
        parentId: '2'
      },
      {
        menuId: '2-5',
        menuName: '人工风险上报',
        routePath: '/risk/manual-report',
        icon: 'Document',
        parentId: '2'
      },
      {
        menuId: '2-6',
        menuName: '数据监控与日志',
        routePath: '/risk/monitor',
        icon: 'DataBoard',
        parentId: '2'
      },
      {
        menuId: '3',
        menuName: '传导分析',
        icon: 'TrendCharts',
        parentId: '0'
      },
      {
        menuId: '3-1',
        menuName: '风险自动分类分级',
        routePath: '/risk-analysis/classification',
        icon: 'Histogram',
        parentId: '3'
      },
      {
        menuId: '3-2',
        menuName: '风险传导路径推演',
        routePath: '/risk-analysis/propagation',
        icon: 'TrendCharts',
        parentId: '3'
      },
      {
        menuId: '3-3',
        menuName: '供应链影响量化测算',
        routePath: '/risk-analysis/supply-impact',
        icon: 'DataAnalysis',
        parentId: '3'
      },
      {
        menuId: '3-4',
        menuName: '供应商物料区域风险画像',
        routePath: '/risk-analysis/profile',
        icon: 'DataBoard',
        parentId: '3'
      },
      {
        menuId: '3-5',
        menuName: '风险分析报告',
        routePath: '/risk-analysis/report',
        icon: 'Document',
        parentId: '3'
      },
      {
        menuId: '4',
        menuName: '协同处置',
        icon: 'Share',
        parentId: '0'
      },
      {
        menuId: '4-1',
        menuName: '风险预警管理',
        routePath: '/risk-disposal/warning',
        icon: 'Warning',
        parentId: '4'
      },
      {
        menuId: '4-2',
        menuName: '应对措施库',
        routePath: '/risk-disposal/response',
        icon: 'Tools',
        parentId: '4'
      },
      {
        menuId: '4-3',
        menuName: '智能方案推荐与审批',
        routePath: '/risk-disposal/smart-plan',
        icon: 'DataAnalysis',
        parentId: '4'
      },
      {
        menuId: '4-4',
        menuName: '任务工单管理',
        routePath: '/risk-disposal/tasks',
        icon: 'List',
        parentId: '4'
      },
      {
        menuId: '4-5',
        menuName: '跨部门协同跟踪',
        routePath: '/risk-disposal/cross-tracking',
        icon: 'Share',
        parentId: '4'
      },
      {
        menuId: '4-6',
        menuName: '处置进度大屏',
        routePath: '/risk-disposal/dashboard',
        icon: 'DataBoard',
        parentId: '4'
      },
      {
        menuId: '5',
        menuName: '闭环学习',
        icon: 'Document',
        parentId: '0'
      },
      {
        menuId: '5-1',
        menuName: '风险事件复盘',
        routePath: '/risk-learning/review',
        icon: 'Document',
        parentId: '5'
      },
      {
        menuId: '5-2',
        menuName: '案例库管理',
        routePath: '/risk-learning/cases',
        icon: 'Files',
        parentId: '5'
      },
      {
        menuId: '5-3',
        menuName: '预警规则优化',
        routePath: '/risk-learning/warning-optimize',
        icon: 'Tools',
        parentId: '5'
      },
      {
        menuId: '5-4',
        menuName: '风险模型参数优化',
        routePath: '/risk-learning/model-optimize',
        icon: 'DataAnalysis',
        parentId: '5'
      },
      {
        menuId: '5-5',
        menuName: '应对措施迭代',
        routePath: '/risk-learning/response-iterate',
        icon: 'TrendCharts',
        parentId: '5'
      },
      {
        menuId: '5-6',
        menuName: '知识沉淀与经验库',
        routePath: '/risk-learning/knowledge',
        icon: 'Files',
        parentId: '5'
      },
      {
        menuId: '6',
        menuName: '系统管理',
        icon: 'Setting',
        parentId: '0'
      },
      {
        menuId: '6-1',
        menuName: '用户与权限',
        routePath: '/system-management/user-permission',
        icon: 'User',
        parentId: '6'
      },
      {
        menuId: '6-2',
        menuName: '系统参数配置',
        routePath: '/system-management/system-config',
        icon: 'Setting',
        parentId: '6'
      },
      {
        menuId: '6-3',
        menuName: '接口对接管理',
        routePath: '/system-management/interface',
        icon: 'Share',
        parentId: '6'
      },
      {
        menuId: '6-4',
        menuName: '日志审计',
        routePath: '/system-management/log-audit',
        icon: 'Document',
        parentId: '6'
      },
      {
        menuId: '6-5',
        menuName: '数据备份与恢复',
        routePath: '/system-management/backup',
        icon: 'Files',
        parentId: '6'
      },
      {
        menuId: '6-6',
        menuName: '公告与帮助中心',
        routePath: '/system-management/announcement',
        icon: 'Document',
        parentId: '6'
      },
      {
        menuId: '7',
        menuName: '基础数据',
        icon: 'DataBoard',
        parentId: '0'
      },
      {
        menuId: '7-1',
        menuName: '风险分类分级定义',
        routePath: '/basic-data/classification-definition',
        icon: 'Histogram',
        parentId: '7'
      }
    ]
    
    const mappedDefaultMenus = defaultMenus.map(menu => ({
      ...menu,
      icon: getIcon(menu.icon)
    }))
    
    menuList.value = buildMenuTree(mappedDefaultMenus)
  }
}

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}

const handleMenuSelect = (index) => {
  if (index && index !== '/') {
    router.push(index)
  }
  activeMenu.value = index
}

const handleCommand = (command) => {
  if (command === 'logout') {
    router.push('/')
  }
}

const handleResize = () => {
  windowWidth.value = window.innerWidth
  if (windowWidth.value < 768) {
    isCollapsed.value = true
  }
}

onMounted(() => {
  loadMenus()
  activeMenu.value = route.path
  window.addEventListener('resize', handleResize)
  if (window.innerWidth < 768) {
    isCollapsed.value = true
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.layout-container {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.aside {
  background: #001529;
  transition: width 0.3s;
  overflow-y: auto;
  overflow-x: hidden;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}

.logo {
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: white;
  font-size: 14px;
  font-weight: bold;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  padding: 0 10px;
  flex-shrink: 0;
}

.logo-text {
  white-space: nowrap;
}

.menu {
  border-right: none;
  background: transparent;
  overflow-y: auto;
  overflow-x: hidden;
  flex: 1;
  min-height: 0;
}

.menu::-webkit-scrollbar {
  width: 4px;
}

.menu::-webkit-scrollbar-thumb {
  background: rgba(255,255,255,0.2);
  border-radius: 2px;
}

:deep(.el-menu) {
  background: transparent;
}

:deep(.el-menu-item),
:deep(.el-sub-menu__title) {
  color: rgba(255,255,255,0.7);
  font-size: 13px;
  height: 44px;
  line-height: 44px;
}

:deep(.el-menu-item:hover),
:deep(.el-sub-menu__title:hover) {
  background: rgba(255,255,255,0.1);
  color: white;
}

:deep(.el-menu-item.is-active) {
  background: #1890ff;
  color: white;
}

:deep(.el-sub-menu .el-menu-item) {
  height: 40px;
  line-height: 40px;
  padding-left: 44px !important;
}

:deep(.el-sub-menu .el-menu-item.is-active) {
  background: #1890ff;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  background: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 15px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.collapse-btn {
  padding: 4px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

.username {
  font-size: 13px;
  color: #333;
}

.main {
  background: #f0f2f5;
  padding: 8px;
  overflow-y: auto;
  flex: 1;
}

@media (max-width: 768px) {
  .logo {
    justify-content: center;
  }

  .username {
    display: none;
  }
}
</style>