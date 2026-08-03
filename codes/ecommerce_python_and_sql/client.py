"""
client.py  –  Command-Line Interface
E-Commerce Mini-Project | PROVIDED (do not modify)

Run:
    python client.py

The client calls your transaction functions in transactions.py.
Make sure your database is initialised first:
    sqlite3 shop.db < schema.sql
"""

import sys
from db import fetch_all_products, fetch_user, fetch_orders_for_user, fetch_order_items
from transactions import checkout, refund_order

# ── Colour helpers (gracefully degrade on Windows) ────────────────
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    def green(s):  return Fore.GREEN  + str(s) + Style.RESET_ALL
    def red(s):    return Fore.RED    + str(s) + Style.RESET_ALL
    def cyan(s):   return Fore.CYAN   + str(s) + Style.RESET_ALL
    def yellow(s): return Fore.YELLOW + str(s) + Style.RESET_ALL
    def bold(s):   return Style.BRIGHT + str(s) + Style.RESET_ALL
except ImportError:
    def green(s):  return str(s)
    def red(s):    return str(s)
    def cyan(s):   return str(s)
    def yellow(s): return str(s)
    def bold(s):   return str(s)


# ── Utilities ─────────────────────────────────────────────────────

def clear():
    print("\n" * 2)

def hr(char="─", width=54):
    print(char * width)

def prompt(msg, valid=None):
    """Read input, optionally validate against a set of options."""
    while True:
        val = input(msg).strip()
        if valid is None or val in valid:
            return val
        print(red(f"  Invalid option. Choose from: {', '.join(valid)}"))

def press_enter():
    input(yellow("\n  Press Enter to continue…"))


# ── Login ─────────────────────────────────────────────────────────

def login():
    print(bold("\n  Welcome to ShopDB"))
    hr()
    while True:
        username = input("  Enter your username (alice / bob): ").strip()
        user = fetch_user(username)
        if user:
            print(green(f"  Logged in as {user['username']} (id={user['user_id']})"))
            return dict(user)
        print(red("  User not found. Try again."))


# ── Product listing ───────────────────────────────────────────────

def show_products(cart):
    clear()
    print(bold("  📦  Product Catalogue"))
    hr()
    products = fetch_all_products()
    if not products:
        print(red("  No products available."))
        return products

    fmt = "  {:<4} {:<24} {:>8}  Stock:{:>4}  In cart:{}"
    print(fmt.format("ID", "Name", "Price", "", ""))
    hr("·")
    for p in products:
        in_cart = cart.get(p["product_id"], 0)
        cart_str = yellow(str(in_cart)) if in_cart else "0"
        print(fmt.format(
            p["product_id"],
            p["name"][:23],
            f"£{p['price']:.2f}",
            p["stock"],
            cart_str
        ))
    hr()
    return products


# ── Cart management ───────────────────────────────────────────────

def cart_total(cart, products):
    price_map = {p["product_id"]: p["price"] for p in products}
    return sum(price_map.get(pid, 0) * qty for pid, qty in cart.items())


def show_cart(cart, products):
    clear()
    print(bold("  🛒  Your Cart"))
    hr()
    if not cart:
        print("  (empty)")
    else:
        price_map = {p["product_id"]: (p["name"], p["price"]) for p in products}
        for pid, qty in cart.items():
            name, price = price_map.get(pid, ("Unknown", 0))
            print(f"  {name[:28]:<28}  x{qty}  £{price * qty:.2f}")
        hr("·")
        print(f"  {'TOTAL':<30}  £{cart_total(cart, products):.2f}")
    hr()


# ── Order history ─────────────────────────────────────────────────

def show_order_history(user):
    clear()
    print(bold(f"  📋  Order History – {user['username']}"))
    hr()
    orders = fetch_orders_for_user(user["user_id"])
    if not orders:
        print("  No orders yet.")
        press_enter()
        return

    for o in orders:
        status_fmt = green(o["status"]) if o["status"] == "paid" else red(o["status"])
        print(f"  Order #{o['order_id']}  |  {o['created_at']}  |  "
              f"£{o['total']:.2f}  |  {status_fmt}")
        items = fetch_order_items(o["order_id"])
        for it in items:
            print(f"      {it['name']:<26} x{it['quantity']}  £{it['line_total']:.2f}")
        print()
    press_enter()


# ── Checkout flow ─────────────────────────────────────────────────

def checkout_flow(user, cart, products):
    if not cart:
        print(red("  Your cart is empty."))
        press_enter()
        return cart

    show_cart(cart, products)
    confirm = prompt("  Proceed to payment? [y/n]: ", {"y", "n"})
    if confirm == "n":
        return cart

    print(cyan("\n  Processing payment…"))
    result = checkout(user_id=user["user_id"], cart=cart)

    if result.success:
        print(green(f"\n  ✅  {result.message}"))
        print(green(f"     Order ID: #{result.data}"))
        cart = {}                   # clear cart on success
    else:
        print(red(f"\n  ❌  {result.message}"))

    press_enter()
    return cart


# ── Refund flow ───────────────────────────────────────────────────

def refund_flow(user):
    orders = fetch_orders_for_user(user["user_id"])
    paid = [o for o in orders if o["status"] == "paid"]
    if not paid:
        print(red("  No refundable orders."))
        press_enter()
        return

    print(bold("\n  Paid orders:"))
    for o in paid:
        print(f"  [{o['order_id']}]  £{o['total']:.2f}  on  {o['created_at']}")

    order_id_str = input("  Enter order ID to refund (or 0 to cancel): ").strip()
    if not order_id_str.isdigit() or int(order_id_str) == 0:
        return

    result = refund_order(user_id=user["user_id"], order_id=int(order_id_str))
    if result.success:
        print(green(f"\n  ✅  {result.message}"))
    else:
        print(red(f"\n  ❌  {result.message}"))
    press_enter()


# ── Main loop ─────────────────────────────────────────────────────

def main():
    user = login()
    cart: dict = {}          # product_id → quantity

    while True:
        products = show_products(cart)

        print("\n  Options:")
        print("  [a] Add item to cart       [r] Remove item from cart")
        print("  [v] View cart              [c] Checkout")
        print("  [h] Order history          [f] Refund an order")
        print("  [q] Quit")
        hr()

        choice = prompt("  > ", {"a", "r", "v", "c", "h", "f", "q"})

        if choice == "q":
            print(bold("\n  Goodbye!\n"))
            sys.exit(0)

        elif choice == "a":
            pid_str = input("  Product ID to add: ").strip()
            if pid_str.isdigit():
                pid = int(pid_str)
                qty_str = input("  Quantity: ").strip()
                if qty_str.isdigit() and int(qty_str) > 0:
                    cart[pid] = cart.get(pid, 0) + int(qty_str)
                    print(green("  Added."))
                else:
                    print(red("  Invalid quantity."))
            else:
                print(red("  Invalid product ID."))
            press_enter()

        elif choice == "r":
            pid_str = input("  Product ID to remove: ").strip()
            if pid_str.isdigit() and int(pid_str) in cart:
                del cart[int(pid_str)]
                print(green("  Removed."))
            else:
                print(red("  Item not in cart."))
            press_enter()

        elif choice == "v":
            show_cart(cart, products)
            press_enter()

        elif choice == "c":
            cart = checkout_flow(user, cart, products)

        elif choice == "h":
            show_order_history(user)

        elif choice == "f":
            refund_flow(user)


if __name__ == "__main__":
    main()
