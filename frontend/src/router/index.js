import { createRouter, createWebHistory } from 'vue-router'
import Layout from '../views/Layout.vue'
import Dashboard from '../views/Dashboard.vue'
import MenuManage from '../views/MenuManage.vue'
import TariffSimulation from '../views/TariffSimulation.vue'
import TariffManagement from '../views/TariffManagement.vue'
import RiskScenarios from '../views/RiskScenarios.vue'
import RiskAnalysis from '../views/RiskAnalysis.vue'
import SystemUser from '../views/SystemUser.vue'
import SystemRole from '../views/SystemRole.vue'

const routes = [
  {
    path: '/',
    component: Layout,
    children: [
      { path: '', redirect: '/dashboard' },
      { path: '/dashboard', name: '首页', component: Dashboard },
      { path: '/tariff', name: '关税管理', component: TariffManagement },
      { path: '/tariff/simulation', name: '关税模拟', component: TariffSimulation },
      { path: '/risk/scenarios', name: '风险场景', component: RiskScenarios },
      { path: '/risk/analysis', name: '风险分析', component: RiskAnalysis },
      { path: '/menu', name: '菜单维护_legacy', component: MenuManage },
      { path: '/system/menu', name: '菜单维护', component: MenuManage },
      { path: '/system/user', name: '用户管理', component: SystemUser },
      { path: '/system/role', name: '角色管理', component: SystemRole }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router