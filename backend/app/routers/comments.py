"""Guestbook ("Tablón"). Public read + write, with anti-spam on the write path.

The board is intentionally open (visitors leave messages without logging in), so
bots POST straight to this endpoint. Defenses, cheapest first:
  1. Honeypot field — real form leaves it empty; bots fill it. Pretend success.
  2. Field validation — sane lengths + a real-looking email.
  3. No links — guestbook spam is almost all link injection.
  4. Per-IP rate limit — best-effort (uses X-Forwarded-For behind nginx).
None of these add a dependency or user friction. See add_comment() for the order.
"""
import re
import time
from collections import deque
from hashlib import md5

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from .. import db

router = APIRouter(prefix="/api/comments", tags=["comments"])

# Links / anchors / BBCode / bare domains with common spam TLDs.
_LINK_RE = re.compile(
    r"https?://|www\.|\[/?url|</?a[\s>]|"
    r"\b\w[\w-]*\.(?:com|net|org|ru|cn|info|biz|xyz|top|shop|online|site|club|link|vip|loan|bet|casino|porn)\b",
    re.I,
)
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")

# In-memory per-IP sliding window (single uvicorn process; resets on restart).
_RECENT: dict[str, deque] = {}
_MAX_PER_WINDOW = 3
_WINDOW_SECONDS = 600  # 10 minutes


def _identicon(name: str) -> str:
    digest = md5((name or "").encode("utf-8")).hexdigest()
    return f"https://www.gravatar.com/avatar/{digest}?d=identicon"


def _client_ip(request: Request) -> str:
    xff = request.headers.get("x-forwarded-for", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _rate_ok(ip: str) -> bool:
    now = time.time()
    dq = _RECENT.setdefault(ip, deque())
    while dq and now - dq[0] > _WINDOW_SECONDS:
        dq.popleft()
    if len(dq) >= _MAX_PER_WINDOW:
        return False
    dq.append(now)
    return True


@router.get("")
def list_comments(session=Depends(db.get_session)):
    C = db.table("comments")
    rows = session.query(C).all()
    out = []
    for r in rows:
        d = db.row_to_dict(r)
        d["identicon"] = _identicon(d.get("name", ""))
        out.append(d)
    out.reverse()  # newest first (parity with the Flask view)
    return out


class CommentIn(BaseModel):
    name: str
    email: str
    comment: str
    website: str = ""  # honeypot: must stay empty; real form hides it


@router.post("")
def add_comment(body: CommentIn, request: Request, session=Depends(db.get_session)):
    # 1. Honeypot — a bot that fills the hidden field gets a fake "ok" and is dropped.
    if body.website.strip():
        return {"ok": True}

    name = (body.name or "").strip()
    email = (body.email or "").strip()
    comment = (body.comment or "").strip()

    # 2. Validation
    if not (2 <= len(name) <= 60) or not (2 <= len(comment) <= 2000):
        raise HTTPException(status_code=422, detail="Nombre o mensaje no válido.")
    if len(email) > 120 or not _EMAIL_RE.match(email):
        raise HTTPException(status_code=422, detail="Correo no válido.")

    # 3. No links (kills the overwhelming majority of guestbook spam)
    if _LINK_RE.search(comment) or _LINK_RE.search(name):
        raise HTTPException(status_code=422, detail="No se permiten enlaces en los comentarios.")

    # 4. Per-IP rate limit
    if not _rate_ok(_client_ip(request)):
        raise HTTPException(status_code=429, detail="Demasiados comentarios. Inténtelo más tarde.")

    C = db.table("comments")
    session.add(C(name=name, email=email, comment=comment))
    session.commit()
    return {"ok": True}
