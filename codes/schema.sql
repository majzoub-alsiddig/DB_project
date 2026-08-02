-- ============================================================
--  E-COMMERCE DATABASE SCHEMA
--  DBMS Mini-Project | Student Task 1 of 2
-- ============================================================
--  Instructions:
--    Complete every section marked TODO.
--    Do NOT modify table names or column names already given.
--    Run this file once to initialise your database:
--        sqlite3 shop.db < schema.sql
-- ============================================================

-- ----------------------------------------------------------------
-- SECTION 1: Core tables (PROVIDED – read carefully, do not edit)
-- ----------------------------------------------------------------

CREATE TABLE IF NOT EXISTS products (
    product_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT    NOT NULL,
    description  TEXT,
    price        REAL    NOT NULL CHECK (price >= 0),
    stock        INTEGER NOT NULL CHECK (stock >= 0)
);

CREATE TABLE IF NOT EXISTS users (
    user_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    username     TEXT    NOT NULL UNIQUE,
    email        TEXT    NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS cards (
    card_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL REFERENCES users(user_id),
    card_number  TEXT    NOT NULL,          -- stored as last-4 digits only
    balance      REAL    NOT NULL CHECK (balance >= 0)
);

-- ----------------------------------------------------------------
-- SECTION 2: TODO – design the orders table
-- ----------------------------------------------------------------
-- Requirements:
--   • Each order belongs to one user.
--   • Record the total amount charged and when the order was placed.
--   • Include a status field: 'pending' | 'paid' | 'failed'|'refunded'
--   • Use a DEFAULT value for status and for the timestamp.
--   • Enforce referential integrity with a FOREIGN KEY.
--
-- TODO: Write the CREATE TABLE statement for "orders" below.

-- <your SQL here>


-- ----------------------------------------------------------------
-- SECTION 3: TODO – design the order_items table
-- ----------------------------------------------------------------
-- Requirements:
--   • Each row records one product line within an order.
--   • Store quantity and the unit price AT TIME OF PURCHASE
--     (prices can change later – this must be a snapshot).
--   • An order can have many items; one item belongs to one order.
--   • Enforce referential integrity for both order and product.
--
-- TODO: Write the CREATE TABLE statement for "order_items" below.

-- <your SQL here>


-- ----------------------------------------------------------------
-- SECTION 4: TODO – useful indexes
-- ----------------------------------------------------------------
-- Add at least TWO indexes that would speed up common queries
-- (e.g. looking up orders by user, or items by order).
--
-- TODO: Write your CREATE INDEX statements below.

-- <your SQL here>


-- ----------------------------------------------------------------
-- SECTION 5: Seed data (PROVIDED – do not edit)
-- ----------------------------------------------------------------

INSERT OR IGNORE INTO products (name, description, price, stock) VALUES
    ('Laptop Pro 15',   'High-performance laptop',        999.99, 10),
    ('Wireless Mouse',  'Ergonomic wireless mouse',        29.99, 50),
    ('USB-C Hub',       '7-in-1 USB-C hub',                49.99, 30),
    ('Mechanical Keyboard', 'RGB mechanical keyboard',    89.99, 20),
    ('Monitor 27"',     '4K IPS display',                399.99,  8),
    ('Webcam HD',       '1080p webcam with mic',           59.99, 25);

INSERT OR IGNORE INTO users (username, email) VALUES
    ('alice',  'alice@example.com'),
    ('bob',    'bob@example.com');

INSERT OR IGNORE INTO cards (user_id, card_number, balance) VALUES
    (1, '4242', 1500.00),   -- alice
    (2, '1234',  200.00);   -- bob
