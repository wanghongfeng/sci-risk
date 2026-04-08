-- ============================================
-- Role Permission Management Script
-- Database Roles: viewer, developer, application
-- ============================================

-- ============================================
-- CREATE ROLES
-- ============================================

-- Database Viewer Role (Read-only access)
CREATE ROLE IF NOT EXISTS sci_db_viewer WITH LOGIN PASSWORD 'viewer_password';

-- Database Developer Role (Read/Write/DDL access)
CREATE ROLE IF NOT EXISTS sci_db_developer WITH LOGIN PASSWORD 'developer_password';

-- Application Service Account Role
CREATE ROLE IF NOT EXISTS sci_app_service WITH LOGIN PASSWORD 'app_password';

-- ============================================
-- SCHEMA PERMISSIONS - SCI_IDL
-- ============================================

-- Viewer: SELECT on all tables
GRANT USAGE ON SCHEMA SCI_IDL TO sci_db_viewer;
GRANT SELECT ON ALL TABLES IN SCHEMA SCI_IDL TO sci_db_viewer;

-- Developer: Full access
GRANT USAGE ON SCHEMA SCI_IDL TO sci_db_developer;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA SCI_IDL TO sci_db_developer;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA SCI_IDL TO sci_db_developer;

-- Application: SELECT/INSERT/UPDATE/DELETE
GRANT USAGE ON SCHEMA SCI_IDL TO sci_app_service;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA SCI_IDL TO sci_app_service;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA SCI_IDL TO sci_app_service;

-- ============================================
-- SCHEMA PERMISSIONS - SCI_ODS
-- ============================================

-- Viewer: SELECT on all tables
GRANT USAGE ON SCHEMA SCI_ODS TO sci_db_viewer;
GRANT SELECT ON ALL TABLES IN SCHEMA SCI_ODS TO sci_db_viewer;

-- Developer: Full access
GRANT USAGE ON SCHEMA SCI_ODS TO sci_db_developer;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA SCI_ODS TO sci_db_developer;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA SCI_ODS TO sci_db_developer;

-- Application: SELECT/INSERT/UPDATE/DELETE
GRANT USAGE ON SCHEMA SCI_ODS TO sci_app_service;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA SCI_ODS TO sci_app_service;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA SCI_ODS TO sci_app_service;

-- ============================================
-- SCHEMA PERMISSIONS - SCI_DW
-- ============================================

-- Viewer: SELECT on all tables
GRANT USAGE ON SCHEMA SCI_DW TO sci_db_viewer;
GRANT SELECT ON ALL TABLES IN SCHEMA SCI_DW TO sci_db_viewer;

-- Developer: Full access
GRANT USAGE ON SCHEMA SCI_DW TO sci_db_developer;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA SCI_DW TO sci_db_developer;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA SCI_DW TO sci_db_developer;

-- Application: SELECT/INSERT/UPDATE/DELETE
GRANT USAGE ON SCHEMA SCI_DW TO sci_app_service;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA SCI_DW TO sci_app_service;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA SCI_DW TO sci_app_service;

-- ============================================
-- SCHEMA PERMISSIONS - SCI_TMP
-- ============================================

-- Viewer: No access (temporary data)
-- Note: TMP schema typically not visible to viewers

-- Developer: Full access
GRANT USAGE ON SCHEMA SCI_TMP TO sci_db_developer;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA SCI_TMP TO sci_db_developer;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA SCI_TMP TO sci_db_developer;

-- Application: SELECT/INSERT/UPDATE/DELETE
GRANT USAGE ON SCHEMA SCI_TMP TO sci_app_service;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA SCI_TMP TO sci_app_service;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA SCI_TMP TO sci_app_service;

-- ============================================
-- SCHEMA PERMISSIONS - SCI_ADS
-- ============================================

-- Viewer: SELECT on all tables
GRANT USAGE ON SCHEMA SCI_ADS TO sci_db_viewer;
GRANT SELECT ON ALL TABLES IN SCHEMA SCI_ADS TO sci_db_viewer;

-- Developer: Full access
GRANT USAGE ON SCHEMA SCI_ADS TO sci_db_developer;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA SCI_ADS TO sci_db_developer;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA SCI_ADS TO sci_db_developer;

-- Application: SELECT/INSERT/UPDATE/DELETE
GRANT USAGE ON SCHEMA SCI_ADS TO sci_app_service;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA SCI_ADS TO sci_app_service;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA SCI_ADS TO sci_app_service;

-- ============================================
-- DEFAULT PRIVILEGES FOR FUTURE OBJECTS
-- ============================================

-- Set default privileges for developer role
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_IDL GRANT ALL ON TABLES TO sci_db_developer;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_IDL GRANT ALL ON SEQUENCES TO sci_db_developer;

ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_ODS GRANT ALL ON TABLES TO sci_db_developer;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_ODS GRANT ALL ON SEQUENCES TO sci_db_developer;

ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_DW GRANT ALL ON TABLES TO sci_db_developer;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_DW GRANT ALL ON SEQUENCES TO sci_db_developer;

ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_TMP GRANT ALL ON TABLES TO sci_db_developer;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_TMP GRANT ALL ON SEQUENCES TO sci_db_developer;

ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_ADS GRANT ALL ON TABLES TO sci_db_developer;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_ADS GRANT ALL ON SEQUENCES TO sci_db_developer;

-- Set default privileges for app service
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_IDL GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO sci_app_service;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_IDL GRANT USAGE, SELECT ON SEQUENCES TO sci_app_service;

ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_ODS GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO sci_app_service;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_ODS GRANT USAGE, SELECT ON SEQUENCES TO sci_app_service;

ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_DW GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO sci_app_service;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_DW GRANT USAGE, SELECT ON SEQUENCES TO sci_app_service;

ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_ADS GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO sci_app_service;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_ADS GRANT USAGE, SELECT ON SEQUENCES TO sci_app_service;

-- ============================================
-- ROLE DESCRIPTIONS
-- ============================================

COMMENT ON ROLE sci_db_viewer IS 'Database Viewer: Read-only access to all schemas for data analysis and reporting';
COMMENT ON ROLE sci_db_developer IS 'Database Developer: Full access to all schemas for development and maintenance';
COMMENT ON ROLE sci_app_service IS 'Application Service Account: Operational access for application runtime';
