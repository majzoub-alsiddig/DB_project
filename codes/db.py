"""
db.py  –  Database access layer
E-Commerce Mini-Project | PROVIDED (do not modify)

Connects to the SQLite database and exposes helper functions
that the server calls to read/write data.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "shop.db")


def get_connection():
    """Return a connection with foreign-key enforcement enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # rows behave like dicts
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# ── Products ──────────────────────────────────────────────────────

def fetch_all_products():
    """Return every product with stock > 0."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT product_id, name, description, price, stock "
            "FROM products WHERE stock > 0 ORDER BY name"
        ).fetchall()


def fetch_product(product_id):
    """Return a single product row, or None."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM products WHERE product_id = ?", (product_id,)
        ).fetchone()


# ── Users & Cards ─────────────────────────────────────────────────

def fetch_user(username):
    """Return the user row for the given username, or None."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()


def fetch_card(user_id):
    """Return the first card on file for a user, or None."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM cards WHERE user_id = ?", (user_id,)
        ).fetchone()


# ── Orders ────────────────────────────────────────────────────────

def fetch_orders_for_user(user_id):
    """Return all orders (newest first) for a given user."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()


def fetch_order_items(order_id):
    """Return line items joined with product names for an order."""
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT oi.quantity, oi.unit_price,
                   p.name,
                   oi.quantity * oi.unit_price AS line_total
            FROM   order_items oi
            JOIN   products    p  ON p.product_id = oi.product_id
            WHERE  oi.order_id = ?
            """,
            (order_id,)
        ).fetchall()
