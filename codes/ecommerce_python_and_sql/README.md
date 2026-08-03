# ShopDB – DBMS Mini-Project

## Overview

You are building the back-end of a simple e-commerce system.
A command-line client is **provided**; your job is to design the
database schema and implement the transaction logic.

```
┌─────────────────────┐          ┌──────────────────────┐
│     client.py       │  calls   │   transactions.py    │
│  (CLI – provided)   │ ──────►  │   ← YOU WRITE THIS   │
└─────────────────────┘          └──────────┬───────────┘
                                            │ uses
                                  ┌─────────▼───────────┐
                                  │       db.py         │
                                  │  (helpers–provided) │
                                  └─────────┬───────────┘
                                            │
                                  ┌─────────▼───────────┐
                                  │      shop.db        │
                                  │  ← YOU DESIGN THIS  │
                                  └─────────────────────┘
```

---

## File Guide

| File | Your task |
|------|-----------|
| `schema.sql` | **Task 1** – complete the SQL schema |
| `transactions.py` | **Task 2** – implement transaction functions |
| `db.py` | Provided. Read it; do not edit. |
| `client.py` | Provided. Read it; do not edit. |

---

## Setup

### Requirements

- Python 3.9+
- SQLite3 (bundled with Python)
- Optional colour output: `pip install colorama`

### First-time setup
 
```bash 
# 1. Create the database from your schema
sqlite3 shop.db < schema.sql

# 2. Verify seed data loaded
sqlite3 shop.db "SELECT * FROM products;"

# 3. Run the app
python client.py
```

Log in as **alice** (balance £1 500) or **bob** (balance £200).

---

## Task 1 – Schema Design (`schema.sql`)

Open `schema.sql`. Three sections are marked **TODO**:

| Section | What to write |
|---------|---------------|
| Section 2 | `CREATE TABLE orders` |
| Section 3 | `CREATE TABLE order_items` |
| Section 4 | At least 2 `CREATE INDEX` statements |

**Constraints to include:**

- `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `CHECK` where appropriate.
- A `DEFAULT` value for `status` and for the timestamp column.
- The unit price in `order_items` must be a **snapshot** (not a FK to products.price).

**Deliverable:** `shop.db` created cleanly by `sqlite3 shop.db < schema.sql` with no errors.

---

## Task 2 – Transaction Functions (`transactions.py`)

Implement the two functions:

### `checkout(user_id, cart) → TxResult`

Completes a purchase atomically:

1. Validate the cart is not empty.
2. For each item: check stock is sufficient → deduct stock.
3. Compute the order total.
4. Check the user's card balance ≥ total → deduct balance.
5. Insert into `orders` (status `'paid'`).
6. Insert one row per item into `order_items`.
7. **COMMIT** – or **ROLLBACK** on any failure.

### `refund_order(user_id, order_id) → TxResult`

Reverses a paid order atomically:

1. Verify the order exists and belongs to this user.
2. Verify status is `'paid'`.
3. Restore stock for each item.
4. Refund the total to the card balance.
5. Set order status to `'refunded'`.
6. **COMMIT** – or **ROLLBACK** on any failure.

### Rules

- Use **one connection** per transaction.
- Issue `conn.execute("BEGIN")` explicitly before any writes.
- Use **parameterised queries** (`?`) – never format values into SQL strings.
- Return a `TxResult` object in every code path.

### Self-test

```bash
python transactions.py
```

All four assertions must pass before submission.

---

## Discussion Questions (in-lab)

1. What would happen if you committed after each SQL statement instead of once at the end?
2. Two users buy the last unit of a product simultaneously – how does SQLite handle this? What would a production database do differently?
3. Why is `unit_price` stored in `order_items` rather than looked up from `products` at query time?
4. What isolation level does SQLite use by default, and what anomalies does it prevent?
