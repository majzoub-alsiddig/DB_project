"""
transactions.py  –  DBMS Transaction Logic
E-Commerce Mini-Project | Student Task 2 of 2

Implement the two functions below.
The client (client.py) calls them during checkout.

Learning goals
--------------
  • Use BEGIN / COMMIT / ROLLBACK explicitly.
  • Understand atomicity: all steps succeed or none do.
  • Handle concurrent stock updates safely (SELECT … FOR UPDATE pattern,
    or equivalent isolation in SQLite).
  • Return meaningful error messages to the caller.
"""

import sqlite3
from db import get_connection


# ── Result helper ─────────────────────────────────────────────────

class TxResult:
    """Simple value object returned by every transaction function."""
    def __init__(self, success: bool, message: str, data=None):
        self.success = success
        self.message = message
        self.data    = data          # optional extra payload

    def __repr__(self):
        return f"TxResult(success={self.success}, message={self.message!r})"


# ─────────────────────────────────────────────────────────────────
#  FUNCTION 1 – checkout
# ─────────────────────────────────────────────────────────────────

def checkout(user_id: int, cart: dict) -> TxResult:
    """
    Process a purchase for `user_id` using the items in `cart`.

    Parameters
    ----------
    user_id : int
        The ID of the logged-in user.
    cart : dict
        Mapping of  product_id (int)  →  quantity (int).
        Example: {1: 2, 4: 1}

    Returns
    -------
    TxResult
        .success  True if the transaction committed, False otherwise.
        .message  Human-readable outcome (shown in the CLI).
        .data     The new order_id on success, None on failure.

    Transaction steps (ALL must succeed, or ROLLBACK everything)
    ----------------
    1.  Validate the cart is not empty.
    2.  For each item in the cart:
          a. Lock / read the current product row.
          b. Check stock >= requested quantity  →  abort if not.
          c. Deduct the quantity from stock.
    3.  Compute the order total  (sum of price * quantity per item).
    4.  Verify the user has a card on file with sufficient balance.
    5.  Deduct the total from the card balance.
    6.  Insert a new row into `orders`  (status = 'paid').
    7.  Insert one row per cart item into `order_items`.
    8.  COMMIT.

    Hints
    -----
    • Open ONE connection and use it for the entire transaction.
    • Use  conn.execute("BEGIN")  before your first write.
    • On any error: conn.rollback(), then return TxResult(False, ...).
    • On success:   conn.commit(),  then return TxResult(True, ..., order_id).
    • SQLite does not support SELECT FOR UPDATE; instead read the row
      inside the same transaction before writing – this is sufficient
      for a single-server setup.
    • Use parameterised queries (?) – never format values into SQL strings.
    """

    # TODO: implement this function
    #raise NotImplementedError("checkout() is not yet implemented")
    
    if not cart:
        return TxResult(False, "Cart is empty.")

    conn = get_connection()
    try:
        conn.execute("BEGIN")

        # Step 2 – validate stock and collect prices
        total = 0.0
        items = []
        for product_id, quantity in cart.items():
            if quantity <= 0:
                conn.rollback()
                return TxResult(False, f"Invalid quantity for product {product_id}.")

            row = conn.execute(
                "SELECT * FROM products WHERE product_id = ?", (product_id,)
            ).fetchone()

            if row is None:
                conn.rollback()
                return TxResult(False, f"Product {product_id} not found.")

            if row["stock"] < quantity:
                conn.rollback()
                return TxResult(
                    False,
                    f"Insufficient stock for '{row['name']}' "
                    f"(requested {quantity}, available {row['stock']})."
                )

            total += row["price"] * quantity
            items.append({
                "product_id": product_id,
                "quantity":   quantity,
                "unit_price": row["price"],
            })

        # Step 3 – deduct stock
        for item in items:
            conn.execute(
                "UPDATE products SET stock = stock - ? WHERE product_id = ?",
    (item["quantity"], item["product_id"])
            )

        # Step 4 – check card balance
        card = conn.execute(
            "SELECT * FROM cards WHERE user_id = ?", (user_id,)
        ).fetchone()

        if card is None:
            conn.rollback()
            return TxResult(False, "No payment card found for this user.")

        if card["balance"] < total:
            conn.rollback()
            return TxResult(
                False,
                f"Insufficient funds. Total £{total:.2f}, "
                f"card balance £{card['balance']:.2f}."
            )

        # Step 5 – deduct balance
        conn.execute(
            "UPDATE cards SET balance = balance - ? WHERE user_id = ?",
    (total, user_id)
        )

        # Step 6 – create order
        cursor = conn.execute(
            
        "INSERT INTO orders (user_id, total, status) VALUES (?, ?, ?)",
    (user_id, total, "paid")
    )
        order_id = cursor.lastrowid

        # Step 7 – create order items
        for item in items:
            conn.execute(
        
        "INSERT INTO order_items (order_id, product_id, quantity, unit_price) "
        "VALUES (?, ?, ?, ?)",
        (order_id, item["product_id"], item["quantity"], item["unit_price"])
            )
            
        conn.commit()
        return TxResult(
            True,
            f"Payment of £{total:.2f} successful. Thank you for your order!",
            data=order_id
        )

    except sqlite3.Error as e:
        conn.rollback()
        return TxResult(False, f"Database error: {e}")
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────
#  FUNCTION 2 – refund_order
# ─────────────────────────────────────────────────────────────────

def refund_order(user_id: int, order_id: int) -> TxResult:
    """
    Refund a previously paid order.

    Parameters
    ----------
    user_id  : int   The requesting user (must own the order).
    order_id : int   The order to refund.

    Returns
    -------
    TxResult  as above.

    Transaction steps (ALL must succeed, or ROLLBACK everything)
    ----------------
    1.  Fetch the order; verify it exists and belongs to `user_id`.
    2.  Check the order status is 'paid'  →  abort if already refunded/failed.
    3.  For each item in order_items: restore the quantity back to stock.
    4.  Refund the order total back to the card balance.
    5.  Update the order status to 'refunded'.
    6.  COMMIT.

    Hints
    -----
    • Same connection/transaction rules as checkout().
    • Think about what happens if the product was deleted after purchase –
      handle (or at least consider) that edge case.
    """

    # TODO: implement this function
    #raise NotImplementedError("refund_order() is not yet implemented")

    conn = get_connection()
    try:
        conn.execute("BEGIN")

        # Step 1 – fetch and verify order ownership
        order = conn.execute(
            "SELECT * FROM orders WHERE order_id = ?", (order_id,)
        ).fetchone()

        if order is None:
            conn.rollback()
            return TxResult(False, f"Order #{order_id} not found.")

        if order["user_id"] != user_id:
            conn.rollback()
            return TxResult(False, "You do not own this order.")

        # Step 2 – must be 'paid' to refund
        if order["status"] != "paid":
            conn.rollback()
            return TxResult(False, f"Order #{order_id} cannot be refunded (status: {order['status']}).")

        # Step 3 – restore stock for each item
        items = conn.execute(
            "SELECT * FROM order_items WHERE order_id = ?", (order_id,)
        ).fetchall()

        for item in items:
            conn.execute(
                "UPDATE products SET stock = stock + ? WHERE product_id = ?",
        (item["quantity"], item["product_id"])
            )

        # Step 4 – refund to card
        conn.execute(
            "UPDATE cards SET balance = balance + ? WHERE user_id = ?",
    (order["total"], user_id)
        )

        # Step 5 – mark as refunded
        conn.execute(
            "UPDATE orders SET status = ? WHERE order_id = ?",
    ("refunded", order_id)
        )

        conn.commit()
        return TxResult(
            True,
            f"Order #{order_id} refunded. £{order['total']:.2f} returned to your card."
        )

    except sqlite3.Error as e:
        conn.rollback()
        return TxResult(False, f"Database error: {e}")
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────
#  Quick self-test  (python transactions.py)
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Transaction self-test ===")

    # Test 1: valid checkout
    cart = {1: 1, 2: 2}           # 1× Laptop Pro, 2× Wireless Mouse
    result = checkout(user_id=1, cart=cart)
    print(f"[checkout valid]   {result}")
    assert result.success, "Expected success for valid cart"

    # Test 2: insufficient stock  (order 100 laptops)
    result2 = checkout(user_id=1, cart={1: 100})
    print(f"[checkout no-stock] {result2}")
    assert not result2.success, "Expected failure for over-stock cart"

    # Test 3: insufficient balance (bob has only £200)
    result3 = checkout(user_id=2, cart={1: 1})   # Laptop costs £999.99
    print(f"[checkout no-funds] {result3}")
    assert not result3.success, "Expected failure for insufficient funds"

    # Test 4: refund the first order
    if result.data:
        result4 = refund_order(user_id=1, order_id=result.data)
        print(f"[refund valid]      {result4}")
        assert result4.success, "Expected success for valid refund"

    print("\nAll self-tests passed ✓")

