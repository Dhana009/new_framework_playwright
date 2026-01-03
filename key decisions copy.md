

# ✅ Web Automation Framework — Key Architectural Decisions (Final)

## 1. Framework Objective (Anchor Decision)

### What are we building?

A **production-grade, parallel, role-aware web automation framework** using **Playwright (Python)** that:

* Supports **Admin, Editor, Viewer** roles
* Runs **tests in parallel** with limited user resources
* Reuses **login state** efficiently
* Uses **business-driven seed data**
* Keeps **tests clean and declarative**

This objective is the anchor. Every decision below exists to serve this goal.

---

## 2. Execution Model (Decision #1)

### Decision

**Tests drive execution requirements, not workers.**

### Meaning

* Workers are just execution slots
* Tests declare *what they need* (role, flow)
* Framework dynamically allocates resources

### Why this matters

* Prevents worker → user hardcoding
* Enables safe parallelism
* Scales as test mix changes

**Status: LOCKED**

---

## 3. User & Role Management (Decision #2)

### Decision

**Users are finite resources managed via role-based pools.**

### Structure

* Separate pools for:

  * ADMIN
  * EDITOR
  * VIEWER
* Users are loaded **explicitly from ENV**
* Pool size = max parallelism for that role

### Behavior

* Test requests a role
* Framework leases one user from that role pool
* If no user available → fail fast

### Why this matters

* Makes resource limits explicit
* Avoids hidden permission bugs
* Matches real production constraints

**Status: LOCKED**

---

## 4. Login Strategy (Decision #3)

### Decision

**Login is cached per user, not per test and not per worker.**

### Meaning

* First time a user is used → login happens
* Auth state (cookies / tokens) is cached
* Subsequent tests reuse the same auth
* Maximum logins = number of users

### Key Clarification

* User lease ends after test
* Auth cache survives across tests

### Why this matters

* Keeps execution fast
* Avoids repeated logins
* Works naturally with parallel execution

**Status: LOCKED**

---

## 5. Lazy Initialization Everywhere (Decision #4)

### Decision

**Everything is lazy unless strictly required.**

### Lazy behaviors include

* User leasing happens only when a test starts
* Login happens only when auth is missing
* Seed data is created only if not present

### Why this matters

* Faster execution
* Deterministic behavior
* No unnecessary setup work

**Status: LOCKED**

---

## 6. Seed Data Philosophy (Decision #5)

### Decision

**Seed data is business-driven, not schema-driven.**

### Meaning

* Seed data exists to support **user flows**
* Derived from UI requirements:

  * Table display
  * Search
  * Filters
  * Sorting
  * Pagination
* We do NOT seed everything the backend schema allows

### Why this matters

* Prevents over-engineering
* Keeps datasets small and stable
* Aligns UI automation with real usage

**Status: LOCKED**

---

## 7. Seed Builders (Decision #6)

### Decision

**Use type-specific seed builders with a shared base.**

### Structure

* Base builder → common fields
* Specialized builders:

  * PHYSICAL
  * DIGITAL
  * SERVICE
* Conditional fields handled per type

### Constraints

* Builders only create **payloads**
* They do NOT decide:

  * How many records
  * When to create
  * Who owns the data

### Why this matters

* Handles conditional schemas cleanly
* Avoids massive factories
* Keeps payloads valid

**Status: LOCKED**

---

## 8. Seed Data Scope by Role (Decision #7)

### Decision

**Seed data scope is defined by role visibility.**

### Breakdown

* **Admin Seed**

  * Created once
  * Global visibility
  * Used by Admin & Viewer tests

* **Editor Seed**

  * Created lazily
  * Scoped per editor user
  * Owned by that editor

* **Viewer**

  * Never creates seed data
  * Only consumes existing data

### Why this matters

* Respects authorization rules
* Avoids invalid setups
* Keeps tests realistic

**Status: LOCKED**

---

## 9. Flow 3 Seed Data Strategy (Decision #8)

### Decision

**Flow 3 uses a shared, read-only baseline dataset.**

### Details

* 31 records (to support pagination)
* Supports:

  * Table rendering
  * Search
  * Filters
  * Sorting
  * Pagination
* Dataset is reused across all Flow 3 tests
* Tests must NOT mutate this data

### Why this matters

* One dataset → many tests
* Stable and deterministic
* Faster execution

**Status: LOCKED**

---

## 10. Editor-Specific Seed Data (Decision #9)

### Decision

**Editor seed data is created lazily per editor using editor credentials.**

### Meaning

* We do NOT pre-create editor seed data
* We do NOT predict which editor runs first
* Whichever editor is leased:

  * Seed is checked
  * Created if missing
  * Reused later

### Important

* Editor seed creation uses **editor API login**
* No admin impersonation

### Why this matters

* Correct permission modeling
* Works with parallelism
* Mirrors production behavior

**Status: LOCKED**

---

## 11. Test Responsibilities (Decision #10)

### Decision

**Tests declare intent, framework handles mechanics.**

### Tests DO

* Declare required role
* Exercise a business flow
* Assert UI behavior

### Tests DO NOT

* Handle login
* Manage users
* Create seed data
* Worry about permissions

### Why this matters

* Clean, readable tests
* Easier debugging
* Framework complexity is centralized

**Status: LOCKED**

---

## 12. Failure Philosophy (Decision #11)

### Decision

**Fail fast on invalid state or missing resources.**

### Examples

* Not enough users → fail
* Required seed cannot be created → fail
* Auth fails → retry once, then fail

### Why this matters

* No silent false positives
* Faster diagnosis
* CI stability

**Status: LOCKED**

---

## 13. Configuration Management (Decision #12)

### Decision

**All environment-specific configuration comes from ENV explicitly.**

### Includes

* Frontend URL
* Backend URL
* MongoDB URI
* DB name
* Collection name
* User credentials
* Reset flags

### Why this matters

* No hidden behavior
* Safe environment switching
* CI/CD friendly

**Status: LOCKED**

---

## 14. What Is Intentionally NOT Frozen

These are **implementation details**, allowed to evolve:

* Fixture names
* Folder structure tweaks
* Auth serialization format
* Retry policies
* Reporting integrations

These do NOT change the architecture.

---

## 15. Final Sanity Check

* No contradictions
* No hidden assumptions
* No shortcuts
* All decisions align with:

  * Production behavior
  * Parallel execution
  * Test pyramid
  * Interview expectations

**Architecture is now officially frozen.**

---

## ✅ Next Step (when you say so)

Now we are in the **execution phase**, not design.

The correct next step is:

👉 **Design Flow 3 test cases one by one (starting with Admin – list loads)**
(no rush, one test at a time, independent and stable)

When you’re ready, just say:

**“Let’s design Flow 3 – Test 1.”**

You’ve done this the right way.



1️⃣ First: What is a “test case” in our context? (Very important)

What is it?
In our framework and design:

A test case = one meaningful user intention validated end-to-end,
not one UI control, not one click, not one assertion.

So:

❌ “Click sort on Name” is not a test case

❌ “Verify page size dropdown” is not a test case

✅ “User can sort items meaningfully” is a test case

This definition is critical.


Decision: Seed data visibility is role-constrained.

Admin seed is global but hidden from editors

Editor seed is private and hidden from everyone else

Viewer sees only admin seed

Tests must never rely on data they are not authorized to see

This is now LOCKED.