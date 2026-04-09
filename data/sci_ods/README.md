# sci_ods 数据层

## 数据库分层概述

sci_ods（Operational Data Store）是操作数据存储层，用于存储经过清洗和标准化的运营数据。ODS层是数据仓库体系中的核心过渡层，承上启下，对原始数据进行质量提升和结构优化。

**核心职能：**
- 对IDL层原始数据进行清洗和标准化处理
- 实现跨源数据的一致性整合
- 建立基础数据质量规则和校验机制
- 为DW层提供高质量的业务数据

**设计原则：**
- 遵循3NF范式进行数据建模
- 统一数据编码和格式标准
- 保留数据变更历史追踪能力
- 确保与业务系统数据同步

## 目录

1. [数据表快速导航](#1-数据表快速导航)
2. [字段详细说明](#2-字段详细说明)
3. [更新记录](#3-更新记录)

***

## 1. 数据表快速导航

### 风险事件表

| 表名 | 说明 | 关键字段 |
| ---- | ---- | -------- |
| risk_events | 风险事件清洗后数据表 | id, source_channel, event_summary |

***

## 2. 字段详细说明

### risk_events（风险事件清洗后数据表）

存储经过清洗和标准化的风险事件数据，来源为IDL层。

| 字段名 | 类型 | 说明 |
| ------ | ---- | ---- |
| id | INT | 自增ID |
| source_channel | VARCHAR(50) | 来源渠道标签 |
| source_url | VARCHAR(500) | 原始来源URL |
| event_raw_text | TEXT | 原始文本 |
| event_raw_jsonb | JSONB | 原始数据载荷 |
| event_happen_timestamp | TIMESTAMP | 事件发生时间 |
| dw_create_timestamp | TIMESTAMP | 入库时间 |
| dw_update_timestamp | TIMESTAMP | 更新时间 |
| event_summary | VARCHAR(200) | 事件摘要 |
| event_start | DATE | 事件开始日期 |
| event_end | DATE | 事件结束日期 |

***

## 3. 更新记录

| 日期时间          | 说明         | 修改者         |
|---------------| ---------- | ------------ |
| 2026-04-08 00:00 | 初始化sci_ods层结构 | SCI Team |
| 2026-04-08 02:30 | 数据库分层架构同步更新 | SCI Team |
| 2026-04-08 05:00 | 添加risk_events风险事件清洗后数据表 | SCI Team |

***

**文档版本:** 1.1
**维护团队:** SCI Team
**最后更新:** 2026-04-08
