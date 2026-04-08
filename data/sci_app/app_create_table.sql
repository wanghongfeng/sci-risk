-- ============================================
-- SCI_APP Schema Table Creation Script
-- Application System Layer Tables
-- ============================================

-- ============================================
-- SEQUENCES
-- ============================================

CREATE SEQUENCE IF NOT EXISTS sci_app.ussesrs_id_seq;

-- ============================================
-- USER MANAGEMENT TABLES
-- ============================================

-- Users: Stores user information
CREATE TABLE sci_app.users (
    id INTEGER DEFAULT nextval('sci_app.users_id_seq'::regclass) NOT NULL,
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
CREATE TABLE sci_app.menu (
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

CREATE INDEX idx_menu_parent ON sci_app.menu(parent_id);
CREATE INDEX idx_menu_code ON sci_app.menu(menu_code);
CREATE INDEX idx_menu_sort ON sci_app.menu(sort_order);
