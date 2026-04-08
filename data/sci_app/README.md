# sci_app 数据层

## 数据库分层概述

sci_app（Application System Layer）是应用系统层，用于存储应用系统所需的用户管理、菜单权限和系统配置信息。独立于数据仓库分层架构，单独维护。

**核心职能：**
- 存储应用系统所需的用户管理信息
- 提供菜单结构和权限控制功能
- 管理系统配置和参数设置
- 支持审计日志和操作记录

**设计原则：**
- 支持灵活的菜单层级结构
- 实现基于角色的访问控制（RBAC）
- 记录关键业务操作的审计日志
- 与数据仓库分层隔离，单独维护

## 目录

1. [数据表快速导航](#1-数据表快速导航)
2. [字段详细说明](#2-字段详细说明)
3. [文件结构](#3-文件结构)
4. [更新记录](#4-更新记录)

***

## 1. 数据表快速导航

### 系统表

| 表名 | 说明 | 关键字段 |
| ---- | ---- | -------- |
| users | 用户信息表 | id, name, role, status |
| menu | 菜单结构表 | menu_id, menu_name, parent_id, route_path |

***

## 2. 字段详细说明

### users（用户信息表）

存储系统用户信息。

| 字段名 | 类型 | 必填 | 中文说明 | 取值示例 |
| ------ | ---- | ---- | -------- | -------- |
| id | INTEGER | ✅ | 用户ID（自增） | 1 |
| name | VARCHAR(255) | ✅ | 用户名称 | admin |
| photo | VARCHAR(255) | ✅ | 用户头像 | admin.png |
| status | VARCHAR(255) | ❌ | 状态 | active, inactive |
| created_at | TIMESTAMP | ❌ | 创建时间 | 2026-03-31 08:45:28 |
| password_hash | VARCHAR(255) | ❌ | 密码哈希 | $2b$12$... |
| role | VARCHAR(255) | ❌ | 角色 | admin, viewer |

**主键:** id

**角色说明:**

- `admin` - 管理员，拥有完全访问权限
- `viewer` - 查看者，只读访问

***

### menu（菜单结构表）

存储系统菜单结构。

| 字段名 | 类型 | 必填 | 中文说明 | 取值示例 |
| ------ | ---- | ---- | -------- | -------- |
| menu_id | VARCHAR(50) | ✅ | 菜单ID | M001 |
| menu_name | VARCHAR(100) | ✅ | 菜单名称 | 首页 |
| menu_code | VARCHAR(50) | ✅ | 菜单代码 | dashboard |
| parent_id | VARCHAR(50) | ❌ | 父菜单ID | 0 |
| route_path | VARCHAR(255) | ❌ | 路由路径 | /dashboard |
| icon | VARCHAR(50) | ❌ | 图标 | Dashboard |
| sort_order | INT | ❌ | 排序 | 1 |
| is_visible | BOOLEAN | ❌ | 是否可见 | TRUE, FALSE |
| permission | VARCHAR(100) | ❌ | 权限标识 | dashboard:view |
| component | VARCHAR(100) | ❌ | 组件路径 | Dashboard |
| created_at | TIMESTAMP | ❌ | 创建时间 | 2026-03-31 05:24:38 |
| updated_at | TIMESTAMP | ❌ | 更新时间 | 2026-03-31 05:24:38 |

**主键:** menu_id

**外键:** parent_id → menu.menu_id

***

## 3. 文件结构

```
sci_app/
├── README.md              # 本文件
├── app_create_table.sql   # 建表脚本
└── seed_data.sql         # 种子数据
```

***

## 4. 更新记录

| 日期时间          | 说明         | 修改者         |
|---------------| ---------- | ------------ |
| 2026-04-08 00:00 | 初始化sci_app层结构 | SCI Team |
| 2026-04-08 02:30 | 数据库分层架构同步更新 | SCI Team |
| 2026-04-08 04:00 | 添加建表脚本和种子数据 | SCI Team |

***

**文档版本:** 1.1
**维护团队:** SCI Team
**最后更新:** 2026-04-08
