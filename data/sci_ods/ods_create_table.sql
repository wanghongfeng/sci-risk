-- ============================================
-- SCI_ODS Schema Table Creation Script
-- Operational Data Store Layer Tables
-- ============================================

-- ============================================
-- SEQUENCES
-- ============================================

CREATE SEQUENCE IF NOT EXISTS sci_ods.risk_events_id_seq;

-- ============================================
-- RISK EVENT TABLES
-- ============================================

-- Risk Events: Stores processed risk events from IDL layer
CREATE TABLE sci_ods.risk_events (
    id INT DEFAULT nextval('sci_ods.risk_events_id_seq'::regclass) PRIMARY KEY,
    source_channel VARCHAR(50),
    source_url VARCHAR(500),
    event_raw_text TEXT,
    event_raw_jsonb JSONB,
    event_happen_timestamp TIMESTAMP,
    dw_create_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dw_update_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_summary VARCHAR(200),
    event_start DATE,
    event_end DATE
);
