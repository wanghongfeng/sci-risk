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

-- Create SCI_APP Schema (Application System Layer)
CREATE SCHEMA IF NOT EXISTS SCI_APP;

