Phase 0 — The smallest working truth

We implement only this, nothing more:

Goal

Reproduce the simple test behavior, but through the framework.

Scope

One role: Admin

One user

One test:

login

open items page

verify table loads

Included

ENV loading

One admin user

UI login

Browser context

Page fixture

Excluded (intentionally)

Editors

Viewers

Parallelism

Seed reset

Mongo cleanup

Editor-specific seed

If this does not work, nothing else matters.

Phase 1 — Add global seed (still admin only)

Then we add:

Admin seed check

Create seed if missing

Use API login only for seed

UI login only for browser

Still:

One role

One test

Phase 2 — Add Viewer

Then:

Viewer user

Viewer test

Same admin seed

Viewer login → read-only verification

No editor yet.

Phase 3 — Add Editor isolation

Only after the above is stable:

Editor users

Editor seed

Visibility isolation

Parallel role usage

Final alignment check

You said:

Let’s understand, make decisions proper, then refactor, then add tests early

That is exactly what this plan does.

No over-engineering.
No big-bang refactor.
No guessing.



# Web Automation Framework – Architectural Decisions (Living Document)

**Status:** ACTIVE
**Last Updated:** Today
**Change Policy:**
Any change to framework behavior must first be reflected here before code changes.

---

## 1. Framework Objective (Anchor Decision)

### Decision

We are building a **web automation framework** using **Playwright (Python)** that:

* Drives the UI through a real browser
* Supports multiple user roles (Admin, Editor, Viewer)
* Executes tests in parallel
* Reuses login sessions intelligently
* Uses backend APIs only for **seed/setup**, not UI validation

This objective governs all downstream decisions.

---

## 2. Role Model (Authorization & Visibility)

### Defined Roles

* **ADMIN**
* **EDITOR**
* **VIEWER**

Roles are explicit and finite.

---

## 3. Data Visibility Rules (LOCKED)

### Admin

* Can create data
* Can see **all data**

  * Admin-created data
  * All editor-created data

### Editor

* Can create data
* Can see **only data created by that same editor**
* Cannot see:

  * Admin-created data
  * Other editors’ data

### Viewer

* Cannot create data
* Can see **everything an admin can see**
* Read-only access

These rules must be enforced by real authentication and backend behavior.
Tests must never simulate or fake visibility.

---

## 4. Test Responsibility Boundary

### Decision

Tests must express **intent only**.

Tests:

* Declare required role
* Exercise a business flow
* Assert UI behavior

Tests must NOT:

* Handle login
* Choose users
* Create seed data
* Manage browser lifecycle
* Enforce permissions manually

All mechanics belong to the framework layer.

---

## 5. User Management Model

### Decision

Users are **finite resources** loaded from environment variables.

* Each role has its own user pool
* Pool size defines maximum parallelism for that role
* If no user is available for a required role → **fail fast**

---

## 6. User Leasing Rules

### Decision

* Each test leases **exactly one user**
* A user cannot be shared between concurrent tests
* User is released only after test completion

No test may reuse another test’s user.

---

## 7. Login Strategy (Lazy & Cached)

### Decision

Login happens **per user**, not per test.

* Login is performed only when needed
* Authentication state is cached per user
* Subsequent tests reuse existing auth
* Maximum logins = number of users, not number of tests

---

## 8. Authentication Separation

### Decision

There are two distinct authentication paths:

#### UI Authentication

* Performed via Playwright
* Produces browser storage state
* Used only for UI navigation

#### API Authentication

* Performed via backend API
* Produces access token
* Used only for seed/setup operations

These mechanisms must never be mixed.

---

## 9. Seed Data Philosophy

### Decision

Seed data is **business-driven**, not schema-driven.

Seed exists to support:

* Table rendering
* Pagination
* Sorting
* Filtering
* Searching

Seed data must reflect real UI usage, not full backend schema coverage.

---

## 10. Global (Admin) Seed Data

### Decision

* Created using **one admin account**
* Created once per environment/run
* Checked before any test executes
* If exists → reused
* If missing → created
* Treated as **read-only** by tests

### Visibility

* Visible to Admin
* Visible to Viewer
* **Not visible to Editor**

---

## 11. Editor Seed Data

### Decision

* Created per editor
* Created lazily (only when editor is used)
* Scoped strictly to that editor
* Uses editor credentials (no admin impersonation)

### Visibility

* Visible only to the owning editor
* Invisible to:

  * Other editors
  * Viewer
  * Admin (unless backend explicitly allows override)

---

## 12. Viewer Data Rules

### Decision

* Viewer never creates seed data
* Viewer depends only on admin/global seed
* Viewer tests must be read-only

---

## 13. Seed Reset Policy

### Decision

Seed reset is **explicit and opt-in**.

* Controlled via `SEED_RESET=true`
* When enabled:

  * Existing seed data is deleted
  * Fresh seed data is created
* Default behavior: reuse existing data

---

## 14. Execution Model (Parallelism)

### Decision

* Workers are generic execution slots
* Tests declare role requirements
* Framework dynamically allocates users
* No worker-to-role mapping
* No hardcoded distribution

---

## 15. Failure Philosophy

### Decision

The framework must **fail fast** if:

* Required user is unavailable
* Authentication fails
* Required seed cannot be created
* Required environment variables are missing

No silent fallbacks. No partial success.

---

## 16. Configuration Source of Truth

### Decision

All environment-specific configuration comes from ENV:

* URLs
* Credentials
* Flags
* Database config

No hardcoded environment assumptions in code.

---

## 17. Change Discipline

### Rule

* Any behavioral change must first update this document
* Code must never lead the design
* This document evolves incrementally and deliberately

---

### End of Document (Version 1.0)
