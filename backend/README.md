# Los décimos de Ildefonso — backend (FastAPI)

The new API for the Vue 3 frontend. It **reuses your existing data** — it does
not create a new database and does not migrate anything.

## Data safety (by design)
- **Postgres** (your collection: `comments`, `numbers_collection`,
  `retailers_collection`) is **reflected at runtime** with `automap` — exactly
  like the old Flask app. The backend issues **no `CREATE`/`DROP`/`ALTER`** and
  no migrations. It reads and writes the same rows the old app does.
- **SQLite** reference data (`towns`, `lottery_retailers`) is opened
  **read-only** and can never be modified.
- The **original Flask app keeps working** — this lives in a separate `backend/`
  folder and shares the same databases, so you always have a fallback.
- Still: **take a backup before first write** (see below).

## Setup
```bash
cd backend
python -m venv .venv && . .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then fill in DB_USER/DB_PASSWORD/DB_ADDRESS/DB_PORT/DB_NAME, SECRET_KEY
uvicorn app.main:app --reload --port 8000
```
Open http://localhost:8000/docs for the interactive API, or
http://localhost:8000/api/health to confirm the DB connected.

`LOCAL_DB_PATH` defaults to the repo's bundled `../app/lotalf.db`, so the
reference endpoints work even before Postgres is configured.

## Back up Postgres first (recommended)
```bash
pg_dump "postgresql://USER:PASS@HOST:PORT/DBNAME" -Fc -f lotalf_backup.dump
# restore if ever needed:  pg_restore -d "postgresql://USER:PASS@HOST:PORT/DBNAME" lotalf_backup.dump
```

## Endpoints (used by the Vue app)
| Area | Route |
|---|---|
| Auth | `POST /api/auth/login` → `{token}`, `GET /api/auth/me` |
| Reference | `GET /api/reference/{regions,provinces?region=,towns?province=}` |
| Comments | `GET/POST /api/comments` |
| Numbers | `GET /api/numbers/{n}`, `GET /api/numbers/hundred/{base}`, `POST /api/numbers/filtered`, `PUT /api/numbers/{n}` |
| Administraciones | `GET /api/retailers/map`, `/one`, `/image`, `PUT /api/retailers` |
| Stats | `GET /api/stats/{numbers,retailers}` |
| Scanner | `POST /api/scan/duplex` (Plustek D620 duplex → front/back base64) |

Write endpoints require `Authorization: Bearer <token>` from `/api/auth/login`.

## What changed vs the Flask app (audit fixes baked in)
- Parameterized + case-insensitive SQLite queries → no SQL injection, and the
  multilingual place names (L'Alfàs del Pi, A Coruña…) never break. Names are
  returned **verbatim**, never `.title()`-mangled.
- Schema reflected **once** at startup, not per request.
- Edit-mode password from `EDIT_PASSWORD` (not hardcoded); stateless signed token.
- Map markers are JSON, not a `<br>`-joined HTML string (no stored-XSS / parsing bug).
- Retailer photos stored straight to Postgres — **no `/tmp` scratch file**.
