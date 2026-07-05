"""One-time, non-destructive migration: add the nullable `image_back` column to
retailers_collection so both scanned faces of a décimo can be stored.

Run AFTER taking a pg_dump backup, once .env is filled in:

    python migrate_image_back.py

It is idempotent (ADD COLUMN IF NOT EXISTS) and adds only a nullable column —
no existing data is touched.
"""
from sqlalchemy import create_engine, text

from app.config import get_settings


def main() -> None:
    url = get_settings().postgres_url
    if not url:
        raise SystemExit("DB_* not set — fill in backend/.env first.")
    engine = create_engine(url)
    with engine.begin() as conn:
        conn.execute(text(
            "ALTER TABLE retailers_collection ADD COLUMN IF NOT EXISTS image_back TEXT"
        ))
    print("OK: retailers_collection.image_back is present (nullable).")


if __name__ == "__main__":
    main()
