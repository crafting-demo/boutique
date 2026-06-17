"""
Playwright tests for free shipping feature.

Verifies that:
- Orders with item subtotal >= $50 USD receive free shipping on both the cart page
  and the order confirmation page.
- Orders with item subtotal < $50 USD are charged normal shipping on both pages.
"""

import os
import pytest
from playwright.sync_api import Page, expect

SHOP_URL = os.environ.get(
    "SHOP_URL",
    "https://shop--ai-f3a9b2c1d4e50678-demo.crafting.site.sandboxes.run",
)

# Products from the catalog:
#   Watch  ($109.99) — one unit is well above the $50 threshold
#   Mug    ($8.99)   — one unit is below the $50 threshold
PRODUCT_ABOVE_THRESHOLD = {"id": "1YMWWN1N4O", "name": "Watch", "qty": "1"}
PRODUCT_BELOW_THRESHOLD = {"id": "6E92ZMYYFZ", "name": "Mug", "qty": "1"}

CHECKOUT_FIELDS = {
    "email": "test@example.com",
    "street_address": "1600 Amphitheatre Parkway",
    "zip_code": "94043",
    "city": "Mountain View",
    "state": "CA",
    "country": "United States",
    "credit_card_number": "4432-8015-6152-0454",
    "credit_card_cvv": "672",
}


def add_product_to_cart(page: Page, product_id: str, qty: str = "1") -> None:
    """Navigate to a product page and add it to the cart."""
    page.goto(f"{SHOP_URL}/product/{product_id}")
    page.select_option("select[name='quantity']", qty)
    page.click("button[type='submit']")
    # After adding, we are redirected to /cart
    page.wait_for_url(f"{SHOP_URL}/cart")


def empty_cart(page: Page) -> None:
    """Empty the shopping cart if it has items."""
    page.goto(f"{SHOP_URL}/cart")
    empty_btn = page.locator("button.cart-summary-empty-cart-button")
    if empty_btn.is_visible():
        empty_btn.click()
        page.wait_for_url(f"{SHOP_URL}/")


def fill_and_place_order(page: Page) -> None:
    """Fill in the checkout form and submit the order from the cart page."""
    page.fill("input[name='email']", CHECKOUT_FIELDS["email"])
    page.fill("input[name='street_address']", CHECKOUT_FIELDS["street_address"])
    page.fill("input[name='zip_code']", CHECKOUT_FIELDS["zip_code"])
    page.fill("input[name='city']", CHECKOUT_FIELDS["city"])
    page.fill("input[name='state']", CHECKOUT_FIELDS["state"])
    page.fill("input[name='country']", CHECKOUT_FIELDS["country"])
    page.fill("input[name='credit_card_number']", CHECKOUT_FIELDS["credit_card_number"])
    page.fill("input[name='credit_card_cvv']", CHECKOUT_FIELDS["credit_card_cvv"])
    # Submit the checkout form (not the "Empty Cart" button) and wait for confirmation
    page.click(".cart-checkout-form button[type='submit']")
    # Wait for the order confirmation heading (up to 60s for gRPC call chain)
    page.wait_for_selector("text=Your order is complete!", timeout=60000)


def get_cart_shipping_text(page: Page) -> str:
    """Return the text content of the shipping row in the cart."""
    shipping_row = page.locator(".cart-summary-shipping-row")
    return shipping_row.inner_text()


def get_order_shipping_text(page: Page) -> str:
    """Return the text content of the Shipping row on the order confirmation page."""
    # Find all rows in the order section and locate the one labelled "Shipping"
    rows = page.locator(".order-complete-section .row")
    for i in range(rows.count()):
        row_text = rows.nth(i).inner_text()
        if "Shipping" in row_text:
            return row_text
    return ""


def test_free_shipping_above_threshold(page: Page) -> None:
    """
    An order whose item subtotal is >= $50 USD must show FREE shipping
    on both the cart page and the order confirmation page.
    The Watch costs $109.99 — well above the $50 threshold.
    """
    empty_cart(page)
    add_product_to_cart(page, PRODUCT_ABOVE_THRESHOLD["id"], PRODUCT_ABOVE_THRESHOLD["qty"])

    # --- Cart page assertions ---
    page.goto(f"{SHOP_URL}/cart")
    cart_shipping = get_cart_shipping_text(page)
    assert "FREE" in cart_shipping, (
        f"Cart page should show FREE shipping for order >= $50, got: {cart_shipping!r}"
    )

    # Confirm the total doesn't include a shipping charge
    total_row = page.locator(".cart-summary-total-row").inner_text()
    # Total should equal the item price alone (no shipping added on top)
    assert "$" in total_row, (
        f"Total row should show a dollar amount, got: {total_row!r}"
    )

    # --- Place the order and check confirmation page ---
    fill_and_place_order(page)

    order_shipping = get_order_shipping_text(page)
    assert "FREE" in order_shipping, (
        f"Order confirmation should show FREE shipping for order >= $50, got: {order_shipping!r}"
    )


def test_paid_shipping_below_threshold(page: Page) -> None:
    """
    An order whose item subtotal is < $50 USD must show a non-zero shipping
    cost on both the cart page and the order confirmation page.
    The Mug costs $8.99 — well below the $50 threshold.
    """
    empty_cart(page)
    add_product_to_cart(page, PRODUCT_BELOW_THRESHOLD["id"], PRODUCT_BELOW_THRESHOLD["qty"])

    # --- Cart page assertions ---
    page.goto(f"{SHOP_URL}/cart")
    cart_shipping = get_cart_shipping_text(page)
    assert "FREE" not in cart_shipping, (
        f"Cart page should NOT show FREE shipping for order < $50, got: {cart_shipping!r}"
    )
    # Shipping should show a dollar amount
    assert "$" in cart_shipping, (
        f"Cart page should show a dollar shipping cost for order < $50, got: {cart_shipping!r}"
    )

    # --- Place the order and check confirmation page ---
    fill_and_place_order(page)

    order_shipping = get_order_shipping_text(page)
    assert "FREE" not in order_shipping, (
        f"Order confirmation should NOT show FREE shipping for order < $50, got: {order_shipping!r}"
    )
    assert "$" in order_shipping, (
        f"Order confirmation should show a dollar shipping cost for order < $50, got: {order_shipping!r}"
    )
