# Tests

Pytest suite for the FastAPI backend. Structured by *layer*, not by feature,
so you can see the difference between testing pure logic, the database, and
the HTTP API:

```
tests/
  conftest.py       # fixtures shared by everything below -- read this first
  factories.py       # helpers for building model rows that have a lot of
                      # required columns (e.g. Exercises)
  unit/               # pure functions, no DB, no network (hashing, JWT)
  crud/               # backend/crud/* functions, called directly against
                      # a real (transactional, rolled-back) DB session
  api/                # full HTTP round trips through the FastAPI app via
                      # httpx.AsyncClient, exactly like a real client would
```

When you add a new feature, the rule of thumb is: if it's a standalone
function with no side effects, it gets a `unit/` test; if it touches the
database, a `crud/` test; if you want to check the route wiring, status
codes, and response shape, an `api/` test. Most features end up with one
or two of the three, not all three -- don't feel obligated to triplicate
everything.

## Running

```bash
# from the repo root, with backend/venv activated (or prefix commands with
# backend/venv/bin/)
pytest
pytest tests/unit                     # just the fast, DB-free tests
pytest -k biometrics                  # anything with "biometrics" in the name
pytest --cov=backend --cov-report=term-missing   # coverage
```

## How the database fixtures work

Tests run against a **real, disposable Postgres database**, not sqlite —
a couple of models (`workout_templates`, `program_templates`,
`exercise_history`) use Postgres's `JSONB` column type, which sqlite can't
represent, so an in-memory sqlite DB would silently test something
different from what runs in production.

- `docker-compose up -d` must be running (the same Postgres container the
  app itself uses) before you run the suite.
- On session start, `tests/conftest.py` creates `<your db name>_test` and
  runs `Base.metadata.create_all` against it. It's dropped again when the
  session ends. Your real database is never touched.
- Every test gets its own `db_session` fixture: one connection, one
  transaction, and a SAVEPOINT-based session (`join_transaction_mode=
  "create_savepoint"`) so that when application code calls `db.commit()`
  internally (which most of `backend/crud` does), it only releases a
  savepoint instead of ending the test's transaction. The outer
  transaction is rolled back after every test, so nothing you create in
  one test is visible in the next — no manual cleanup, no test ordering
  dependencies.
- `client` is an `httpx.AsyncClient` pointed at the FastAPI app in-process
  (via `ASGITransport`, no real socket), with the `get_db` dependency
  overridden to hand out that same `db_session`. That's what lets a test
  set up rows with the ORM and then immediately see them through the API,
  or vice versa.
- `auth_client` is a `client` that has already called `/auth/register`
  and `/auth/token` for a throwaway user and carries its bearer token in
  `Authorization` — reach for this whenever the route you're testing
  requires `get_current_user`.

## A note on the `xfail` tests

A few tests (search for `xfail` in `tests/api/`) document real bugs found
while writing this suite — places where a service function is missing a
`return`, or a route's `response_model` doesn't match what it actually
returns, so FastAPI's response validation turns a 200 into an unhandled
500. They're marked `xfail` (expected-to-fail) rather than deleted so
they: (a) don't break the suite today, and (b) start failing loudly — as
an "unexpectedly passing" test — the moment someone fixes the underlying
bug, which is your cue to remove the `xfail` marker. It's a useful pattern
any time you find a real bug that's out of scope for what you're doing
right now but still worth a permanent record of.

## Extending this

- New CRUD module → copy the shape of `tests/crud/test_user_crud.py`.
- New router → copy `tests/api/test_biometrics_api.py`; use `auth_client`
  if it needs a logged-in user, `client` if it doesn't.
- New model with several required, non-obvious columns → add a
  `build_x` / `persist_x` pair to `tests/factories.py` rather than
  repeating the field list in every test.
