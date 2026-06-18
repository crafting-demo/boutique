const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: '.',
  timeout: 60000,
  retries: 1,
  use: {
    baseURL: process.env.BASE_URL || 'http://frontend:8080',
    headless: true,
    ignoreHTTPSErrors: true,
  },
});
