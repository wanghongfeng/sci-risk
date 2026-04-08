-- Database Schema for SCI Risk System
-- Generated from Neon Database: holy-darkness-17426941
-- Database: neondb

-- ============================================
-- SEQUENCES
-- ============================================

CREATE SEQUENCE IF NOT EXISTS sci_dw.inventory_id_seq;
CREATE SEQUENCE IF NOT EXISTS sci_dw.logistics_id_seq;
CREATE SEQUENCE IF NOT EXISTS sci_dw.order_items_id_seq;
CREATE SEQUENCE IF NOT EXISTS sci_dw.orders_id_seq;
CREATE SEQUENCE IF NOT EXISTS sci_dw.risk_mapping_mapping_id_seq;
CREATE SEQUENCE IF NOT EXISTS sci_dw.users_id_seq;

-- ============================================
-- MASTER DATA TABLES
-- ============================================

-- Factory Master: Stores factory information
CREATE TABLE sci_dw.factory_master (
    factory_id VARCHAR(255) NOT NULL,
    factory_name VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    capacity INTEGER NOT NULL,
    main_markets VARCHAR(255),
    established_date DATE,
    status VARCHAR(255),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (factory_id)
);

CREATE INDEX idx_factory_country ON sci_dw.factory_master(country);

-- Supplier Master: Stores supplier/vendor information
CREATE TABLE sci_dw.supplier_master (
    supplier_id VARCHAR(255) NOT NULL,
    supplier_name VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    tier INTEGER NOT NULL,
    supplier_type VARCHAR(255),
    established_date DATE,
    credit_rating VARCHAR(255),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (supplier_id)
);

CREATE INDEX idx_supplier_country ON sci_dw.supplier_master(country);

-- Product Master: Stores product information
CREATE TABLE sci_dw.product_master (
    product_id VARCHAR(255) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    factory_id VARCHAR(255) NOT NULL,
    target_markets VARCHAR(255),
    base_price NUMERIC NOT NULL,
    product_type VARCHAR(255),
    launch_date DATE,
    PRIMARY KEY (product_id),
    FOREIGN KEY (factory_id) REFERENCES sci_dw.factory_master(factory_id)
);

CREATE INDEX idx_product_factory ON sci_dw.product_master(factory_id);

-- ============================================
-- SUPPLY CHAIN TABLES
-- ============================================

-- Bill of Materials Master: Stores BOM information
CREATE TABLE sci_dw.bom_master (
    bom_id VARCHAR(255) NOT NULL,
    product_id VARCHAR(255) NOT NULL,
    key_component_id VARCHAR(255) NOT NULL,
    key_component_name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    price NUMERIC NOT NULL,
    supplier_id VARCHAR(255),
    PRIMARY KEY (bom_id),
    FOREIGN KEY (product_id) REFERENCES sci_dw.product_master(product_id)
);

CREATE INDEX idx_bom_product ON sci_dw.bom_master(product_id);

-- Supply Path: Stores supply chain paths
CREATE TABLE sci_dw.supply_path (
    path_id VARCHAR(255) NOT NULL,
    key_component_id VARCHAR(255) NOT NULL,
    supplier_id VARCHAR(255) NOT NULL,
    supply_country VARCHAR(255) NOT NULL,
    factory_id VARCHAR(255) NOT NULL,
    path_type VARCHAR(255),
    lead_time INTEGER,
    transportation_mode VARCHAR(255),
    PRIMARY KEY (path_id),
    FOREIGN KEY (supplier_id) REFERENCES sci_dw.supplier_master(supplier_id),
    FOREIGN KEY (factory_id) REFERENCES sci_dw.factory_master(factory_id)
);

CREATE INDEX idx_supply_path_factory ON sci_dw.supply_path(factory_id);
CREATE INDEX idx_supply_path_supplier ON sci_dw.supply_path(supplier_id);

-- Tariff Rule: Stores tariff regulations
CREATE TABLE sci_dw.tariff_rule (
    tariff_id VARCHAR(255) NOT NULL,
    origin_country VARCHAR(255) NOT NULL,
    destination_country VARCHAR(255) NOT NULL,
    product_type VARCHAR(255) NOT NULL,
    current_tariff NUMERIC NOT NULL,
    future_tariff NUMERIC,
    effective_date DATE NOT NULL,
    expiry_date DATE,
    rule_status VARCHAR(255),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (tariff_id)
);

CREATE INDEX idx_tariff_origin ON sci_dw.tariff_rule(origin_country);
CREATE INDEX idx_tariff_destination ON sci_dw.tariff_rule(destination_country);
CREATE INDEX idx_tariff_product ON sci_dw.tariff_rule(product_type);

-- ============================================
-- RISK MANAGEMENT TABLES
-- ============================================

-- Risk Mapping: Stores risk assessment results
CREATE TABLE sci_dw.risk_mapping (
    mapping_id INTEGER DEFAULT nextval('sci_dw.risk_mapping_mapping_id_seq'::regclass) NOT NULL,
    path_id VARCHAR(255) NOT NULL,
    product_id VARCHAR(255) NOT NULL,
    factory_id VARCHAR(255) NOT NULL,
    supplier_id VARCHAR(255),
    origin_country VARCHAR(255) NOT NULL,
    destination_country VARCHAR(255) NOT NULL,
    current_tariff NUMERIC,
    tariff_risk_level VARCHAR(255),
    product_risk_level VARCHAR(255),
    factory_risk_level VARCHAR(255),
    overall_risk_level VARCHAR(255),
    risk_score INTEGER,
    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (mapping_id),
    FOREIGN KEY (path_id) REFERENCES sci_dw.supply_path(path_id),
    FOREIGN KEY (product_id) REFERENCES sci_dw.product_master(product_id),
    FOREIGN KEY (factory_id) REFERENCES sci_dw.factory_master(factory_id)
);

CREATE INDEX idx_risk_mapping_path ON sci_dw.risk_mapping(path_id);
CREATE INDEX idx_risk_mapping_product ON sci_dw.risk_mapping(product_id);
CREATE INDEX idx_risk_mapping_factory ON sci_dw.risk_mapping(factory_id);
CREATE INDEX idx_risk_mapping_overall ON sci_dw.risk_mapping(overall_risk_level);

-- ============================================
-- SALES ORDER TABLES
-- ============================================

-- Sales Order: Stores sales order information
CREATE TABLE sci_dw.sales_order (
    order_id VARCHAR(255) NOT NULL,
    product_id VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    sales_country VARCHAR(255) NOT NULL,
    price NUMERIC NOT NULL,
    order_date DATE NOT NULL,
    delivery_date DATE,
    status VARCHAR(255),
    PRIMARY KEY (order_id),
    FOREIGN KEY (product_id) REFERENCES sci_dw.product_master(product_id)
);

CREATE INDEX idx_sales_order_product ON sci_dw.sales_order(product_id);
CREATE INDEX idx_sales_order_country ON sci_dw.sales_order(sales_country);

-- ============================================
-- OPERATIONAL TABLES
-- ============================================

-- Inventory: Stores inventory/stock information
CREATE TABLE sci_dw.inventory (
    id INTEGER DEFAULT nextval('sci_dw.inventory_id_seq'::regclass) NOT NULL,
    sku VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(255),
    quantity INTEGER NOT NULL,
    unit_price NUMERIC,
    warehouse_location VARCHAR(255),
    status VARCHAR(255),
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    PRIMARY KEY (id),
    UNIQUE (sku)
);

CREATE INDEX ix_public_inventory_category ON sci_dw.inventory(category);

-- Orders: Stores customer orders
CREATE TABLE sci_dw.orders (
    id INTEGER DEFAULT nextval('sci_dw.orders_id_seq'::regclass) NOT NULL,
    order_no VARCHAR(255) NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_contact VARCHAR(255),
    total_amount NUMERIC,
    status VARCHAR(255) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    PRIMARY KEY (id),
    UNIQUE (order_no)
);

-- Order Items: Stores order line items
CREATE TABLE sci_dw.order_items (
    id INTEGER DEFAULT nextval('sci_dw.order_items_id_seq'::regclass) NOT NULL,
    order_id INTEGER NOT NULL,
    sku VARCHAR(255) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC NOT NULL,
    total_price NUMERIC NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (order_id) REFERENCES sci_dw.orders(id) ON DELETE CASCADE
);

CREATE INDEX ix_public_order_items_order_id ON sci_dw.order_items(order_id);

-- Logistics: Stores logistics/shipping information
CREATE TABLE sci_dw.logistics (
    id INTEGER DEFAULT nextval('sci_dw.logistics_id_seq'::regclass) NOT NULL,
    tracking_no VARCHAR(255) NOT NULL,
    order_id INTEGER,
    carrier VARCHAR(255),
    origin VARCHAR(255),
    destination VARCHAR(255),
    status VARCHAR(255) NOT NULL,
    estimated_delivery TIMESTAMP,
    actual_delivery TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    PRIMARY KEY (id),
    UNIQUE (tracking_no)
);

CREATE INDEX ix_public_logistics_order_id ON sci_dw.logistics(order_id);

-- ============================================
-- USER MANAGEMENT TABLES
-- ============================================

-- Users: Stores user information
CREATE TABLE sci_dw.users (
    id INTEGER DEFAULT nextval('sci_dw.users_id_seq'::regclass) NOT NULL,
    name VARCHAR(255) NOT NULL,
    photo VARCHAR(255) NOT NULL,
    status VARCHAR(255) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    password_hash VARCHAR(255) NOT NULL DEFAULT '',
    role VARCHAR(255) NOT NULL DEFAULT 'viewer',
    PRIMARY KEY (id)
);

-- ============================================
-- MENU TABLES
-- ============================================

-- Menu: Stores navigation menu structure
CREATE TABLE sci_dw.menu (
    menu_id VARCHAR(50) PRIMARY KEY,
    menu_name VARCHAR(100) NOT NULL,
    menu_code VARCHAR(50) NOT NULL,
    parent_id VARCHAR(50) DEFAULT '0',
    route_path VARCHAR(255),
    icon VARCHAR(50),
    sort_order INT DEFAULT 0,
    is_visible BOOLEAN DEFAULT TRUE,
    permission VARCHAR(100),
    component VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_menu_parent ON sci_dw.menu(parent_id);
CREATE INDEX idx_menu_code ON sci_dw.menu(menu_code);
CREATE INDEX idx_menu_sort ON sci_dw.menu(sort_order);
