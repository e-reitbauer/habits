---
id: playwright
title: Playwright
paths: ["**/playwright.config.*", "**/e2e/**", "**/*.e2e.ts"]
commands: ["npx playwright", "playwright"]
---
Playwright. Follow the official best practices (playwright.dev/docs/best-practices).

Locators and assertions
- Locate the way a user would: `getByRole` with a `name`, `getByLabel`, `getByPlaceholder`, `getByText`. Use `getByTestId` only where nothing accessible exists. No CSS or XPath tied to layout or generated class names.
- Use web-first assertions that wait on their own: `await expect(locator).toBeVisible()`, `toHaveText`, `toHaveURL`. Never `waitForTimeout`, and never assert on a one-off `isVisible()` result.
- Narrow with chaining and filters (`.filter({ hasText })`, a role inside a region) rather than `nth()`.

Structure
- Tests are independent and safe to run in parallel: each creates its own data (through the API, in fixtures) and uses unique names.
- Sign in once: a setup project saves `storageState` and tests reuse it. Don't log in through the UI in every test.
- Put shared setup in custom fixtures. Use page objects only where they remove real duplication.
- Mock third-party and network edges with `page.route` when the test isn't about them.

Config and debugging
- Set `baseURL`, `trace: 'on-first-retry'` and `screenshot: 'only-on-failure'`; retries only in CI.
- Debug from the trace (`npx playwright show-trace`) or `--ui`, and read it before changing the test.
- While iterating, run one test: `npx playwright test <file> -g "<name>" --project=chromium`.

Hygiene
- Gitignore `test-results/`, `playwright-report/`, `blob-report/`, `playwright/.cache/` and the auth state folder.
- Writing tests is different from driving a browser yourself to check visuals. Do the latter only where the project allows it.
