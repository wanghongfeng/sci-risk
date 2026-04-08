# sci\_dw 数据层

## 数据库分层概述

sci\_dw（Data Warehouse Layer）是数据仓库层，用于存储经过整合和建模的业务数据。DW层是数据仓库体系中的核心分析层，采用维度建模方法，为业务报表和数据分析提供统一的数据视图。

**核心职能：**

- 对ODS层数据进行维度建模和主题域划分
- 构建星型/雪花模型的事实表和维度表
- 支持多维度业务报表和分析需求
- 提供历史数据快照和趋势分析能力

**设计原则：**

- 采用Kimball维度建模方法论
- 事实表遵循3NF规范，维度表可适度反规范化
- 支持缓慢变化维（SCD）处理数据历史变更
- 确保数据一致性和业务口径统一

## 目录

1. [数据表快速导航](#1-数据表快速导航)
2. [字段详细说明](#2-字段详细说明)
3. [业务场景说明](#3-业务场景说明)
4. [快速开始](#4-快速开始)
5. [文件结构](#5-文件结构)
6. [更新记录](#6-更新记录)

***

## 1. 数据表快速导航

### 主数据表

| 表名               | 说明     | 关键字段                                    |
| ---------------- | ------ | --------------------------------------- |
| factory\_master  | 工厂主数据  | factory\_id, country, capacity          |
| supplier\_master | 供应商主数据 | supplier\_id, tier, credit\_rating      |
| product\_master  | 产品主数据  | product\_id, product\_type, base\_price |

### 供应链表

| 表名           | 说明   | 关键字段                                        |
| ------------ | ---- | ------------------------------------------- |
| bom\_master  | 物料清单 | bom\_id, key\_component\_id, quantity       |
| supply\_path | 供应路径 | path\_id, lead\_time, transportation\_mode  |
| tariff\_rule | 关税规则 | tariff\_id, current\_tariff, future\_tariff |

### 业务表

| 表名            | 说明   | 关键字段                              |
| ------------- | ---- | --------------------------------- |
| risk\_mapping | 风险映射 | overall\_risk\_level, risk\_score |
| sales\_order  | 销售订单 | order\_id, quantity, status       |

***

## 2. 字段详细说明

### factory\_master（工厂主数据表）

存储海尔集团全球工厂信息。

| 字段名               | 类型           | 必填 | 中文说明    | 取值示例                |
| ----------------- | ------------ | -- | ------- | ------------------- |
| factory\_id       | VARCHAR(50)  | ✅  | 工厂唯一标识符 | F001                |
| factory\_name     | VARCHAR(100) | ✅  | 工厂名称    | 海尔青岛工厂              |
| country           | VARCHAR(50)  | ✅  | 工厂所在国家  | 中国、越南、德国            |
| capacity          | INT          | ✅  | 年产能（台）  | 500000              |
| main\_markets     | VARCHAR(255) | ❌  | 主要销售市场  | 中国, 亚洲, 欧洲          |
| established\_date | DATE         | ❌  | 工厂成立日期  | 2000-01-01          |
| status            | VARCHAR(20)  | ❌  | 运营状态    | 运行中、停产、维护中          |
| last\_updated     | TIMESTAMP    | ❌  | 最后更新时间  | 2024-01-01 10:00:00 |

**主键:** factory\_id

**状态取值:**

- `运行中` - 正常生产
- `停产` - 暂停生产
- `维护中` - 设备维护

***

### supplier\_master（供应商主数据表）

存储供应商信息，包含层级和信用评级。

| 字段名               | 类型           | 必填 | 中文说明     | 取值示例                |
| ----------------- | ------------ | -- | -------- | ------------------- |
| supplier\_id      | VARCHAR(50)  | ✅  | 供应商唯一标识符 | S001                |
| supplier\_name    | VARCHAR(100) | ✅  | 供应商名称    | 海尔压缩机供应商            |
| country           | VARCHAR(50)  | ✅  | 供应商所在国家  | 中国、韩国、日本            |
| tier              | INT          | ✅  | 供应商层级    | 1、2、3               |
| supplier\_type    | VARCHAR(50)  | ❌  | 供应商类型    | 核心供应商、重要供应商         |
| established\_date | DATE         | ❌  | 供应商成立日期  | 1995-01-01          |
| credit\_rating    | VARCHAR(10)  | ❌  | 信用评级     | AAA、AA、A、B          |
| last\_updated     | TIMESTAMP    | ❌  | 最后更新时间   | 2024-01-01 10:00:00 |

**主键:** supplier\_id

**层级说明:**

- `1` - 核心供应商，直接供应关键零部件（如压缩机、冷凝器）
- `2` - 重要供应商，供应重要零部件（如面板）
- `3` - 一般供应商，供应辅助材料（如包装）

**信用评级:** AAA（最优）→ AA → A → B（一般）

***

### product\_master（产品主数据表）

存储产品目录信息。

| 字段名             | 类型            | 必填 | 中文说明       | 取值示例       |
| --------------- | ------------- | -- | ---------- | ---------- |
| product\_id     | VARCHAR(50)   | ✅  | 产品唯一标识符    | P001       |
| product\_name   | VARCHAR(100)  | ✅  | 产品型号       | HRF-500    |
| factory\_id     | VARCHAR(50)   | ✅  | 生产工厂ID（外键） | F001       |
| target\_markets | VARCHAR(255)  | ❌  | 目标销售市场     | 中国, 欧洲, 北美 |
| base\_price     | DECIMAL(10,2) | ✅  | 基础价格（元）    | 4999.00    |
| product\_type   | VARCHAR(50)   | ❌  | 产品类型       | 高端冰箱、旗舰冰箱  |
| launch\_date    | DATE          | ❌  | 产品上市日期     | 2023-01-01 |

**主键:** product\_id
**外键:** factory\_id → factory\_master.factory\_id

**产品类型分类:**

| 产品类型  | 价格区间       | 说明           |
| ----- | ---------- | ------------ |
| 旗舰冰箱  | >5500元     | 高端变频压缩机，智能控制 |
| 高端冰箱  | 4000-5500元 | 变频压缩机        |
| 中高端冰箱 | 3000-4000元 | 部分变频功能       |
| 中端冰箱  | 2000-3000元 | 定频压缩机        |
| 经济型冰箱 | <2000元     | 基础配置         |

***

### bom\_master（物料清单表）

存储产品的关键零部件构成（BOM - Bill of Materials）。

| 字段名                  | 类型            | 必填 | 中文说明     | 取值示例   |
| -------------------- | ------------- | -- | -------- | ------ |
| bom\_id              | VARCHAR(50)   | ✅  | BOM唯一标识符 | B001   |
| product\_id          | VARCHAR(50)   | ✅  | 产品ID（外键） | P001   |
| key\_component\_id   | VARCHAR(50)   | ✅  | 关键零部件编码  | C001   |
| key\_component\_name | VARCHAR(100)  | ✅  | 关键零部件名称  | 变频压缩机  |
| quantity             | INT           | ✅  | 零部件数量    | 1      |
| price                | DECIMAL(10,2) | ✅  | 零部件单价（元） | 800.00 |
| supplier\_id         | VARCHAR(50)   | ❌  | 首选供应商ID  | S001   |

**主键:** bom\_id
**外键:** product\_id → product\_master.product\_id

**BOM示例 - 产品 HRF-500:**

```
HRF-500 (P001)
├── 变频压缩机 C001 - 800元 - S001（海尔压缩机供应商）
├── 高效冷凝器 C002 - 300元 - S002（海尔冷凝器供应商）
├── 智能控制器 C003 - 200元 - S003（海尔控制器供应商）
└── 钢化玻璃面板 C004 - 150元 - S004（海尔面板供应商）

零部件成本合计: 1450元
```

***

### supply\_path（供应路径表）

存储零部件从供应商到工厂的供应链路径。

| 字段名                  | 类型          | 必填 | 中文说明       | 取值示例      |
| -------------------- | ----------- | -- | ---------- | --------- |
| path\_id             | VARCHAR(50) | ✅  | 路径唯一标识符    | SP001     |
| key\_component\_id   | VARCHAR(50) | ✅  | 关键零部件ID    | C001      |
| supplier\_id         | VARCHAR(50) | ✅  | 供应商ID（外键）  | S001      |
| supply\_country      | VARCHAR(50) | ✅  | 零部件供应国     | 中国        |
| factory\_id          | VARCHAR(50) | ✅  | 目标工厂ID（外键） | F001      |
| path\_type           | VARCHAR(50) | ❌  | 路径类型       | 直接供应、代理供应 |
| lead\_time           | INT         | ❌  | 运输前置时间（天）  | 5         |
| transportation\_mode | VARCHAR(50) | ❌  | 运输方式       | 公路、海运、空运  |

**主键:** path\_id
**外键:**

- supplier\_id → supplier\_master.supplier\_id
- factory\_id → factory\_master.factory\_id

**运输方式:**

- `公路` - 适合短途、国内运输
- `海运` - 适合长途、国际运输
- `空运` - 适合紧急零部件
- `海运+公路` - 国际+国内联运

***

### tariff\_rule（关税规则表）

存储各国间的进出口关税规则。

| 字段名                  | 类型           | 必填 | 中文说明     | 取值示例       |
| -------------------- | ------------ | -- | -------- | ---------- |
| tariff\_id           | VARCHAR(50)  | ✅  | 关税规则唯一标识 | T001       |
| origin\_country      | VARCHAR(50)  | ✅  | 原产国      | 中国         |
| destination\_country | VARCHAR(50)  | ✅  | 目的国      | 美国         |
| product\_type        | VARCHAR(50)  | ✅  | 产品类型     | 高端冰箱       |
| current\_tariff      | DECIMAL(5,2) | ✅  | 当前关税率（%） | 25.00      |
| future\_tariff       | DECIMAL(5,2) | ❌  | 未来预期关税率  | 20.00      |
| effective\_date      | DATE         | ✅  | 关税规则生效日期 | 2023-01-01 |
| expiry\_date         | DATE         | ❌  | 关税规则到期日期 | 2024-12-31 |
| rule\_status         | VARCHAR(20)  | ❌  | 规则状态     | 有效、失效、草稿   |

**主键:** tariff\_id

**关税示例:**

| tariff\_id | origin | destination | product\_type | current | future | status |
| ---------- | ------ | ----------- | ------------- | ------- | ------ | ------ |
| T001       | 中国     | 美国          | 高端冰箱          | 25%     | 20%    | 有效     |
| T005       | 中国     | 欧盟          | 高端冰箱          | 10%     | 8%     | 有效     |
| T009       | 越南     | 美国          | 高端冰箱          | 10%     | 8%     | 有效     |

***

### risk\_mapping（风险映射表）

综合评估供应链风险，关联供应路径、产品、工厂和关税信息。

| 字段名                  | 类型           | 必填 | 中文说明       | 取值示例                |
| -------------------- | ------------ | -- | ---------- | ------------------- |
| mapping\_id          | SERIAL       | ✅  | 风险映射ID（自增） | 1                   |
| path\_id             | VARCHAR(50)  | ✅  | 供应路径ID（外键） | SP001               |
| product\_id          | VARCHAR(50)  | ✅  | 产品ID（外键）   | P001                |
| factory\_id          | VARCHAR(50)  | ✅  | 工厂ID（外键）   | F001                |
| supplier\_id         | VARCHAR(50)  | ❌  | 供应商ID      | S001                |
| origin\_country      | VARCHAR(50)  | ✅  | 原产国        | 中国                  |
| destination\_country | VARCHAR(50)  | ✅  | 目的国        | 美国                  |
| current\_tariff      | DECIMAL(5,2) | ❌  | 当前关税率      | 25.00               |
| tariff\_risk\_level  | VARCHAR(10)  | ❌  | 关税风险等级     | 高、中、低               |
| product\_risk\_level | VARCHAR(10)  | ❌  | 产品风险等级     | 高、中、低               |
| factory\_risk\_level | VARCHAR(10)  | ❌  | 工厂风险等级     | 高、中、低               |
| overall\_risk\_level | VARCHAR(10)  | ❌  | 综合风险等级     | 高、中、低               |
| risk\_score          | INT          | ❌  | 风险评分（1-9）  | 9                   |
| assessment\_date     | TIMESTAMP    | ❌  | 风险评估日期     | 2024-01-01 10:00:00 |

**主键:** mapping\_id (自增)
**外键:**

- path\_id → supply\_path.path\_id
- product\_id → product\_master.product\_id
- factory\_id → factory\_master.factory\_id

**风险等级说明:**

| 风险维度 | 高             | 中            | 低      |
| ---- | ------------- | ------------ | ------ |
| 关税风险 | 当前≥20%或涨幅≥10% | 当前≥10%或涨幅≥5% | 其他     |
| 产品风险 | 旗舰/高端且价格≥5000 | 中高端或受关税影响大   | 经济型/中端 |
| 工厂风险 | 中国→美国且关税高     | 中美关税上涨       | 其他国家组合 |
| 综合风险 | 评分≥7分         | 评分5-6分       | 评分<5分  |

**评分规则:**

```
高 = 3分
中 = 2分
低 = 1分

综合评分 = 关税风险分 + 产品风险分 + 工厂风险分
```

***

### sales\_order（销售订单表）

存储产品销售订单信息。

| 字段名            | 类型            | 必填 | 中文说明      | 取值示例       |
| -------------- | ------------- | -- | --------- | ---------- |
| order\_id      | VARCHAR(50)   | ✅  | 订单唯一标识    | SO001      |
| product\_id    | VARCHAR(50)   | ✅  | 产品ID（外键）  | P001       |
| quantity       | INT           | ✅  | 订购数量      | 100        |
| sales\_country | VARCHAR(50)   | ✅  | 销售目的国家    | 中国         |
| price          | DECIMAL(10,2) | ✅  | 订单单价（元）   | 4999.00    |
| order\_date    | DATE          | ✅  | 订单日期      | 2023-01-15 |
| delivery\_date | DATE          | ❌  | 预计/实际交付日期 | 2023-01-20 |
| status         | VARCHAR(20)   | ❌  | 订单状态      | 已完成、处理中    |

**主键:** order\_id
**外键:** product\_id → product\_master.product\_id

**订单状态:**

- `已完成` - 订单已交付
- `处理中` - 订单正在处理
- `已取消` - 订单已取消
- `待处理` - 等待确认

***

## 3. 业务场景说明

### 场景一：关税风险分析

**目标:** 评估中国出口美国的高端冰箱关税风险

**数据流向:**

```
factory_master (F001-青岛工厂)
    ↓
product_master (P001-HRF-500)
    ↓
bom_master (获取零部件成本)
    ↓
supply_path (获取供应路径)
    ↓
tariff_rule (中国→美国关税25%)
    ↓
risk_mapping (关税风险=高, 产品风险=高, 综合风险=高)
```

### 场景二：供应商替代方案

**目标:** 寻找越南工厂的压缩机供应商

**查询逻辑:**

```sql
-- 查找越南工厂的供应路径
SELECT sp.path_id, sm.supplier_name, sm.country, sm.tier
FROM supply_path sp
JOIN supplier_master sm ON sp.supplier_id = sm.supplier_id
WHERE sp.factory_id = 'F002'  -- 越南工厂
AND sp.key_component_id = 'C001';  -- 压缩机
```

### 场景三：风险评分计算

**逻辑:**

```python
# 关税风险
current_tariff = 25  # 中国→美国
future_tariff = 20
tariff_risk = "高"   # 当前≥20%

# 产品风险
product_type = "高端冰箱"
base_price = 4999
tariff_impact = "高"
product_risk = "高"  # 高端冰箱且价格≥5000

# 工厂风险
factory_country = "中国"
destination = "美国"
factory_risk = "高"  # 中国→美国高关税

# 综合评分
risk_score = 3 + 3 + 3 = 9  # 综合风险=高
```

***

## 4. 快速开始

### 4.1 初始化数据库

```bash
# 进入py文件夹
cd data-service/py

# 执行SQL脚本创建表
psql $DATABASE_URL -f risk_data_model.sql

# 插入示例数据
psql $DATABASE_URL -f insert_sample_data.sql
psql $DATABASE_URL -f insert_tariff_data.sql
```

### 4.2 生成风险映射

```bash
# 运行风险评估脚本
python risk_mapping.py
```

### 4.3 查询风险数据

```sql
-- 查看高风险供应链
SELECT
    f.factory_name,
    p.product_name,
    rm.overall_risk_level,
    rm.risk_score
FROM risk_mapping rm
JOIN factory_master f ON rm.factory_id = f.factory_id
JOIN product_master p ON rm.product_id = p.product_id
WHERE rm.overall_risk_level = '高'
ORDER BY rm.risk_score DESC;
```

***

## 5. 文件结构

```
data-service/
├── py/                           # Python脚本目录
│   ├── risk_mapping.py          # 风险映射生成脚本
│   ├── adjust_tariff_rules.py    # 关税规则调整脚本
│   ├── create_tariff.py          # 关税表创建脚本
│   ├── insert_tariff.py          # 关税数据插入脚本
│   ├── verify_risk_mapping.py    # 风险映射验证脚本
│   ├── update_tariff.py          # 关税更新脚本
│   ├── check_tariff_dates.py     # 关税日期检查脚本
│   ├── update_tariff_dates.py    # 关税日期更新脚本
│   ├── execute_sql.py            # SQL执行脚本
│   └── *.sql                     # SQL脚本文件
│
│   ├── risk_data_model.sql       # 完整数据模型
│   ├── risk_mapping.sql          # 风险映射表定义
│   ├── create_tariff_table.sql   # 关税表定义
│   ├── insert_sample_data.sql    # 示例数据
│   ├── insert_tariff_data.sql    # 关税示例数据
│   ├── adjust_tariff_rules.sql   # 关税调整SQL
│   ├── update_tariff.sql         # 关税更新SQL
│   ├── update_tariff_dates.sql   # 关税日期更新SQL
│   └── data_model_documentation.md  # 数据模型文档（原）
│
├── DATA_DICTIONARY.md            # 数据字典（完整中文版）
├── schema.sql                    # 数据库Schema定义
└── README.md                     # 本文件
```

***

## 6. 更新记录

| 日期时间             | 数据端 | 后端 | 算法 | 前端 | 说明                                    |
| ---------------- | --- | -- | -- | -- | ------------------------------------- |
| 2026-04-04 17:00 | ✅   | -  | -  | -  | 初始数据库结构设计与seed\_data初始化               |
| 2026-04-04 18:00 | ✅   | -  | -  | -  | 新增menu菜单表（M001/M002/M203/M008）        |
| 2026-04-04 19:00 | ✅   | ✅  | -  | -  | 后端实现菜单管理CRUD接口（/api/menu/\*），采用标准三层架构 |
| 2026-04-04 20:00 | ✅   | -  | -  | -  | menu表新增M804菜单管理（/system/menu）         |
| 2026-04-08 00:00 | ✅   | -  | -  | -  | 数据库分层架构设计                             |
| 2026-04-08 02:30 | ✅   | -  | -  | -  | seed\_data.sql所有INSERT语句添加sci\_dw.前缀  |

***

## 附录：表间关系

```
工厂 (factory_master)
  ├── 1:N → 产品 (product_master)
  ├── 1:N → 供应路径 (supply_path)
  └── 1:N → 风险映射 (risk_mapping)

供应商 (supplier_master)
  └── 1:N → 供应路径 (supply_path)

产品 (product_master)
  ├── 1:N → BOM (bom_master)
  ├── 1:N → 销售订单 (sales_order)
  └── 1:N → 风险映射 (risk_mapping)

供应路径 (supply_path)
  └── 1:N → 风险映射 (risk_mapping)

关税规则 (tariff_rule)
  └── 被 risk_mapping 引用（通过 origin/dest/product_type）

订单 (orders) ← 1:N → 订单明细 (order_items)
```

***

**文档版本:** 3.0
**维护团队:** SCI Team
**最后更新:** 2026-04-08
