"""
Playwright e2e tests for free shipping on orders >= $50.

Tests the full user flow:
1. Order OVER $50: Add a Watch ($109.99), verify FREE shipping on cart page,
   place order, verify FREE shipping on confirmation page.
2. Order UNDER $50: Add a Bamboo Glass Jar ($5.49), verify shipping is NOT free
   on cart page, place order, verify shipping is NOT free on confirmation page.
"""
import os
import re
import pytest
from playwright.sync_api import Page, expect

BASE_URL = os.environ.get(
    "BASE_URL",
    "https://shop--ai-d8f3a7b1c2e49f06-demo.crafting.site.sandboxes.run",
)

# Product IDs from products.json
WATCH_ID = "1YMWWN1N4O"       # $109.99 - over $50
GLASS_JAR_ID = "9SIQT8TOJO"   # $5.49  - under $50


def _empty_cart(page: Page):
    """Navigate to cart and empty it if items exist."""
    page.goto(f"{BASE_URL}/cart")
    page.wait_for_load_state("networkidle")
    empty_btn = page.locator("button:has-text('Empty Cart')")
    if empty_btn.count() > 0:
        empty_btn.click()
        page.wait_for_load_state("networkidle")


def _add_product(page: Page, product_id: str, quantity: int = 1):
    """Add a product to cart by visiting its page and submitting the form."""
    page.goto(f"{BASE_URL}/product/{product_id}")
    page.wait_for_load_state("networkidle")
    page.select_option('select[name="quantity"]', str(quantity))
    page.click('button:has-text("Add to Cart")')
    page.wait_for_load_state("networkidle")


def _place_order(page: Page):
    """Fill in checkout form and place order from the cart page."""
    page.click('button:has-text("Place Order")')
    page.wait_for_load_state("networkidle")


class TestFreeShippingOver50:
    """Order with subtotal >= $50 should get free shipping."""

    def test_cart_shows_free_shipping(self, page: Page):
        _empty_cart(page)
        _add_product(page, WATCH_ID, 1)  # $109.99

        # Should now be on cart page
        page.wait_for_selector(".cart-summary-shipping-row")

        shipping_row = page.locator(".cart-summary-shipping-row")
        shipping_text = shipping_row.inner_text()
        assert "FREE" in shipping_text, (
            f"Expected 'FREE' in shipping row for order >= $50, got: {shipping_text}"
        )

        # Total should NOT include shipping (should equal item price)
        total_row = page.locator(".cart-summary-total-row")
        total_text = total_row.inner_text()
        assert "$109.99" in total_text, (
            f"Expected total $109.99 (no shipping), got: {total_text}"
        )

    def test_order_confirmation_shows_free_shipping(self, page: Page):
        _empty_cart(page)
        _add_product(page, WATCH_ID, 1)  # $109.99

        _place_order(page)

        # Verify we're on the order confirmation page
        expect(page.locator("text=Your order is complete!")).to_be_visible(timeout=15000)

        # Check Shipping row shows FREE
        page_content = page.content()
        assert "FREE" in page_content, (
            "Expected 'FREE' on order confirmation page for order >= $50"
        )

        # Verify the Shipping row specifically
        shipping_cells = page.locator("text=Shipping").locator("..")
        shipping_row_text = shipping_cells.inner_text()
        assert "FREE" in shipping_row_text, (
            f"Expected 'FREE' in Shipping row, got: {shipping_row_text}"
        )

        # Total should equal item price (no shipping)
        total_row = page.locator("text=Total Paid").locator("..")
        total_text = total_row.inner_text()
        assert "$109.99" in total_text, (
            f"Expected Total Paid $109.99 (no shipping), got: {total_text}"
        )


class TestPaidShippingUnder50:
    """Order with subtotal < $50 should have normal (non-free) shipping."""

    def test_cart_shows_paid_shipping(self, page: Page):
        _empty_cart(page)
        _add_product(page, GLASS_JAR_ID, 1)  # $5.49

        page.wait_for_selector(".cart-summary-shipping-row")

        shipping_row = page.locator(".cart-summary-shipping-row")
        shipping_text = shipping_row.inner_text()
        assert "FREE" not in shipping_text, (
            f"Did NOT expect 'FREE' shipping for order < $50, got: {shipping_text}"
        )
        # Shipping should show a dollar amount
        assert "$" in shipping_text, (
            f"Expected a dollar-amount shipping cost, got: {shipping_text}"
        )

    def test_order_confirmation_shows_paid_shipping(self, page: Page):
        _empty_cart(page)
        _add_product(page, GLASS_JAR_ID, 1)  # $5.49

        _place_order(page)

        expect(page.locator("text=Your order is complete!")).to_be_visible(timeout=15000)

        # The Shipping row should show a dollar amount, not FREE
        shipping_cells = page.locator("text=Shipping").locator("..")
        shipping_row_text = shipping_cells.inner_text()
        assert "FREE" not in shipping_row_text, (
            f"Did NOT expect 'FREE' in Shipping row for order < $50, got: {shipping_row_text}"
        )
        assert "$" in shipping_row_text, (
            f"Expected a dollar-amount shipping cost in confirmation, got: {shipping_row_text}"
        )
