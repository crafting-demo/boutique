const { test, expect } = require('@playwright/test');

// Watch costs $109.99 — well over $50 threshold
const EXPENSIVE_PRODUCT_ID = '1YMWWN1N4O';
// Bamboo Glass Jar costs $5.49 — under $50 threshold
const CHEAP_PRODUCT_ID = '9SIQT8TOJO';

test.describe('Free shipping on orders over $50', () => {

  test.beforeEach(async ({ page }) => {
    // Empty the cart before each test by visiting cart and clicking empty if available
    await page.goto('/cart');
    const emptyBtn = page.locator('button:has-text("Empty Cart")');
    if (await emptyBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await emptyBtn.click();
      await page.waitForURL('**/');
    }
  });

  test('order over $50 gets free shipping on cart page and confirmation page', async ({ page }) => {
    // Add Watch ($109.99) to cart — this is over $50
    await page.goto(`/product/${EXPENSIVE_PRODUCT_ID}`);
    await page.locator('button:has-text("Add to Cart")').click();
    await page.waitForURL('**/cart');

    // ASSERT: Cart page shows "FREE" shipping
    const cartShippingRow = page.locator('.cart-summary-shipping-row');
    await expect(cartShippingRow).toBeVisible();
    const cartShippingValue = cartShippingRow.locator('.text-right');
    await expect(cartShippingValue).toHaveText('FREE');

    // ASSERT: Cart total should NOT include shipping (total = item subtotal)
    const cartTotalRow = page.locator('.cart-summary-total-row');
    const cartTotalValue = cartTotalRow.locator('.text-right');
    await expect(cartTotalValue).toHaveText('$109.99');

    // Place the order using the pre-filled form values
    await page.locator('button:has-text("Place Order")').click();
    await page.waitForURL('**/cart/checkout');

    // ASSERT: Order confirmation page exists
    await expect(page.locator('text=Your order is complete!')).toBeVisible();

    // ASSERT: Order confirmation page shows "FREE" shipping
    const shippingRow = page.locator('.border-bottom-solid.padding-y-24').filter({ hasText: 'Shipping' });
    await expect(shippingRow).toBeVisible();
    const shippingValue = shippingRow.locator('.text-right');
    await expect(shippingValue).toHaveText('FREE');

    // ASSERT: Total paid equals the item cost (no shipping)
    const totalRow = page.locator('.padding-y-24').filter({ hasText: 'Total Paid' });
    await expect(totalRow).toBeVisible();
    const totalValue = totalRow.locator('.text-right');
    await expect(totalValue).toHaveText('$109.99');
  });

  test('order under $50 gets normal shipping on cart page and confirmation page', async ({ page }) => {
    // Add Bamboo Glass Jar ($5.49) to cart — this is under $50
    await page.goto(`/product/${CHEAP_PRODUCT_ID}`);
    await page.locator('button:has-text("Add to Cart")').click();
    await page.waitForURL('**/cart');

    // ASSERT: Cart page shows a dollar amount for shipping (NOT "FREE")
    const cartShippingRow = page.locator('.cart-summary-shipping-row');
    await expect(cartShippingRow).toBeVisible();
    const cartShippingValue = cartShippingRow.locator('.text-right');
    const cartShippingText = await cartShippingValue.textContent();
    expect(cartShippingText.trim()).not.toBe('FREE');
    expect(cartShippingText.trim()).toMatch(/^\$/);

    // ASSERT: Total includes shipping (should be more than $5.49)
    const cartTotalRow = page.locator('.cart-summary-total-row');
    const cartTotalText = await cartTotalRow.locator('.text-right').textContent();
    const totalVal = parseFloat(cartTotalText.trim().replace('$', ''));
    expect(totalVal).toBeGreaterThan(5.49);

    // Place the order
    await page.locator('button:has-text("Place Order")').click();
    await page.waitForURL('**/cart/checkout');

    // ASSERT: Order confirmation page exists
    await expect(page.locator('text=Your order is complete!')).toBeVisible();

    // ASSERT: Order confirmation page shows a shipping cost (NOT "FREE")
    const shippingRow = page.locator('.border-bottom-solid.padding-y-24').filter({ hasText: 'Shipping' });
    await expect(shippingRow).toBeVisible();
    const shippingValue = shippingRow.locator('.text-right');
    const orderShippingText = await shippingValue.textContent();
    expect(orderShippingText.trim()).not.toBe('FREE');
    expect(orderShippingText.trim()).toMatch(/^\$/);

    // ASSERT: Total paid includes shipping
    const totalRow = page.locator('.padding-y-24').filter({ hasText: 'Total Paid' });
    await expect(totalRow).toBeVisible();
    const totalPaidText = await totalRow.locator('.text-right').textContent();
    const orderTotal = parseFloat(totalPaidText.trim().replace('$', ''));
    expect(orderTotal).toBeGreaterThan(5.49);
  });

});
