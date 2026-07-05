# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

LotAlfWeb ("Los Décimos de Ildefonso") is a Flask web app for tracking a personal
collection of Spanish *Lotería Nacional* tickets (*décimos*) and the lottery
retailers (*administraciones*) they came from. The UI is entirely in Spanish.
It shows retailers on a Leaflet map, lets an authenticated user mark numbers/retailers
as owned, and renders collection statistics.

## Running

```bash
pip install -r requirements.txt
python run.py            # dev server (Flask), imports the app object from app/
gunicorn app:app         # production entrypoint (gunicorn is in requirements)
```

There is **no test suite, linter, or build step** configured in this repo.

### Required environment variables

The app will not start without these — the form classes and the Postgres DB
wrappers read them at import/instantiation time:

- `DB_USER`, `DB_PASSWORD`, `DB_ADDRESS`, `DB_PORT`, `DB_NAME` — PostgreSQL connection
- `SECRET_KEY` — Flask session signing (falls back to a hardcoded default in `config.py`)

Note: `NumberForm`/`RetailerForm` in `app/forms.py` open a SQLite connection **at class
definition time** (module import). Importing `app.forms` (and therefore `app.routes`)
touches `app/lotalf.db` immediately.

## Architecture

### App wiring
`app/__init__.py` builds a single module-level `app` object (no app factory),
configures Flask-Bootstrap, then imports `app.routes` at the bottom. All routes live
in `app/routes.py`. `run.py` and the gunicorn entrypoint both just re-export this `app`.

### Two-database split — this is the central design fact
The app reads from **two different databases** with two different access styles:

1. **SQLite reference data** (`app/lotalf.db`, wrapped by `app/local_db.py`) —
   read-only lookup data checked into the repo. Tables: `towns` (region → province →
   town hierarchy) and `lottery_retailers` (the full known-universe of retailers).
   Queries are built with **raw f-string SQL** (no parameterization).

2. **PostgreSQL collection data** (env-configured, one wrapper class per table) —
   the user's mutable collection, accessed via **SQLAlchemy `automap_base`** which
   reflects the schema at runtime rather than declaring models:
   - `app/numbers_collection_db.py` → `numbers_collection` table
   - `app/retailers_collection_db.py` → `retailers_collection` table
   - `app/comments_db.py` → `comments` table (the guestbook/"Tablón")

   Each wrapper opens its own engine + session in `__init__`; callers are expected to
   call `close_connection()`. Query results are returned as **pandas DataFrames** and
   most route logic manipulates them with pandas before serializing to JSON.

The `local_db` (SQLite, all-known retailers) and `retailers_collection_db` (Postgres,
owned retailers) are queried in parallel and merged: `update_map` builds the full set
from SQLite, overlays owned rows from Postgres via a pandas `.update()` on a
`(retailer_province, retailer_town, retailer_number)` multi-index, and flags each as
owned/not-owned to pick the map marker color.

### Frontend
Server-rendered Jinja2 templates extending `bootstrap_base.html` → `base.html`
(navbar + login box). Interactivity is jQuery + AJAX POSTs to the JSON routes, plus
**Leaflet** with `markercluster` for the retailer map. `app/templates/map.html`
exposes an `insert_map` macro pulled server-side via `get_template_attribute` and
injected with generated marker JavaScript from `create_marker()` in `routes.py`
(marker JS is built by string concatenation). Chart rendering helpers live in
`app/static/statistics_utils.js`; retailer-page logic in `app/static/retailers_utils.js`.

### Auth & sessions
"Edit mode" is a single hardcoded password (`2Galletas!` in the `/login` route) that
sets `session['logged_in']`. All mutating routes gate on `session['logged_in']`.
Cascading dropdowns (region → province → town) and the "current number" are also kept
in the Flask `session` and drive server-side `SelectField.choices` population.

### Image upload flow
Retailer photos round-trip through a temp file at `/tmp/image.jpg`: the browser POSTs
a base64 webp to `/store_image` (written to disk), and `retailers_collection`
reads it back, base64-encodes it, and stores it in the Postgres `image` column.
This path is Unix-specific (`/tmp`).

## Conventions & gotchas

- **Location strings are stored lowercase** in the DBs and `.title()`-cased for display.
  Route handlers routinely `.title()` values before querying SQLite but pass raw values
  to Postgres — keep this asymmetry in mind when adding filters.
- The `RequiredIf` validator in `forms.py` is a custom conditional-required WTForms
  validator (its `super().__init__` is intentionally not fully wired — copied from a gist).
- Several DB methods `print()` their SQL for debugging; that's existing behavior, not a bug.
- Windows dev note: the primary shell here is PowerShell, but the image-upload and
  temp-file code assumes a Unix `/tmp`.
