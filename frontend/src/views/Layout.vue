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
        menuName: '风险分析',
        routePath: '/risk-analysis',
        icon: 'Warning',
        parentId: '0'
      },
      {
        menuId: '3',
        menuName: '风险场景',
        routePath: '/risk-scenarios',
        icon: 'List',
        parentId: '0'
      },
      {
        menuId: '4',
        menuName: '费率管理',
        routePath: '/tariff-management',
        icon: 'Money',
        parentId: '0'
      },
      {
        menuId: '5',
        menuName: '费率模拟',
        routePath: '/tariff-simulation',
        icon: 'Tools',
        parentId: '0'
      },
      {
        menuId: '6',
        menuName: '系统设置',
        icon: 'Setting',
        parentId: '0'
      },
      {
        menuId: '6-1',
        menuName: '用户管理',
        routePath: '/system/user',
        icon: 'Avatar',
        parentId: '6'
      },
      {
        menuId: '6-2',
        menuName: '角色管理',
        routePath: '/system/role',
        icon: 'Share',
        parentId: '6'
      },
      {
        menuId: '6-3',
        menuName: '菜单管理',
        routePath: '/system/menu',
        icon: 'List',
        parentId: '6'
      },
      {
        menuId: '7',
        menuName: '算法概览',
        routePath: '/algorithm-overview',
        icon: 'Tools',
        parentId: '0'
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
  padding: 15px;
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