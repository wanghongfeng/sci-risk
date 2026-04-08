-- ============================================
-- Role Permission Management Script
-- Database Roles: a_appconnect, a_application
-- ============================================

-- ============================================
-- CREATE ROLES
-- ============================================

-- Database Developer Role (Read/Write/DDL access)
CREATE ROLE  a_appconnect WITH LOGIN PASSWORD 'developer_password';

-- Application Service Account Role
CREATE ROLE  a_application WITH LOGIN PASSWORD 'app_password';

-- ============================================
-- SCHEMA PERMISSIONS - SCI_IDL
-- ============================================

-- Developer: Full access
GRANT USAGE ON SCHEMA SCI_IDL TO a_appconnect;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA SCI_IDL TO a_appconnect;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA SCI_IDL TO a_appconnect;

-- Application: SELECT/INSERT/UPDATE/DELETE
GRANT USAGE ON SCHEMA SCI_IDL TO a_application;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA SCI_IDL TO a_application;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA SCI_IDL TO a_application;

-- ============================================
-- SCHEMA PERMISSIONS - SCI_ODS
-- ============================================

-- Developer: Full access
GRANT USAGE ON SCHEMA SCI_ODS TO a_appconnect;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA SCI_ODS TO a_appconnect;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA SCI_ODS TO a_appconnect;

-- Application: SELECT/INSERT/UPDATE/DELETE
GRANT USAGE ON SCHEMA SCI_ODS TO a_application;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA SCI_ODS TO a_application;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA SCI_ODS TO a_application;

-- ============================================
-- SCHEMA PERMISSIONS - SCI_DW
-- ============================================

-- Developer: Full access
GRANT USAGE ON SCHEMA SCI_DW TO a_appconnect;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA SCI_DW TO a_appconnect;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA SCI_DW TO a_appconnect;

-- Application: SELECT/INSERT/UPDATE/DELETE
GRANT USAGE ON SCHEMA SCI_DW TO a_application;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA SCI_DW TO a_application;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA SCI_DW TO a_application;

-- ============================================
-- SCHEMA PERMISSIONS - SCI_TMP
-- ============================================

-- Developer: Full access
GRANT USAGE ON SCHEMA SCI_TMP TO a_appconnect;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA SCI_TMP TO a_appconnect;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA SCI_TMP TO a_appconnect;

-- Application: SELECT/INSERT/UPDATE/DELETE
GRANT USAGE ON SCHEMA SCI_TMP TO a_application;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA SCI_TMP TO a_application;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA SCI_TMP TO a_application;

-- ============================================
-- SCHEMA PERMISSIONS - SCI_ADS
-- ============================================

-- Developer: Full access
GRANT USAGE ON SCHEMA SCI_ADS TO a_appconnect;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA SCI_ADS TO a_appconnect;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA SCI_ADS TO a_appconnect;

-- Application: SELECT/INSERT/UPDATE/DELETE
GRANT USAGE ON SCHEMA SCI_ADS TO a_application;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA SCI_ADS TO a_application;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA SCI_ADS TO a_application;

-- ============================================
-- SCHEMA PERMISSIONS - SCI_APP
-- ============================================

-- Developer: Full access
GRANT USAGE ON SCHEMA SCI_APP TO a_appconnect;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA SCI_APP TO a_appconnect;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA SCI_APP TO a_appconnect;

-- Application: ALL privileges (full access for application service)
GRANT ALL PRIVILEGES ON SCHEMA SCI_APP TO a_application;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA SCI_APP TO a_application;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA SCI_APP TO a_application;

-- ============================================
-- DEFAULT PRIVILEGES FOR FUTURE OBJECTS
-- ============================================

-- Set default privileges for a_appconnect role
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_IDL GRANT ALL ON TABLES TO a_appconnect;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_IDL GRANT ALL ON SEQUENCES TO a_appconnect;

ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_ODS GRANT ALL ON TABLES TO a_appconnect;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_ODS GRANT ALL ON SEQUENCES TO a_appconnect;

ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_DW GRANT ALL ON TABLES TO a_appconnect;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_DW GRANT ALL ON SEQUENCES TO a_appconnect;

ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_TMP GRANT ALL ON TABLES TO a_appconnect;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_TMP GRANT ALL ON SEQUENCES TO a_appconnect;

ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_ADS GRANT ALL ON TABLES TO a_appconnect;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_ADS GRANT ALL ON SEQUENCES TO a_appconnect;

ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_APP GRANT ALL ON TABLES TO a_appconnect;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_APP GRANT ALL ON SEQUENCES TO a_appconnect;

-- Set default privileges for a_application
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_IDL GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO a_application;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_IDL GRANT USAGE, SELECT ON SEQUENCES TO a_application;

ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_ODS GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO a_application;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_ODS GRANT USAGE, SELECT ON SEQUENCES TO a_application;

ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_DW GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO a_application;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_DW GRANT USAGE, SELECT ON SEQUENCES TO a_application;

ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_ADS GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO a_application;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_ADS GRANT USAGE, SELECT ON SEQUENCES TO a_application;

ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_APP GRANT ALL ON TABLES TO a_application;
ALTER DEFAULT PRIVILEGES IN SCHEMA SCI_APP GRANT ALL ON SEQUENCES TO a_application;

-- ============================================
-- ROLE DESCRIPTIONS
-- ============================================

COMMENT ON ROLE a_appconnect IS 'Database Developer: Full access to all schemas for development and maintenance';
COMMENT ON ROLE a_application IS 'Application Service Account: Operational access for application runtime';
