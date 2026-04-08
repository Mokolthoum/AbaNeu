-- =============================================
-- VulnBank Database Schema
-- Generated: 2026-03-08
-- Database: SQLite3
-- WARNING: This file should not be publicly accessible!
-- =============================================

-- Users Table (Django auth_user)
CREATE TABLE IF NOT EXISTS auth_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME,
    is_superuser BOOL NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOL NOT NULL,
    is_active BOOL NOT NULL,
    date_joined DATETIME NOT NULL
);

-- User Profiles
CREATE TABLE IF NOT EXISTS bank_userprofile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id),
    bio TEXT DEFAULT '',
    phone VARCHAR(20) DEFAULT '',
    address TEXT DEFAULT '',
    profile_picture VARCHAR(100),
    date_of_birth DATE,
    national_id VARCHAR(20) DEFAULT ''
);

-- Bank Accounts
CREATE TABLE IF NOT EXISTS bank_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    account_number VARCHAR(20) NOT NULL UNIQUE,
    account_type VARCHAR(20) DEFAULT 'savings',
    balance DECIMAL(12,2) DEFAULT 0.00,
    created_at DATETIME NOT NULL,
    is_active BOOL DEFAULT TRUE
);

-- Transactions
CREATE TABLE IF NOT EXISTS bank_transaction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_account_id INTEGER NOT NULL REFERENCES bank_account(id),
    receiver_account_id INTEGER NOT NULL REFERENCES bank_account(id),
    amount DECIMAL(12,2) NOT NULL,
    description TEXT DEFAULT '',
    timestamp DATETIME NOT NULL,
    reference_number VARCHAR(30) DEFAULT ''
);

-- Support Tickets
CREATE TABLE IF NOT EXISTS bank_supportticket (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'open',
    created_at DATETIME NOT NULL,
    response TEXT DEFAULT ''
);

-- Uploaded Documents
CREATE TABLE IF NOT EXISTS bank_uploadeddocument (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES auth_user(id),
    title VARCHAR(200) NOT NULL,
    file VARCHAR(100) NOT NULL,
    description TEXT DEFAULT '',
    uploaded_at DATETIME NOT NULL
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_account_user ON bank_account(user_id);
CREATE INDEX IF NOT EXISTS idx_transaction_sender ON bank_transaction(sender_account_id);
CREATE INDEX IF NOT EXISTS idx_transaction_receiver ON bank_transaction(receiver_account_id);
CREATE INDEX IF NOT EXISTS idx_transaction_timestamp ON bank_transaction(timestamp);
CREATE INDEX IF NOT EXISTS idx_support_user ON bank_supportticket(user_id);

-- Default admin user (password: admin123)
-- INSERT INTO auth_user (username, password, is_superuser, is_staff, is_active, email, first_name, last_name, date_joined)
-- VALUES ('admin', 'pbkdf2_sha256$...', 1, 1, 1, 'admin@vulnbank.local', 'Admin', 'User', '2026-01-01');
