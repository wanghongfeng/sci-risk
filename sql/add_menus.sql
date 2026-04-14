-- 删除乱码数据
DELETE FROM menu WHERE menu_id = 'P001';

-- ============================================
-- 1. 风险感知
-- ============================================
INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P001', '风险感知', 'risk-perception', '0', '/risk-perception', 'DataAnalysis', 1, true, 'risk:perception', 'RiskPerception');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P101', '全球风险数据采集', 'global-risk-collection', 'P001', '/risk/global-collection', 'DataBoard', 1, true, 'risk:global:collection', 'GlobalRiskCollection');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P102', '风险事件库管理', 'risk-event-management', 'P001', '/risk/event-management', 'Document', 2, true, 'risk:event:manage', 'RiskEventManagement');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P103', '供应链网络主数据', 'supply-chain-master', 'P001', '/risk/supply-chain', 'Compass', 3, true, 'risk:supply:chain', 'SupplyChainMaster');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P104', '风险暴露地图', 'risk-exposure-map', 'P001', '/risk/exposure-map', 'Histogram', 4, true, 'risk:exposure:map', 'RiskExposureMap');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P105', '人工风险上报', 'manual-risk-report', 'P001', '/risk/manual-report', 'Edit', 5, true, 'risk:manual:report', 'ManualRiskReport');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P106', '数据监控与日志', 'data-monitor', 'P001', '/risk/monitor', 'TrendCharts', 6, true, 'risk:monitor', 'DataMonitor');

-- ============================================
-- 2. 传导分析
-- ============================================
INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P002', '传导分析', 'risk-analysis', '0', '/risk-analysis', 'TrendCharts', 2, true, 'risk:analysis', 'RiskAnalysis');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P201', '风险自动分类分级', 'risk-classification', 'P002', '/risk-analysis/classification', 'Folder', 1, true, 'risk:analysis:classification', 'RiskClassification');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P202', '风险传导路径推演', 'risk-propagation', 'P002', '/risk-analysis/propagation', 'Connection', 2, true, 'risk:analysis:propagation', 'RiskPropagation');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P203', '供应链影响量化测算', 'supply-impact', 'P002', '/risk-analysis/supply-impact', 'DataLine', 3, true, 'risk:analysis:supply-impact', 'SupplyImpact');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P204', '供应商物料区域风险画像', 'risk-profile', 'P002', '/risk-analysis/profile', 'User', 4, true, 'risk:analysis:profile', 'RiskProfile');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P205', '风险分析报告', 'risk-report', 'P002', '/risk-analysis/report', 'Document', 5, true, 'risk:analysis:report', 'RiskReport');

-- ============================================
-- 3. 协同处置
-- ============================================
INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P003', '协同处置', 'risk-disposal', '0', '/risk-disposal', 'Tools', 3, true, 'risk:disposal', 'RiskDisposal');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P301', '风险预警管理', 'risk-warning', 'P003', '/risk-disposal/warning', 'Bell', 1, true, 'risk:disposal:warning', 'RiskWarning');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P302', '应对措施库', 'response-measures', 'P003', '/risk-disposal/response', 'Collection', 2, true, 'risk:disposal:response', 'ResponseMeasures');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P303', '智能方案推荐与审批', 'smart-plan', 'P003', '/risk-disposal/smart-plan', 'Cpu', 3, true, 'risk:disposal:smart-plan', 'SmartPlan');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P304', '任务工单管理', 'task-orders', 'P003', '/risk-disposal/tasks', 'Tickets', 4, true, 'risk:disposal:tasks', 'TaskOrders');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P305', '跨部门协同跟踪', 'cross-dept-tracking', 'P003', '/risk-disposal/cross-tracking', 'Link', 5, true, 'risk:disposal:cross-tracking', 'CrossDeptTracking');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P306', '处置进度大屏', 'disposal-dashboard', 'P003', '/risk-disposal/dashboard', 'DataBoard', 6, true, 'risk:disposal:dashboard', 'DisposalDashboard');

-- ============================================
-- 4. 闭环学习
-- ============================================
INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P004', '闭环学习', 'risk-learning', '0', '/risk-learning', 'Reading', 4, true, 'risk:learning', 'RiskLearning');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P401', '风险事件复盘', 'risk-review', 'P004', '/risk-learning/review', 'Clock', 1, true, 'risk:learning:review', 'RiskReview');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P402', '案例库管理', 'case-management', 'P004', '/risk-learning/cases', 'FolderOpened', 2, true, 'risk:learning:cases', 'CaseManagement');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P403', '预警规则优化', 'warning-optimize', 'P004', '/risk-learning/warning-optimize', 'Setting', 3, true, 'risk:learning:warning-optimize', 'WarningOptimize');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P404', '风险模型参数优化', 'model-optimize', 'P004', '/risk-learning/model-optimize', 'MagicStick', 4, true, 'risk:learning:model-optimize', 'ModelOptimize');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P405', '应对措施迭代', 'response-iterate', 'P004', '/risk-learning/response-iterate', 'Refresh', 5, true, 'risk:learning:response-iterate', 'ResponseIterate');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P406', '知识沉淀与经验库', 'knowledge-base', 'P004', '/risk-learning/knowledge', 'Notebook', 6, true, 'risk:learning:knowledge', 'KnowledgeBase');

-- ============================================
-- 5. 系统管理
-- ============================================
INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P005', '系统管理', 'system-management', '0', '/system-management', 'Setting', 5, true, 'system:management', 'SystemManagement');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P501', '用户与权限', 'user-permission', 'P005', '/system-management/user-permission', 'User', 1, true, 'system:management:user-permission', 'UserPermission');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P502', '系统参数配置', 'system-config', 'P005', '/system-management/system-config', 'Tools', 2, true, 'system:management:system-config', 'SystemConfig');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P503', '接口对接管理', 'interface-management', 'P005', '/system-management/interface', 'Connection', 3, true, 'system:management:interface', 'InterfaceManagement');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P504', '日志审计', 'log-audit', 'P005', '/system-management/log-audit', 'Document', 4, true, 'system:management:log-audit', 'LogAudit');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P505', '数据备份与恢复', 'data-backup', 'P005', '/system-management/backup', 'Box', 5, true, 'system:management:backup', 'DataBackup');

INSERT INTO menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component)
VALUES ('P506', '公告与帮助中心', 'announcement-help', 'P005', '/system-management/announcement', 'Message', 6, true, 'system:management:announcement', 'AnnouncementHelp');
