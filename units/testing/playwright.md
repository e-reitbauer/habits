---
id: playwright
title: Playwright
paths: ["**/playwright.config.*", "**/e2e/**", "**/*.e2e.ts"]
commands: ["npx playwright", "playwright"]
---
Playwright:
- Locate elements by role, label or test id (`getByRole`, `getByLabel`, `getByTestId`). Avoid CSS and XPath selectors tied to layout.
- Use web-first assertions (`await expect(locator).toBeVisible()`); never `waitForTimeout` or manual sleeps.
- Keep tests independent, each with its own data. Reuse sign-in through `storageState` in a setup project instead of logging in through the UI in every test.
- Keep traces on failure (`trace: 'on-first-retry'`), and read the trace before guessing at a fix.
- Generated output (`test-results/`, `playwright-report/`, `blob-report/`, the auth state folder) stays gitignored.
- Writing Playwright tests is different from driving a browser yourself to check visuals. Do the latter only where the project allows it; some projects prefer that the user checks visuals.
