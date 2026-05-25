# Spec: Login and Logout

## Overview
Implement session-based login and logout so registered users can authenticate into Spendly and securely sign out. This step upgrades the existing stub `GET /login` into a fully functional POST-accepting route that validates credentials, starts a Flask session, and redirects to the dashboard (placeholder for now). The `GET /logout` stub is also completed — it clears the session and redirects back to the landing page. After this step, the app knows *who* is logged in, which is the prerequisite for all protected routes (profile, expense list, add/edit/delete) in future steps.

## Depends on
- Step 01 — Database setup (`users` table, `get_db()`, `check_password_hash`)
- Step 02 — Registration (`create_user()` — users must exist before they can log in)

## Routes
- `GET /login` — render login form — public (already exists as stub, upgrade to handle flash messages)
- `POST /login` — validate credentials, start session, redirect to `/dashboard` (or `/` for now) — public
- `GET /logout` — clear session, flash confirmation, redirect to `/` — logged-in (stub already exists, implement it)

## Database changes
No new tables or columns needed.

A new DB helper must be added to `database/db.py`:
- `get_user_by_email(email)` — fetches one row from `users` by email (case-insensitive). Returns a `sqlite3.Row` or `None` if not found. Used by the login route to look up the user before verifying the password.

## Templates
- **Modify:** `templates/login.html`
  - The form already has `method="POST"` and `action="{{ url_for('login') }}"` — keep it
  - Add a flash message block above the form (same pattern as `register.html`) to display errors such as "Invalid email or password"
  - No other visual changes needed

- **Modify:** `templates/base.html`
  - Update the `nav-links` section to show context-aware links:
    - When **not** logged in (no `session['user_id']`): show existing "Sign in" and "Get started" links
    - When **logged in**: hide "Sign in" / "Get started"; show the user's name and a "Sign out" link pointing to `url_for('logout')`
  - Use Jinja2 `{% if session.get('user_id') %}` to branch — no Python changes needed

## Files to change
- `app.py` — upgrade `login()` to handle `GET` and `POST`; implement `logout()`; import `session` from Flask
- `database/db.py` — add `get_user_by_email(email)` helper
- `templates/login.html` — add flash message display block
- `templates/base.html` — make nav links session-aware

## Files to create
None.

## New dependencies
No new dependencies. Uses `werkzeug.security.check_password_hash` (already installed) and Flask's built-in `session`, `flash`, `redirect`, `url_for`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use f-strings in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- Use Flask's built-in `session` dict (not cookies or JWT) — `app.secret_key` is already set
- Store only `user_id` and `user_name` in the session — never store the password hash or full row
- On failed login, show a **generic** error message: "Invalid email or password" — do not reveal whether the email exists
- On successful login, `flash` a welcome message and `redirect` to `url_for('landing')` (dashboard does not exist yet)
- `logout()` must call `session.clear()` before redirecting
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values
- Use `url_for()` for every internal link — never hardcode URLs

## Definition of done
- [ ] `GET /login` renders the login form without errors
- [ ] Submitting the form with a valid email + password starts a session, flashes a welcome message, and redirects
- [ ] Submitting with a wrong password re-renders the login form with "Invalid email or password" — no session started
- [ ] Submitting with an email that does not exist re-renders the login form with the same generic error
- [ ] Submitting with empty fields re-renders the form with a validation error (server-side)
- [ ] `GET /logout` clears the session, flashes "You have been signed out", and redirects to `/`
- [ ] After logout, visiting `/login` shows the login form (session is gone)
- [ ] `base.html` navbar shows "Sign in / Get started" when logged out, and user name + "Sign out" when logged in
- [ ] The demo user (`demo@spendly.com` / `password123`) can log in and out successfully
