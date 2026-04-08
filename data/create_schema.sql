-- ============================================
-- Schema Creation Script
-- Create all SCI schemas in the database
-- ============================================

-- Create SCI_IDL Schema (Interface/Data Landing Layer)
CREATE SCHEMA IF NOT EXISTS SCI_IDL;

-- Create SCI_ODS Schema (Operational Data Store Layer)
CREATE SCHEMA IF NOT EXISTS SCI_ODS;

-- Create SCI_DW Schema (Data Warehouse Layer)
CREATE SCHEMA IF NOT EXISTS SCI_DW;

-- Create SCI_TMP Schema (Temporary Layer)
CREATE SCHEMA IF NOT EXISTS SCI_TMP;

-- Create SCI_ADS Schema (Application Data Store Layer)
CREATE SCHEMA IF NOT EXISTS SCI_ADS;

-- Grant usage on schemas to public role (if needed)
GRANT USAGE ON SCHEMA SCI_IDL TO public;
GRANT USAGE ON SCHEMA SCI_ODS TO public;
GRANT USAGE ON SCHEMA SCI_DW TO public;
GRANT USAGE ON SCHEMA SCI_TMP TO public;
GRANT USAGE ON SCHEMA SCI_ADS TO public;
