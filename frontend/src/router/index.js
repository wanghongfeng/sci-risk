import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import Layout from '../views/Layout.vue'
import Dashboard from '../views/Dashboard.vue'
import MenuManage from '../views/MenuManage.vue'
import TariffSimulation from '../views/TariffSimulation.vue'
import TariffManagement from '../views/TariffManagement.vue'
import RiskScenarios from '../views/RiskScenarios.vue'
import RiskAnalysis from '../views/RiskAnalysis.vue'
import SystemUser from '../views/SystemUser.vue'
import SystemRole from '../views/SystemRole.vue'
import AlgorithmOverview from '../views/AlgorithmOverview.vue'
import GlobalRiskCollection from '../views/GlobalRiskCollection.vue'
import RiskEventManagement from '../views/RiskEventManagement.vue'
import SupplyChainMaster from '../views/SupplyChainMaster.vue'
import RiskExposureMap from '../views/RiskExposureMap.vue'
import ManualRiskReport from '../views/ManualRiskReport.vue'
import DataMonitor from '../views/DataMonitor.vue'
import RiskClassification from '../views/RiskClassification.vue'
import RiskPropagation from '../views/RiskPropagation.vue'
import SupplyImpact from '../views/SupplyImpact.vue'
import RiskProfile from '../views/RiskProfile.vue'
import RiskReport from '../views/RiskReport.vue'
import RiskWarning from '../views/RiskWarning.vue'
import ResponseMeasures from '../views/ResponseMeasures.vue'
import SmartPlan from '../views/SmartPlan.vue'
import TaskOrders from '../views/TaskOrders.vue'
import CrossDepartment from '../views/CrossDepartment.vue'
import DisposalDashboard from '../views/DisposalDashboard.vue'
import RiskReview from '../views/RiskReview.vue'
import CaseManagement from '../views/CaseManagement.vue'
import RuleOptimization from '../views/RuleOptimization.vue'
import RiskModelOptimization from '../views/RiskModelOptimization.vue'
import MeasureIteration from '../views/MeasureIteration.vue'
import KnowledgeBase from '../views/KnowledgeBase.vue'
import UserManagement from '../views/UserManagement.vue'
import SystemConfig from '../views/SystemConfig.vue'
import InterfaceManagement from '../views/InterfaceManagement.vue'
import LogAudit from '../views/LogAudit.vue'
import DataBackup from '../views/DataBackup.vue'
import Announcement from '../views/Announcement.vue'
import ClassificationDefinition from '../views/ClassificationDefinition.vue'

const routes = [
  {
    path: '/',
    component: Layout,
    children: [
      { path: '', redirect: '/dashboard' },
      { path: '/dashboard', name: '首页', component: Dashboard },
      { path: '/algorithm', name: '算法总览', component: AlgorithmOverview },
      { path: '/tariff', name: '关税管理', component: TariffManagement },
      { path: '/tariff/simulation', name: '关税模拟', component: TariffSimulation },
      { path: '/risk/scenarios', name: '风险场景', component: RiskScenarios },
      { path: '/risk/analysis', name: '风险分析', component: RiskAnalysis },
      { path: '/menu', name: '菜单维护_legacy', component: MenuManage },
      { path: '/system/menu', name: '菜单维护', component: MenuManage },
      { path: '/system/user', name: '用户管理', component: SystemUser },
      { path: '/system/role', name: '角色管理', component: SystemRole },
      { path: '/risk/global-collection', name: '全球风险数据采集', component: GlobalRiskCollection },
      { path: '/risk/event-management', name: '风险事件库管理', component: RiskEventManagement },
      { path: '/risk/supply-chain', name: '供应链网络主数据', component: SupplyChainMaster },
      { path: '/risk/exposure-map', name: '风险暴露地图', component: RiskExposureMap },
      { path: '/risk/manual-report', name: '人工风险上报', component: ManualRiskReport },
      { path: '/risk/monitor', name: '数据监控与日志', component: DataMonitor },
      { path: '/risk-analysis/classification', name: '风险自动分类分级', component: RiskClassification },
      { path: '/risk-analysis/propagation', name: '风险传导路径推演', component: RiskPropagation },
      { path: '/risk-analysis/supply-impact', name: '供应链影响量化测算', component: SupplyImpact },
      { path: '/risk-analysis/profile', name: '供应商物料区域风险画像', component: RiskProfile },
      { path: '/risk-analysis/report', name: '风险分析报告', component: RiskReport },
      { path: '/risk-disposal/warning', name: '风险预警管理', component: RiskWarning },
      { path: '/risk-disposal/response', name: '应对措施库', component: ResponseMeasures },
      { path: '/risk-disposal/smart-plan', name: '智能方案推荐与审批', component: SmartPlan },
      { path: '/risk-disposal/tasks', name: '任务工单管理', component: TaskOrders },
      { path: '/risk-disposal/cross-tracking', name: '跨部门协同跟踪', component: CrossDepartment },
      { path: '/risk-disposal/dashboard', name: '处置进度大屏', component: DisposalDashboard },
      { path: '/risk-learning/review', name: '风险事件复盘', component: RiskReview },
      { path: '/risk-learning/cases', name: '案例库管理', component: CaseManagement },
      { path: '/risk-learning/warning-optimize', name: '预警规则优化', component: RuleOptimization },
      { path: '/risk-learning/model-optimize', name: '风险模型参数优化', component: RiskModelOptimization },
      { path: '/risk-learning/response-iterate', name: '应对措施迭代', component: MeasureIteration },
      { path: '/risk-learning/knowledge', name: '知识沉淀与经验库', component: KnowledgeBase },
      { path: '/system-management/user-permission', name: '用户与权限', component: UserManagement },
      { path: '/system-management/system-config', name: '系统参数配置', component: SystemConfig },
      { path: '/system-management/interface', name: '接口对接管理', component: InterfaceManagement },
      { path: '/system-management/log-audit', name: '日志审计', component: LogAudit },
      { path: '/system-management/backup', name: '数据备份与恢复', component: DataBackup },
      { path: '/system-management/announcement', name: '公告与帮助中心', component: Announcement },
      { path: '/basic-data/classification-definition', name: '风险分类分级定义', component: ClassificationDefinition }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes
})

export default router