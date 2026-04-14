-- ============================================
-- Schema Creation Script
-- Create all SCI schemas in the database
-- ============================================

-- Create SCI_IDL Schema (Interface/Data Landing Layer)
CREATE SCHEMA IF NOT EXISTS SCI_IDL;
ALTER SCHEMA SCI_IDL OWNER TO a_appconnect;

-- Create SCI_ODS Schema (Operational Data Store Layer)
CREATE SCHEMA IF NOT EXISTS SCI_ODS;
ALTER SCHEMA SCI_ODS OWNER TO a_appconnect;

-- Create SCI_DW Schema (Data Warehouse Layer)
CREATE SCHEMA IF NOT EXISTS SCI_DW;
ALTER SCHEMA SCI_DW OWNER TO a_appconnect;

-- Create SCI_TMP Schema (Temporary Layer)
CREATE SCHEMA IF NOT EXISTS SCI_TMP;
ALTER SCHEMA SCI_TMP OWNER TO a_appconnect;

-- Create SCI_ADS Schema (Application Data Store Layer)
CREATE SCHEMA IF NOT EXISTS SCI_ADS;
ALTER SCHEMA SCI_ADS OWNER TO a_appconnect;

-- Create SCI_APP Schema (Application System Layer)
CREATE SCHEMA IF NOT EXISTS SCI_APP;
ALTER SCHEMA SCI_APP OWNER TO a_appconnect;

