# Ledgerly design system

Ledgerly is invoicing for freelance translators. Screens are calm and exact: numbers line up, status is
always written out, and there is one primary action per view.

## Tokens

All values live in `styles/tokens.css`. Use the custom properties; never write a color, font, size or
spacing value anywhere else. If something you need has no token, add the token there first.

## Components

All component styles live in `styles/components.css`.

| Component | Markup | Use for |
|---|---|---|
| Action button | `<a class="action-button">` or `<button class="action-button">`; variants `action-button--secondary`, `action-button--quiet` | every call to action; one primary per view |
| Panel | `<div class="panel"><h3 class="panel__title">…</h3>…</div>` | grouping related content; this is the app's card |
| Banner | `<div class="banner" role="status">…</div>`; variants `banner--danger`, `banner--success` | full-width messages above the content |
| Badge | `<span class="badge">Paid</span>`; variants `badge--danger`, `badge--success` | short statuses, always as text |
| Data table | `<table class="data-table">`; class `num` on numeric cells | lists of records; numbers right-aligned |
| Site header, nav, footer | see `index.html` | the frame of every page |
