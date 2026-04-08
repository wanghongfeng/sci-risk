-- ============================================
-- SCI_APP Schema Seed Data Script
-- Initial data for Application System Layer
-- ============================================

-- ============================================
-- USER DATA (7 records)
-- ============================================
INSERT INTO sci_app.users (name, photo, status, created_at, password_hash, role) VALUES
('Jerry-供应链专家', '1_jerry.jpg', 'active', '2026-03-31 05:24:38', '', 'viewer'),
('Tom-技术架构师', 'tom.jpg', 'active', '2026-03-31 05:24:38', '', 'viewer'),
('admin', 'admin.png', 'active', '2026-03-31 08:45:28', '$2b$12$plGLBEg27UxkNSMYG1XE2.C5J8EEDND5y7el/ApgpInzFQMIrwgPe', 'admin'),
('test_viewer_pytest', 'test.png', 'active', '2026-03-31 08:47:55', '$2b$12$uoqmWOCJNTn3asbdwAgKdeB.skCOe8SGUK8RYDCLDzSxaDU6qPYUW', 'viewer'),
('hellohello', '123919', 'active', '2026-03-31 09:00:32', '$2b$12$8MI/Vxkjj78M1v4ToXdvfOHcHwrmOa.mqoamQbY76FqVifEjdeh7m', 'viewer'),
('test_viewer_pytest', 'test.png', 'active', '2026-03-31 09:08:05', '$2b$12$YFgUMi8IVZUHz12gwYT8keiuJ5sZf6jsIU6hGd54xB7GKORZ.J3im', 'viewer');

-- ============================================
-- MENU DATA (6 records)
-- ============================================
INSERT INTO sci_app.menu (menu_id, menu_name, menu_code, parent_id, route_path, icon, sort_order, is_visible, permission, component) VALUES
('M001', '首页', 'dashboard', '0', '/dashboard', 'Dashboard', 1, TRUE, 'dashboard:view', 'Dashboard'),
('M002', '关税管理', 'tariff', '0', '/tariff', 'TariffIcon', 2, TRUE, 'tariff:manage', 'TariffLayout'),
('M203', '关税模拟', 'tariff-sim', 'M002', '/tariff/simulation', NULL, 3, TRUE, 'tariff:sim', 'TariffSimulation'),
('M008', '系统设置', 'system', '0', '/system', 'SystemIcon', 8, TRUE, 'system:manage', 'SystemLayout'),
('M804', '菜单管理', 'menu-manage', 'M008', '/system/menu', NULL, 1, TRUE, 'system:menu', 'MenuManage'),
('M805', '算法总览', 'algorithm-overview', 'M008', '/algorithm', 'Cpu', 2, TRUE, 'algorithm:view', 'AlgorithmOverview');
