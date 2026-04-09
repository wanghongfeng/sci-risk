-- ============================================
-- SCI_IDL Schema Table Creation Script
-- Interface/Data Landing Layer Tables
-- ============================================

-- ============================================
-- SEQUENCES
-- ============================================

CREATE SEQUENCE IF NOT EXISTS sci_idl.risk_events_id_seq;

-- ============================================
-- RISK EVENT TABLES
-- ============================================

-- Risk Events: Stores raw risk events from external sources
CREATE TABLE sci_idl.risk_events (
    id INT DEFAULT nextval('sci_idl.risk_events_id_seq'::regclass) PRIMARY KEY,
    source_channel VARCHAR(50),
    source_url VARCHAR(500),
    event_raw_text TEXT,
    event_raw_jsonb JSONB,
    event_happen_timestamp TIMESTAMP,
    dw_create_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
